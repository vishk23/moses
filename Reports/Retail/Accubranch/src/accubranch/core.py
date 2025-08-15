"""
Core business logic for Accubranch account data processing.

This module handles:
1. Account data generation for current period
2. 5-year historical analysis
3. Data transformation and output generation
"""

import sys
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import numpy as np
import pandas as pd

import src.config as config
import src.accubranch.data_cleaning_main
import src.accubranch.annual_deposit_history
import cdutils.acct_file_creation.core
import cdutils.pkey_sqlite
import cdutils.hhnbr
import cdutils.loans.calculations
import cdutils.inactive_date
import cdutils.input_cleansing


def create_primary_key(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create Primary Key (Tax Owner of Account).
    Checks for required columns before creating the key.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with tax reporting columns
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with added 'Primary Key' column
    """
    df = df.copy()
    
    if 'taxrptfororgnbr' in df.columns and 'taxrptforpersnbr' in df.columns:
        df['Primary Key'] = np.where(
            df['taxrptfororgnbr'].isnull(), 
            'P' + df['taxrptforpersnbr'].astype(str), 
            'O' + df['taxrptfororgnbr'].astype(str)
        )
        print("Created Primary Key column")
    else:
        print("Warning: Required columns for Primary Key not found")
        print(f"Available columns: {list(df.columns)}")
        df['Primary Key'] = 'UNKNOWN'
    
    return df


def create_address_field(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create consolidated address field from available address columns.
    Checks for multiple possible column name patterns.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with address columns
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with added 'Address' column
    """
    def concat_address(text1, text2, text3):
        parts = [str(p).strip() for p in [text1, text2, text3] if p and str(p).strip() and str(p) != 'nan']
        return ' '.join(parts) if parts else pd.NA
    
    df = df.copy()
    
    # Check for different possible address column patterns
    address_patterns = [
        ('text1', 'text2', 'text3'),  # Original pattern
        ('addr1', 'addr2', 'addr3'),  # Alternative pattern
        ('address1', 'address2', 'address3'),  # Another alternative
        ('street1', 'street2', 'street3'),  # Yet another alternative
    ]
    
    address_cols = None
    for pattern in address_patterns:
        if all(col in df.columns for col in pattern):
            address_cols = pattern
            print(f"Using address columns: {address_cols}")
            break
    
    if address_cols:
        df['Address'] = df.apply(
            lambda row: concat_address(row.get(address_cols[0]), row.get(address_cols[1]), row.get(address_cols[2])),
            axis=1
        )
    else:
        print("Warning: No address columns found, setting Address to empty")
        print(f"Available columns: {list(df.columns)}")
        df['Address'] = pd.NA
    
    return df


def map_account_type(acct_code: str) -> str:
    """
    Map mjaccttypcd to friendly Account Type.
    
    Parameters:
    -----------
    acct_code : str
        Major account type code
        
    Returns:
    --------
    str
        Friendly account type name
    """
    return config.ACCOUNT_TYPE_MAPPING.get(str(acct_code).upper(), 'Other')


def apply_account_type_mapping(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply account type mapping and handle small business loans.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with mjaccttypcd and loanofficer columns
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with added 'Account Type' column
    """
    df = df.copy()
    df['Account Type'] = df['mjaccttypcd'].apply(map_account_type)
    
    # Handle small business loans
    df['Account Type'] = np.where(
        (df['Account Type'] == 'Commercial Loan') & 
        (df['loanofficer'].isin(config.SMALL_BUSINESS_OFFICERS)),
        'Small Business Loan',
        df['Account Type']
    )
    return df


def apply_loan_amount_logic(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply original loan amount logic for loan accounts only.
    Checks for multiple possible column names for original loan amount.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with loan amount columns
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with updated loan amount column
    """
    df = df.copy()
    
    # Check for different possible loan amount column names
    loan_amount_cols = ['orig_ttl_loan_amt']
    loan_col = None
    
    for col in loan_amount_cols:
        if col in df.columns:
            loan_col = col
            print(f"Using loan amount column: {loan_col}")
            break
    
    if loan_col and 'mjaccttypcd' in df.columns:
        df['Original Balance (Loans)'] = np.where(
            df['mjaccttypcd'].isin(config.LOAN_ACCOUNT_TYPES),
            df[loan_col],
            pd.NA
        )
        print(f"Applied loan amount logic using {loan_col}")
    else:
        print("Warning: Required columns for loan amount logic not found")
        df['Original Balance (Loans)'] = pd.NA
    
    return df


def create_business_individual_flag(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create Business/Individual flag based on organization number.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with taxrptfororgnbr column
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with added 'Business/Individual' column
    """
    df = df.copy()
    df['Business/Individual'] = np.where(
        df['taxrptfororgnbr'].isnull(),
        'Individual',
        'Business'
    )
    return df


def apply_column_renaming(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply standard column renaming for output.
    Only renames columns that actually exist in the DataFrame.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with renamed columns
    """
    df = df.copy()
    
    # Define potential column mappings
    column_mappings = {
        'cityname': 'City',
        'statecd': 'State', 
        'zipcd': 'Zip',
        'branchname': 'Branch Associated',
        'contractdate': 'Date Account Opened',
        'Net Balance': 'Current Balance',
        'datebirth': 'Date of Birth',
        # Add potential alternative column names from cdutils
        'city': 'City',
        'state': 'State',
        'zip': 'Zip',
        'branch': 'Branch Associated',
        'opendate': 'Date Account Opened',
        'dob': 'Date of Birth'
    }
    
    # Only apply mappings for columns that actually exist
    existing_mappings = {old_col: new_col for old_col, new_col in column_mappings.items() 
                        if old_col in df.columns}
    
    if existing_mappings:
        print(f"Renaming columns: {existing_mappings}")
        df = df.rename(columns=existing_mappings)
    else:
        print("No matching columns found for renaming")
    
    return df


def select_final_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Select final columns for output.
    Only selects columns that actually exist in the DataFrame.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with selected columns
    """
    desired_columns = [
        'Primary Key',
        'Address',
        'City',
        'State',
        'Zip',
        'Branch Associated',
        'Account Type',
        'Date Account Opened',
        'Current Balance',
        'Original Balance (Loans)',
        'Date of Birth'
    ]
    
    # Only select columns that actually exist
    available_columns = [col for col in desired_columns if col in df.columns]
    missing_columns = [col for col in desired_columns if col not in df.columns]
    
    if missing_columns:
        print(f"Warning: Missing columns in output: {missing_columns}")
        print(f"Available columns: {list(df.columns)}")
    
    print(f"Selecting {len(available_columns)} columns for output: {available_columns}")
    
    return df[available_columns].copy()


def process_current_account_data() -> pd.DataFrame:
    """
    Process current account data with all transformations.
    
    Returns:
    --------
    pd.DataFrame
        Processed account data ready for output
    """
    print("Fetching current account data...")
    
    # Determine the date to use
    current_date = config.CURRENT_DATA_DATE or None 
    print(f"Using date: {current_date}")
    
    # Use the data cleaning pipeline to get complete account data with addresses and person info
    data_current = src.accubranch.data_cleaning_main.run_data_cleaning_pipeline(
        as_of_date=current_date,
        data_source="production",
        exclude_org_types=config.EXCLUDE_ORG_TYPES
    )
    
    print(f"Retrieved {len(data_current)} records")
    print(f"Available columns: {list(data_current.columns)}")
    
    print("Applying data transformations...")
    
    # Apply all transformations in sequence
    data_current = create_primary_key(data_current)
    data_current = create_address_field(data_current)
    
    # Filter to target account types (if column exists)
    # Note: data_cleaning_main may have already done some filtering
    if 'mjaccttypcd' in data_current.columns:
        initial_count = len(data_current)
        data_current = data_current[
            data_current['mjaccttypcd'].isin(config.ALL_TARGET_ACCOUNT_TYPES)
        ].copy()
        print(f"Filtered to target account types: {len(data_current)} of {initial_count} records")
    else:
        print("Warning: mjaccttypcd column not found, skipping account type filtering")
    
    # Exclude ACH Manager products (if column exists)
    if 'currmiaccttypcd' in data_current.columns:
        initial_count = len(data_current)
        data_current = data_current[
            ~data_current['currmiaccttypcd'].isin(config.EXCLUDE_ACCOUNT_TYPES)
        ].copy()
        print(f"Excluded ACH Manager products: {len(data_current)} of {initial_count} records")
    else:
        print("Warning: currmiaccttypcd column not found, skipping ACH Manager exclusion")
    
    # Apply business logic transformations
    data_current = apply_account_type_mapping(data_current)
    data_current = apply_loan_amount_logic(data_current)
    data_current = create_business_individual_flag(data_current)
    data_current = apply_column_renaming(data_current)
    data_current = select_final_columns(data_current)
    
    return data_current


def process_historical_data() -> pd.DataFrame:
    """
    Process 5-year historical data for branch analysis.
    
    Returns:
    --------
    pd.DataFrame
        Historical analysis data
    """
    print("Processing 5-year historical data...")
    
    dataframes = []
    dates = []
    
    for year_config in config.HISTORICAL_YEARS:
        print(f"Processing year {year_config['year']}...")
        year_date = datetime.strptime(year_config['date'], '%Y-%m-%d')
        
        # Use the data cleaning pipeline for historical data too
        year_data = src.accubranch.data_cleaning_main.run_data_cleaning_pipeline(
            as_of_date=year_date,
            data_source="production", 
            exclude_org_types=config.EXCLUDE_ORG_TYPES
        )
        
        dataframes.append(year_data)
        dates.append(year_config['date'])
    
    print("Creating time series analysis...")
    five_yr_history = src.accubranch.annual_deposit_history.create_time_series_analysis(
        dataframes, dates
    )
    
    return five_yr_history


def process_account_data():
    """
    Main function to process all account data and generate outputs.
    """
    # Process current account data
    current_data = process_current_account_data()
    
    # Save current account data
    print(f"Saving account data to {config.ACCOUNT_OUTPUT_FILE}")
    current_data.to_parquet(config.ACCOUNT_OUTPUT_FILE, index=False)
    print(f"✓ Account data saved: {len(current_data)} records")
    
    # Process historical data
    historical_data = process_historical_data().reset_index()
    
    # Save historical data
    print(f"Saving historical data to {config.FIVE_YR_HISTORY_FILE}")
    historical_data.to_parquet(config.FIVE_YR_HISTORY_FILE, index=False)
    print(f"✓ Historical data saved: {len(historical_data)} records")
