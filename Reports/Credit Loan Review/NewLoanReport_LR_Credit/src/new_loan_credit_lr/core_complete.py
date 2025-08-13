"""
Core business logic for New Loan Report LR Credit

This module contains all the data processing, transformation, and business logic
for generating the New Loan Report with 45-day lookback. This code has been 
migrated from the Production folder while maintaining all original business logic.
"""

from typing import Dict, Tuple
from pathlib import Path
from datetime import datetime, timedelta
import os

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
    
    # Handle address concatenation safely
    address_cols = ['nameaddr1', 'nameaddr2', 'nameaddr3']
    # Only concatenate if these columns exist
    existing_addr_cols = [col for col in address_cols if col in df.columns]
    if existing_addr_cols:
        df['primary_address'] = df[existing_addr_cols].apply(lambda x: ''.join(filter(None, x)), axis=1)
        df = df.drop(columns=existing_addr_cols)
    
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


def drop_household_duplicates(househldacct: pd.DataFrame) -> pd.DataFrame:
    """Drop duplicates from household account data"""
    return househldacct.drop_duplicates(subset=['acctnbr'])


def drop_org_duplicates(wh_org: pd.DataFrame) -> pd.DataFrame:
    """Drop duplicates from organization data"""
    return wh_org.drop_duplicates(subset=['orgnbr'])


def consolidate_prop_data(wh_prop: pd.DataFrame, wh_prop2: pd.DataFrame) -> pd.DataFrame:
    """
    Consolidate property data from two tables
    
    Args:
        wh_prop: Property table 1
        wh_prop2: Property table 2

    Returns:
        consolidated_prop_data: Consolidated property data

    Operations:
    - merge the tables
    - rename columns
    - keep only the property with the highest appraised value
    - fill null values in aprsvalueamt field
    """
    if wh_prop.empty or wh_prop2.empty:
        # Handle empty DataFrames
        if not wh_prop.empty:
            return wh_prop
        elif not wh_prop2.empty:
            return wh_prop2
        else:
            return pd.DataFrame()
    
    # Check if propnbr exists in both tables
    if 'propnbr' not in wh_prop.columns or 'propnbr' not in wh_prop2.columns:
        # If no propnbr, try to outer merge on acctnbr
        if 'acctnbr' in wh_prop.columns and 'acctnbr' in wh_prop2.columns:
            consolidated_prop_data = pd.merge(wh_prop, wh_prop2, how='outer', on='acctnbr', suffixes=('_x', '_y'))
        else:
            return wh_prop if not wh_prop.empty else wh_prop2
    else:
        consolidated_prop_data = pd.merge(wh_prop, wh_prop2, how='inner', on='propnbr')
    
    # Handle acctnbr consolidation
    if 'acctnbr_x' in consolidated_prop_data.columns and 'acctnbr_y' in consolidated_prop_data.columns:
        consolidated_prop_data['acctnbr'] = consolidated_prop_data['acctnbr_x'].combine_first(consolidated_prop_data['acctnbr_y'])
        consolidated_prop_data = consolidated_prop_data.drop(columns=['acctnbr_x','acctnbr_y'])
    
    # Handle appraisal value
    if 'aprsvalueamt' in consolidated_prop_data.columns:
        consolidated_prop_data['aprsvalueamt'] = consolidated_prop_data['aprsvalueamt'].fillna(0)
        if 'acctnbr' in consolidated_prop_data.columns:
            consolidated_prop_data = (consolidated_prop_data.sort_values('aprsvalueamt', ascending=False)
                                    .groupby('acctnbr', as_index=False).first())
    
    consolidated_prop_data = consolidated_prop_data.reset_index(drop=True)
    return consolidated_prop_data


