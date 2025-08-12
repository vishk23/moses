# %%
# %%
# Weekly Loan Report
# Developed by CD
# v2.0.4-prod

from io import StringIO
import time
import numpy as np
import os
from datetime import datetime, timedelta, date
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from typing import List
from collections import defaultdict, Counter
import pandas as pd
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from io import StringIO
from pathlib import Path
import asyncio
import nest_asyncio
import sys
import win32com.client as win32
nest_asyncio.apply()

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def retrieve_data():
    """
    Retrieve data from COCC database
    """
    class DatabaseHandler:
        """
        This class abstracts the connection to the database and allows a clean
        interface for the developer to use.

        This connector can handle async queries

        """
        def __init__(self, tns_admin_path):
            """
            Args:
                tns_admin_path (str): Oracle driver path
                credentials_path_db1 (str): Database 1 credentials path
                credentials_path_db1 (str): Databsae 2 credentials path
            """
            os.environ['TNS_ADMIN'] = tns_admin_path
            
            # Load private key
            key_key_path = r'\\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Chad Projects\Utility\env_admin\key.key'
            with open(key_key_path, "rb") as key_file:
                key = key_file.read()

            cipher = Fernet(key)
            
            # Load encrypted data
            encoded_env_path = r'\\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Chad Projects\Utility\env_admin\.env.enc'
            with open(encoded_env_path, "rb") as encrypted_file:
                encrypted_data = encrypted_file.read()

            decrypted_data = cipher.decrypt(encrypted_data).decode()

            env_file = StringIO(decrypted_data)
            load_dotenv(stream=env_file)

            self.username1 = os.getenv('main_username')
            self.password1 = os.getenv('main_password')
            self.dsn1 = os.getenv('main_dsn')

            self.username2 = os.getenv('datamart_username')
            self.password2 = os.getenv('datamart_password')
            self.dsn2 = os.getenv('datamart_dsn')

            self.connection_string1 = f'oracle+oracledb://{self.username1}:{self.password1}@{self.dsn1}'
            self.connection_string2 = f'oracle+oracledb://{self.username2}:{self.password2}@{self.dsn2}'

            self.engine1 = create_async_engine(self.connection_string1, max_identifier_length=128, echo=False, future=True)
            self.engine1.dialect.hide_parameters = True
            self.engine2 = create_async_engine(self.connection_string2, max_identifier_length=128, echo=False, future=True)
            self.engine1.dialect.hide_parameters = True


        async def query(self, sql_query, engine=1):
            """
            This allows abstraction of the connection and the class
            so the developer can query a single table as a dataframe

            Args:
                sql_query (str): The query to SQL database is passed as a string
                engine (int): This selects the database. There are two engines:
                    1 -> R1625
                    2 -> COCC DataMart

            Returns:
                df: The SQL query is returned as a pandas DataFrame

            Usage:
                df = db_handler.query("SELECT * FROM DB.TABLE", engine=1)

                In this example, db_handler = DatabaseHandler(args)
            """
            if engine == 1:
                selected_engine = self.engine1
            elif engine == 2:
                selected_engine = self.engine2
            else:
                raise ValueError("Engine must be 1 or 2")

            async with selected_engine.connect() as connection:
                result = await connection.execute(sql_query)
                rows = result.fetchall()
                if not rows:
                    return pd.DataFrame()
                df = pd.DataFrame(rows, columns=result.keys())
            return df

        async def close(self):
            if self.engine1:
                await self.engine1.dispose()
            if self.engine2:
                await self.engine2.dispose()


    # Database Connection Configuration
    tns_admin_path = r'\\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Chad Projects\Utility\env_admin\tns_admin'
    db_handler = DatabaseHandler(tns_admin_path)

    async def fetch_data(queries):
        try:
            tasks = {query['key']: asyncio.create_task(db_handler.query(query['sql'], query['engine'])) for query in queries}
            results = await asyncio.gather(*tasks.values())
            return {key: df for key, df in zip(tasks.keys(), results)}
        except Exception as e:
            print(f"Error")
            raise
        finally:
            await db_handler.close()

    def run_sql_queries():
        # lookup table
        # Engine 1
        lookup_df = text("""
        SELECT 
            *
        FROM 
            sys.all_tab_columns col
        """)

        # acctcommon
        # engine 2
        wh_acctcommon = text("""
        SELECT 
            a.ACCTNBR,
            a.LOANOFFICER,
            a.OWNERSORTNAME,
            a.PRODUCT,
            a.CURRACCTSTATCD,
            a.NOTEBAL,
            a.BOOKBALANCE,
            a.NOTEINTRATE,
            a.DATEMAT,
            a.TAXRPTFORORGNBR,
            a.TAXRPTFORPERSNBR,
            a.CONTRACTDATE,
            a.MJACCTTYPCD,
            a.CURRMIACCTTYPCD,
            a.NAMEADDR1,
            a.NAMEADDR2,
            a.NAMEADDR3,
            a.PRIMARYOWNERCITY,
            a.PRIMARYOWNERSTATE,
            a.PRIMARYOWNERZIPCD,
            a.NOTEOPENAMT
        FROM 
            COCCDM.WH_ACCTCOMMON_TEMP a
        """)

        wh_loans = text("""
        SELECT
            a.ACCTNBR,
            a.ORIGDATE,
            a.ORIGBAL,
            a.FDICCATDESC,
            a.RUNDATE,
            a.AVAILBALAMT
        FROM
            COCCDM.WH_LOANS_TEMP a
        """)

        wh_acctloan = text("""
        SELECT
            a.ACCTNBR,
            a.MININTRATE,
            a.FDICCATCD,
            a.PROPNBR,
            a.TOTALPCTSOLD,
            a.RISKRATINGCD,
            a.COBAL,
            a.CREDLIMITCLATRESAMT
        FROM
            COCCDM.WH_ACCTLOAN_TEMP a
        """)

        wh_org = text("""
        SELECT
            a.ORGNBR,
            a.NAICSCD,
            a.NAICSCDDESC
        FROM
            COCCDM.WH_ORG a
        """)

        wh_prop = text("""
        SELECT
            a.ACCTNBR,
            a.PROPNBR,
            a.APRSVALUEAMT,
            a.APRSDATE,
            a.PROPADDR1,
            a.PROPADDR2,
            a.PROPADDR3,
            a.PROPCITY,
            a.PROPSTATE,
            a.PROPZIP,
            a.PROPTYPECD
        FROM
            COCCDM.WH_PROP a
        """)

        wh_prop2 = text("""
        SELECT
            a.ACCTNBR,
            a.PROPNBR,
            a.PROPDESC,
            a.PROPTYPDESC
        FROM
            COCCDM.WH_PROP2 a
        """)

        househldacct = text("""
        SELECT 
            a.ACCTNBR,
            a.HOUSEHOLDNBR,
            a.DATELASTMAINT
        FROM 
            OSIEXTN.HOUSEHLDACCT a
        """)

        queries = [
            {'key':'wh_acctcommon', 'sql':wh_acctcommon, 'engine':2},
            {'key':'wh_loans', 'sql':wh_loans, 'engine':2},
            {'key':'wh_acctloan', 'sql':wh_acctloan, 'engine':2},
            {'key':'wh_org', 'sql':wh_org, 'engine':2},
            {'key':'wh_prop', 'sql':wh_prop, 'engine':2},
            {'key':'wh_prop2', 'sql':wh_prop2, 'engine':2},
            {'key':'househldacct', 'sql':househldacct, 'engine':1},
        ]

        async def run_queries():
            return await fetch_data(queries)
        
        loop = asyncio.get_event_loop()
        if loop.is_running():
            return loop.run_until_complete(run_queries())
        else:
            return asyncio.run(run_queries())
        
    data = run_sql_queries()
    
    return data

