"""
Join functions for Accubranch project.

This module provides functions to join account data with customer data,
applying data cleaning and filtering logic.

Note: All join fields (customer numbers, address numbers) are automatically
cast to strings to ensure consistent joins regardless of the original data types
in CSV files. This prevents join failures due to type mismatches between
integer and float types that can occur when pandas reads CSV data.
"""

import pandas as pd


def join_accounts_with_orgs(acct_df, wh_org_df, exclude_org_types=None):
    """
    Join account data with organization data, applying data cleaning and filtering.
    
    Parameters:
    -----------
    acct_df : pd.DataFrame
        Account data with taxrptfororgnbr column
    wh_org_df : pd.DataFrame  
        Organization data with orgnbr, orgtypcd, adddate columns
    exclude_org_types : list, optional
        List of organization type codes to exclude from results
        (e.g., ['NONPROF', 'PART'] to exclude nonprofits and partnerships)
        
    Returns:
    --------
    pd.DataFrame
        Merged dataframe with organization data joined to accounts,
        excluding specified organization types
        
    Example:
    --------
    >>> # Load data
    >>> acct_df = pd.read_csv('assets/mock_data/acct_df.csv')
    >>> wh_org_df = pd.read_csv('assets/mock_data/wh_org.csv')
    >>> 
    >>> # Join and exclude nonprofits
    >>> result = join_accounts_with_orgs(acct_df, wh_org_df, exclude_org_types=['NONPROF'])
    >>> 
    >>> # Check results
    >>> print(f"Original accounts: {len(acct_df)}")
    >>> print(f"After join and filter: {len(result)}")
    """
    if exclude_org_types is None:
        exclude_org_types = []
    
    # Ensure join fields are strings for consistent joins, but preserve nulls
    acct_df = acct_df.copy()
    wh_org_df = wh_org_df.copy()
    
    # Cast to string but handle numeric types properly and preserve NaN/None values
    # For taxrptfororgnbr: handle mixed string/numeric data
    def safe_string_cast(series):
        """Convert series to string, handling numeric types properly"""
        result = series.astype(str)  # Start with string conversion
        # Only convert numeric values to avoid .0 suffix
        numeric_mask = pd.to_numeric(series, errors='coerce').notna()
        if numeric_mask.any():
            result.loc[numeric_mask] = pd.to_numeric(series[numeric_mask], errors='coerce').astype(int).astype(str)
        # Handle nulls properly
        result = result.replace('nan', pd.NA).replace('<NA>', pd.NA)
        return result
    
    acct_df['taxrptfororgnbr'] = safe_string_cast(acct_df['taxrptfororgnbr'])
    wh_org_df['orgnbr'] = safe_string_cast(wh_org_df['orgnbr'])
    
    # Step 1: Sort wh_org by adddate descending and remove duplicates
    # This keeps the most recent record for each orgnbr
    wh_org_cleaned = wh_org_df.sort_values('adddate', ascending=False).drop_duplicates(
        subset=['orgnbr'], keep='first'
    )
    
    # Step 2: Drop adddate column since it's only needed for deduplication
    wh_org_cleaned = wh_org_cleaned.drop(columns=['adddate'])
    
    # Step 3: Assert precondition that orgnbr is unique after cleaning
    assert wh_org_cleaned['orgnbr'].is_unique, "orgnbr should be unique after deduplication"
    
    # Step 4: Left join accounts with organizations
    # Join on taxrptfororgnbr (from accounts) = orgnbr (from organizations)
    merged_df = pd.merge(
        acct_df, 
        wh_org_cleaned, 
        left_on='taxrptfororgnbr', 
        right_on='orgnbr', 
        how='left'
    )
    
    # Step 5: Exclude specified organization types
    if exclude_org_types:
        # Only exclude where orgtypcd is not null and in the exclude list
        exclude_mask = merged_df['orgtypcd'].notna() & merged_df['orgtypcd'].isin(exclude_org_types)
        merged_df = merged_df[~exclude_mask]
        
        print(f"Excluded {exclude_mask.sum()} records with organization types: {exclude_org_types}")
    
    return merged_df