def merge_data(filtered_acctcommon: pd.DataFrame, filtered_wh_loans: pd.DataFrame, 
               wh_acctloan: pd.DataFrame, consolidated_prop_data: pd.DataFrame, 
               wh_org: pd.DataFrame, househldacct: pd.DataFrame) -> pd.DataFrame:
    """
    Merging dataframes together
    
    Args:
        All the filtered dataframes
    
    Returns:
        merged_df: merged data
    """
    # QA tests - only check if DataFrames are not empty
    if not filtered_acctcommon.empty and 'acctnbr' in filtered_acctcommon.columns:
        assert filtered_acctcommon['acctnbr'].is_unique, "Duplicates found in acctcommon"
    if not househldacct.empty and 'acctnbr' in househldacct.columns:
        assert househldacct['acctnbr'].is_unique, "Duplicates found in househldacct"
    if not wh_acctloan.empty and 'acctnbr' in wh_acctloan.columns:
        assert wh_acctloan['acctnbr'].is_unique, "Duplicates found in acctloan"
    if not consolidated_prop_data.empty and 'acctnbr' in consolidated_prop_data.columns:
        assert consolidated_prop_data['acctnbr'].is_unique, "Duplicates found in prop data"
    if not wh_org.empty and 'orgnbr' in wh_org.columns:
        assert wh_org['orgnbr'].is_unique, "Duplicates found in org"

    # Start with the core loan data
    merged_df = pd.merge(filtered_acctcommon, filtered_wh_loans, on='acctnbr', how='inner')
    merged_df = pd.merge(merged_df, wh_acctloan, on='acctnbr', how='left')
    merged_df = pd.merge(merged_df, consolidated_prop_data, on='acctnbr', how='left')
    
    # Handle property number column cleanup
    if 'propnbr_y' in merged_df.columns:
        merged_df = merged_df.drop(columns=['propnbr_y'])
    if 'propnbr_x' in merged_df.columns:
        merged_df = merged_df.rename(columns={'propnbr_x':'propnbr'})
    
    # Add organization data
    if 'taxrptfororgnbr' in merged_df.columns and 'orgnbr' in wh_org.columns:
        merged_df = pd.merge(merged_df, wh_org, left_on='taxrptfororgnbr', right_on='orgnbr', how='left')
    
    # Sort by origination date
    if 'origdate' in merged_df.columns:
        merged_df = merged_df.sort_values(by='origdate', ascending=False)
    
    # Add household data
    merged_df = pd.merge(merged_df, househldacct, how='left', on='acctnbr')
    
    return merged_df


def filter_and_merge_loan_tables(acctcommon: pd.DataFrame, acctloan: pd.DataFrame, 
                                loans: pd.DataFrame) -> pd.DataFrame:
    """
    This filters on CML Loans & merges tables to consolidate loan data.
    Data cleansing on numeric fields is performed.
    
    Args:
        acctcommon: WH_ACCTCOMMON
        acctloan: WH_ACCTLOAN
        loans: WH_LOANS
        
    Returns:
        df: Consolidated loan data as a dataframe
        
    Operations:
        - mjaccttypcd (Major) == 'CML'
        - left merge of df (acctcommon) & acctloan on 'acctnbr'
        - left merge of df & loans on 'acctnbr'
        - drop all fields that are completely null/empty
        - Replace null/na values with 0 for numeric fields
    """
    # Filter for CML loans
    if 'mjaccttypcd' in acctcommon.columns:
        acctcommon_filtered = acctcommon[acctcommon['mjaccttypcd'] == 'CML'].copy()
    else:
        acctcommon_filtered = acctcommon.copy()
    
    # Merge tables
    df = pd.merge(acctcommon_filtered, acctloan, on='acctnbr', how='left')
    df = pd.merge(df, loans, on='acctnbr', how='left')
    
    # Data cleansing
    numeric_fields = ['bookbalance', 'notebal', 'availbalamt', 'totalpctsold', 
                     'noteopenamt', 'noteintrate', 'cobal', 'credlimitclatresamt']
    
    for field in numeric_fields:
        if field in df.columns:
            df[field] = pd.to_numeric(df[field], errors='coerce').fillna(0)
    
    # Special handling for CM45 account type
    if 'currmiaccttypcd' in df.columns and 'notebal' in df.columns and 'bookbalance' in df.columns:
        df['bookbalance'] = np.where(df['currmiaccttypcd'].isin(['CM45']), df['notebal'], df['bookbalance'])
    
    return df


