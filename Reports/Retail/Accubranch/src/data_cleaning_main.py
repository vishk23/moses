"""
Data cleaning main pipeline for Accubranch project.

This module implements the high-level data pipeline workflow:
1. Generate/load the acct_df (account data)
2. Merge with organization data and exclude Municipal & Fiduciary accounts
3. Merge with person data to get DOB (join on taxrptforpersnbr)
4. Append address data through orgaddruse/persaddruse tables to get address details

The result is a comprehensive dataframe that serves as the backbone for:
- Account Section reporting (as of any date)
- Annual deposit analysis

Data sources are modular and can be easily swapped between mock data and production database.
"""

import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

import src.accubranch.acct_file_creation
import src.accubranch.acct_data_gathering
from src.accubranch.join_functions import (
    join_accounts_with_orgs,
    join_accounts_with_persons,
    join_accounts_with_addresses
)


def load_mock_data() -> Dict[str, pd.DataFrame]:
    """
    Load data from mock CSV files.
    
    Returns:
    --------
    dict
        Dictionary containing all required dataframes for the pipeline
    """
    base_path = Path("assets/mock_data")
    
    return {
        'wh_org': pd.read_csv(base_path / "wh_org.csv"),
        'wh_pers': pd.read_csv(base_path / "wh_pers.csv"),
        'wh_addr': pd.read_csv(base_path / "wh_addr.csv"),
        'orgaddruse': pd.read_csv(base_path / "orgaddruse.csv"),
        'persaddruse': pd.read_csv(base_path / "persaddruse.csv")
    }


def load_production_data() -> Dict[str, pd.DataFrame]:
    """
    Load data from production database.
    
    This is a placeholder function that would be implemented to connect
    to the actual production database and retrieve the required tables.
    
    Returns:
    --------
    dict
        Dictionary containing all required dataframes for the pipeline
    """
    data = src.accubranch.acct_data_gathering.fetch_data()
    return data


