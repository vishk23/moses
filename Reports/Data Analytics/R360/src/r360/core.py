"""
R360 Core Implementation

Contains the main logic for generating relationship keys based on different grouping criteria.
All business logic is consolidated here for clean modular structure.
"""

from datetime import datetime
from pathlib import Path
import pandas as pd
import numpy as np
import hashlib
import base64
import os
from typing import Optional

from .fetch_data import fetch_data
import cdutils.pkey_sqlite # type: ignore
from .._version import __version__


# ============================================================================
# UNION FIND IMPLEMENTATION
# ============================================================================

class UnionFind:
    """
    Implements the Union-Find (disjoint set union) data structure to manage disjoint sets efficiently

    Attributes:
        parent (list): Parent pointer for each element in the set
        rank (list): Rank of the element, used fo runion by rank optimization
    """

    def __init__(self, n):
        """
        Initializes the Union-Find structure.

        Args:
            n (int): The number of elements in the set
        """
        self.parent = [i for i in range(n)]
        self.rank = [1] * n

    def find(self, x):
        """
        Finds the root of the set containing x with path compression.

        Args:
            x (int): The element to find the set for.

        Returns:
            int: The root of the set containing x.
        """
        res = x
        while res != self.parent[res]:
            self.parent[res] = self.parent[self.parent[res]] # path compression
            res = self.parent[res]
        return res
    
    def union(self, x1, x2):
        """
        Unions two sets containing x1 and x2, with union by rank (the set with more children gets parent status)

        Args:
            x1 (int): An element from the first set
            x2 (int): An element from the second set
        
        Returns:
            int: 0 if x1 and x2 are already in the same set, otherwise 1
        """
        p1, p2 = self.find(x1), self.find(x2)
        if p1 == p2:
            return 0 # No union occurs
        if self.rank[p1] >= self.rank[p2]:
            self.parent[p2] = p1 # Union by rank
            self.rank[p1] += self.rank[p2]
        else:
            self.parent[p1] = p2
            self.rank[p2] += self.rank[p1]
        return 1


# ============================================================================
# DATA TRANSFORMATION AND CLEANING FUNCTIONS
# ============================================================================

def merging_and_data_cleaning(acctcommon, persaddruse, orgaddruse, wh_addr):
    """
    Apply a series of merging & data cleaning operations.

    Args:
        acctcommon
        persaddruse
        orgaddruse
        wh_addr

    Returns:
        df

    Operations
    - Merge acctcommon & persaddruse and save as df
    - Merge df & orgaddruse and save as df
    - Create combined addrnbr field to allow merge with wh_addr table
    - Merge df & wh_addr table
    - Concatenate address
    """
    # Merging
    df = pd.merge(acctcommon, persaddruse, how='left', left_on='taxrptforpersnbr', right_on='persnbr')
    df = pd.merge(df, orgaddruse, how='left', left_on='taxrptfororgnbr', right_on='orgnbr')

    # Create a combined addrnbr field to allow merge with addr table
    df['addrnbr'] = np.where(df['addrnbr_x'].isnull(), df['addrnbr_y'], df['addrnbr_x'])

    # More merging
    df = pd.merge(df, wh_addr, on='addrnbr', how='left')

    # Address concatenation
    df['address_concat'] = df[['text1', 'text2', 'text3', 'cityname', 'statecd', 'zipcd']].apply(
        lambda row: ', '.join(filter(None, row.fillna('').astype(str))) if row.notna().any() else None, axis=1  # type: ignore
    )
    # Take a slice of the dataframe
    df = df[['acctnbr','address_concat']].copy()

    return df


def clean_ownership_data(wh_allroles):
    """
    Clean the data, changing data types, creating CIFNBR and a concatenation of roles associated with each acctnbr
    """
    # Change data types
    wh_allroles['persnbr'] = wh_allroles['persnbr'].apply(lambda x: str(int(x)) if not np.isnan(x) else '')
    wh_allroles['orgnbr'] = wh_allroles['orgnbr'].apply(lambda x: str(int(x)) if not np.isnan(x) else '')

    # Create CIFNBR
    wh_allroles['CIFNBR'] = np.where(wh_allroles['orgnbr'] == '', 'P' + wh_allroles['persnbr'], 'O' + wh_allroles['orgnbr'])

    # Create a new df grouping on acctnbr and concatenate roles
    df = wh_allroles.groupby('acctnbr')['CIFNBR'].apply(lambda x: ','.join(x.unique())).reset_index()
    df.rename(columns={'CIFNBR': 'CIF'}, inplace=True)

    return df


