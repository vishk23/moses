"""
Core business logic for Accubranch transaction data processing.

This module handles:
1. Transaction data fetching and processing
2. Account data merging
3. Data transformation and output generation
"""

import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Optional
import numpy as np
import pandas as pd

import src.config as config
import src.transactions.fetch_data


def create_customer_unique_id(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create Customer Unique ID (Tax Owner of Account) for transaction data.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with taxrptfororgnbr and taxrptforpersnbr columns
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with added 'Customer Unique ID' column
    """
    df = df.copy()
    df['Customer Unique ID'] = np.where(
        df['taxrptfororgnbr'].isnull(), 
        'P' + df['taxrptforpersnbr'].fillna(0).astype(int).astype(str), 
        'O' + df['taxrptfororgnbr'].fillna(0).astype(int).astype(str)
    )
    return df


def parse_datetime_fields(df: pd.DataFrame) -> pd.DataFrame:
    """
    Parse datetime field into separate date and time columns.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with actdatetime column
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with added 'Date of Transaction' and 'Time of Transaction' columns
    """
    df = df.copy()
    datetime_series = pd.to_datetime(df['actdatetime'], errors='coerce')
    df['Date of Transaction'] = datetime_series.dt.strftime('%Y-%m-%d')
    df['Time of Transaction'] = datetime_series.dt.strftime('%H:%M:%S')
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


def apply_column_renaming(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply standard column renaming for transaction output.
    
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
        'branchname': 'Branch of Transaction',
        'rtxntypdesc': 'Type of Transaction',
        'rtxnsourcecd': 'Type of Teller'
    })


def select_final_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Select final columns for transaction output.
    
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
        'Customer Unique ID',
        'Date of Transaction',
        'Time of Transaction',
        'Branch of Transaction',
        'Type of Teller',
        'Type of Transaction',
        'Account Type'
    ]
    return df[final_columns].copy()


def process_transaction_data(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    """
    Main function to process transaction data and generate output.
    
    Parameters:
    -----------
    start_date : datetime, optional
        Start date for transaction window. Defaults to 2024-06-30
    end_date : datetime, optional
        End date for transaction window. Defaults to 2025-06-30
    """
    # Set default date range if not provided
    if start_date is None:
        start_date = config.TRANSACTION_START_DATE
    if end_date is None:
        end_date = config.TRANSACTION_END_DATE
    
    print(f"Fetching transaction data from {start_date.date()} to {end_date.date()}...")
    
    # Fetch transaction data
    transaction_result = src.transactions.fetch_data.fetch_transactions_window(
        start_date=start_date, 
        end_date=end_date
    )
    rtxn = transaction_result['query'].copy()
    
    print(f"Retrieved {len(rtxn)} transaction records")
    
    # Fetch account data for merging
    print("Fetching account data for merging...")
    acct_result = src.transactions.fetch_data.fetch_account_data(datetime(2025, 6, 30))
    acct_data = acct_result['wh_acctcommon'].copy()
    
    print(f"Retrieved {len(acct_data)} account records")
    
    # Merge transaction and account data
    print("Merging transaction and account data...")
    merged_rtxn = pd.merge(rtxn, acct_data, on='acctnbr', how='left')
    
    print("Applying data transformations...")
    
    # Apply all transformations in sequence
    merged_rtxn = create_customer_unique_id(merged_rtxn)
    merged_rtxn = parse_datetime_fields(merged_rtxn)
    merged_rtxn = apply_account_type_mapping(merged_rtxn)
    merged_rtxn = apply_column_renaming(merged_rtxn)
    merged_rtxn = select_final_columns(merged_rtxn)
    
    # Save to output file
    print(f"Saving transaction data to {config.TRANSACTION_OUTPUT_FILE}")
    merged_rtxn.to_csv(config.TRANSACTION_OUTPUT_FILE, index=False)
    print(f"✓ Transaction data saved: {len(merged_rtxn)} records")