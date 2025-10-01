import pandas as pd
from deltalake import DeltaTable
from pathlib import Path
import cdutils.input_cleansing # type: ignore

## Should be located elsewhere, todo. Works for now on local.
BASE_PATH = Path(r"C:\Users\w322800\Documents\lakehouse") 
# Bronze
BRONZE = BASE_PATH / "bronze"
# Silver
SILVER = BASE_PATH / "silver"
# Gold
GOLD = BASE_PATH / "gold"

def append_pm():
    """
    Extract PM role from WH_ALLROLES to attach to dataframes. PERSNAME will come from WH_PERS
    """
    allroles = DeltaTable(BRONZE / "wh_allroles").to_pandas()
    pm = allroles[allroles['acctrolecd'] == 'PTMR'].copy()
    assert pm['acctnbr'].is_unique, "There exist duplicate PMs assigned to a single acctnbr in wh_allroles"

    pm = pm[[
        'acctnbr',
        'persnbr'
    ]].copy()

    # Cast types
    pm_schema = {
        'acctnbr':'str',
        'persnbr':'str'
    }

    pm = cdutils.input_cleansing.cast_columns(pm, pm_schema) 


    pers = DeltaTable(BRONZE / "wh_pers").to_pandas()
    # Could add in manual deduplication logic here, but historically we've never had a duplicate in this table

    assert pers['persnbr'].is_unique, "Duplicates on wh_pers table"

    pers = pers[[
        'persnbr',
        'persname'
    ]].copy()

    # Cast types
    pers_schema = {
        'persnbr':'str'
    }

    pers = cdutils.input_cleansing.cast_columns(pers, pers_schema) 

    # Merge
    pm = pm.merge(pers, on='persnbr', how='left')
    pm = pm[[
        'acctnbr',
        'persname'
    ]].copy()

    return pm

    