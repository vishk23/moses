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

    # Identify rows with valid (non-null) orgnbr before casting
    has_org = df[orgnbr_field].notna()

    df_schema = {
        orgnbr_field: 'str'
    }
    df = cdutils.input_cleansing.cast_columns(df, df_schema)

    # Initialize customer_id if it doesn't exist
    if 'customer_id' not in df.columns:
        df['customer_id'] = pd.NA

    # Update only where customer_id is missing and orgnbr was valid
    update_mask = df['customer_id'].isna() & has_org
    df.loc[update_mask, 'customer_id'] = "O" + df.loc[update_mask, orgnbr_field]

    df = df.drop(orgnbr_field, axis=1).copy()
    return df
    

def persify(df, persnbr_field):
    """
    Take in a df, enforce persnbr field cleansing and type checking, and add "P" prefix
    """
    if persnbr_field not in df.columns:
        raise ValueError(f"Column '{persnbr_field}' does not exist in the DataFrame")

    # Identify rows with valid (non-null) persnbr before casting
    has_pers = df[persnbr_field].notna()

    df_schema = {
        persnbr_field: 'str'
    }
    df = cdutils.input_cleansing.cast_columns(df, df_schema)

    # Initialize customer_id if it doesn't exist
    if 'customer_id' not in df.columns:
        df['customer_id'] = pd.NA

    # Update only where customer_id is missing and persnbr was valid
    update_mask = df['customer_id'].isna() & has_pers
    df.loc[update_mask, 'customer_id'] = "P" + df.loc[update_mask, persnbr_field]

    df = df.drop(persnbr_field, axis=1).copy()
    return df
