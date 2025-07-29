import pandas as pd
from pathlib import Path

def merge_org_with_view_taxid(wh_org, vieworgtaxid):
    """
    Merge WH_ORG with VIEWORGTAXID to update tax information.
    Performs a left join to replace taxid and taxidtypcd fields where matches exist.
    
    Args:
        wh_org: DataFrame with organization data
        vieworgtaxid: DataFrame with updated tax information (orgnbr, taxidtypcd, taxid)
        
    Returns:
        DataFrame: Updated wh_org with tax information replaced where matches exist
    """
    print("Merging WH_ORG with VIEWORGTAXID...")
    
    # Validate inputs
    assert wh_org is not None, "wh_org DataFrame must not be None"
    assert vieworgtaxid is not None, "vieworgtaxid DataFrame must not be None"
    assert 'orgnbr' in wh_org.columns, "wh_org must have 'orgnbr' column"
    assert 'orgnbr' in vieworgtaxid.columns, "vieworgtaxid must have 'orgnbr' column"
    
    # Check for duplicates in vieworgtaxid
    duplicates = vieworgtaxid.duplicated(subset=['orgnbr'], keep=False)
    if duplicates.any():
        duplicate_orgnbrs = vieworgtaxid.loc[duplicates, 'orgnbr'].unique()
        raise ValueError(f"Duplicate orgnbr values found in vieworgtaxid: {duplicate_orgnbrs}")
    
    print(f"  WH_ORG records: {len(wh_org):,}")
    print(f"  VIEWORGTAXID records: {len(vieworgtaxid):,}")
    
    # Make a copy to avoid modifying the original
    wh_org_updated = wh_org.copy()
    
    # Identify overlapping columns (excluding the join key)
    overlap_cols = [col for col in vieworgtaxid.columns if col in wh_org.columns and col != 'orgnbr']
    print(f"  Overlapping columns to update: {overlap_cols}")
    
    if not overlap_cols:
        print("  No overlapping columns found, returning original wh_org")
        return wh_org_updated
    
    # Handle dtype mismatches for join key
    if wh_org_updated['orgnbr'].dtype != vieworgtaxid['orgnbr'].dtype:
        print(f"  Converting orgnbr dtypes for join: {wh_org_updated['orgnbr'].dtype} -> {vieworgtaxid['orgnbr'].dtype}")
        try:
            vieworgtaxid_copy = vieworgtaxid.copy()
            # Convert both to string for reliable joining
            wh_org_updated['orgnbr'] = wh_org_updated['orgnbr'].apply(lambda x: str(int(float(x))) if pd.notnull(x) else x)
            vieworgtaxid_copy['orgnbr'] = vieworgtaxid_copy['orgnbr'].apply(lambda x: str(int(float(x))) if pd.notnull(x) else x)
        except Exception as e:
            raise ValueError(f"Cannot convert orgnbr dtypes for join: {e}")
    else:
        vieworgtaxid_copy = vieworgtaxid.copy()
    
    # Perform left join to get matching records
    merged = wh_org_updated.merge(
        vieworgtaxid_copy[['orgnbr'] + overlap_cols], 
        on='orgnbr', 
        how='left', 
        suffixes=('', '_view')
    )
    
    # Update the overlapping columns where view data exists
    matches_found = 0
    for col in overlap_cols:
        view_col = f"{col}_view"
        # Update where view data is not null
        mask = merged[view_col].notna()
        merged.loc[mask, col] = merged.loc[mask, view_col]
        matches_found += mask.sum()
        # Drop the temporary view column
        merged = merged.drop(columns=[view_col])
    
    print(f"  Updated {matches_found:,} field values from view table")
    print(f"  Organizations with tax updates: {merged['orgnbr'].isin(vieworgtaxid_copy['orgnbr']).sum():,}")
    
    return merged

