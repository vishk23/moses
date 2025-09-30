import pytest
import pandas as pd
import src.silver.customer_dim.core

def test_datatype_cleansing():
    """
    Testing that the validation and data type casting worked.

    We'll use 
    """
    wh_org = pd.DataFrame({
        'orgnbr': [100, 100, 101],
        'orgname': ['Org A', 'Org A', 'Org C']
    })    
    
    key_field = 'orgnbr'
    df = src.silver.customer_dim.core.datatype_cleansing(wh_org, key_field)
    assert df[key_field].dtype == 'str'

# def test_dedupe_raw_tables():
#     """
#     Testing deduplication logic on raw tables from db
#     """"
#     wh_org = {
#         'orgnbr':[100, 100, 101, 102]
#     }
#     key_field = 'orgnbr'
#     df = src.silver.customer_dim.dedupe_raw_tables(wh_org)
#     assert df['orgnbr']