# %%
# data = retrieve_data()

# %%
# wh_acctcommon = data['wh_acctcommon'].copy()
# wh_loans = data['wh_loans'].copy()
# wh_acctloan = data['wh_acctloan'].copy()
# wh_org = data['wh_org'].copy()
# wh_pers = data['wh_pers'].copy()
# wh_prop = data['wh_prop'].copy()
# wh_prop2 = data['wh_prop2'].copy()
# orgaddruse = data['orgaddruse'].copy()
# persaddruse = data['persaddruse'].copy()
# wh_addr = data['wh_addr'].copy()

# %%
def filter_acctcommon(df):
    """
    Filter acctcommon table

    Args:
        df: acctcommon table from COCC

    Returns:
        result_df: dataframe after filters are applied
    
    Operations:
    [MJACCTTYPCD] IN ("CML", "CNS", "MTG", "MLN") 
    AND 
    [CURRMIACCTTYPCD] != "CI07"
    If [MJACCTTYPCD] IN "CNS", [CURRMIACCTTYPCD] IN ("IL02", "IL11", "IL12", "IL13", "IL14") 
    AND 
    !IsNull([TAXRPTFORORGNBR])
    - Concatenate address fields into one primary_address field
    """
    df = df[df['mjaccttypcd'].isin(['CML', 'MTG', 'MLN'])]
    df = df[df['currmiaccttypcd'] != 'CI07']
    df['primary_address'] = df[['nameaddr1','nameaddr2','nameaddr3']].apply(lambda x: ''.join(filter(None, x)), axis=1)
    df = df.drop(columns=['nameaddr1','nameaddr2','nameaddr3'])
    return df