def join_accounts_with_persons(acct_df, wh_pers_df):
    """
    Join account data with person data.
    
    Parameters:
    -----------
    acct_df : pd.DataFrame
        Account data with taxrptforpersnbr column
    wh_pers_df : pd.DataFrame  
        Person data with persnbr, datebirth, adddate columns
        
    Returns:
    --------
    pd.DataFrame
        Merged dataframe with person data joined to accounts
        
    Example:
    --------
    >>> # Load data
    >>> acct_df = pd.read_csv('assets/mock_data/acct_df.csv')
    >>> wh_pers_df = pd.read_csv('assets/mock_data/wh_pers.csv')
    >>> 
    >>> # Join accounts with person data
    >>> result = join_accounts_with_persons(acct_df, wh_pers_df)
    >>> 
    >>> # Check results
    >>> print(f"Original accounts: {len(acct_df)}")
    >>> print(f"After join: {len(result)}")
    """
    # Ensure join fields are strings for consistent joins, but preserve nulls
    acct_df = acct_df.copy()
    wh_pers_df = wh_pers_df.copy()
    
    # Cast to string but handle numeric types properly and preserve NaN/None values
    # For taxrptforpersnbr: handle mixed string/numeric data
    def safe_string_cast(series):
        """Convert series to string, handling numeric types properly"""
        result = series.astype(str)  # Start with string conversion
        # Only convert numeric values to avoid .0 suffix
        numeric_mask = pd.to_numeric(series, errors='coerce').notna()
        if numeric_mask.any():
            result.loc[numeric_mask] = pd.to_numeric(series[numeric_mask], errors='coerce').astype(int).astype(str)
        # Handle nulls properly
        result = result.replace('nan', pd.NA).replace('<NA>', pd.NA)
        return result
    
    acct_df['taxrptforpersnbr'] = safe_string_cast(acct_df['taxrptforpersnbr'])
    wh_pers_df['persnbr'] = safe_string_cast(wh_pers_df['persnbr'])
    
    # Sort wh_pers by adddate descending and remove duplicates
    # This keeps the most recent record for each persnbr
    wh_pers_cleaned = wh_pers_df.sort_values('adddate', ascending=False).drop_duplicates(
        subset=['persnbr'], keep='first'
    )
    
    # Drop adddate column since it's only needed for deduplication
    wh_pers_cleaned = wh_pers_cleaned.drop(columns=['adddate'])
    
    # Assert precondition that persnbr is unique after cleaning
    assert wh_pers_cleaned['persnbr'].is_unique, "persnbr should be unique after deduplication"
    
    # Left join accounts with persons
    # Join on taxrptforpersnbr (from accounts) = persnbr (from persons)
    merged_df = pd.merge(
        acct_df, 
        wh_pers_cleaned, 
        left_on='taxrptforpersnbr', 
        right_on='persnbr', 
        how='left'
    )
    
    return merged_df


