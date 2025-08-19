"""
Core Transformations
"""
from typing import Dict
from pathlib import Path

import pandas as pd # type: ignore
import numpy as np # type: ignore
def acctcommon_cleaning(wh_acctcommon):
    """
    Filtering to only active, non-performing or dormant accounts
    """
    wh_acctcommon = wh_acctcommon[wh_acctcommon['curracctstatcd'].isin(['ACT','NPFM','DORM'])].copy()
    return wh_acctcommon



# %%
def merge_dfs(wh_acctcommon, househldacct):
    """
    Mergine acctcommon & household dataframes
    """
    househldacct = househldacct.sort_values(by='datelastmaint', ascending=False).drop_duplicates(subset='acctnbr', keep='first').copy()
    assert househldacct['acctnbr'].is_unique, "Duplicates found"
    merged_df = pd.merge(wh_acctcommon, househldacct, on='acctnbr', how='left')
    return merged_df



def main_pipeline(data: Dict) -> pd.DataFrame:
    """
    Main data pipeline 
    """

    wh_acctcommon = data['wh_acctcommon'].copy()
    househldacct = data['househldacct'].copy()
    
    wh_acctcommon = acctcommon_cleaning(wh_acctcommon)

    df = merge_dfs(wh_acctcommon, househldacct)

    df = df[['acctnbr','householdnbr','ownersortname','product','loanofficer','acctofficer','bookbalance','noteintrate','mjaccttypcd','contractdate','datemat']].copy()


    
    return df 


    


