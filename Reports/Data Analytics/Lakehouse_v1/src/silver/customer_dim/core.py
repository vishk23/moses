import src.silver.customer_dim.fetch_data
import cdutils.deduplication # type: ignore
import cdutils.input_cleansing # type: ignore
import pandas as pd

def sort_dedupe_raw(df, dedupe_list):
    if 'adddate' in df.columns:
        df_sorted = df.sort_values(by='adddate', ascending=False)
    else:
        pass

    result = cdutils.deduplication.dedupe(dedupe_list)
    return result


def generate_customer_dim_table():
    """
    Create Customer Dim table with P+persnbr or O+orgnbr as primary key
    """
    data = src.silver.customer_dim.fetch_data.fetch_data()
    wh_pers = data['wh_pers'].copy()
    wh_org =data['wh_org'].copy()

    # Cast datatypes for consistent downstream joins
    wh_pers_schema = {
        'persnbr': 'str'
    }
    wh_pers = cdutils.input_cleansing.cast_columns(wh_pers, wh_pers_schema)
    wh_org_schema = {
        'orgnbr': 'str'
    }
    wh_org = cdutils.input_cleansing.cast_columns(wh_org, wh_org_schema)

    # Sort descending and dedupe primary keys 
    dedupe_list = [
            {'df':wh_org, 'field':'orgnbr'}
        ]
    wh_org = sort_dedupe_raw(wh_org, dedupe_list)
    # Org-ify function
    
    # Pers-ify function

    # Concat fields into single customer dim 