def merge_pers_with_view_taxid(wh_pers, viewperstaxid):
    """
    Merge WH_PERS with VIEWPERSTAXID to update tax information.
    Performs a left join to replace taxid field where matches exist.
    
    Args:
        wh_pers: DataFrame with person data
        viewperstaxid: DataFrame with updated tax information (persnbr, taxid)
        
    Returns:
        DataFrame: Updated wh_pers with tax information replaced where matches exist
    """
    print("Merging WH_PERS with VIEWPERSTAXID...")
    
    # Validate inputs
    assert wh_pers is not None, "wh_pers DataFrame must not be None"
    assert viewperstaxid is not None, "viewperstaxid DataFrame must not be None"
    assert 'persnbr' in wh_pers.columns, "wh_pers must have 'persnbr' column"
    assert 'persnbr' in viewperstaxid.columns, "viewperstaxid must have 'persnbr' column"
    
    # Check for duplicates in viewperstaxid
    duplicates = viewperstaxid.duplicated(subset=['persnbr'], keep=False)
    if duplicates.any():
        duplicate_persnbrs = viewperstaxid.loc[duplicates, 'persnbr'].unique()
        raise ValueError(f"Duplicate persnbr values found in viewperstaxid: {duplicate_persnbrs}")
    
    print(f"  WH_PERS records: {len(wh_pers):,}")
    print(f"  VIEWPERSTAXID records: {len(viewperstaxid):,}")
    
    # Make a copy to avoid modifying the original
    wh_pers_updated = wh_pers.copy()
    
    # Identify overlapping columns (excluding the join key)
    overlap_cols = [col for col in viewperstaxid.columns if col in wh_pers.columns and col != 'persnbr']
    print(f"  Overlapping columns to update: {overlap_cols}")
    
    if not overlap_cols:
        print("  No overlapping columns found, returning original wh_pers")
        return wh_pers_updated
    
    # Handle dtype mismatches for join key
    if wh_pers_updated['persnbr'].dtype != viewperstaxid['persnbr'].dtype:
        print(f"  Converting persnbr dtypes for join: {wh_pers_updated['persnbr'].dtype} -> {viewperstaxid['persnbr'].dtype}")
        try:
            viewperstaxid_copy = viewperstaxid.copy()
            # Convert both to string for reliable joining
            wh_pers_updated['persnbr'] = wh_pers_updated['persnbr'].apply(lambda x: str(int(float(x))) if pd.notnull(x) else x)
            viewperstaxid_copy['persnbr'] = viewperstaxid_copy['persnbr'].apply(lambda x: str(int(float(x))) if pd.notnull(x) else x)
        except Exception as e:
            raise ValueError(f"Cannot convert persnbr dtypes for join: {e}")
    else:
        viewperstaxid_copy = viewperstaxid.copy()
    
    # Perform left join to get matching records
    merged = wh_pers_updated.merge(
        viewperstaxid_copy[['persnbr'] + overlap_cols], 
        on='persnbr', 
        how='left', 
        suffixes=('', '_view')
    )
    
    # Update the overlapping columns where view data exists
    matches_found = 0
    for col in overlap_cols:
        view_col = f"{col}_view"
        # Update where view data is not null
        mask = merged[view_col].notna()
        merged.loc[mask, col] = merged.loc[mask, view_col]
        matches_found += mask.sum()
        # Drop the temporary view column
        merged = merged.drop(columns=[view_col])
    
    print(f"  Updated {matches_found:,} field values from view table")
    print(f"  Persons with tax updates: {merged['persnbr'].isin(viewperstaxid_copy['persnbr']).sum():,}")
    
    return merged

