"""
Core Transformations
"""
from typing import Dict
from pathlib import Path

import pandas as pd # type: ignore
import numpy as np # type: ignore


def main_pipeline(data: Dict) -> pd.DataFrame:
    """
    Main data pipeline 
    """

    # # Unpack data into dataframes
    wh_acctcommon = data['wh_acctcommon'].copy()

    df = wh_acctcommon.copy()

    # Set column types
    numeric_cols = ['noteintrate','bookbalance','notebal']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col])
    
    return df 


    


