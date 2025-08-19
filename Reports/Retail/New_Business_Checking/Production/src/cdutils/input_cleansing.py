"""
Easy way to clean data types from different sources

Usage:
    import src.cdutils.input_cleansing.enforce_schema

You need to define the schema as a dict:
schema = {
    'column': dtype,
}

"""
from typing import Dict

import pandas as pd # type: ignore

def enforce_schema(df: pd.DataFrame, schema: Dict) -> pd.DataFrame:
    df = df.copy()
    for column, dtype in schema.items():
        if column in df.columns:
            try:
                df[column] = df[column].astype(dtype)
            except Exception as e:
                print(f"[ERROR] Failed to convert '{column}' to {dtype}: e")
    return df