def create_org_table_with_address(wh_org, orgaddruse, wh_addr):
    """
    Merge WH_ORG with ORGADDRUSE and WH_ADDR to create an organization table with address info.
    Filters ORGADDRUSE to only 'PRI' address use codes and selects only essential fields.
    Performs pre-condition validation on input DataFrames and join keys.
    """
    # Basic asserts
    assert wh_org is not None, "wh_org DataFrame must not be None"
    assert orgaddruse is not None, "orgaddruse DataFrame must not be None"
    assert wh_addr is not None, "wh_addr DataFrame must not be None"
    
    # Validate join key datatypes
    assert 'orgnbr' in wh_org.columns, "wh_org must have 'orgnbr' column"
    assert 'orgnbr' in orgaddruse.columns, "orgaddruse must have 'orgnbr' column"
    assert 'addrnbr' in orgaddruse.columns, "orgaddruse must have 'addrnbr' column"
    assert 'addrnbr' in wh_addr.columns, "wh_addr must have 'addrnbr' column"
    
    # Handle orgnbr dtype mismatch with automatic conversion
    if wh_org['orgnbr'].dtype != orgaddruse['orgnbr'].dtype:
        print(f"Warning: orgnbr dtype mismatch - wh_org: {wh_org['orgnbr'].dtype}, orgaddruse: {orgaddruse['orgnbr'].dtype}")
        print("Converting both orgnbr columns to string for reliable joining...")
        try:
            orgaddruse = orgaddruse.copy()
            wh_org = wh_org.copy()
            
            # Convert both to string, handling floats by removing decimal points
            wh_org['orgnbr'] = wh_org['orgnbr'].apply(lambda x: str(int(float(x))) if pd.notnull(x) else x)
            orgaddruse['orgnbr'] = orgaddruse['orgnbr'].apply(lambda x: str(int(float(x))) if pd.notnull(x) else x)
                
            print(f"Successfully converted both orgnbr columns to string")
        except Exception as e:
            raise ValueError(f"Cannot convert orgnbr dtypes for join: wh_org has {wh_org['orgnbr'].dtype}, orgaddruse has {orgaddruse['orgnbr'].dtype}. Error: {e}")
    
    # Handle addrnbr dtype mismatch with automatic conversion  
    if orgaddruse['addrnbr'].dtype != wh_addr['addrnbr'].dtype:
        print(f"Warning: addrnbr dtype mismatch - orgaddruse: {orgaddruse['addrnbr'].dtype}, wh_addr: {wh_addr['addrnbr'].dtype}")
        print("Converting both addrnbr columns to string for reliable joining...")
        try:
            orgaddruse = orgaddruse.copy()
            wh_addr = wh_addr.copy()
            
            # Convert both to string, handling floats by removing decimal points
            orgaddruse['addrnbr'] = orgaddruse['addrnbr'].apply(lambda x: str(int(float(x))) if pd.notnull(x) else x)
            wh_addr['addrnbr'] = wh_addr['addrnbr'].apply(lambda x: str(int(float(x))) if pd.notnull(x) else x)
                
            print(f"Successfully converted both addrnbr columns to string")
        except Exception as e:
            raise ValueError(f"Cannot convert addrnbr dtypes for join: orgaddruse has {orgaddruse['addrnbr'].dtype}, wh_addr has {wh_addr['addrnbr'].dtype}. Error: {e}")
    
    # Filter ORGADDRUSE to only 'PRI' address use codes and select essential fields
    orgaddruse_filtered = orgaddruse[orgaddruse['addrusecd'] == 'PRI'][['orgnbr', 'addrnbr', 'addrusecd']].copy()
    
    # Select essential address fields from WH_ADDR
    addr_fields = ['addrnbr', 'text1', 'text2', 'text3', 'cityname', 'statecd', 'zipcd', 'zipsuf',
                   'addrlinetypdesc1', 'addrlinetypcd1', 'addrlinetypdesc2', 'addrlinetypcd2', 
                   'addrlinetypdesc3', 'addrlinetypcd3']
    # Only include fields that exist in the DataFrame
    available_addr_fields = [field for field in addr_fields if field in wh_addr.columns]
    wh_addr_filtered = wh_addr[available_addr_fields].copy()
    
    # Merge ORGADDRUSE with WH_ADDR
    orgaddruse_addr = pd.merge(orgaddruse_filtered, wh_addr_filtered, how='left', on='addrnbr')
    
    # Merge WH_ORG (all fields) with address info
    org_with_address = pd.merge(wh_org, orgaddruse_addr, how='left', on='orgnbr')
    
    return org_with_address

