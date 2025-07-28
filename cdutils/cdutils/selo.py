
import cdutils.deduplication # type: ignore
import cdutils.database.connect # type: ignore
import cdutils.input_cleansing # type: ignore
from sqlalchemy import text # type: ignore
import pandas as pd

def fetch_from_allroles():
        """
        Gets data from COCC
        """
        wh_allroles = text(f"""
        SELECT
            *
        FROM 
            OSIBANK.WH_ALLROLES a
        """)

        wh_pers = text(f"""
        SELECT
            *
        FROM
            OSIBANK.WH_PERS a
        """)

        queries = [
            {'key':'wh_allroles', 'sql':wh_allroles, 'engine':1},
            {'key':'wh_pers', 'sql':wh_pers, 'engine':1},
        ]

        data = cdutils.database.connect.retrieve_data(queries)
        return data


def append_selo(df: pd.DataFrame):
    """
    Attach secondary lending officer to any dataframe
    """
    
    data = fetch_from_allroles()

    wh_allroles = data['wh_allroles'].copy()
    wh_pers = data['wh_pers'].copy()

    selo = wh_allroles[wh_allroles['acctrolecd'] == 'SELO'].copy()

    selo = selo.sort_values(by='datelastmaint', ascending=False).copy()
    selo = cdutils.deduplication.dedupe([{'df':selo, 'field':'acctnbr'}])


    pers = wh_pers.sort_values(by='datelastmaint', ascending=False).copy()
    pers = cdutils.deduplication.dedupe([{'df':pers, 'field':'persnbr'}])

    # Asserts
    assert selo['acctnbr'].is_unique, "selo not unique on acctnbr"
    assert pers['persnbr'].is_unique, "pers not unique on persnbr"


    selo = selo[['acctnbr','persnbr']].copy()
    pers = pers[['persnbr','perssortname']].copy()


    merged_df = pd.merge(selo, pers, on='persnbr',how='left')

    merged_df = merged_df[['acctnbr','perssortname']].copy()
    merged_df = merged_df.rename(columns={'perssortname':'Secondary Lending Officer'}).copy()

    schema_df = {
                'acctnbr': str,
            }

    df = cdutils.input_cleansing.enforce_schema(df, schema_df)

    schema_merged_df = {
                'acctnbr': str,
            }

    merged_df = cdutils.input_cleansing.enforce_schema(merged_df, schema_merged_df)
    
    assert df['acctnbr'].is_unique, "acctnbr not unique in df"

    final_df = pd.merge(df, merged_df, on='acctnbr', how='left')

    return final_df