# %%
def filter_wh_loans(df):
    """
    Filter wh_loans

    Args:
        df: WH_LOANS_TEMP from COCCDM db table
    
    Returns:
        result_df: filtered dataframe of wh_loans

    Operations:
    - Create a day difference between 
    """
    df['day diff'] = (df['rundate'] - df['origdate']).dt.days + 1
    result_df = df[df['day diff'] <= 45]
    return result_df
    
def drop_household_duplicates(househldacct):
    househldacct = househldacct.sort_values(by='datelastmaint', ascending=False).drop_duplicates(subset='acctnbr', keep='first').copy()
    return househldacct

def drop_org_duplicates(wh_org):
    wh_org = wh_org.drop_duplicates(subset='orgnbr', keep='first').copy()
    return wh_org

# %%
# filtered_wh_loans = filter_wh_loans(wh_loans)

# %%
def consolidate_prop_data(wh_prop, wh_prop2):
    """
    Consolidate property data between the two property tables in COCC

    Args:
        wh_prop
        wh_prop2

    Returns:
        consolidated_prop_data

    Operations:
    - merge the tables
    - rename columns
    - keep only the property with the highest appraised value
    - fill null values in aprsvalueamt field

    """
    consolidated_prop_data = pd.merge(wh_prop, wh_prop2, how='inner', on='propnbr')
    consolidated_prop_data['acctnbr'] = consolidated_prop_data['acctnbr_x'].combine_first(consolidated_prop_data['acctnbr_y'])
    consolidated_prop_data = consolidated_prop_data.drop(columns=['acctnbr_x','acctnbr_y'])
    consolidated_prop_data['aprsvalueamt'] = consolidated_prop_data['aprsvalueamt'].fillna(0)
    consolidated_prop_data = (consolidated_prop_data.sort_values('aprsvalueamt', ascending=False).groupby('acctnbr', as_index=False).first())
    consolidated_prop_data = consolidated_prop_data.reset_index(drop=True)
    return consolidated_prop_data

# %%
# consolidated_prop_data = consolidate_prop_data(wh_prop, wh_prop2)

# %%
def merge_data(filtered_acctcommon, filtered_wh_loans, wh_acctloan, consolidated_prop_data, wh_org, househldacct):
    """
    Merging dataframes together
    
    Args:
        dfs: all dataframes
    
    Returns:
        merged_df: merged data
    """

    # QA tests
    assert filtered_acctcommon['acctnbr'].is_unique, "Duplicates found"
    assert househldacct['acctnbr'].is_unique, "Duplicates found"
    assert wh_acctloan['acctnbr'].is_unique, "Duplicates found"
    assert consolidated_prop_data['acctnbr'].is_unique, "Duplicates found"
    assert wh_org['orgnbr'].is_unique, "Duplicates found"

    merged_df = pd.merge(filtered_acctcommon, filtered_wh_loans, on='acctnbr', how='inner')
    merged_df = pd.merge(merged_df, wh_acctloan, on='acctnbr', how='left')
    merged_df = pd.merge(merged_df, consolidated_prop_data, on='acctnbr', how='left')
    merged_df = merged_df.drop(columns=['propnbr_y'])
    merged_df = merged_df.rename(columns={'propnbr_x':'propnbr'})
    merged_df = pd.merge(merged_df, wh_org, left_on='taxrptfororgnbr', right_on='orgnbr', how='left').sort_values(by='origdate', ascending=False)
    merged_df = pd.merge(merged_df, househldacct, how='left', on='acctnbr')
    return merged_df

