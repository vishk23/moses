import pandas as pd
from sqlalchemy import text

import cdutils.database.connect # type: ignore

# Function to add interest rate
def add_noteintrate(df):
    """
    Add interest rate
    """
    def retrieve_data():
        """
        Execute a SQL query against the COCC database. You can define whatever tables you want as separate dataframes

        Args:
            n/a

        Returns:
            data (dict): Dictionary (Key/Value pair) with all of the table names you set as keys and the values are the raw data tables from the SQL database
        """
        acctcommon = text("""
        SELECT 
            a.ACCTNBR,
            a.NOTEINTRATE
        FROM 
            OSIBANK.WH_ACCTCOMMON a
        """)

        queries = [
            {'key':'acctcommon', 'sql':acctcommon, 'engine':1},
        ]
        data = cdutils.database.connect.retrieve_data(queries)
        return data

    data = retrieve_data()
    acctcommon = data['acctcommon'].copy()
    acctcommon['acctnbr'] = acctcommon['acctnbr'].astype(str)
    acctcommon['noteintrate'] = pd.to_numeric(acctcommon['noteintrate'])
    
    # Asserts
    assert df is not None
    assert pd.api.types.is_string_dtype(df['acctnbr']), "acctnbr is not a string"
    
    df = pd.merge(df, acctcommon, on='acctnbr', how='left')

    return df
