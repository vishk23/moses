import pandas as pd
from sqlalchemy import text # type: ignore
import cdutils.database.connect # type: ignore
import cdutils.input_cleansing # type: ignore

def append_tax_id_to_pers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Append table with SSN. 
    """
    def fetch_data():
        # acctcommon
        viewperstaxid = text("""
        SELECT 
            *
        FROM 
            OSIBANK.VIEWPERSTAXID
        """)

        queries = [
            {'key':'viewperstaxid', 'sql':viewperstaxid, 'engine':1},
        ]

        data = cdutils.database.connect.retrieve_data(queries)
        return data

    data = fetch_data()
    viewperstaxid = data['viewperstaxid'].copy()

    schema_viewperstaxid = {
        'persnbr':'str'
    }

    schema_df = {
        'persnbr':'str'
    }

    viewperstaxid = cdutils.input_cleansing.enforce_schema(viewperstaxid, schema_viewperstaxid)
    df = cdutils.input_cleansing.enforce_schema(df, schema_df)

    assert df['persnbr'].is_unique, "Duplicates exist"
    assert viewperstaxid['persnbr'].is_unique, "Duplicates exist"

    df = pd.merge(df, viewperstaxid, on='persnbr', how='left')

    return df