def column_to_index(column):
    """
    Convert Excel column letters to column index for formatting
    """
    index = 0
    for i, char in enumerate(reversed(column.upper())):
        index += (ord(char) - 64) * (26 ** i)
    return index

# %%
# merged_df = merge_data(filtered_acctcommon, filtered_wh_loans, wh_acctloan, consolidated_prop_data, wh_org)






# %%
# Potential Outstanding
def filter_and_merge_loan_tables(acctcommon, acctloan, loans):
    """
    This filters on CML Loans & merges tables to consolidate loan data.
    Data cleansing on numeric fields is performed.
    
    Args:
        acctcommon: WH_ACCTCOMMON
        acctloan: WH_ACCTLOAN
        loans: WH_LOANS
        
    Returns:
        df: Consolidated loan data as a dataframe
        
    Operations:
        - mjaccttypcd (Major) == 'CML'
        - left merge of df (acctcommon) & acctloan on 'acctnbr'
        - left merge of df & loans on 'acctnbr'
        - drop all fields that are completely null/empty
        - Replace null/na values with 0 for numeric fields:
            - total pct sold
            - avail bal amt
            - credit limit collateral reserve amt
        - loans with risk rating 4 or 5 are excluded
    """
    # CML loans
    df = acctcommon[acctcommon['mjaccttypcd'].isin(['CML'])]
    df = df[df['curracctstatcd'].isin(['ACT','NPFM'])]

    # Merging and dropping blank fields
    df = pd.merge(df, acctloan, on='acctnbr', how='left', suffixes=('_df', '_acctloan'))
    df = pd.merge(df, loans, on='acctnbr', how='left', suffixes=('_df', '_loans'))
    df = df.dropna(axis=1, how='all')
    
    # Data Cleansing
    df['totalpctsold'] = df['totalpctsold'].fillna(0)
    df['availbalamt'] = df['availbalamt'].fillna(0)
    df['credlimitclatresamt'] = df['credlimitclatresamt'].fillna(0)
    
    return df



def append_total_exposure_field(df):
    """ 
    Single Obligor Exposure Calculation
    
    Args:
        df: loan_data is loaded in
    
    Returns:
        df: loan_data is returned with new fields appended
        
    Operations:
        bookbalance -> if currmiaccttypcd == 'CM45', use notebal, else bookbalance
            - Tax Exempt bonds always have $0 as book balance so adjustment is made
        net balance == bookbalance - cobal
            - BCSB balance - Charged off amount (COBAL)
        net available == available balance amount * (1 - total pct sold)
        net collateral reserve == collateral reserve * (1 - total pct sold)
        total exposure == net balance + net available + net collateral reserve
    """
    # QA test
    list_of_numeric = ['bookbalance','notebal','availbalamt','totalpctsold','noteopenamt','noteintrate','cobal','credlimitclatresamt']
    for col in list_of_numeric:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    def convert_to_float(value):
        try:
            return float(value)
        except:
            return None
        
    for col in list_of_numeric:
        df[col] = df[col].apply(convert_to_float)
    
    # Tax Exempt bonds always have $0 Book Balance so need to take NOTEBAL
    df['bookbalance'] = np.where(df['currmiaccttypcd'].isin(['CM45']), df['notebal'], df['bookbalance'])
    df['Net Balance'] = df['bookbalance'] - df['cobal']
    df['Net Available'] = df['availbalamt'] * (1 - df['totalpctsold'])
    df['Net Collateral Reserve'] = df['credlimitclatresamt'] * (1 - df['totalpctsold'])
    df['Total Exposure'] = df['Net Balance'] + df['Net Available'] + df['Net Collateral Reserve']
    return df



