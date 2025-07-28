from typing import List
import pandas as pd

def filter_to_business_deposits(df: pd.DataFrame, minors: List) -> pd.DataFrame:
    """
    Filter the total deposit account dataset to specific business minors
    """
    df = df[df['currmiaccttypcd'].isin(minors)].copy()
    return df