def run_data_cleaning_pipeline(
    as_of_date: datetime,
    data_source: str = "mock",
    exclude_org_types: Optional[list] = None,
    address_use_type: str = "PRI"
) -> pd.DataFrame:
    """
    Run the complete data cleaning pipeline following the workflow:
    1. Generate account data for specified date
    2. Exclude accounts with 'muni' in branchname (case insensitive)
    3. Merge with organizations (excluding Municipal & Fiduciary)
    4. Merge with persons to get DOB
    5. Append address information
    
    Parameters:
    -----------
    as_of_date : datetime
        The date for which to generate account data
    data_source : str, default "mock"
        Data source to use ("mock" or "production")
    exclude_org_types : list, optional
        Organization types to exclude (defaults to Municipal & Fiduciary)
    address_use_type : str, default "PRI"
        Address use type to filter for (e.g., 'PRI' for primary addresses)
        
    Returns:
    --------
    pd.DataFrame
        Comprehensive dataframe with account, customer, and address data
        
    Example:
    --------
    >>> from datetime import datetime
    >>> result = run_data_cleaning_pipeline(
    ...     as_of_date=datetime(2024, 12, 31),
    ...     data_source="mock",
    ...     exclude_org_types=['MUNIC', 'FIDUC']
    ... )
    >>> print(f"Final dataset: {len(result)} accounts with {len(result.columns)} columns")
    """
    
    # Set default exclusions for Municipal & Fiduciary accounts
    if exclude_org_types is None:
        exclude_org_types = ['MUNI', 'TRST']  # Municipal & Fiduciary Accounts
    
    print(f"Starting data cleaning pipeline for {as_of_date.date()}")
    print(f"Using data source: {data_source}")
    print(f"Excluding organization types: {exclude_org_types}")
    
    # Step 1: Load supporting data based on source
    print("\n=== Step 1: Loading supporting data ===")
    if data_source == "mock":
        data_tables = load_mock_data()
        print("Loaded mock data from CSV files")
    elif data_source == "production":
        data_tables = load_production_data()
        print("Loaded production data from database")
    else:
        raise ValueError(f"Unknown data source: {data_source}. Use 'mock' or 'production'")
    
    # Step 2: Generate account data for the specified date
    print(f"\n=== Step 2: Generating account data for {as_of_date.date()} ===")
    # acct_df = generate_acct_df_for_date(as_of_date)
    # Here is where you call your own function
    acct_df = src.accubranch.acct_file_creation.query_df_on_date(as_of_date)
    print(f"Generated {len(acct_df)} account records")
    print(f"Account types: {acct_df['mjaccttypcd'].value_counts().to_dict()}")
    
    # Step 2.5: Exclude accounts with 'muni' in branchname (case insensitive)
    print(f"\n=== Step 2.5: Excluding accounts with 'muni' in branchname ===")
    initial_count = len(acct_df)
    if 'branchname' in acct_df.columns:
        acct_df = acct_df[~acct_df['branchname'].str.contains('muni',case=False, na=False)]
        excluded_count = initial_count - len(acct_df)
        print(f"Excluded {excluded_count} accounts assigned to MUNI Branches")
        print(f"Remaining accounts: {len(acct_df)}")
    else:
        print("No branchname column found - skipping muni branch exclusion")
    
    # Step 3: Merge with organizations and exclude specified types
    print(f"\n=== Step 3: Merging with organizations (excluding {exclude_org_types}) ===")
    org_merged_df = join_accounts_with_orgs(
        acct_df, 
        data_tables['wh_org'], 
        exclude_org_types=exclude_org_types
    )
    print(f"After organization merge and filtering: {len(org_merged_df)} accounts")
    
    # Step 4: Merge with persons to get DOB (join on taxrptforpersnbr)
    print(f"\n=== Step 4: Merging with persons to append DOB ===")
    pers_merged_df = join_accounts_with_persons(org_merged_df, data_tables['wh_pers'])
    person_accounts = pers_merged_df['datebirth'].notna().sum()
    print(f"After person merge: {len(pers_merged_df)} accounts ({person_accounts} with person data)")
    
    # Step 5: Append address information
    print(f"\n=== Step 5: Appending address information ===")
    
    # Split accounts by customer type for address joins
    org_accounts = pers_merged_df[pers_merged_df['taxrptfororgnbr'].notna()]
    person_accounts = pers_merged_df[pers_merged_df['taxrptforpersnbr'].notna()]
    other_accounts = pers_merged_df[
        pers_merged_df['taxrptfororgnbr'].isna() & pers_merged_df['taxrptforpersnbr'].isna()
    ]
    
    print(f"Organization accounts: {len(org_accounts)}")
    print(f"Person accounts: {len(person_accounts)}")
    print(f"Other accounts (no customer link): {len(other_accounts)}")
    
    # Join organization addresses
    if len(org_accounts) > 0:
        org_with_addr = join_accounts_with_addresses(
            org_accounts, 
            data_tables['orgaddruse'], 
            data_tables['wh_addr'], 
            address_use_type=address_use_type
        )
        org_addr_count = org_with_addr['text1'].notna().sum()
        print(f"Organization accounts with addresses: {org_addr_count}/{len(org_accounts)}")
    else:
        org_with_addr = pd.DataFrame()
    
    # Join person addresses
    if len(person_accounts) > 0:
        pers_with_addr = join_accounts_with_addresses(
            person_accounts, 
            data_tables['persaddruse'], 
            data_tables['wh_addr'], 
            address_use_type=address_use_type
        )
        pers_addr_count = pers_with_addr['text1'].notna().sum()
        print(f"Person accounts with addresses: {pers_addr_count}/{len(person_accounts)}")
    else:
        pers_with_addr = pd.DataFrame()
    
    # Combine all results
    dataframes_to_combine = []
    if len(org_with_addr) > 0:
        dataframes_to_combine.append(org_with_addr)
    if len(pers_with_addr) > 0:
        dataframes_to_combine.append(pers_with_addr)
    if len(other_accounts) > 0:
        # Add empty address columns to other_accounts to match schema
        address_cols = ['text1', 'text2', 'text3', 'cityname', 'statecd', 'zipcd', 'addrnbr']
        for col in address_cols:
            if col not in other_accounts.columns:
                other_accounts[col] = pd.NA
        dataframes_to_combine.append(other_accounts)
    
    if dataframes_to_combine:
        final_df = pd.concat(dataframes_to_combine, ignore_index=True)
    else:
        final_df = pers_merged_df  # Fallback if no addresses found
    
    # Step 6: Final summary
    print(f"\n=== Pipeline Complete ===")
    print(f"Final dataset: {len(final_df)} accounts with {len(final_df.columns)} columns")
    total_with_addresses = final_df['text1'].notna().sum()
    print(f"Accounts with address data: {total_with_addresses}/{len(final_df)} ({total_with_addresses/len(final_df)*100:.1f}%)")
    
    # Summary by account type
    print(f"\nAccount type summary:")
    for acct_type, count in final_df['mjaccttypcd'].value_counts().items():
        print(f"  {acct_type}: {count}")
    
    return final_df


def main():
    """
    Example usage of the data cleaning pipeline.
    """
    # Example 1: Run with mock data
    print("=== Running Data Cleaning Pipeline with Mock Data ===")
    
    result = run_data_cleaning_pipeline(
        as_of_date=datetime(2024, 12, 31),
        data_source="mock",
        exclude_org_types=['MUNIC', 'FIDUC', 'NONPROF'],  # Example exclusions
        address_use_type="PRI"
    )
    
    print(f"\nSample of final data:")
    print(result[['acctnbr', 'mjaccttypcd', 'ownersortname', 'Net Balance', 
                  'orgtypcd', 'datebirth', 'text1', 'cityname', 'statecd']].head())
    
    # Example 2: Show how easy it would be to switch to production
    # (commented out since production loader isn't implemented)
    # production_result = run_data_cleaning_pipeline(
    #     as_of_date=datetime(2024, 12, 31),
    #     data_source="production"
    # )


if __name__ == "__main__":
    main()
