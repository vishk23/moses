
def coalesce_columns(df, suffix1, suffix2):
    """
    Identifies columns with suffixes, creates a new coalesced column,
    and drops the old ones. It prioritizes the column with suffix2.
    """
    df_copy = df.copy()
    # Find all columns that have the first suffix
    cols1 = [c for c in df_copy.columns if c.endswith(suffix1)]
    
    for col1 in cols1:
        # Get the base column name and the corresponding column with the second suffix
        base_name = col1.removesuffix(suffix1)
        col2 = f"{base_name}{suffix2}"
        
        if col2 in df_copy.columns:
            # Create the new coalesced column.
            # It takes the value from col2 first, and if that is null, it takes the value from col1.
            df_copy[base_name] = df_copy[col2].fillna(df_copy[col1])
            
            # Drop the old suffixed columns
            df_copy = df_copy.drop(columns=[col1, col2])
            print(f"Coalesced '{base_name}' from '{col1}' and '{col2}'.")
            
    return df_copy