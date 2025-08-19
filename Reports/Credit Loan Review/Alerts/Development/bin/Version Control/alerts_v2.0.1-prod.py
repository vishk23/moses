# %%
# Portfolio Alerts
# Developed by CD
# v2.0.1-prod

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
        # engine 1
        acctcommon = text("""
        SELECT 
            a.ACCTNBR, 
            a.EFFDATE, 
            a.MJACCTTYPCD, 
            a.PRODUCT, 
            a.CURRMIACCTTYPCD, 
            a.BOOKBALANCE, 
            a.LOANOFFICER, 
            a.OWNERNAME, 
            a.CURRACCTSTATCD, 
            a.CONTRACTDATE, 
            a.NOTEBAL
        FROM 
            OSIBANK.WH_ACCTCOMMON a
        WHERE 
            a.CURRACCTSTATCD IN ('ACT')
        """)

        acctloan = text("""
        SELECT 
            a.ACCTNBR, 
            a.COBAL, 
            a.CREDITLIMITAMT, 
            a.RISKRATINGCD, 
            a.TOTALPCTSOLD, 
            a.CREDLIMITCLATRESAMT
        FROM 
            OSIBANK.WH_ACCTLOAN a
        """)

        loans = text("""
        SELECT 
            a.ACCTNBR, 
            a.AVAILBALAMT
        FROM 
            OSIBANK.WH_LOANS a
        """)

        househldacct = text("""
        SELECT 
            a.HOUSEHOLDNBR, 
            a.ACCTNBR
        FROM 
            OSIEXTN.HOUSEHLDACCT a
        """)

        allroles = text("""
        SELECT 
            *
        FROM 
            OSIBANK.WH_ALLROLES a
        WHERE
            a.ACCTROLECD IN ('GUAR')
        """)

        persaddruse = text("""
        SELECT 
            *
        FROM 
            OSIBANK.PERSADDRUSE
        """)

        wh_addr = text("""
        SELECT 
            *
        FROM 
            OSIBANK.WH_ADDR
        """)

        pers = text("""
        SELECT 
            *
        FROM 
            OSIBANK.PERS
        """)

        acctstatistichist = text("""
        SELECT 
            *
        FROM 
            OSIBANK.ACCTSTATISTICHIST
        """)

        acctloanlimithist = text("""
        SELECT 
            *
        FROM 
            OSIBANK.ACCTLOANLIMITHIST
        """)

        queries = [
            {'key':'acctcommon', 'sql':acctcommon, 'engine':1},
            {'key':'acctloan', 'sql':acctloan, 'engine':1},
            {'key':'loans', 'sql':loans, 'engine':1},
            {'key':'househldacct', 'sql':househldacct, 'engine':1},
            {'key':'allroles', 'sql':allroles, 'engine':1},
            {'key':'persaddruse', 'sql':persaddruse, 'engine':1},
            {'key':'wh_addr', 'sql':wh_addr, 'engine':1},
            {'key':'pers', 'sql':pers, 'engine':1},
            {'key':'acctstatistichist', 'sql':acctstatistichist, 'engine':1},
            {'key':'acctloanlimithist', 'sql':acctloanlimithist, 'engine':1},
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


#################################
# Core ETL

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

    # Merging and dropping blank fields
    df = pd.merge(df, acctloan, on='acctnbr', how='left', suffixes=('_df', '_acctloan'))
    df = pd.merge(df, loans, on='acctnbr', how='left', suffixes=('_df', '_loans'))
    df = df.dropna(axis=1, how='all')
    
    # Data Cleansing
    df['totalpctsold'] = df['totalpctsold'].fillna(0)
    df['availbalamt'] = df['availbalamt'].fillna(0)
    df['credlimitclatresamt'] = df['credlimitclatresamt'].fillna(0)
    df = df[~df['riskratingcd'].isin(['4','5'])]
    df = df[~df['curracctstatcd'].isin(['NPFM'])] # This is handled by SQL query normally
    
    # Unit test
    assert not df['curracctstatcd'].isin(['NPFM']).any(), "NPFM loans were not filtered out"
    assert not df['riskratingcd'].isin(['4','5']).any(), "4 and 5 rated loans were not filtered out"
    
    return df


#################################
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
    
    
    # Tax Exempt bonds always have $0 Book Balance so need to take NOTEBAL
    df['bookbalance'] = np.where(df['currmiaccttypcd'].isin(['CM45']), df['notebal'], df['bookbalance'])
    df['Net Balance'] = df['bookbalance'] - df['cobal']
    df['Net Available'] = df['availbalamt'] * (1 - df['totalpctsold'])
    df['Net Collateral Reserve'] = df['credlimitclatresamt'] * (1 - df['totalpctsold'])
    df['Total Exposure'] = df['Net Balance'] + df['Net Available'] + df['Net Collateral Reserve']
    return df

def drop_hh_duplicates(df):
    """
    Drop duplicate rows in Household table
    
    Args:
        df: HOUSEHLDACCT table (COCC)
        
    Returns:
        cleaned_df: de-duplicated df
        
    Operations:
        - drop_duplicates(subset='acctnbr', keep='first')
    """
    cleaned_df = df.drop_duplicates(subset='acctnbr', keep='first')
    
    assert cleaned_df['acctnbr'].duplicated().sum() == 0, "There are duplicate acctnbrs" 
    
    return cleaned_df

def append_household_number(df, househldacct):
    """
    Append Household Number to Loan Data
    
    Args:
        df: loan_data
        househldacct: Household Acct Table from COCC (OSIEXTEN.HOUSEHLDACCT)
    
    Returns:
        df: loan_data with household number appended
        
    Operations:
        - Left merge of df & househldacct table on 'acctnbr'
    """
    df = pd.merge(df, househldacct, on='acctnbr', how='left', suffixes=('_df', '_househldacct'))
    return df


def household_total_exposure(df):
    """
    Household Total Exposure:
    Grouping on household key, the total exposure is summed
    
    Args:
        df: loan_data
    
    Returns:
        household_grouping_df: A new dataframe with 2 columns:
            - Householdnbr
            - Total Exposure ($)
    
    Operations:
        - Group By: Householdnbr
        - Sum: Total Exposure
    
    """
    household_grouping_df = df.groupby('householdnbr')['Total Exposure'].sum().reset_index()
    household_grouping_df = pd.DataFrame(household_grouping_df)
    return household_grouping_df


def append_household_exposure(df, household_grouping_df):
    """
    Append household exposure back to loan_data
    
    Args:
        df: loan_data
        household_grouping_df: df with household number & total exposure
        
    Returns:
        df: loan data after appending household exposure
        
    Operations:
        - Left merge of df & household_grouping_df on 'householdnbr'
        
    """
    df = pd.merge(df, household_grouping_df, on='householdnbr', how='left', suffixes=('_df','_hhgroup'))
    return df

def filter_to_target_products(df):
    """ 
    Filtering data down to products within Alerts criteria
    
    Args:
        df: loan_data
    
    Returns:
        df: loan_data after filters are applied to set the scope of Alerts system
        
    Operations:
        - currmiaccttypcd (minor) is in:
            - "CM06","CM11","CM30","CM52","CM57","CM62","CM71","CM76"
        - creditlimitamt <= $500,000
        - total household exposure <= $1,000,000
    """
    # Lines of Credit
    df = df[df['currmiaccttypcd'].isin(["CM06","CM11","CM30","CM52","CM57","CM62","CM71","CM76"])]
    # Credit Limit Amount <= $500M & Household Exposure <= $1MM
    df = df[(df['creditlimitamt'] <= 500000) & (df['Total Exposure_hhgroup'] <= 1000000)]
    return df


#################################
# Personal Guarantors extracted
def personal_guarantors(allroles, persaddruse, wh_addr, pers):
    """
    Personal Guarantor information is pulled from COCC and several tables are merged.
    
    Args:
        allroles: ALLROLES table (COCC)
        persaddruse: PERSADDRUSE table (COCC)
        wh_addr: WH_ADDR table (COCC)
        pers: WH_PERS table (COCC)
        
    Returns:
        df: Dataframe of personal guarantors
        
    Operations:
        - allroles table where 'acctrolecd' = 'GUAR' (guarantor role)
        - allroles where 'persnbr' is not null (this excludes organizations)
        - persaddruse where 'addrusecd' == 'PRI' (only primary address is considered)
        - left merge of allroles & persaddruse tables on 'persnbr'
        - left merge of df (merged df from earlier step) & wh_addr on 'addrnbr'
        - left merge of df & pers on 'persnbr'
        - filtered out unnecessary fields
            - keeping only ['acctnbr','persnbr','firstname','lastname','text1',
                            'cityname','statecd','zipcd']
    """
    allroles = allroles[allroles['acctrolecd'] == 'GUAR']
    allroles = allroles[allroles['persnbr'].notnull()]
    persaddruse = persaddruse[persaddruse['addrusecd'] == "PRI"]
    # Merge
    df = pd.merge(allroles, persaddruse, on='persnbr',how='left', suffixes=('_allroles','_persaddruse'))
    df = pd.merge(df, wh_addr, on='addrnbr',how='left', suffixes=('_df','_addr'))
    df = pd.merge(df, pers, on='persnbr', how='left', suffixes=('_df','_pers'))
    df = df[['acctnbr','persnbr','firstname','lastname','text1','cityname','statecd','zipcd']]
    return df

def merge_guar_with_loan_data(df, pg_section):
    """
    Merging Loan Data & Personal Guarantor information
    
    Args:
        df: loan_data
        pg_section: personal guarantor dataframe
    
    Returns:
        df: loan_data merged with personal guarantor data (inner merge)
        
    Operations:
        - Inner merge of df & pg_section (personal guarantor section) on 'acctnbr'
    """
    df = pd.merge(df, pg_section, on='acctnbr', how='inner', suffixes=('_df','_pg'))
    return df


#################################
def acctstatistichist_cleaning(df, acctcommon):
    """ 
    Cleans acctstatistichist table and adds new fields for filtering
    
    Args:
        df: ACCTSTATISTICHIST table (COCC)
        acctcommon: WH_ACCTCOMMON table (COCC)
            - Used for current date
    
    Returns:
        df: ACCSTATISTICHIST with new calculated date fields
            - 'event_date': date (month) of event occurance
            - 'current_date': current_date
            - 'year_start': First day of year (used for YTD calculations)
            - 'year_ago_date': Today's date minus 1 year (for TTM calculations)
        
    Operations:
        - monthcd zero fill 2 digits
        - monthcd to string type
        - yearnbr to string type
        - event_date field = df['yearnbr'] + "-" + df['monthcd'] + "-01"
        - current_date == First record in EFFDATE field from acctcommon table
            -> this is appended to the dataframe as 'current_date' column
        - year_start = current_date year + '01-01'
        - year_ago_date = current_date - 1 year
    """
    df['monthcd'] = df['monthcd'].str.zfill(2)
    df['monthcd'] = df['monthcd'].astype(str)
    df['yearnbr'] = df['yearnbr'].astype(str)
    df['event_date'] = df['yearnbr'] + "-" + df['monthcd'] + "-01"
    df['event_date'] = pd.to_datetime(df['event_date'])
    
    current_date = acctcommon['effdate'][0]
    df['current_date'] = current_date
    
    df['year_start'] = pd.to_datetime(df['current_date'].dt.year.astype(str) + '-01-01')
    df['year_ago_date'] = df['current_date'] - pd.DateOffset(years=1)
    
    return df


#################################
def count_pd(df):
    """
    This will count past due (15+) flags on the account
    
    Args:
        df: ACCTSTATISTICHIST table (COCC)
        
    Returns:
        merged_df: A dataframe with 3 columns:
            - acctnbr
            - ytd_pd (count)
            - ttm_pd (count)
    
    Operations:
        - ytd_df created where event_date >= year_start date
        - ttm_df created where event_date >= year_ago date
        - statistictypcd (statistic type code) = 'PD'
        - Group by acctnbr, sum statistic count
        - rename columns to ytd_pd & ttm_pd
        - Outer merge ytd_df & ttm_df on acctnbr
        - fill null values with 0
    """
    ytd_df = df[df['event_date'] >= df['year_start']]
    ttm_df = df[df['event_date'] >= df['year_ago_date']]
    
    ytd_df = ytd_df[ytd_df['statistictypcd'].isin(['PD'])]
    ttm_df = ttm_df[ttm_df['statistictypcd'].isin(['PD'])]
    
    # Unit Tests
    assert (ytd_df['event_date'] >= ytd_df['year_start']).all(), "Filtering did not apply correctly"
    assert (ttm_df['event_date'] >= ttm_df['year_ago_date']).all(), "Filtering did not apply correctly"
    
    ytd_df = ytd_df.groupby('acctnbr')['statisticcount'].sum().reset_index()
    ttm_df = ttm_df.groupby('acctnbr')['statisticcount'].sum().reset_index()
    
    ytd_df = ytd_df.rename(columns={'statisticcount':'ytd_pd'})
    ttm_df = ttm_df.rename(columns={'statisticcount':'ttm_pd'})
    
    merged_df = pd.merge(ytd_df, ttm_df, on='acctnbr', how='outer')
    merged_df['ytd_pd'] = merged_df['ytd_pd'].fillna(0)
    merged_df['ttm_pd'] = merged_df['ttm_pd'].fillna(0)
    
    # Unit Tests
    assert merged_df['ytd_pd'].isnull().sum() == 0, "There are null values"
    assert merged_df['ttm_pd'].isnull().sum() == 0, "There are null values"

    
    return merged_df


#################################
def count_pd30(df):
    """
    This will count past due (30+) flags on the account
    
    Args:
        df: ACCTSTATISTICHIST table (COCC)
        
    Returns:
        merged_df: A dataframe with 3 columns:
            - acctnbr
            - ytd_pd30 (count)
            - ttm_pd30 (count)
    
    Operations:
        - ytd_df created where event_date >= year_start date
        - ttm_df created where event_date >= year_ago date
        - statistictypcd (statistic type code) = 'PD30'
        - Group by acctnbr, sum statistic count
        - rename columns to ytd_pd30 & ttm_pd30
        - Outer merge ytd_df & ttm_df on acctnbr
        - fill null values with 0
    """
    ytd_df = df[df['event_date'] >= df['year_start']]
    ttm_df = df[df['event_date'] >= df['year_ago_date']]
    
    ytd_df = ytd_df[ytd_df['statistictypcd'].isin(['PD30'])]
    ttm_df = ttm_df[ttm_df['statistictypcd'].isin(['PD30'])]
    
    # Unit Tests
    assert (ytd_df['event_date'] >= ytd_df['year_start']).all(), "Filtering did not apply correctly"
    assert (ttm_df['event_date'] >= ttm_df['year_ago_date']).all(), "Filtering did not apply correctly"
    
    ytd_df = ytd_df.groupby('acctnbr')['statisticcount'].sum().reset_index()
    ttm_df = ttm_df.groupby('acctnbr')['statisticcount'].sum().reset_index()
    
    ytd_df = ytd_df.rename(columns={'statisticcount':'ytd_pd30'})
    ttm_df = ttm_df.rename(columns={'statisticcount':'ttm_pd30'})
    
    merged_df = pd.merge(ytd_df, ttm_df, on='acctnbr', how='outer')
    merged_df['ytd_pd30'] = merged_df['ytd_pd30'].fillna(0)
    merged_df['ttm_pd30'] = merged_df['ttm_pd30'].fillna(0)
    
    # Unit Tests
    assert merged_df['ytd_pd30'].isnull().sum() == 0, "There are null values"
    assert merged_df['ttm_pd30'].isnull().sum() == 0, "There are null values"

    
    return merged_df


#################################
def append_pd_info(loan_data, pd_df, pd30_df):
    """
    Appending past due and past due 30 counts to loan data
    
    Args:
        loan_data: filtered down loan_data
        pd_df: past due 15 days data
        pd30_df: past due 30 days data
        
    Returns:
        df: loan_data, with appended past due and past due 30 counts
    
    Operations:
    """
    df = pd.merge(loan_data, pd_df, on='acctnbr', how='left')
    df = pd.merge(df, pd30_df, on='acctnbr', how='left')
    
    df['ytd_pd'] = df['ytd_pd'].fillna(0)
    df['ttm_pd'] = df['ttm_pd'].fillna(0)
    df['ytd_pd30'] = df['ytd_pd30'].fillna(0)
    df['ttm_pd30'] = df['ttm_pd30'].fillna(0)
    
    assert df['ytd_pd'].isnull().sum() == 0, "There are null values"
    assert df['ttm_pd'].isnull().sum() == 0, "There are null values"
    assert df['ytd_pd30'].isnull().sum() == 0, "There are null values"
    assert df['ttm_pd30'].isnull().sum() == 0, "There are null values"
    
    return df


#################################
def deposit_criteria_testing():
    """
    Consolidates deposits by household and calculates deposit change (%) over trailing 12 months
        
    Returns:
        grouped_df: deposit dataframe with deposit change over time and count of overdrafts for each household
        
    Operations:
        - Access daily deposit update from Excel file on DA-1 drive
        - Fill null values with 0 for columns:
            - NOTEBAL
            - Year Ago Balance
            - TTM Overdrafts
        - Group by household number and sum NOTEBAL, Year Ago Balance, and TTM Overdrafts
        - Deposit Change Pct = (NOTEBAL/Year Ago Balance) - 1
        - Renamed HOUSEHOLDNBR field to match loan_data householdnbr field
    """
    deposit_file_path = r'\\10.161.85.66\Home\Share\Line of Business_Shared Services\Commercial Credit\Deposits\DailyDeposit\DailyDeposit.xlsx'
    deposit_data = pd.read_excel(deposit_file_path, engine='openpyxl')
    
    deposit_data['NOTEBAL'].fillna(0)
    deposit_data['Year Ago Balance'].fillna(0)
    deposit_data['TTM Overdrafts'].fillna(0)

    grouped_df = deposit_data.groupby('HOUSEHOLDNBR').agg({
        'NOTEBAL':'sum',
        'Year Ago Balance':'sum',
        'TTM Overdrafts':'sum'
    }).reset_index()
    
    grouped_df['Deposit Change Pct'] = (grouped_df['NOTEBAL']/grouped_df['Year Ago Balance']) - 1
    grouped_df = grouped_df.rename(columns={'HOUSEHOLDNBR':'householdnbr'})
    
    return grouped_df 


#################################
def append_deposit_data(loan_data, deposit_data):
    """
    Append deposit criteria to the loan data
    
    Args:
        loan_data: loan data
        deposit_data: deposit data aggregated to household
        
    Returns:
        merged_df: loan_data with deposit data appended
        
    Operations:
        - left merge with loan_data & deposit data on householdnbr
    
    """
    merged_df = pd.merge(loan_data, deposit_data, on='householdnbr', how='left')
    return merged_df


#################################
def line_utilization_fetch(loan_data):
    """
    This function gathers line utilization data over past 12 months for each item
    
    Args:
        db_handler: Database Connection abstraction for SQL query
        loan_data: loan_data is passed in for unique account numbers
        
    Returns:
        df1: Line Utilization
            - 2 column table with:
                - acctnbr
                - avg line utilization over trailing 12 months
            
        df2: 30 Day Cleanup Provision
            - 2 column table with:
                - acctnbr
                - cleanup (1=Fail, 0=Pass)
    Operations:
        - unique account numbers extracted from loan_data
        - current_date and year_ago_date are calculated from loan_data (effdate)
        - SQL Query:
            SELECT b.ACCTNBR, b.EFFDATE, b.BOOKBALANCE, c.CREDITLIMITAMT
            FROM COCCDM.WH_ACCTCOMMON b
            JOIN COCCDM.WH_ACCTLOAN c
            ON b.ACCTNBR = c.ACCTNBR AND b.EFFDATE = c.EFFDATE
            WHERE b.ACCTNBR IN ({acctnbr_placeholder})
            AND b.EFFDATE BETWEEN TO_DATE('{year_ago_date}', 'yyyy-mm-dd hh24:mi:ss') AND TO_DATE('{current_date}', 'yyyy-mm-dd hh24:mi:ss')
        - if creditlimitamt is null, replace with 0
        - Calculate line utilization:
            - ttm line utilization = bookbalance / creditlimit amount
            - fill na values with 0 (0/0) and inf with 100 (credit limit = 0, bookbalance > 0)
            - group by acctnbr and take average line utilization
        - Calculate 30 day cleanup provision:
            - sort by acctnbr and effdate in ascending order
            - create a rolling 30 day window and adjust slider through full date range for each
            acctnbr
            - return 0 if it was paid to 0 for at least 30 days in past year, else return 1 (fail)
    
    """
    acctnbrs = loan_data['acctnbr'].unique().tolist()
    acctnbr_placeholder = ', '.join([f"'{acct}'" for acct in acctnbrs])
    
    current_date = loan_data['effdate'][0]
    temp_data = {
        'current_date': [current_date]
    }

    temp_df = pd.DataFrame(temp_data)
    temp_df

    temp_df['year_ago_date'] = temp_df['current_date'] - pd.DateOffset(years=1)

    current_date = temp_df['current_date'][0].strftime('%Y-%m-%d')+' 00:00:00'
    year_ago_date = temp_df['year_ago_date'][0].strftime('%Y-%m-%d')+' 00:00:00'
    
    def retrieve_data():

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
            query = text(f"""
                SELECT b.ACCTNBR, b.EFFDATE, b.BOOKBALANCE, c.CREDITLIMITAMT
                FROM COCCDM.WH_ACCTCOMMON b
                JOIN COCCDM.WH_ACCTLOAN c
                ON b.ACCTNBR = c.ACCTNBR AND b.EFFDATE = c.EFFDATE
                WHERE b.ACCTNBR IN ({acctnbr_placeholder})
                AND b.EFFDATE BETWEEN TO_DATE('{year_ago_date}', 'yyyy-mm-dd hh24:mi:ss') AND TO_DATE('{current_date}', 'yyyy-mm-dd hh24:mi:ss')
            """)

            queries = [
                {'key':'query', 'sql':query, 'engine':2},
                # {'key':'acctcommon', 'sql':acctcommon, 'engine':1},
                # {'key':'persaddruse', 'sql':persaddruse, 'engine':1},
                # {'key':'orgaddruse', 'sql':orgaddruse, 'engine':1},
                # {'key':'wh_addr', 'sql':wh_addr, 'engine':1},
                # {'key':'wh_allroles', 'sql':wh_allroles, 'engine':1},
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

    data = retrieve_data()
    df = data['query'].copy()
    
    df['bookbalance'] = pd.to_numeric(df['bookbalance'], errors='coerce')
    df['creditlimitamt'] = pd.to_numeric(df['creditlimitamt'], errors='coerce')
    
    df['creditlimitamt'] = df['creditlimitamt'].fillna(0)
    
    df1 = df
    df1['ttm line utilization'] = df1['bookbalance'] / df1['creditlimitamt']
    df1['ttm line utilization'] = df1['ttm line utilization'].fillna(0)
    df1['ttm line utilization'] = df1['ttm line utilization'].replace([np.inf], 1.00)
    df1 = df1.groupby('acctnbr')['ttm line utilization'].mean().reset_index()
    
    df2 = df
    df2['effdate'] = pd.to_datetime(df2['effdate'])
    df2 = df2.sort_values(by=['acctnbr','effdate'])
    
    def check_30_day_cleanup(group):
        group['rolling_zeros'] = group['bookbalance'].rolling(window=30).apply(lambda x: (x == 0).all(), raw=True)
        return 0 if (group['rolling_zeros'] == 1).any() else 1
    
    df2 = df2.groupby('acctnbr').apply(check_30_day_cleanup, include_groups=False).reset_index(name='cleanup_provision')
    
    return df1, df2


#################################
def append_line_utilization_data(loan_data, utilization_data, cleanup_data):
    """
    Appends line utilization data to loan_data
    
    Args:
        utilization_data: df with line utilization % over ttm
        cleanup_data : df with 30-day cleanup test (boolean)
        
    Returns:
        df: loan_data with additional tests
        
    Operations:
        - left merge with acctnbr & utilization data on acctnbr
        - left merge with acctnbr & cleanup_data on acctnbr
    """
    df = pd.merge(loan_data, utilization_data, on='acctnbr', how='left')
    df = pd.merge(df, cleanup_data, on='acctnbr', how='left')
    return df


#################################
def get_inactive_date(acctloanlimithist):
    """
    Getting inactive date for each item
    
    Args: 
        acctloanlimithist: ACCTLOANLIMITHIST table (COCC)
        
    Returns:
        df: df with the most recent inactive date per product
        
    Operations:
        - ensure inactivedate is a datetime field
        - groupby acctnbr, take max inactive date
    """
    acctloanlimithist['inactivedate'] = pd.to_datetime(acctloanlimithist['inactivedate'])
    df = acctloanlimithist.groupby('acctnbr')['inactivedate'].max().reset_index()
    
    assert df['acctnbr'].duplicated().sum() == 0, "There are duplicate acctnbrs"
    
    return df


#################################
def append_inactive_date(loan_data, inactive_date_df):
    """
    Append inactive date to loan_data
    
    Args:
        loan_data: loan_data
        inactive_date_df = df with the most recent inactive date per product
    
    Returns:
        df: loan_data with inactive date appended
    
    Operations:
        - left merge with loan_data & inactive_date on acctnbr
    
    """
    df = pd.merge(loan_data, inactive_date_df, on='acctnbr', how='left')
    return df


#################################
def criteria_flags(loan_data):
    """
    Criteria flags are assigned on to each line item for
    identification of fails.
    
    Args:
        loan_data
        
        # Parameters
        ttm_pd_amt = 3
        ttm_pd30_amt = 1
        ttm_overdrafts = 5
        deposit_change_pct = -.3
        min_deposits = 250000
        utilization_limit = .6
        
    Returns:
        df: loan_data with new identifier flag columns
            ['past_due_flag']
            ['ttm_overdrafts_flag']
            ['deposit_change_flag']
            ['ttm_utilization_flag']
            - 'cleanup_provision' already exists as a boolean column
    
    Operations:
        - parameters are set
        - if ttm_pd > parameter or ttm_pd30 >= parameter, then past_due_flag = 1, else 0
        - if ttm_overdrafts >= parameter, then ttm_overdrafts_flag = 1, else 0
        - if deposit_change_pct >= parameter, then deposit_change_flag = 1, else 0
        - if ttm_line_utilization >= parameter, then ttm_utilization_flag = 1, else 0
        - flag created for passing all tests (1: passed all, 0: failed at least 1)
    """
    
    # Parameters
    ttm_pd_amt = 3
    ttm_pd30_amt = 1
    ttm_overdrafts = 5
    deposit_change_pct = -.3
    min_deposits = 250000
    utilization_limit = .6
    
    # Flag Column Creation
    loan_data['past_due_flag'] = np.where((loan_data['ttm_pd'] >= ttm_pd_amt) | (loan_data['ttm_pd30'] >= ttm_pd30_amt), 1, 0) 
    loan_data['ttm_overdrafts_flag'] = np.where((loan_data['TTM Overdrafts'] >= ttm_overdrafts), 1, 0)
    loan_data['deposit_change_flag'] = np.where((loan_data['Deposit Change Pct'] <= deposit_change_pct) & (loan_data['Year Ago Balance'] >= min_deposits), 1, 0)
    loan_data['ttm_utilization_flag'] = np.where((loan_data['ttm line utilization'] >= .6), 1, 0)
    loan_data['passed_all_flag'] = np.where((loan_data['past_due_flag'] == 0) & (loan_data['ttm_overdrafts_flag'] == 0) & (loan_data['deposit_change_flag'] == 0) & (loan_data['ttm_utilization_flag'] == 0) & (loan_data['cleanup_provision'] == 0), 1, 0)
    
    return loan_data


# #################################
def main():

        # Database Connection Configuration
    data = retrieve_data()


    acctcommon = data['acctcommon'].copy()
    acctloan = data['acctloan'].copy()
    loans = data['loans'].copy()
    househldacct = data['househldacct'].copy()

    # # Data for Xactus
    # allroles = data['allroles'].copy()
    # persaddruse = data['persaddruse'].copy()
    # wh_addr = data['wh_addr'].copy()
    # pers = data['pers'].copy()

    acctstatistichist = data['acctstatistichist'].copy()
    acctloanlimithist = data['acctloanlimithist'].copy()

    # Core ETL
    loan_data = filter_and_merge_loan_tables(acctcommon, acctloan, loans)
    loan_data = append_total_exposure_field(loan_data)
    househldacct = drop_hh_duplicates(househldacct)
    loan_data = append_household_number(loan_data, househldacct)
    household_grouping_df = household_total_exposure(loan_data)
    loan_data = append_household_exposure(loan_data, household_grouping_df)
    loan_data = filter_to_target_products(loan_data)
    acctstatistic_output = acctstatistichist_cleaning(acctstatistichist, acctcommon)
    pd_df = count_pd(acctstatistic_output)
    pd30_df = count_pd30(acctstatistic_output)
    loan_data = append_pd_info(loan_data, pd_df, pd30_df)
    deposit_data = deposit_criteria_testing()
    loan_data = append_deposit_data(loan_data, deposit_data)
    utilization_data, cleanup_data = line_utilization_fetch(loan_data)
    loan_data = append_line_utilization_data(loan_data, utilization_data, cleanup_data)
    inactive_date_df = get_inactive_date(acctloanlimithist)
    loan_data = append_inactive_date(loan_data, inactive_date_df)
    loan_data = criteria_flags(loan_data)

    # Consolidation of the columns necessary
    final_df = loan_data[['acctnbr','effdate','ownername','product','loanofficer','inactivedate','Net Balance','Net Available','Net Collateral Reserve','cobal','creditlimitamt','Total Exposure_hhgroup','ttm_pd','ttm_pd30','TTM Overdrafts','NOTEBAL','Year Ago Balance','Deposit Change Pct','ttm line utilization','cleanup_provision','riskratingcd','past_due_flag','ttm_overdrafts_flag','deposit_change_flag','ttm_utilization_flag','passed_all_flag']]

    # Writing output
    file_path = r'\\10.161.85.66\Home\Share\Data & Analytics Initiatives\Project Management\Chad Projects\Alerts\Production\Output\alerts.xlsx'
    final_df.to_excel(file_path, index=False, engine='openpyxl')

    # Produce Documentation (docstrings)
    documentation_list = [
                            filter_and_merge_loan_tables, 
                            append_total_exposure_field, 
                            append_household_number, 
                            household_total_exposure, 
                            append_household_exposure, 
                            filter_to_target_products,
                            acctstatistichist_cleaning,
                            count_pd,
                            count_pd30,
                            append_pd_info,
                            deposit_criteria_testing,
                            append_deposit_data,
                            line_utilization_fetch,
                            append_line_utilization_data,
                            get_inactive_date,
                            append_inactive_date,
                            criteria_flags]

    # for i in documentation_list:
    #     print(help(i))
    #     print("")
        
    print('Execution Complete!')
    
if __name__ == "__main__":
    main()

    