def create_pers_table_with_address(wh_pers, persaddruse, wh_addr):
    """
    Merge WH_PERS with PERSADDRUSE and WH_ADDR to create a person table with address info.
    Filters PERSADDRUSE to only 'PRI' address use codes and selects only essential fields.
    Performs pre-condition validation on input DataFrames and join keys.
    """
    # Basic asserts
    assert wh_pers is not None, "wh_pers DataFrame must not be None"
    assert persaddruse is not None, "persaddruse DataFrame must not be None"
    assert wh_addr is not None, "wh_addr DataFrame must not be None"
    
    # Validate join key datatypes
    assert 'persnbr' in wh_pers.columns, "wh_pers must have 'persnbr' column"
    assert 'persnbr' in persaddruse.columns, "persaddruse must have 'persnbr' column"
    assert 'addrnbr' in persaddruse.columns, "persaddruse must have 'addrnbr' column"
    assert 'addrnbr' in wh_addr.columns, "wh_addr must have 'addrnbr' column"
    
    # Handle persnbr dtype mismatch with automatic conversion
    if wh_pers['persnbr'].dtype != persaddruse['persnbr'].dtype:
        print(f"Warning: persnbr dtype mismatch - wh_pers: {wh_pers['persnbr'].dtype}, persaddruse: {persaddruse['persnbr'].dtype}")
        print("Converting both persnbr columns to string for reliable joining...")
        try:
            persaddruse = persaddruse.copy()
            wh_pers = wh_pers.copy()
            
            # Convert both to string, handling floats by removing decimal points
            wh_pers['persnbr'] = wh_pers['persnbr'].apply(lambda x: str(int(float(x))) if pd.notnull(x) else x)
            persaddruse['persnbr'] = persaddruse['persnbr'].apply(lambda x: str(int(float(x))) if pd.notnull(x) else x)
                
            print(f"Successfully converted both persnbr columns to string")
        except Exception as e:
            raise ValueError(f"Cannot convert persnbr dtypes for join: wh_pers has {wh_pers['persnbr'].dtype}, persaddruse has {persaddruse['persnbr'].dtype}. Error: {e}")
    
    # Handle addrnbr dtype mismatch with automatic conversion  
    if persaddruse['addrnbr'].dtype != wh_addr['addrnbr'].dtype:
        print(f"Warning: addrnbr dtype mismatch - persaddruse: {persaddruse['addrnbr'].dtype}, wh_addr: {wh_addr['addrnbr'].dtype}")
        print("Converting both addrnbr columns to string for reliable joining...")
        try:
            persaddruse = persaddruse.copy()
            wh_addr = wh_addr.copy()
            
            # Convert both to string, handling floats by removing decimal points
            persaddruse['addrnbr'] = persaddruse['addrnbr'].apply(lambda x: str(int(float(x))) if pd.notnull(x) else x)
            wh_addr['addrnbr'] = wh_addr['addrnbr'].apply(lambda x: str(int(float(x))) if pd.notnull(x) else x)
                
            print(f"Successfully converted both addrnbr columns to string")
        except Exception as e:
            raise ValueError(f"Cannot convert addrnbr dtypes for join: persaddruse has {persaddruse['addrnbr'].dtype}, wh_addr has {wh_addr['addrnbr'].dtype}. Error: {e}")
    
    # Filter PERSADDRUSE to only 'PRI' address use codes and select essential fields
    persaddruse_filtered = persaddruse[persaddruse['addrusecd'] == 'PRI'][['persnbr', 'addrnbr', 'addrusecd']].copy()
    
    # Select essential address fields from WH_ADDR
    addr_fields = ['addrnbr', 'text1', 'text2', 'text3', 'cityname', 'statecd', 'zipcd', 'zipsuf',
                   'addrlinetypdesc1', 'addrlinetypcd1', 'addrlinetypdesc2', 'addrlinetypcd2', 
                   'addrlinetypdesc3', 'addrlinetypcd3']
    # Only include fields that exist in the DataFrame
    available_addr_fields = [field for field in addr_fields if field in wh_addr.columns]
    wh_addr_filtered = wh_addr[available_addr_fields].copy()
    
    # Merge PERSADDRUSE with WH_ADDR
    persaddruse_addr = pd.merge(persaddruse_filtered, wh_addr_filtered, how='left', on='addrnbr')
    
    # Merge WH_PERS (all fields) with address info
    pers_with_address = pd.merge(wh_pers, persaddruse_addr, how='left', on='persnbr')
    
    return pers_with_address

