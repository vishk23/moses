import pandas as pd
from typing import Optional

def cast_all_null_columns_to_string(df: pd.DataFrame) -> pd.DataFrame:
    """
    Helper function, since parquet cannot store columns with null type
    """
    is_all_null = df.isnull().all()

    all_null_cols = is_all_null[is_all_null].index.tolist()

    if not all_null_cols:
        print("No all-null columns found. Returning original dataframe")
        return df

    dtype_mapping = {col: 'string' for col in all_null_cols}

    df = df.astype(dtype_mapping)
    final_df = df.copy()

    return final_df


def add_load_timestamp(
    df: pd.DataFrame, 
    col_name: str = "load_timestamp_utc"
) -> pd.DataFrame:
    """
    Adds a column with the current UTC timestamp to a DataFrame.

    This function is idempotent and safe to run on any DataFrame. If the
    specified column name already exists, it will be overwritten with the
    new timestamp. It does not affect any other columns.

    Args:
        df: The pandas DataFrame to modify.
        col_name: The name for the new timestamp column. 
                  Defaults to 'load_timestamp_utc'.

    Returns:
        A new DataFrame with the added timestamp column.
    """
    df_copy = df.copy()
    df_copy[col_name] = pd.Timestamp.now(tz='UTC')
    return df_copy