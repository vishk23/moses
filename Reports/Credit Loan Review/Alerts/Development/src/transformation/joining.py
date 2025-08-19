"""
Joining/Cleaning module

Usage:
    import src.transformation.joining
"""
import pandas as pd # type: ignore


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
    df = df[~df['product'].isin(['ACH Manager'])]  

    
    # Unit test
    assert not df['curracctstatcd'].isin(['NPFM']).any(), "NPFM loans were not filtered out"
    assert not df['riskratingcd'].isin(['4','5']).any(), "4 and 5 rated loans were not filtered out"
    
    return df

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

def get_inactive_date(acctloanlimithist: pd.DataFrame) -> pd.DataFrame:
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
    df = pd.DataFrame(df)

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