def filter_to_active_accounts(acct_df, wh_allroles, pers_with_address=None, org_with_address=None):
    """
    Filter person or organization data to only include records linked to active accounts.
    Takes either pers_with_address OR org_with_address as input.
    
    Args:
        acct_df: DataFrame with active account numbers
        wh_allroles: DataFrame linking accounts to persons/organizations
        pers_with_address: Optional DataFrame of persons with addresses
        org_with_address: Optional DataFrame of organizations with addresses
        
    Returns:
        Filtered DataFrame containing only records linked to active accounts
    """
    # Basic asserts
    assert acct_df is not None, "acct_df DataFrame must not be None"
    assert wh_allroles is not None, "wh_allroles DataFrame must not be None"
    
    # Validate that exactly one of pers_with_address or org_with_address is provided
    if pers_with_address is not None and org_with_address is not None:
        raise ValueError("Provide either pers_with_address OR org_with_address, not both")
    if pers_with_address is None and org_with_address is None:
        raise ValueError("Must provide either pers_with_address or org_with_address")
    
    # Validate required columns
    assert 'acctnbr' in acct_df.columns, "acct_df must have 'acctnbr' column"
    assert 'acctnbr' in wh_allroles.columns, "wh_allroles must have 'acctnbr' column"
    
    # Determine which table we're working with and set up join logic
    if pers_with_address is not None:
        target_df = pers_with_address
        join_key = 'persnbr'
        assert 'persnbr' in wh_allroles.columns, "wh_allroles must have 'persnbr' column"
        assert 'persnbr' in target_df.columns, "pers_with_address must have 'persnbr' column"
        
        # Handle persnbr dtype mismatch with automatic conversion
        if target_df['persnbr'].dtype != wh_allroles['persnbr'].dtype:
            print(f"Warning: persnbr dtype mismatch - pers_with_address: {target_df['persnbr'].dtype}, wh_allroles: {wh_allroles['persnbr'].dtype}")
            print("Converting both persnbr columns to string for reliable joining...")
            try:
                wh_allroles = wh_allroles.copy()
                target_df = target_df.copy()
                
                # Convert both to string, handling floats by removing decimal points
                target_df['persnbr'] = target_df['persnbr'].apply(lambda x: str(int(float(x))) if pd.notnull(x) else x)
                wh_allroles['persnbr'] = wh_allroles['persnbr'].apply(lambda x: str(int(float(x))) if pd.notnull(x) else x)
                    
                print(f"Successfully converted both persnbr columns to string")
            except Exception as e:
                raise ValueError(f"Cannot convert persnbr dtypes for join: pers_with_address has {target_df['persnbr'].dtype}, wh_allroles has {wh_allroles['persnbr'].dtype}. Error: {e}")
    else:
        # org_with_address is not None (validated above)
        target_df = org_with_address
        assert target_df is not None, "org_with_address must not be None"
        join_key = 'orgnbr'
        assert 'orgnbr' in wh_allroles.columns, "wh_allroles must have 'orgnbr' column"
        assert 'orgnbr' in target_df.columns, "org_with_address must have 'orgnbr' column"
        
        # Handle orgnbr dtype mismatch with automatic conversion
        if target_df['orgnbr'].dtype != wh_allroles['orgnbr'].dtype:
            print(f"Warning: orgnbr dtype mismatch - org_with_address: {target_df['orgnbr'].dtype}, wh_allroles: {wh_allroles['orgnbr'].dtype}")
            print("Converting both orgnbr columns to string for reliable joining...")
            try:
                wh_allroles = wh_allroles.copy()
                target_df = target_df.copy()
                
                # Convert both to string, handling floats by removing decimal points
                target_df['orgnbr'] = target_df['orgnbr'].apply(lambda x: str(int(float(x))) if pd.notnull(x) else x)
                wh_allroles['orgnbr'] = wh_allroles['orgnbr'].apply(lambda x: str(int(float(x))) if pd.notnull(x) else x)
                    
                print(f"Successfully converted both orgnbr columns to string")
            except Exception as e:
                raise ValueError(f"Cannot convert orgnbr dtypes for join: org_with_address has {target_df['orgnbr'].dtype}, wh_allroles has {wh_allroles['orgnbr'].dtype}. Error: {e}")
    
    # Handle acctnbr dtype mismatch with automatic conversion
    if acct_df['acctnbr'].dtype != wh_allroles['acctnbr'].dtype:
        print(f"Warning: acctnbr dtype mismatch - acct_df: {acct_df['acctnbr'].dtype}, wh_allroles: {wh_allroles['acctnbr'].dtype}")
        print("Converting both acctnbr columns to string for reliable joining...")
        try:
            wh_allroles = wh_allroles.copy()
            acct_df = acct_df.copy()
            
            # Convert both to string, handling floats by removing decimal points
            acct_df['acctnbr'] = acct_df['acctnbr'].apply(lambda x: str(int(float(x))) if pd.notnull(x) else str(x))
            wh_allroles['acctnbr'] = wh_allroles['acctnbr'].apply(lambda x: str(int(float(x))) if pd.notnull(x) else str(x))
                
            print(f"Successfully converted both acctnbr columns to string")
        except Exception as e:
            raise ValueError(f"Cannot convert acctnbr dtypes for join: acct_df has {acct_df['acctnbr'].dtype}, wh_allroles has {wh_allroles['acctnbr'].dtype}. Error: {e}")
    
    # Filter WH_ALLROLES to only the join key and acctnbr for filtering purposes
    wh_allroles_filtered = wh_allroles[['acctnbr', join_key]].copy()
    
    # Filter to only active accounts by inner joining with acct_df
    active_roles = pd.merge(wh_allroles_filtered, acct_df[['acctnbr']], how='inner', on='acctnbr')
    
    # Get unique entity IDs (orgnbr/persnbr) that have active accounts
    active_entities = active_roles[join_key].drop_duplicates()
    
    # Filter target DataFrame to only include entities with active accounts
    # Use semi-join pattern: filter target_df where join_key is in active_entities
    result = target_df[target_df[join_key].isin(active_entities)].copy()
    
    return result

