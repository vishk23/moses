"""
Fetching data module. Aim is import all necessary fields up front, but if needed, you can define another function to be called here.

Usage:
    import src.cdutils.database
"""

from sqlalchemy import text # type: ignore
import pandas as pd # type: ignore

import cdutils.database.connect
import cdutils.input_cleansing # type: ignore


def append_primary_address(df: pd.DataFrame) -> pd.DataFrame:
    """
    Take in a df with persnbr and append the primary address
    """
    def fetch_data():
        # acctcommon
        # engine 1

        wh_addr = text("""
        SELECT
            *
        FROM
            OSIBANK.WH_ADDR
        """)

        persaddruse = text("""
        SELECT
            *
        FROM
            OSIBANK.PERSADDRUSE a
        WHERE
            a.ADDRUSECD = 'PRI'
        """)    

        queries = [
            {'key':'wh_addr', 'sql':wh_addr, 'engine':1},
            {'key':'persaddruse', 'sql':persaddruse, 'engine':1},
        ]

        data = cdutils.database.connect.retrieve_data(queries)
        return data
    
    data = fetch_data()

    wh_addr = data['wh_addr'].copy()
    persaddruse = data['persaddruse'].copy()

    assert persaddruse['persnbr'].is_unique, "Fail"

    schema_persaddruse = {
        'addrnbr':'str',
        'persnbr':'str'
    }

    schema_wh_addr = {
        'addrnbr':'str'
    }

    persaddruse = cdutils.input_cleansing.enforce_schema(persaddruse, schema_persaddruse)
    wh_addr = cdutils.input_cleansing.enforce_schema(wh_addr, schema_wh_addr)

    wh_addr = wh_addr[['addrnbr','text1','cityname','statecd','zipcd']].copy()

    merged_address = pd.merge(persaddruse, wh_addr, how='left', on='addrnbr')

    merged_address = merged_address[['persnbr','text1','cityname','statecd','zipcd']].copy()

    schema_df = {
        'persnbr':'str'
    }

    df = cdutils.input_cleansing.enforce_schema(df, schema_df)

    df = pd.merge(df, merged_address, how='left', on='persnbr')

    return df 