def address_ownership_consolidation(address_df: pd.DataFrame, ownership_df: pd.DataFrame) -> dict:
    """
    Series of merging and additional cleaning steps applied, such as adjusting column data types.
    This outputs a dictionary.

    Args: 
        address_df (pd.DataFrame): Address dataframe
        ownership_df (pd.DataFrame): Ownership dataframe

    Returns:
        data_dict (dict): Dataframe is transformed to a dictionary with acctnbr as the key
    """
    # Merging
    merged_df = pd.merge(address_df, ownership_df, how='outer',on='acctnbr')

    # Changing data type
    columns_to_str = ['address_concat','CIF']
    merged_df[columns_to_str] = merged_df[columns_to_str].astype(str)

    # Convert to a dictionary
    data_dict = merged_df.set_index('acctnbr').to_dict(orient='index')

    return data_dict


def post_grouping_cleanup(updated_data: dict, acctcommon: pd.DataFrame) -> pd.DataFrame:
    """
    After grouping and assigning keys, final cleaning steps for putting back into a dataframe and appending extra fields

    Args:
        updated_data (dict): dictionary with acctnbr as the key
        acctcommon (pd.DataFrame): OSIBANK.WH_ACCTCOMMON (R1625)
    
    Returns:
        df (pd.DataFrame): final dataframe 
    """
    # Convert dictionary to dataframe
    df = pd.DataFrame.from_dict(updated_data, orient='index')
    df['acctnbr'] = df.index
    df = df[['acctnbr'] + [col for col in df.columns if col != 'acctnbr']]

    # Append additional fields
    additional_fields = acctcommon[['acctnbr','ownersortname','product','curracctstatcd','bookbalance','noteintrate','mjaccttypcd']].copy()
    df = pd.merge(df, additional_fields, how='left', on='acctnbr')
    
    # Change datatype
    df['acctnbr'] = df['acctnbr'].astype(str)
    
    return df


# ============================================================================
# HASHING FUNCTIONS
# ============================================================================

def hash_key(data: dict, key_field: str, new_key_field: Optional[str]=None) -> dict:
    """
    Hashes the specified key field in the data dictionary and optionally writes the hashed value to a new key.

    Args:
        data (dict): A dictionary where each entry contains the key_field to hash
        key_field (str): The name of the field to hash(e.g., 'concatenated_address')
        new_key_field (str, optional): The name of the field to write the hashed value to. If None, overwrite original key

    Returns:
        dict: The updated dictionary with hashed values for the specified field.
    """

    for _, details in data.items():
        if key_field in details and details[key_field]:
            original_value = details[key_field]
            if original_value in ('None','nan'):
                write_key = new_key_field if new_key_field else key_field
                details[write_key] = None
                continue
            # Generate hash key (BLAKE2b algorithm) and truncate to 10 digits
            hashed_value = hashlib.blake2b(original_value.encode(), digest_size=8).digest()
            hashed_value = base64.urlsafe_b64encode(hashed_value).decode('utf-8')
            # Write the new key or overwrite existing key
            write_key = new_key_field if new_key_field else key_field
            details[write_key] = hashed_value
    return data


# ============================================================================
# KEY ASSIGNMENT FUNCTIONS
# ============================================================================

def assign_helper_keys(data: dict) -> dict:
    """
    Groups accounts into disjoint sets based on shared CIFs and assigns helper keys.

    Args:
        data (dict): A dictionary where each account contains the attribute 'CIF' which is a concatenated list of ownership entities
    
    Returns:
        dict: The updated data with assigned helper key
    """
    cif_map = {}
    account_ids = list(data.keys())
    n = len(account_ids)

    # Initialize Union-Find
    uf = UnionFind(n)

    # Perform union operations based on shared CIFs
    for i, acct in enumerate(account_ids):
        cifs = data[acct]['CIF'].split(',')
        cifs = [cif for cif in cifs if cif not in ('O500','O501','nan')] # Excluding IOLTA shared ownership & nan (for no roles)
        for cif in cifs:
            if cif in cif_map:
                uf.union(i, cif_map[cif])
            else:
                cif_map[cif] = i

    # Assign unique helper keys to disjoint sets
    helper_keys = {}
    for i, acct in enumerate(account_ids):
        root = uf.find(i)
        if root not in helper_keys:
            helper_keys[root] = len(helper_keys) + 1
        data[acct]['helper_key'] = helper_keys[root]

    return data


# ============================================================================
# HISTORICAL KEY FUNCTIONS
# ============================================================================

