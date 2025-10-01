import pytest
import pandas as pd
import cdutils.input_cleansing # type: ignore
from datetime import datetime

def test_input_cleansing():
    """
    Testing that the validation and data type casting worked.

    We'll use 
    """
    wh_org = pd.DataFrame({
        'orgnbr': [100, 100, 101],
        'orgname': ['Org A', 'Org A', 'Org C']
    })    

    schema_wh_org = {
        'orgnbr': 'str',
        'orgname': 'str'
    }

    wh_org = cdutils.input_cleansing.cast_columns(wh_org, schema_wh_org)

    assert wh_org['orgnbr'].dtype == 'string'

def test_dedupe_raw_tables():
    """
    Testing deduplication logic on raw tables from db
    """
    wh_org = pd.DataFrame({
        'orgnbr':["100", "100", "101", "102"],
        'adddate':[datetime(2025,1,1), datetime(2024,1,1), datetime(2025,1,1), datetime(2025,1,1)]
    })
    
    # TODO more here.