def join_accounts_with_addresses(acct_df, addr_use_df, wh_addr_df, address_use_type='PRI'):
    """
    Join account data with address data through address use tables.
    
    Parameters:
    -----------
    acct_df : pd.DataFrame
        Account data with taxrptfororgnbr or taxrptforpersnbr columns
    addr_use_df : pd.DataFrame  
        Address use data (persaddruse or orgaddruse) with customer number, addrusecd, addrnbr columns
    wh_addr_df : pd.DataFrame
        Address master data with addrnbr, text1, text2, text3, cityname, statecd, zipcd columns
    address_use_type : str, optional
        Address use code to filter on (default 'PRI' for primary addresses)
        
    Returns:
    --------
    pd.DataFrame
        Merged dataframe with address data joined to accounts
        
    Example:
    --------
    >>> # Load data
    >>> acct_df = pd.read_csv('assets/mock_data/acct_df.csv')
    >>> pers_addr_df = pd.read_csv('assets/mock_data/persaddruse.csv')
    >>> wh_addr_df = pd.read_csv('assets/mock_data/wh_addr.csv')
    >>> 
    >>> # Join person accounts with primary addresses
    >>> person_accounts = acct_df[acct_df['taxrptforpersnbr'].notna()]
    >>> result = join_accounts_with_addresses(person_accounts, pers_addr_df, wh_addr_df)
    """
    # Filter address use data for specified type (e.g., 'PRI' for primary)
    addr_use_filtered = addr_use_df[addr_use_df['addrusecd'] == address_use_type].copy()
    
    # Determine the customer number column based on what's in addr_use_df
    if 'persnbr' in addr_use_filtered.columns:
        customer_col = 'persnbr'
        acct_join_col = 'taxrptforpersnbr'
    elif 'orgnbr' in addr_use_filtered.columns:
        customer_col = 'orgnbr'
        acct_join_col = 'taxrptfororgnbr'
    else:
        raise ValueError("Address use dataframe must contain either 'persnbr' or 'orgnbr' column")
    
    # Ensure join fields are strings for consistent joins, but preserve nulls
    acct_df = acct_df.copy()
    wh_addr_df = wh_addr_df.copy()
    
    # Cast to string but handle numeric types properly and preserve NaN/None values
    # For address fields: handle mixed string/numeric data
    def safe_string_cast(series):
        """Convert series to string, handling numeric types properly"""
        result = series.astype(str)  # Start with string conversion
        # Only convert numeric values to avoid .0 suffix
        numeric_mask = pd.to_numeric(series, errors='coerce').notna()
        if numeric_mask.any():
            result.loc[numeric_mask] = pd.to_numeric(series[numeric_mask], errors='coerce').astype(int).astype(str)
        # Handle nulls properly
        result = result.replace('nan', pd.NA).replace('<NA>', pd.NA)
        return result
    
    acct_df[acct_join_col] = safe_string_cast(acct_df[acct_join_col])
    addr_use_filtered[customer_col] = safe_string_cast(addr_use_filtered[customer_col])
    addr_use_filtered['addrnbr'] = safe_string_cast(addr_use_filtered['addrnbr'])
    wh_addr_df['addrnbr'] = safe_string_cast(wh_addr_df['addrnbr'])
    
    # Remove duplicates - keep most recent effective date for each customer
    addr_use_cleaned = addr_use_filtered.sort_values('effdate', ascending=False).drop_duplicates(
        subset=[customer_col], keep='first'
    )
    
    # Join accounts with address use data
    merged_df = pd.merge(
        acct_df,
        addr_use_cleaned[[customer_col, 'addrnbr']],
        left_on=acct_join_col,
        right_on=customer_col,
        how='left'
    )
    
    # Join with address master data to get address details
    address_fields = ['addrnbr', 'text1', 'text2', 'text3', 'cityname', 'statecd', 'zipcd']
    merged_df = pd.merge(
        merged_df,
        wh_addr_df[address_fields],
        on='addrnbr',
        how='left'
    )
    
    return merged_df


if __name__ == "__main__":
    # Example usage and testing
    import os
    
    # Check if mock data exists
    if os.path.exists('assets/mock_data/acct_df.csv'):
        print("Testing join functions with mock data...")
        
        # Load data
        acct_df = pd.read_csv('assets/mock_data/acct_df.csv')
        wh_org_df = pd.read_csv('assets/mock_data/wh_org.csv')
        
        print(f"Original accounts: {len(acct_df)}")
        print(f"Organization records: {len(wh_org_df)}")
        
        # Test organization join
        result = join_accounts_with_orgs(acct_df, wh_org_df, exclude_org_types=['NONPROF'])
        print(f"After join and exclude NONPROF: {len(result)}")
        
        # Check if address data exists
        if os.path.exists('assets/mock_data/wh_addr.csv') and os.path.exists('assets/mock_data/orgaddruse.csv'):
            wh_addr_df = pd.read_csv('assets/mock_data/wh_addr.csv')
            org_addr_df = pd.read_csv('assets/mock_data/orgaddruse.csv')
            
            # Test address join for organization accounts
            org_accounts = result[result['taxrptfororgnbr'].notna()]
            if len(org_accounts) > 0:
                addr_result = join_accounts_with_addresses(org_accounts, org_addr_df, wh_addr_df)
                print(f"Organization accounts with addresses: {len(addr_result)}")
                print(f"Accounts with text1 address: {addr_result['text1'].notna().sum()}")
    else:
        print("Mock data not found. Run the mock data generator first:")
        print("python -m tests.utility")