def get_most_recent_file(folder_path):
    today_str = datetime.now().strftime('%Y%m%d')
    today_date = datetime.strptime(today_str, '%Y%m%d')

    files = os.listdir(folder_path)

    csv_files = [f for f in files if f.startswith("r360_") and f.endswith(".csv")]

    valid_files = {}
    for file in csv_files:
        try:
            date_str = file.split("_")[1].split(".csv")[0]
            file_date = datetime.strptime(date_str, '%Y%m%d')
            if file_date < today_date:
                valid_files[file_date] = file
        except (IndexError, ValueError):
            continue

    if not valid_files:
        print("No history")
        return None
    else:
        most_recent_date = max(valid_files.keys())
        most_recent_file = valid_files[most_recent_date]

        return os.path.join(folder_path, most_recent_file)


def retrieve_historical_keys(history_path):
    if history_path is None:
        return None
    else:
        history = pd.read_csv(history_path)
        return history
    

def append_historical_keys(data, history=None):
    if history is None:
        return data
    else:
        data = pd.DataFrame.from_dict(data, orient='index').copy()
        data = data.reset_index().copy()
        data = data.rename(columns={'index':'acctnbr'})
        history_subset = history[['acctnbr','portfolio_key']]
        assert history_subset['acctnbr'].is_unique, "Duplicates found"
        data = pd.merge(data, history_subset, on='acctnbr', how='left')
        data = data.set_index('acctnbr')
        data = data.to_dict(orient='index').copy()
        return data


# ============================================================================
# PORTFOLIO KEY ASSIGNMENT FUNCTIONS
# ============================================================================

def assign_portfolio_keys(data):
    """
    Groups accounts into disjoint sets based on shared address or helper keys (shared ownership) and assigns unique portfolio keys.

    Args:
        data (dict): A dictionary where each account contains the attributes including address_key and helper_key.

    Returns:
        dict: The updated data with assigned portfolio keys.
    """

    address_map = {}
    helper_map = {}
    account_ids = list(data.keys())
    n = len(account_ids)

    # Initialize Union-Find
    uf = UnionFind(n)

    # Perform union operations based on address_key and helper_key
    for i, acct in enumerate(account_ids):
        attributes = data[acct]
        address = attributes['address_key']
        helper = attributes['helper_key']

        if address not in (None, 'None', 'nan','-grcQPptQrw=','ShNDlbk0gXo=','uA9lf4xIAz8='): # These are IOLTA addresses & 29 Broadway respectively
            if address in address_map:
                uf.union(i, address_map[address])
            else:
                address_map[address] = i

        if helper in helper_map:
            uf.union(i, helper_map[helper])
        else:
            helper_map[helper] = i

    # Assign unique portfolio keys to disjoint sets
    portfolio_keys = {}
    sets_by_root = {}

    for i, acct in enumerate(account_ids):
        root = uf.find(i)
        sets_by_root.setdefault(root, []).append(acct)

    portfolio_keys = {}
    sets_with_no_keys = []

    for root, accounts in sets_by_root.items():
        hist_keys = [
            int(data[acct].get('portfolio_key'))
            for acct in accounts
            if pd.notna(data[acct].get('portfolio_key'))
            ]
        if len(hist_keys) > 0:
            hist_key_counts = pd.Series(hist_keys).value_counts()
            # print(hist_key_counts)
            pkey = hist_key_counts[hist_key_counts == hist_key_counts.max()].index.min()
            # print(pkey)
        else:
            pkey = None
            sets_with_no_keys.append((root, accounts))
        for acct in accounts:
            if pkey is not None:
                if pkey not in portfolio_keys:
                    portfolio_keys[pkey] = []
                portfolio_keys[pkey].append(acct)

    used_keys = set(portfolio_keys.keys())
    new_key = 1

    for root, accounts in sets_with_no_keys:
        while new_key in used_keys:
            new_key += 1
        pkey = new_key
        portfolio_keys[pkey] = accounts
        used_keys.add(pkey)

    for pkey, accounts in portfolio_keys.items():
        for acct in accounts:
            data[acct]['portfolio_key'] = pkey
        
    return data


