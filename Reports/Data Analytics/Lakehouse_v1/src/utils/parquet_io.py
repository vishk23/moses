import pandas as pd

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
