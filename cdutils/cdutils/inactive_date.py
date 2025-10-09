# Append inactive date
import cdutils.deduplication # type: ignore
import cdutils.database.connect # type: ignore
import cdutils.input_cleansing # type: ignore
from sqlalchemy import text # type: ignore
import pandas as pd

def fetch_data():
    """
    Gets data from COCC
    """
    acctloanlimithist = text("""
    SELECT 
        *
    FROM 
        OSIBANK.ACCTLOANLIMITHIST
    """)

    queries = [
        {'key':'acctloanlimithist', 'sql':acctloanlimithist, 'engine':1},
    ]

    data = cdutils.database.connect.retrieve_data(queries)
    return data

def append_inactive_date(df: pd.DataFrame) -> pd.DataFrame:
    """
    Getting inactive date for each item and appending to dataframe
    
    Args: 
        df: Takes in any dataframe 

    Returns:
        df: df with the most recent inactive date per product
        
    Operations:
        - ensure inactivedate is a datetime field
        - groupby acctnbr, take max inactive date
    """
    data = fetch_data()
    acctloanlimithist = data['acctloanlimithist'].copy()


    acctloanlimithist['inactivedate'] = pd.to_datetime(acctloanlimithist['inactivedate'])
    inactive_df = acctloanlimithist.groupby('acctnbr')['inactivedate'].max().reset_index()
    inactive_df = pd.DataFrame(inactive_df)

    assert inactive_df['acctnbr'].is_unique, "There are duplicate acctnbrs"

    inactive_df_schema = {
        'acctnbr': str
    }

    inactive_df = cdutils.input_cleansing.enforce_schema(inactive_df, inactive_df_schema)

    df = pd.merge(df, inactive_df, how='left', on='acctnbr')

    return df