def assign_address_only_keys(data):
    """
    Groups accounts into disjoint sets based on shared address only and assigns unique portfolio keys.

    Args:
        data (dict): A dictionary where each account contains the attributes including address_key and helper_key.

    Returns:
        dict: The updated data with assigned portfolio keys.
    """

    address_map = {}
    account_ids = list(data.keys())
    n = len(account_ids)

    # Initialize Union-Find
    uf = UnionFind(n)

    # Perform union operations based on address_key only
    for i, acct in enumerate(account_ids):
        attributes = data[acct]
        address = attributes['address_key']

        if address not in (None, 'None', 'nan','-grcQPptQrw=','ShNDlbk0gXo=','uA9lf4xIAz8='): # These are IOLTA addresses & 29 Broadway respectively
            if address in address_map:
                uf.union(i, address_map[address])
            else:
                address_map[address] = i

    # Assign unique portfolio keys to disjoint sets
    portfolio_keys = {}
    sets_by_root = {}

    for i, acct in enumerate(account_ids):
        root = uf.find(i)
        sets_by_root.setdefault(root, []).append(acct)

    portfolio_keys = {}
    sets_with_no_keys = []

    for root, accounts in sets_by_root.items():
        hist_keys = [
            int(data[acct].get('portfolio_key'))
            for acct in accounts
            if pd.notna(data[acct].get('portfolio_key'))
            ]
        if len(hist_keys) > 0:
            hist_key_counts = pd.Series(hist_keys).value_counts()
            pkey = hist_key_counts[hist_key_counts == hist_key_counts.max()].index.min()
        else:
            pkey = None
            sets_with_no_keys.append((root, accounts))
        for acct in accounts:
            if pkey is not None:
                if pkey not in portfolio_keys:
                    portfolio_keys[pkey] = []
                portfolio_keys[pkey].append(acct)

    used_keys = set(portfolio_keys.keys())
    new_key = 1

    for root, accounts in sets_with_no_keys:
        while new_key in used_keys:
            new_key += 1
        pkey = new_key
        portfolio_keys[pkey] = accounts
        used_keys.add(pkey)

    for pkey, accounts in portfolio_keys.items():
        for acct in accounts:
            data[acct]['portfolio_key'] = pkey
        
    return data


def assign_ownership_only_keys(data):
    """
    Groups accounts into disjoint sets based on shared ownership only and assigns unique portfolio keys.

    Args:
        data (dict): A dictionary where each account contains the attributes including address_key and helper_key.

    Returns:
        dict: The updated data with assigned portfolio keys.
    """

    helper_map = {}
    account_ids = list(data.keys())
    n = len(account_ids)

    # Initialize Union-Find
    uf = UnionFind(n)

    # Perform union operations based on helper_key only (ownership)
    for i, acct in enumerate(account_ids):
        attributes = data[acct]
        helper = attributes['helper_key']

        if helper in helper_map:
            uf.union(i, helper_map[helper])
        else:
            helper_map[helper] = i

    # Assign unique portfolio keys to disjoint sets
    portfolio_keys = {}
    sets_by_root = {}

    for i, acct in enumerate(account_ids):
        root = uf.find(i)
        sets_by_root.setdefault(root, []).append(acct)

    portfolio_keys = {}
    sets_with_no_keys = []

    for root, accounts in sets_by_root.items():
        hist_keys = [
            int(data[acct].get('portfolio_key'))
            for acct in accounts
            if pd.notna(data[acct].get('portfolio_key'))
            ]
        if len(hist_keys) > 0:
            hist_key_counts = pd.Series(hist_keys).value_counts()
            pkey = hist_key_counts[hist_key_counts == hist_key_counts.max()].index.min()
        else:
            pkey = None
            sets_with_no_keys.append((root, accounts))
        for acct in accounts:
            if pkey is not None:
                if pkey not in portfolio_keys:
                    portfolio_keys[pkey] = []
                portfolio_keys[pkey].append(acct)

    used_keys = set(portfolio_keys.keys())
    new_key = 1

    for root, accounts in sets_with_no_keys:
        while new_key in used_keys:
            new_key += 1
        pkey = new_key
        portfolio_keys[pkey] = accounts
        used_keys.add(pkey)

    for pkey, accounts in portfolio_keys.items():
        for acct in accounts:
            data[acct]['portfolio_key'] = pkey
        
    return data


def generate_portfolio_key(save_to_db=True):
    """Generate portfolio key that groups by address OR ownership"""
    # Import config to check historical database settings
    from .. import config
    use_historical = config.HISTORICAL_DB_CONFIG.get('portfolio', True)
    
    if save_to_db:
        db_path = config.DB_DIR / 'assets/current.db'
        current_engine = cdutils.pkey_sqlite.create_sqlite_engine(str(db_path))
    else:
        current_engine = None
    
    # Get and process data
    data = _get_processed_data()
    
    # Get historical keys for persistence based on config
    if use_historical and current_engine:
        print("📊 Loading historical portfolio keys for persistence...")
        history = cdutils.pkey_sqlite.get_most_recent_historical_key(engine=current_engine)
        data = append_historical_keys(data, history)
    elif use_historical is False:
        print("🔄 Generating fresh portfolio keys (no historical data)")
        data = append_historical_keys(data, None)
    else:
        print("⏭️  Skipping historical database operations entirely")
        data = append_historical_keys(data, None)
    
    # Assign portfolio key (groups by address OR ownership)
    data = assign_portfolio_keys(data)
    
    # Clean up and return
    df = _finalize_data(data)
    
    if save_to_db and current_engine:
        _save_to_database(df, current_engine)
    
    return df


