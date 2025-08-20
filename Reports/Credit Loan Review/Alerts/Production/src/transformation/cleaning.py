"""
Data Cleaning module

Usage src.transformation.cleaning
"""
import pandas as pd # type: ignore

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

def acctstatistichist_cleaning(df: pd.DataFrame, acctcommon: pd.DataFrame) -> pd.DataFrame:
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
    df['monthcd'] = df['monthcd'].astype(str).str.zfill(2)
    df['yearnbr'] = df['yearnbr'].astype(str)
    df['event_date'] = df['yearnbr'] + "-" + df['monthcd'] + "-01"
    df['event_date'] = pd.to_datetime(df['event_date'])

    current_date = acctcommon['effdate'][0]
    df['current_date'] = pd.to_datetime(current_date)

    df['year_start'] = pd.to_datetime(df['current_date'])
    df['year_start'] = df['year_start'].dt.year.astype(str) + '-01-01'
    df['year_ago_date'] = df['current_date'] - pd.DateOffset(years=1)
    
    return df