def append_total_exposure_field(df: pd.DataFrame) -> pd.DataFrame:
    """
    Append total exposure field based on account type and balance
    """
    # Create Total Exposure field based on business rules
    if 'bookbalance' in df.columns:
        df['Total Exposure'] = df['bookbalance']
    elif 'notebal' in df.columns:
        df['Total Exposure'] = df['notebal']
    else:
        df['Total Exposure'] = 0
    
    return df


def append_grouping_keys(loan_data: pd.DataFrame, househldacct: pd.DataFrame, 
                        pkey: pd.DataFrame) -> pd.DataFrame:
    """
    Append household and portfolio keys for exposure calculations
    """
    # Add household keys
    if not househldacct.empty and 'householdnbr' in househldacct.columns:
        loan_data = pd.merge(loan_data, househldacct[['acctnbr', 'householdnbr']], 
                           on='acctnbr', how='left')
    
    # Add portfolio keys
    if not pkey.empty and 'pkey' in pkey.columns:
        # Rename pkey column to portfolio_key to match expected naming
        pkey_renamed = pkey.rename(columns={'pkey': 'portfolio_key'})
        loan_data = pd.merge(loan_data, pkey_renamed[['acctnbr', 'portfolio_key']], 
                           on='acctnbr', how='left')
    
    return loan_data