# %%
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
            if file_date <= today_date:
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
    
def append_grouping_keys(loan_data, househldacct, pkey):
    assert househldacct['acctnbr'].is_unique, "Duplicates found"
    assert pkey['acctnbr'].is_unique, "Duplicates found"

    loan_data = pd.merge(loan_data, househldacct, on='acctnbr', how='left')
    loan_data = pd.merge(loan_data, pkey, on='acctnbr', how='left')
    return loan_data

def retrieve_historical_keys(history_path):
    if history_path is None:
        return None
    else:
        history = pd.read_csv(history_path)
        return history
    
# def append_historical_keys(data, history=None):
#     if history is None:
#         return data
#     else:
#         history_subset = history[['acctnbr','portfolio_key']]
#         assert history_subset['acctnbr'].is_unique, "Duplicates found"
#         data = pd.merge(data, history_subset, on='acctnbr', how='left')
#         data = data.set_index('acctnbr')
#         data = data.to_dict(orient='index').copy()
#         return data
    


# %%
def calculate_total_exposure(df):
    hh_exposure = df.groupby('householdnbr', as_index=False)['Total Exposure'].sum()
    hh_exposure = hh_exposure.rename(columns={'Total Exposure':'total_exposure_hh'}).copy()
    pkey_exposure = df.groupby('portfolio_key', as_index=False)['Total Exposure'].sum()
    pkey_exposure = pkey_exposure.rename(columns={'Total Exposure':'total_exposure_pkey'}).copy()
    hh_exposure = pd.DataFrame(hh_exposure)
    pkey_exposure = pd.DataFrame(pkey_exposure)

    df = pd.merge(df, hh_exposure, on='householdnbr', how='left')
    df = pd.merge(df, pkey_exposure, on='portfolio_key', how='left')
    return df

# %%
def append_exposure(df, keys_df):
    # QA test
    list_of_numeric = ['bookbalance','notebal','availbalamt','totalpctsold','noteopenamt','noteintrate','cobal','credlimitclatresamt']
    for col in list_of_numeric:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    def convert_to_float(value):
        try:
            return float(value)
        except:
            return None
        
    for col in list_of_numeric:
        df[col] = df[col].apply(convert_to_float)

    assert df['acctnbr'].is_unique, "Duplicates found"
    assert keys_df['acctnbr'].is_unique, "Duplicates found"

    df = pd.merge(df, keys_df, how='left', on='acctnbr')
    return df

# %%
# NEW LOAN section
def split_data(df):
    """
    Goal is to split the data between CML & MTG for this section, add subtitles, and necessary blank fields
    """
    df['Notes'] = None
    df['Next Rev Date'] = None
    df['Appr in CT File'] = None
    df['Exceptions on List'] = None

    cml = df.loc[df['mjaccttypcd'] == 'CML', [
        'Notes',
        'Next Rev Date',
        'Appr in CT File',
        'Exceptions on List',
        'householdnbr',
        'contractdate',
        'product',
        'loanofficer',
        'ownersortname',
        'acctnbr',
        'origbal',
        'notebal',
        'availbalamt',
        'total_exposure_hh',
        'total_exposure_pkey',
        'riskratingcd',
        'fdiccatcd',
        'fdiccatdesc',
        'naicscd',
        'naicscddesc',
        'proptypecd',
        'proptypdesc',
        'noteintrate',
        'propnbr',
        'propdesc',
        'noteopenamt'
    ]].copy()

    cml = cml.sort_values(by='contractdate', ascending=False)

    mtg = df.loc[df['mjaccttypcd'] == 'MTG', [
        'Notes',
        'Next Rev Date',
        'Appr in CT File',
        'Exceptions on List',
        'householdnbr',
        'contractdate',
        'product',
        'loanofficer',
        'ownersortname',
        'acctnbr',
        'origbal',
        'notebal',
        'availbalamt',
        'total_exposure_hh',
        'total_exposure_pkey',
        'riskratingcd',
        'fdiccatcd',
        'fdiccatdesc',
        'naicscd',
        'naicscddesc',
        'proptypecd',
        'proptypdesc',
        'noteintrate',
        'propnbr',
        'propdesc',
        'noteopenamt'
    ]].copy()

    mtg = mtg.sort_values(by='contractdate', ascending=False)

    def create_subtitle_row(df, subtitle):
        """
        Create a new row with a subtitle to break sections apart

        Args:
            df: either cml or mtg
            subtitle (str): section title
        
        Returns:
            df with additional row for subtitle
        """
        new_row = pd.DataFrame(columns=df.columns)
        new_row.loc[1, 'product'] = subtitle
        new_row = new_row.fillna('')
        df = pd.concat([new_row, df]).copy()
        return df
    
    cml = create_subtitle_row(cml, 'Commercial Loans')
    mtg = create_subtitle_row(mtg, 'Residential Loans')

    blank_row = pd.DataFrame(columns=cml.columns)
    blank_row = blank_row.fillna('')
    
    df = pd.concat([cml, blank_row])
    df = pd.concat([df, mtg])

    return df



