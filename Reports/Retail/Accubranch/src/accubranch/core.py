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
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with taxrptfororgnbr and taxrptforpersnbr columns
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with added 'Primary Key' column
    """
    df = df.copy()
    df['Primary Key'] = np.where(
        df['taxrptfororgnbr'].isnull(), 
        'P' + df['taxrptforpersnbr'].astype(str), 
        'O' + df['taxrptfororgnbr'].astype(str)
    )
    return df


def create_address_field(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create consolidated address field from text1, text2, text3.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with text1, text2, text3 columns
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with added 'Address' column
    """
    def concat_address(text1, text2, text3):
        parts = [str(p).strip() for p in [text1, text2, text3] if p and str(p).strip()]
        return ' '.join(parts) if parts else pd.NA
    
    df = df.copy()
    df['Address'] = df.apply(
        lambda row: concat_address(row.get('text1'), row.get('text2'), row.get('text3')),
        axis=1
    )
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
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with mjaccttypcd and orig_ttl_loan_amt columns
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with updated orig_ttl_loan_amt column
    """
    df = df.copy()
    df['orig_ttl_loan_amt'] = np.where(
        df['mjaccttypcd'].isin(config.LOAN_ACCOUNT_TYPES),
        df['orig_ttl_loan_amt'],
        pd.NA
    )
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
    return df.rename(columns={
        'cityname': 'City',
        'statecd': 'State',
        'zipcd': 'Zip',
        'branchname': 'Branch Associated',
        'contractdate': 'Date Account Opened',
        'Net Balance': 'Current Balance',
        'orig_ttl_loan_amt': 'Original Balance (Loans)',
        'datebirth': 'Date of Birth'
    })


def select_final_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Select final columns for output.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with selected columns
    """
    final_columns = [
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
    return df[final_columns].copy()


def process_current_account_data() -> pd.DataFrame:
    """
    Process current account data with all transformations.
    
    Returns:
    --------
    pd.DataFrame
        Processed account data ready for output
    """
    print("Fetching current account data...")
    
    # Fetch current data using cdutils
    data_current = cdutils.acct_file_creation.core.query_df_on_date(config.CURRENT_DATA_DATE)
    
    print("Applying data transformations...")
    
    # Apply all transformations in sequence
    data_current = create_primary_key(data_current)
    data_current = create_address_field(data_current)
    
    # Filter to target account types
    data_current = data_current[
        data_current['mjaccttypcd'].isin(config.ALL_TARGET_ACCOUNT_TYPES)
    ].copy()
    
    # Exclude ACH Manager products
    data_current = data_current[
        ~data_current['currmiaccttypcd'].isin(config.EXCLUDE_ACCOUNT_TYPES)
    ].copy()
    
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
        
        year_data = cdutils.acct_file_creation.core.query_df_on_date(year_date)
        
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
    current_data.to_csv(config.ACCOUNT_OUTPUT_FILE, index=False)
    print(f"✓ Account data saved: {len(current_data)} records")
    
    # Process historical data
    historical_data = process_historical_data()
    
    # Save historical data
    print(f"Saving historical data to {config.FIVE_YR_HISTORY_FILE}")
    historical_data.to_csv(config.FIVE_YR_HISTORY_FILE, index=False)
    print(f"✓ Historical data saved: {len(historical_data)} records")
