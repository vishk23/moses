import pandas as pd
def enforce_schema(df: pd.DataFrame, schema: dict) -> pd.DataFrame:
    """
    Enforce a given schema on the columns of a DataFrame.
    
    The schema is a dictionary mapping column names to the desired data type.
    This function addresses several edge cases:
    
      1. Missing Columns:
         - If a column specified in the schema is missing, it is created with default None values.
         
      2. Float to String without Decimals:
         - For columns expected to be strings but currently floats, the function formats the
           numbers without decimals (e.g., 10.0 -> "10") and preserves missing values.
           
      3. Whitespace in String Columns:
         - When converting to string, the function strips any extra whitespace.
         
      4. Numeric Conversion for int/float:
         - Uses `pd.to_numeric` with error coercion for columns needing numeric conversion.
         - For integer conversion, it casts the result to Pandas’ nullable integer type ('Int64')
           which supports missing values.
           
      5. Datetime Conversion:
         - For columns expected to be datetime (using 'datetime' or pd.Timestamp as the desired type),
           it uses `pd.to_datetime` with errors coerced into NaT.
           
      6. Fallback Conversion:
         - For any other desired type, it uses a simple astype conversion.
    
    :param df: The input DataFrame.
    :param schema: A dictionary where keys are column names and values are the desired types.
                   Supported type indicators include: str, int, float, 'datetime' (or pd.Timestamp).
    :return: A new DataFrame with the enforced schema.

    Usage:
        schema_wh_org = {
            'orgnbr': str,
            'orgname': str
        }

        wh_org = cdutils.input_cleansing.enforce_schema(wh_org, schema_wh_org)
    """
    df = df.copy()
    
    for column, desired_dtype in schema.items():
        # Handle missing columns by creating them with default None values.
        if column not in df.columns:
            print(f"Column '{column}' not found. Creating it with default None values.")
            df[column] = None
        try:
            # When the desired type is str
            if desired_dtype == str:
                if pd.api.types.is_float_dtype(df[column]):
                    # Format floats as strings with no decimals.
                    df[column] = df[column].apply(lambda x: f"{x:.0f}" if pd.notnull(x) else None)
                else:
                    # Ensure all values are strings and strip whitespace.
                    df[column] = df[column].astype(str).str.strip()
            # Convert to integer: use pd.to_numeric and then cast to Pandas' nullable integer type.
            elif desired_dtype == int:
                df[column] = pd.to_numeric(df[column], errors='coerce').astype("Int64")
                
            # Convert to float: use pd.to_numeric.
            elif desired_dtype == float:
                df[column] = pd.to_numeric(df[column], errors='coerce')
                
            # Convert to datetime: allow desired dtype to be 'datetime' or pd.Timestamp.
            elif desired_dtype in ['datetime', pd.Timestamp]:
                df[column] = pd.to_datetime(df[column], errors='coerce')
                
            # Fallback: attempt a simple astype conversion for other types.
            else:
                df[column] = df[column].astype(desired_dtype)
                
        except Exception as e:
            print(f"[ERROR] Conversion failed for column '{column}' to {desired_dtype}: {e}")
    
    return df