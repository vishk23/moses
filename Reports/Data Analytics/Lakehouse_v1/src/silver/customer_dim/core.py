import src.silver.customer_dim.fetch_data
import cdutils.deduplication # type: ignore
import cdutils.customer_dim # type: ignore
import cdutils.input_cleansing # type: ignore
import pandas as pd
import src.config
from deltalake import DeltaTable

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
    # data = src.silver.customer_dim.fetch_data.fetch_data()
    # wh_pers = data['wh_pers'].copy()
    # wh_org =data['wh_org'].copy()

    wh_pers = DeltaTable(src.config.BRONZE / "wh_pers").to_pandas()
    wh_org = DeltaTable(src.config.BRONZE / "wh_org").to_pandas()

    # Sort descending and dedupe primary keys 
    dedupe_list = [
            {'df':wh_org, 'field':'orgnbr'}
        ]
    wh_org = sort_dedupe_raw(wh_org, dedupe_list)

    dedupe_list = [
            {'df':wh_pers, 'field':'persnbr'}
        ]
    wh_pers = sort_dedupe_raw(wh_pers, dedupe_list)

    # Org + Persify
    wh_org = cdutils.customer_dim.orgify(wh_org, 'orgnbr')
    wh_pers = cdutils.customer_dim.persify(wh_pers, 'persnbr')

    # Concat fields
    customer_dim = pd.concat([wh_org, wh_pers], ignore_index=True)
    
    # Coalesce customer name + filter down
    customer_dim['customer_name'] = customer_dim['orgname'].fillna(customer_dim['persname'])
    customer_dim = customer_dim[[
        'customer_id',
        'customer_name',
        'adddate'
    ]].copy()

    # Add taxid

    # Join with account data to get counts and balances

    return customer_dim