def merge_with_input_file(my_df, input_folder, entity_type):
    """
    Merge processed dataframe with input Excel file containing additional notes/columns.
    
    Args:
        my_df: The processed dataframe (org_final or pers_final)
        input_folder: Path to folder containing Excel file (data/inputs/org or data/inputs/pers)
        entity_type: 'org' or 'pers' for error messages
        
    Returns:
        Merged dataframe with additional columns from input file
    """
    import glob
    
    # Basic validation
    assert my_df is not None, f"{entity_type}_df must not be None"
    assert input_folder is not None, "input_folder must not be None"
    assert entity_type in ['org', 'pers'], "entity_type must be 'org' or 'pers'"
    
    # Convert to Path object if string
    input_path = Path(input_folder) if not isinstance(input_folder, Path) else input_folder
    assert input_path.exists(), f"Input folder {input_path} does not exist"
    
    # Find Excel files in the input folder
    excel_files = list(input_path.glob("*.xlsx")) + list(input_path.glob("*.xls"))
    
    # Assert exactly one Excel file exists
    if len(excel_files) == 0:
        raise FileNotFoundError(f"No Excel files found in {input_path}")
    elif len(excel_files) > 1:
        raise ValueError(f"Multiple Excel files found in {input_path}. Expected exactly one file: {[f.name for f in excel_files]}")
    
    excel_file = excel_files[0]
    print(f"Reading {entity_type} input file: {excel_file.name}")
    
    # Read the Excel file
    try:
        janet_df = pd.read_excel(excel_file)
    except Exception as e:
        raise ValueError(f"Failed to read Excel file {excel_file}: {e}")
    
    if len(janet_df) == 0:
        raise ValueError(f"Excel file {excel_file.name} is empty")
    
    print(f"Janet's file has {len(janet_df):,} records and {len(janet_df.columns)} columns")
    
    # Convert my dataframe columns to uppercase for matching
    my_df_upper = my_df.copy()
    my_df_upper.columns = my_df_upper.columns.str.upper()
    
    # Janet's columns should already be uppercase, but ensure it
    janet_df.columns = janet_df.columns.str.upper()
    
    print(f"My {entity_type} columns (uppercase): {sorted(my_df_upper.columns)}")
    print(f"Janet's columns: {sorted(janet_df.columns)}")
    
    # Determine join key based on entity type
    join_key = 'ORGNBR' if entity_type == 'org' else 'PERSNBR'
    
    # Validate join key exists
    if join_key not in my_df_upper.columns:
        raise ValueError(f"Join key {join_key} not found in {entity_type} dataframe")
    if join_key not in janet_df.columns:
        raise ValueError(f"Join key {join_key} not found in Janet's file")
    
    # Validate data types match for join key
    if my_df_upper[join_key].dtype != janet_df[join_key].dtype:
        print(f"Warning: Converting {join_key} dtypes for join - my_df: {my_df_upper[join_key].dtype}, janet_df: {janet_df[join_key].dtype}")
        print("Converting both columns to string for reliable joining...")
        try:
            # Convert both to string, handling floats by removing decimal points
            my_df_upper[join_key] = my_df_upper[join_key].apply(lambda x: str(int(float(x))) if pd.notnull(x) else str(x))
            janet_df[join_key] = janet_df[join_key].apply(lambda x: str(int(float(x))) if pd.notnull(x) else str(x))
            print(f"Successfully converted both {join_key} columns to string")
        except Exception as e:
            raise ValueError(f"Cannot convert {join_key} dtypes for join: {e}")
    
    # Find columns that are only in Janet's file (extra notes/data)
    my_columns = set(my_df_upper.columns)
    janet_columns = set(janet_df.columns)
    
    # Columns only in Janet's file (these are the ones we want to add)
    extra_columns = janet_columns - my_columns
    print(f"Extra columns from Janet's file: {sorted(extra_columns)}")
    
    # Columns that overlap (should be the same data, we'll keep mine)
    overlap_columns = my_columns & janet_columns
    print(f"Overlapping columns: {sorted(overlap_columns)}")
    
    # Select only the join key and extra columns from Janet's file
    janet_subset = janet_df[[join_key] + list(extra_columns)].copy()
    
    # Perform left merge to keep all my records and add Janet's extra columns
    result = pd.merge(my_df_upper, janet_subset, on=join_key, how='left')
    
    print(f"Merge result: {len(result):,} records, {len(result.columns)} columns")
    print(f"Added {len(extra_columns)} extra columns from Janet's file")
    
    return result

