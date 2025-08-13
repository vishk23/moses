"""
Core business logic for New Loan Report LR Credit

This module contains all the data processing, transformation, and business logic
for generating the New Loan Report with 45-day lookback.
"""

from typing import Dict, Tuple
from pathlib import Path
from datetime import datetime

import pandas as pd  # type: ignore
import numpy as np  # type: ignore

import cdutils.pkey_sqlite
import src.config


def filter_acctcommon(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter acctcommon table

    Args:
        df: acctcommon table from COCC

    Returns:
        result_df: dataframe after filters are applied
    
    Operations:
    [MJACCTTYPCD] IN ("CML", "CNS", "MTG", "MLN") 
    AND 
    [CURRMIACCTTYPCD] != "CI07"
    If [MJACCTTYPCD] IN "CNS", [CURRMIACCTTYPCD] IN ("IL02", "IL11", "IL12", "IL13", "IL14") 
    AND 
    !IsNull([TAXRPTFORORGNBR])
    - Concatenate address fields into one primary_address field
    """
    df = df[df['mjaccttypcd'].isin(['CML', 'MTG', 'MLN'])]
    df = df[df['currmiaccttypcd'] != 'CI07']
    df['primary_address'] = df[['nameaddr1','nameaddr2','nameaddr3']].apply(lambda x: ''.join(filter(None, x)), axis=1)
    df = df.drop(columns=['nameaddr1','nameaddr2','nameaddr3'])
    return df


def filter_wh_loans(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter wh_loans

    Args:
        df: WH_LOANS_TEMP from COCCDM db table
    
    Returns:
        result_df: filtered dataframe of wh_loans
    
    Operations:
    - Filter by loan origination date within last 45 days
    """
    # Calculate 45 days ago from today
    forty_five_days_ago = pd.Timestamp.now() - pd.Timedelta(days=45)
    
    # Convert origdate to datetime if it's not already
    df['origdate'] = pd.to_datetime(df['origdate'])
    
    # Filter for loans originated in the last 45 days
    df_filtered = df[df['origdate'] >= forty_five_days_ago].copy()
    
    return df_filtered


def main_pipeline(data: Dict[str, pd.DataFrame]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Main data pipeline for New Loan Report
    
    Args:
        data: Dictionary containing all required DataFrames
        
    Returns:
        Tuple containing new_loan_page and cra_page DataFrames
    """
    # Extract data from dictionary
    wh_acctcommon = data['wh_acctcommon'].copy()
    wh_loans = data['wh_loans'].copy()
    wh_acctloan = data['wh_acctloan'].copy()
    wh_org = data['wh_org'].copy()
    wh_prop = data['wh_prop'].copy()
    wh_prop2 = data['wh_prop2'].copy()
    househldacct = data['househldacct'].copy()

    # Apply initial filters
    filtered_acctcommon = filter_acctcommon(wh_acctcommon)
    filtered_wh_loans = filter_wh_loans(wh_loans)
    
    # Merge the filtered data to create the base dataset
    # Start with filtered loan data (45-day lookback)
    base_df = filtered_wh_loans.merge(
        filtered_acctcommon,
        on='acctnbr',
        how='left'
    )
    
    # Add loan account details
    base_df = base_df.merge(
        wh_acctloan,
        on='acctnbr',
        how='left'
    )
    
    # Add organization information for business loans
    base_df = base_df.merge(
        wh_org,
        left_on='taxrptfororgnbr',
        right_on='orgnbr',
        how='left'
    )
    
    # Add property information if available
    prop_combined = combine_property_data(wh_prop, wh_prop2)
    base_df = base_df.merge(
        prop_combined,
        on='acctnbr',
        how='left'
    )
    
    # Add household information
    base_df = base_df.merge(
        househldacct,
        on='acctnbr',
        how='left'
    )
    
    # Calculate additional fields and exposure
    base_df = calculate_exposure_fields(base_df, househldacct)
    
    # Split into NEW LOAN and CRA sections
    new_loan_page = create_new_loan_section(base_df)
    cra_page = create_cra_section(base_df)
    
    return new_loan_page, cra_page


def combine_property_data(wh_prop: pd.DataFrame, wh_prop2: pd.DataFrame) -> pd.DataFrame:
    """
    Combine property data from both property tables
    """
    # Merge property tables
    combined = wh_prop.merge(
        wh_prop2,
        on='acctnbr',
        how='outer'
    )
    
    # Consolidate key fields
    if 'acctnbr_x' in combined.columns and 'acctnbr_y' in combined.columns:
        combined['acctnbr'] = combined['acctnbr_x'].combine_first(combined['acctnbr_y'])
    
    return combined


def calculate_exposure_fields(df: pd.DataFrame, househldacct: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate total exposure fields using pkey lookup
    """
    # Get pkey database connection
    if src.config.ENV == 'prod':
        pkey_db_path = src.config.PKEY_DB_PATH
    else:
        pkey_db_path = Path('.')  # Use local directory for dev
    
    current_engine = cdutils.pkey_sqlite.create_sqlite_engine(
        'current.db', 
        use_default_dir=False, 
        base_dir=pkey_db_path
    )
    
    pkey = cdutils.pkey_sqlite.query_current_db(engine=current_engine)
    
    # Add household grouping keys
    df = df.merge(
        househldacct[['acctnbr', 'householdnbr']],
        on='acctnbr',
        how='left'
    )
    
    # Add pkey grouping
    df = df.merge(
        pkey[['acctnbr', 'pkey']],
        on='acctnbr',
        how='left'
    )
    
    # Calculate total exposures
    # This would need the specific exposure calculation logic from the Production code
    # For now, placeholder
    df['total_exposure_hh'] = 0
    df['total_exposure_pkey'] = 0
    
    return df


def create_new_loan_section(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create the NEW LOAN section of the report
    """
    # Select and format columns for the NEW LOAN sheet
    new_loan_columns = [
        'acctnbr',
        'ownersortname', 
        'origdate',
        'noteopenamt',
        'fdiccatdesc',
        'loanofficer',
        'acctofficer'
    ]
    
    new_loan_df = df[new_loan_columns].copy()
    
    # Format dates
    new_loan_df['origdate'] = pd.to_datetime(new_loan_df['origdate']).dt.strftime('%m/%d/%Y')
    
    # Format currency columns
    new_loan_df['noteopenamt'] = pd.to_numeric(new_loan_df['noteopenamt'], errors='coerce')
    
    return new_loan_df


def create_cra_section(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create the CRA section of the report
    """
    # Filter for CRA-relevant loans (this would need specific business logic)
    cra_df = df.copy()
    
    # Select CRA-specific columns
    cra_columns = [
        'acctnbr',
        'ownersortname',
        'origdate', 
        'noteopenamt',
        'fdiccatdesc'
    ]
    
    cra_section = cra_df[cra_columns].copy()
    
    # Format dates
    cra_section['origdate'] = pd.to_datetime(cra_section['origdate']).dt.strftime('%m/%d/%Y')
    
    # Format currency
    cra_section['noteopenamt'] = pd.to_numeric(cra_section['noteopenamt'], errors='coerce')
    
    return cra_section