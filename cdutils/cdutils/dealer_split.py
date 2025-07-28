
import cdutils.deduplication # type: ignore
import cdutils.database.connect # type: ignore
import cdutils.input_cleansing # type: ignore
from sqlalchemy import text # type: ignore
import pandas as pd

def fetch_from_acctuserfield():
        """
        Gets data from COCC
        """
        wh_acctuserfields = text(f"""
        SELECT
            *
        FROM 
            OSIBANK.WH_ACCTUSERFIELDS a
        """)

        queries = [
            {'key':'wh_acctuserfields', 'sql':wh_acctuserfields, 'engine':1},
        ]

        data = cdutils.database.connect.retrieve_data(queries)
        return data


def append_dealersplit(df: pd.DataFrame):
    """
    Attach secondary lending officer to any dataframe
    """
    
    data = fetch_from_acctuserfield()

    wh_acctuserfields = data['wh_acctuserfields'].copy()

    splt = wh_acctuserfields[wh_acctuserfields['acctuserfieldcd'] == 'SPLT'].copy()

    splt = splt.sort_values(by='datelastmaint', ascending=False).copy()
    splt = cdutils.deduplication.dedupe([{'df':splt, 'field':'acctnbr'}])


    # Asserts
    assert splt['acctnbr'].is_unique, "splt not unique on acctnbr"


    splt = splt[['acctnbr','acctuserfieldvalue']].copy()

    splt = splt.rename(columns={'acctuserfieldvalue':'SPLT'}).copy()
    splt['SPLT'] = pd.to_numeric(splt['SPLT'], errors="coerce").fillna(0.0)

    schema_df = {
                'acctnbr': str,
            }

    df = cdutils.input_cleansing.enforce_schema(df, schema_df)

    schema_splt = {
                'acctnbr': str,
                'SPLT': float
            }

    splt = cdutils.input_cleansing.enforce_schema(splt, schema_splt)
    
    assert df['acctnbr'].is_unique, "acctnbr not unique in df"

    final_df = pd.merge(df, splt, on='acctnbr', how='left')
    final_df['SPLT'] = pd.to_numeric(final_df['SPLT'], errors="coerce").fillna(0.0)


    return final_df



