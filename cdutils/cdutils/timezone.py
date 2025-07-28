import pandas as pd

def make_datetimes_naive(df):
    """
    Make datetimes naive (not tied to specific timezone).

    Sometimes this is necessary before writing to Excel
    """

    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            if df[col].dt.tz is not None:
                df[col] = df[col].dt.tz_localize(None)

    return df

def normalize_timezones(df, target_tz='America/New_York'):
    """
    Set naive timezones to a specific timzezone
    """
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            if df[col].dt.tz is not None:
                df[col] = df[col].dt.tz_convert(target_tz)
            else:
                df[col] = df[col].dt.tz_localize(target_tz)

    return df

# Convert datetime to string (the above ones were being weird when writing to excel)
def convert_datetime_to_str(df):
    """
    Convert datetime fields to str
    """
    df_copy = df.copy()
    for col in df_copy.columns:
        if pd.api.types.is_datetime64_any_dtype(df_copy[col]):
            df_copy[col] = df_copy[col].dt.strftime("%m/%d/%Y")
    return df_copy