def process_input_files():
    """
    Process both org and pers input files if they exist.
    This function is called from main() to handle the input file merging step.
    """
    results = {}
    
    # Check for org input file
    org_input_path = Path("data/inputs/org")
    if org_input_path.exists():
        excel_files = list(org_input_path.glob("*.xlsx")) + list(org_input_path.glob("*.xls"))
        if excel_files:
            print(f"Found org input file to process: {excel_files[0].name}")
            results['has_org_input'] = True
        else:
            print("No org Excel file found in data/inputs/org")
            results['has_org_input'] = False
    else:
        print("data/inputs/org folder does not exist")
        results['has_org_input'] = False
    
    # Check for pers input file
    pers_input_path = Path("data/inputs/pers")
    if pers_input_path.exists():
        excel_files = list(pers_input_path.glob("*.xlsx")) + list(pers_input_path.glob("*.xls"))
        if excel_files:
            print(f"Found pers input file to process: {excel_files[0].name}")
            results['has_pers_input'] = True
        else:
            print("No pers Excel file found in data/inputs/pers")
            results['has_pers_input'] = False
    else:
        print("data/inputs/pers folder does not exist")
        results['has_pers_input'] = False
    
    return results

def archive_input_file(input_folder, entity_type):
    """
    Move processed Excel file from input folder to archive folder.
    
    Args:
        input_folder: Path to folder containing Excel file (data/inputs/org or data/inputs/pers)
        entity_type: 'org' or 'pers' for error messages
    
    Returns:
        Path to archived file if successful, None if no file to archive
    """
    import shutil
    
    # Basic validation
    assert input_folder is not None, "input_folder must not be None"
    assert entity_type in ['org', 'pers'], "entity_type must be 'org' or 'pers'"
    
    # Convert to Path object if string
    input_path = Path(input_folder) if not isinstance(input_folder, Path) else input_folder
    assert input_path.exists(), f"Input folder {input_path} does not exist"
    
    # Find Excel files in the input folder
    excel_files = list(input_path.glob("*.xlsx")) + list(input_path.glob("*.xls"))
    
    if len(excel_files) == 0:
        print(f"No Excel files found in {input_path} to archive")
        return None
    elif len(excel_files) > 1:
        print(f"Warning: Multiple Excel files found in {input_path}, archiving all")
    
    # Create archive folder
    archive_path = Path("data/archive")
    archive_path.mkdir(exist_ok=True)
    
    archived_files = []
    
    for excel_file in excel_files:
        # Destination path in archive
        archive_file = archive_path / excel_file.name
        
        # Move file to archive (overwrite if exists)
        if archive_file.exists():
            print(f"Overwriting existing archive file: {archive_file.name}")
        
        shutil.move(str(excel_file), str(archive_file))
        archived_files.append(archive_file.resolve())  # Use absolute path
        print(f"Archived {excel_file.name} -> {archive_file}")
    
    return archived_files[0] if len(archived_files) == 1 else archived_files