def generate_address_key(save_to_db=True):
    """Generate address key that groups by address only"""
    # Import config to check historical database settings
    from .. import config
    use_historical = config.HISTORICAL_DB_CONFIG.get('address', True)
    
    if save_to_db:
        db_path = config.DB_DIR / 'address.db'
        current_engine = cdutils.pkey_sqlite.create_sqlite_engine(str(db_path))
    else:
        current_engine = None
    
    # Get and process data
    data = _get_processed_data()
    
    # Get historical keys for persistence based on config
    if use_historical and current_engine:
        print("📊 Loading historical address keys for persistence...")
        history = cdutils.pkey_sqlite.get_most_recent_historical_key(engine=current_engine)
        data = append_historical_keys(data, history)
    elif use_historical is False:
        print("🔄 Generating fresh address keys (no historical data)")
        data = append_historical_keys(data, None)
    else:
        print("⏭️  Skipping historical database operations entirely")
        data = append_historical_keys(data, None)
    
    # Assign address-only portfolio key
    data = assign_address_only_keys(data)
    
    # Clean up and return
    df = _finalize_data(data)
    
    if save_to_db and current_engine:
        _save_to_database(df, current_engine)
    
    return df


def generate_ownership_key(save_to_db=True):
    """Generate ownership key that groups by ownership only"""
    # Import config to check historical database settings
    from .. import config
    use_historical = config.HISTORICAL_DB_CONFIG.get('ownership', True)
    
    if save_to_db:
        db_path = config.DB_DIR / 'ownership.db'
        current_engine = cdutils.pkey_sqlite.create_sqlite_engine(str(db_path))
    else:
        current_engine = None
    
    # Get and process data
    data = _get_processed_data()
    
    # Get historical keys for persistence based on config
    if use_historical and current_engine:
        print("📊 Loading historical ownership keys for persistence...")
        history = cdutils.pkey_sqlite.get_most_recent_historical_key(engine=current_engine)
        data = append_historical_keys(data, history)
    elif use_historical is False:
        print("🔄 Generating fresh ownership keys (no historical data)")
        data = append_historical_keys(data, None)
    else:
        print("⏭️  Skipping historical database operations entirely")
        data = append_historical_keys(data, None)
    
    # Assign ownership-only portfolio key
    data = assign_ownership_only_keys(data)
    
    # Clean up and return
    df = _finalize_data(data)
    
    if save_to_db and current_engine:
        _save_to_database(df, current_engine)
    
    return df


def _get_processed_data():
    """Common data processing steps"""
    # Fetch raw data
    data = fetch_data()
    
    # Unpack data
    acctcommon = data['acctcommon'].copy()
    persaddruse = data['persaddruse'].copy()
    orgaddruse = data['orgaddruse'].copy()
    wh_addr = data['wh_addr'].copy()
    wh_allroles = data['wh_allroles'].copy()
    
    # Merge & Clean Data
    address_df = merging_and_data_cleaning(acctcommon, persaddruse, orgaddruse, wh_addr)
    ownership_df = clean_ownership_data(wh_allroles)
    data_dict = address_ownership_consolidation(address_df, ownership_df)
    
    # Create hash keys
    data_dict = hash_key(data_dict, 'address_concat', 'address_key')
    data_dict = hash_key(data_dict, 'CIF', 'ownership_key')
    
    # Assign helper key (shared ownership grouping)
    data_dict = assign_helper_keys(data_dict)
    
    return data_dict


def _finalize_data(data_dict):
    """Common data finalization steps"""
    # Get fresh acctcommon data for additional fields
    fresh_data = fetch_data()
    acctcommon = fresh_data['acctcommon'].copy()
    
    # Final cleanup and field addition
    df = post_grouping_cleanup(data_dict, acctcommon)
    
    return df


def _save_to_database(df, engine):
    """Save results to database"""
    df_subset = df[['acctnbr', 'portfolio_key']].copy()
    cdutils.pkey_sqlite.write_current_run_to_current_db(df_subset, engine=engine)