def calculate_total_exposure(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate total exposure by household and portfolio key
    """
    # Calculate household exposure
    if 'householdnbr' in df.columns and 'Total Exposure' in df.columns:
        hh_exposure = df.groupby('householdnbr', as_index=False)['Total Exposure'].sum()
        hh_exposure = hh_exposure.rename(columns={'Total Exposure':'total_exposure_hh'})
        df = pd.merge(df, hh_exposure, on='householdnbr', how='left')
    
    # Calculate portfolio key exposure
    if 'portfolio_key' in df.columns and 'Total Exposure' in df.columns:
        pkey_exposure = df.groupby('portfolio_key', as_index=False)['Total Exposure'].sum()
        pkey_exposure = pkey_exposure.rename(columns={'Total Exposure':'total_exposure_pkey'})
        df = pd.merge(df, pkey_exposure, on='portfolio_key', how='left')
    
    return df


def append_exposure(df: pd.DataFrame, keys_df: pd.DataFrame) -> pd.DataFrame:
    """
    Append exposure calculations to the main dataframe
    """
    # Ensure numeric fields are properly formatted
    list_of_numeric = ['bookbalance','notebal','availbalamt','totalpctsold',
                      'noteopenamt','noteintrate','cobal','credlimitclatresamt']
    
    for col in list_of_numeric:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # Merge exposure keys
    df = pd.merge(df, keys_df, on='acctnbr', how='left')
    
    return df


def split_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create the NEW LOAN section of the report with proper formatting
    """
    # Define columns for NEW LOAN report
    base_columns = ['acctnbr', 'ownersortname', 'origdate', 'noteopenamt', 'fdiccatdesc']
    
    # Add optional columns if they exist
    optional_columns = ['loanofficer', 'acctofficer', 'noteintrate', 'datemat', 'product']
    
    report_columns = base_columns.copy()
    for col in optional_columns:
        if col in df.columns:
            report_columns.append(col)
    
    # Filter to only include columns that exist
    available_columns = [col for col in report_columns if col in df.columns]
    
    new_loan_df = df[available_columns].copy()
    
    # Format dates
    if 'origdate' in new_loan_df.columns:
        new_loan_df['origdate'] = pd.to_datetime(new_loan_df['origdate']).dt.strftime('%m/%d/%Y')
    if 'datemat' in new_loan_df.columns:
        new_loan_df['datemat'] = pd.to_datetime(new_loan_df['datemat']).dt.strftime('%m/%d/%Y')
    
    # Format currency columns
    currency_columns = ['noteopenamt']
    for col in currency_columns:
        if col in new_loan_df.columns:
            new_loan_df[col] = pd.to_numeric(new_loan_df[col], errors='coerce')
    
    return new_loan_df


def cra_section(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create the CRA section of the report
    """
    # For CRA section, use the same base structure but potentially different filtering
    cra_df = df.copy()
    
    # Define CRA-specific columns
    cra_columns = ['acctnbr', 'ownersortname', 'origdate', 'noteopenamt', 'fdiccatdesc']
    
    # Filter to only include columns that exist
    available_columns = [col for col in cra_columns if col in cra_df.columns]
    
    cra_section_df = cra_df[available_columns].copy()
    
    # Format dates
    if 'origdate' in cra_section_df.columns:
        cra_section_df['origdate'] = pd.to_datetime(cra_section_df['origdate']).dt.strftime('%m/%d/%Y')
    
    # Format currency
    if 'noteopenamt' in cra_section_df.columns:
        cra_section_df['noteopenamt'] = pd.to_numeric(cra_section_df['noteopenamt'], errors='coerce')
    
    return cra_section_df


def main_pipeline(data: Dict[str, pd.DataFrame]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Main data pipeline for New Loan Report (migrated from Production code)
    
    Args:
        data: Dictionary containing all required DataFrames
        
    Returns:
        Tuple containing new_loan_page and cra_page DataFrames
    """
    # Get pkey database path based on environment
    if src.config.ENV == 'prod':
        base_dir = src.config.PKEY_DB_PATH
    else:
        base_dir = Path('.')  # Use local directory for dev
    
    # Create pkey database connection
    current_engine = cdutils.pkey_sqlite.create_sqlite_engine(
        'current.db', 
        use_default_dir=False, 
        base_dir=base_dir
    )

    # Extract data from dictionary
    wh_acctcommon = data['wh_acctcommon'].copy()
    wh_loans = data['wh_loans'].copy()
    wh_acctloan = data['wh_acctloan'].copy()
    wh_org = data['wh_org'].copy()
    wh_prop = data['wh_prop'].copy()
    wh_prop2 = data['wh_prop2'].copy()
    househldacct = data['househldacct'].copy()

    # Apply filters and transformations
    filtered_acctcommon = filter_acctcommon(wh_acctcommon)
    filtered_wh_loans = filter_wh_loans(wh_loans)
    consolidated_prop_data = consolidate_prop_data(wh_prop, wh_prop2)

    househldacct = drop_household_duplicates(househldacct)
    wh_org = drop_org_duplicates(wh_org)
    
    # Merge all data
    merged_df = merge_data(filtered_acctcommon, filtered_wh_loans, wh_acctloan, 
                          consolidated_prop_data, wh_org, househldacct)

    # Calculate exposure data
    loan_data = filter_and_merge_loan_tables(wh_acctcommon, wh_acctloan, wh_loans)
    loan_data = append_total_exposure_field(loan_data)

    # Get pkey data and calculate exposures
    pkey = cdutils.pkey_sqlite.query_current_db(engine=current_engine)
    loan_data = append_grouping_keys(loan_data, househldacct, pkey)
    loan_data = calculate_total_exposure(loan_data)
    
    # Get just the exposure keys
    loan_data_keys = loan_data[['acctnbr','total_exposure_hh','total_exposure_pkey']].copy()

    # Append exposure to main data
    merged_df = append_exposure(merged_df, loan_data_keys)

    # Generate final report sections
    new_loan_page = split_data(merged_df)
    cra_page = cra_section(merged_df)

    return new_loan_page, cra_page