# %%
# CRA section
def cra_section(df):
    """
    CRA Sheet creation
    """
    df['#'] = None
    # df['Committed'] = None
    df['Round'] = None
    df['Gross Sales'] = None
    df['MSA'] = None
    df['State'] = None
    df['County'] = None
    df['Census'] = None
    df['SBP'] = None
    df['Reason'] = None
    df['Comments'] = None

    df = df.loc[~(df['currmiaccttypcd'].isin(['CM15','CM16']))].copy()
    df = df.loc[df['mjaccttypcd'] != 'MTG'].copy()

    df = df.loc[df['mjaccttypcd'] == 'CML', [
        '#',
        'contractdate',
        'ownersortname',
        'acctnbr',
        'noteopenamt',
        'Round',
        'Gross Sales',
        'primary_address',
        'primaryownercity',
        'primaryownerstate',
        'primaryownerzipcd',
        'Comments',
        'fdiccatcd',
        'MSA',
        'State',
        'County',
        'Census',
        'product',
        'SBP',
        'Reason',
        'noteintrate',
        'loanofficer',
        'origdate',
        'proptypdesc',
        'riskratingcd'
    ]].copy()

    df = df.sort_values(by='contractdate', ascending=False)

    return df



# %%
# %%
# %%
def main():
    data = retrieve_data()

    wh_acctcommon = data['wh_acctcommon'].copy()
    wh_loans = data['wh_loans'].copy()
    wh_acctloan = data['wh_acctloan'].copy()
    wh_org = data['wh_org'].copy()
    wh_prop = data['wh_prop'].copy()
    wh_prop2 = data['wh_prop2'].copy()
    househldacct = data['househldacct'].copy()


    filtered_acctcommon = filter_acctcommon(wh_acctcommon)
    filtered_wh_loans = filter_wh_loans(wh_loans)
    consolidated_prop_data = consolidate_prop_data(wh_prop, wh_prop2)

    househldacct = drop_household_duplicates(househldacct)
    wh_org = drop_org_duplicates(wh_org)
    merged_df = merge_data(filtered_acctcommon, filtered_wh_loans, wh_acctloan, consolidated_prop_data, wh_org, househldacct)

    # %%
    loan_data = filter_and_merge_loan_tables(wh_acctcommon, wh_acctloan, wh_loans)
    loan_data = append_total_exposure_field(loan_data)

    # %%
    historical_path = r'\\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Chad Projects\R360\Production\Output'
    historical_path = get_most_recent_file(historical_path)

    pkey = retrieve_historical_keys(historical_path)
    pkey = pkey.loc[:,['acctnbr','portfolio_key']].copy()
    loan_data = append_grouping_keys(loan_data, househldacct, pkey)


    # %%

    loan_data = calculate_total_exposure(loan_data)
    loan_data_keys = loan_data.loc[:,['acctnbr','total_exposure_hh','total_exposure_pkey']].copy()


    merged_df = append_exposure(merged_df, loan_data_keys)

    # %%
    new_loan_page = split_data(merged_df)
    cra_page = cra_section(merged_df)

    # %%


    # Output to excel
    current_date = datetime.now().strftime('%Y%m%d')
    file_path = r'\\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Chad Projects\Weekly Reports\NewLoanReport_LR_Credit\Production\Output'
    file_name = f'Loan_Report_45_day_lookback_{current_date}.xlsx'
    full_path = os.path.join(file_path, file_name)
    with pd.ExcelWriter(full_path, mode='w', engine='openpyxl') as writer:
        new_loan_page.to_excel(writer, sheet_name='NEW LOAN', index=False)
        cra_page.to_excel(writer, sheet_name='CRA', index=False)

    try:
        excel = win32.Dispatch("Excel.Application")
        excel.Visible = False
        workbook = excel.Workbooks.Open(full_path)
        
        ## NEW LOAN
        sheet = workbook.Worksheets("NEW LOAN")

        sheet.Columns.AutoFit()

        # Bold top row
        top_row = sheet.Rows(1)
        top_row.Font.Bold = True

        # Add bottom border to header row
        bottom_border = top_row.Borders(9)
        bottom_border.LineStyle = 1
        bottom_border.Weight = 2

        date_columns = ["F"]

        for col in date_columns:
            col_index = column_to_index(col)
            sheet.Columns(col_index).NumberFormat = "mm/dd/yyyy"

        dollar_columns = ["K","L","M","N","O","Z"]
        
        for col in dollar_columns:
            col_index = column_to_index(col)
            sheet.Columns(col_index).NumberFormat = "$###,##0.00"

        percentage_columns = ["W"]
        
        for col in percentage_columns:
            col_index = column_to_index(col)
            sheet.Columns(col_index).NumberFormat = "0.00%"
        

        # Freeze top row
        sheet.Application.ActiveWindow.SplitRow = 1
        sheet.Application.ActiveWindow.FreezePanes = True

        ## CRA
        sheet = workbook.Worksheets("CRA")

        sheet.Columns.AutoFit()

        # Bold top row
        top_row = sheet.Rows(1)
        top_row.Font.Bold = True

        # Add bottom border to header row
        bottom_border = top_row.Borders(9)
        bottom_border.LineStyle = 1
        bottom_border.Weight = 2

        date_columns = ["B","W"]

        for col in date_columns:
            col_index = column_to_index(col)
            sheet.Columns(col_index).NumberFormat = "mm/dd/yyyy"

        dollar_columns = ["E"]
        
        for col in dollar_columns:
            col_index = column_to_index(col)
            sheet.Columns(col_index).NumberFormat = "$###,##0.00"


        percentage_columns = ["U"]
        
        for col in percentage_columns:
            col_index = column_to_index(col)
            sheet.Columns(col_index).NumberFormat = "0.00%"
        

        # Freeze top row
        sheet.Application.ActiveWindow.SplitRow = 1
        sheet.Application.ActiveWindow.FreezePanes = True


        workbook.Save()
        workbook.Close()

        print(f"Excel file saved with autofit at {file_path}")
    finally:
        try:
            if 'workbook' in locals() and workbook is not None:
                workbook.Close(SaveChanges=False)
        except:
            pass
        try:
            if 'excel' in locals():
                excel.Quit()
        except:
            pass
        print("Excel process complete")

    # Email
    recipients = [
        # "chad.doorley@bcsbmail.com"
        "paul.kocak@bcsbmail.com",
        "linda.clark@bcsbmail.com"
    ]
    bcc_recipients = [
        "chad.doorley@bcsbmail.com"
    ]
    outlook = win32.Dispatch("Outlook.Application")
    message = outlook.CreateItem(0)
    # message.Display()
    message.To = ";".join(recipients)
    message.BCC = ";".join(bcc_recipients)
    message.Subject = f"Weekly Loan Report - {datetime.now().strftime('%m/%d/%Y')}"
    message.Body = "Hi all, \n\nAttached is the Weekly Loan Report with a 45 day lookback. Please let me know if you have any questions."
    message.Attachments.Add(str(full_path))
    message.Send()
    print("Email sent!")


# %%
if __name__ == '__main__':
    main()

# %%



# %%





# %%



