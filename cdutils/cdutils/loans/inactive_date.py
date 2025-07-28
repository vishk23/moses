import cdutils.database.connect # type: ignore
import cdutils.input_cleansing
from sqlalchemy import text # type: ignore
import pandas as pd

def fetch_data():
    """
    Main data query
    """
    acctloanlimithist = text("""
    SELECT
        a.ACCTNBR,
        a.INACTIVEDATE
    FROM
        OSIBANK.ACCTLOANLIMITHIST a
    """)

    queries = [
        {'key':'acctloanlimithist', 'sql':acctloanlimithist, 'engine':1},
    ]

    data = cdutils.database.connect.retrieve_data(queries)
    return data

#################################
def append_inactive_date(loan_data):
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
    data = fetch_data()
    acctloanlimithist = data['acctloanlimithist'].copy()
    acctloanlimithist['inactivedate'] = pd.to_datetime(acctloanlimithist['inactivedate'])
    inactive_date_df = acctloanlimithist.groupby('acctnbr')['inactivedate'].max().reset_index()

    # Enforce schema
    inactive_date_df_schema = {
        'acctnbr': str
    }
    inactive_date_df = cdutils.input_cleansing.enforce_schema(inactive_date_df, inactive_date_df_schema)

    loan_data_schema = {
        'acctnbr': str
    }
    loan_data = cdutils.input_cleansing.enforce_schema(loan_data, loan_data_schema)

    assert inactive_date_df['acctnbr'].is_unique, "There are duplicate acctnbrs"
    assert loan_data['acctnbr'].is_unique, "There are duplicate acctnbrs"
    df = pd.merge(loan_data, inactive_date_df, on='acctnbr', how='left')
    return df



