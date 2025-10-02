import cdutils.input_cleansing # type: ignore
import pandas as pd

def orgify(df, orgnbr_field):
    """
    Take in a df, enforce orgnbr cleansing and add "O" prefix

    For example:
    12345 becomes O12345
    """
    if orgnbr_field not in df.columns:
        raise ValueError(f"Column '{orgnbr_field}' does not exist in the DataFrame")

    df_schema = {
        orgnbr_field: 'str'
    }
    df = cdutils.input_cleansing.cast_columns(df, df_schema)

    df['customer_id'] = "O" + df[orgnbr_field]
    df = df.drop(orgnbr_field, axis=1).copy()
    return df
    

def persify(df, persnbr_field):
    """
    Take in a df, enforce persnbr field cleansing and type checking, and add "P" prefix
    """
    if persnbr_field not in df.columns:
        raise ValueError(f"Column '{persnbr_field}' does not exist in the DataFrame")

    df_schema = {
        persnbr_field: 'str'
    }
    df = cdutils.input_cleansing.cast_columns(df, df_schema)
    df['customer_id'] = "P" + df[persnbr_field]
    df = df.drop(persnbr_field, axis=1).copy()
    return df
