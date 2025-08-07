"""
Core business logic for CRE Reporting Board.

This module contains all the processing logic for generating the CRE loader file.
All data transformations, calculations, joining logic, and output generation happens here.
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
import src.config
from src.cre_board_reporting.fetch_data import fetch_prop_data
import cdutils.acct_file_creation.core
import cdutils.input_cleansing

# =============================================================================
# DATA TRANSFORMATION AND JOINING FUNCTIONS
# =============================================================================

def join_prop_tables(wh_prop, wh_prop2):
    """
    Merging property tables on acctnbr and propnbr

    Args:
        wh_prop (pd.DataFrame): Property information from OSIBANK
        wh_prop2 (pd.DataFrame): Additional property details from OSIBANK
    
    Returns:
        df (pd.DataFrame): Combined property tables
    """
    # Merge property tables
    df = pd.merge(wh_prop, wh_prop2, on=['acctnbr', 'propnbr'], how='left')
    
    return df

def consolidation_with_one_prop(main_loan_data, property_data):
    """
    Consolidate loan data with single property information.
    
    For loans with multiple properties, this groups by property type and takes
    the property type with the highest total appraised value per account.
    
    Args:
        main_loan_data (pd.DataFrame): Consolidated loan data
        property_data (pd.DataFrame): Property data
        
    Returns:
        pd.DataFrame: Loan data with property information based on highest value property type
    """
    # Create mapping from individual property types to groups
    proptype_mapping = {code: group for group, codes in src.config.PROPERTY_TYPE_GROUPS.items() for code in codes}
    
    # Add cleaned property type to property data
    property_data = property_data.copy()
    property_data['Cleaned PropType'] = property_data['proptypdesc'].map(proptype_mapping).fillna(property_data['proptypdesc'])
    
    # Group by account and cleaned property type, sum appraisal values
    type_totals = (
        property_data.groupby(['acctnbr','Cleaned PropType'], as_index=False, dropna=False)
        .agg(tot_appraisal_cleaned=('aprsvalueamt','sum'))
    )
    
    # Find the property type with highest total appraisal per account
    idx = type_totals.groupby('acctnbr')['tot_appraisal_cleaned'].idxmax()
    top_type_cleaned = type_totals.loc[idx]
    
    # Also group by original property type description
    type_totals_orig = (
        property_data.groupby(['acctnbr','proptypdesc'], as_index=False, dropna=False)
        .agg(tot_appraisal_proptypdesc=('aprsvalueamt','sum'))
    )
    
    # Find the original property type with highest total appraisal per account
    idx_orig = type_totals_orig.groupby('acctnbr')['tot_appraisal_proptypdesc'].idxmax()
    top_type_orig = type_totals_orig.loc[idx_orig]
    
    # Merge the cleaned property type info with loan data
    result = pd.merge(main_loan_data, top_type_cleaned, on='acctnbr', how='left')
    
    # Merge the original property type info
    result = pd.merge(result, top_type_orig, on='acctnbr', how='left')
    
    return result

def consolidation_with_multiple_props(main_loan_data, property_data):
    """
    Consolidate loan data keeping all property information.
    
    Args:
        main_loan_data (pd.DataFrame): Consolidated loan data
        property_data (pd.DataFrame): Property data
        
    Returns:
        pd.DataFrame: Loan data with all properties (may have multiple rows per loan)
    """
    # Merge keeping all properties
    multiple_prop_data = pd.merge(
        main_loan_data, 
        property_data, 
        on='acctnbr', 
        how='left'
    )
    
    return multiple_prop_data

# =============================================================================
# I-CRE PRODUCTION & BALANCE GROWTH FUNCTIONS
# =============================================================================

def fetch_icre_data_for_year(year: int):
    """
    Fetch I-CRE loan data for a specific year.
    
    Args:
        year (int): The year to fetch data for
        
    Returns:
        tuple: (all_icre_loans, originated_this_year)
    """
    print(f"Fetching I-CRE data for {year}...")
    
    # Get loan data for the specified year-end
    year_end_date = datetime(year, 12, 31)
    main_loan_data = cdutils.acct_file_creation.core.query_df_on_date(year_end_date)
    
    # Filter to I-CRE loans only
    icre_loans = main_loan_data[main_loan_data['fdiccatcd'].isin(['REMU', 'RENO'])].copy()
    
    # Get current property data (since historical property data is not available)
    prop_data_dict = fetch_prop_data()
    prop_data = join_prop_tables(prop_data_dict['wh_prop'], prop_data_dict['wh_prop2'])
    prop_data.columns = prop_data.columns.str.lower()
    
    # Enforce consistent data types
    loan_schema = {'acctnbr': str}
    prop_schema = {'acctnbr': str, 'propnbr': str}
    
    icre_loans = cdutils.input_cleansing.enforce_schema(icre_loans, loan_schema)
    prop_data = cdutils.input_cleansing.enforce_schema(prop_data, prop_schema)
    
    # Consolidate with property data
    icre_with_props = consolidation_with_one_prop(icre_loans, prop_data)
    
    # Sort by Total Exposure
    icre_with_props = icre_with_props.sort_values(
        by=['Total Exposure', 'acctnbr'], 
        ascending=[False, True]
    )
    
    # Filter to loans originated in specified year
    year_start = datetime(year, 1, 1)
    originated_this_year = icre_with_props[
        pd.to_datetime(icre_with_props['origdate']) >= year_start
    ].copy()
    
    print(f"Found {len(icre_with_props)} total I-CRE loans and {len(originated_this_year)} originated in {year}")
    
    return icre_with_props, originated_this_year

def calculate_production_summary(years: list = None):
    """
    Calculate I-CRE production totals by year.
    
    Args:
        years (list): List of years to analyze. If None, uses config.ICRE_ANALYSIS_YEARS
        
    Returns:
        pd.DataFrame: Production summary by year
    """
    if years is None:
        years = src.config.ICRE_ANALYSIS_YEARS
        
    print("Calculating I-CRE production summary...")
    
    production_results = []
    
    for year in years:
        _, originated_loans = fetch_icre_data_for_year(year)
        
        # Sum original total loan amounts for production
        total_production = originated_loans['orig_ttl_loan_amt'].sum()
        
        production_results.append({
            'Year': year, 
            'Production Total': total_production,
            'Number of Loans': len(originated_loans)
        })
        
        print(f"{year}: ${total_production:,.2f} in production ({len(originated_loans)} loans)")
    
    return pd.DataFrame(production_results)

def calculate_balance_summary(years: list = None):
    """
    Calculate I-CRE balance totals by year.
    
    Args:
        years (list): List of years to analyze. If None, uses config.ICRE_ANALYSIS_YEARS
        
    Returns:
        pd.DataFrame: Balance summary by year
    """
    if years is None:
        years = src.config.ICRE_ANALYSIS_YEARS
        
    print("Calculating I-CRE balance summary...")
    
    balance_results = []
    
    for year in years:
        all_loans, _ = fetch_icre_data_for_year(year)
        
        # Sum net balances for total portfolio
        total_balance = all_loans['Net Balance'].sum()
        
        balance_results.append({
            'Year': year, 
            'Balance Total': total_balance,
            'Number of Loans': len(all_loans)
        })
        
        print(f"{year}: ${total_balance:,.2f} in balances ({len(all_loans)} loans)")
    
    return pd.DataFrame(balance_results)

def generate_icre_reports():
    """
    Generate I-CRE production and balance reports.
    
    Returns:
        tuple: (production_output_path, balance_output_path)
    """
    print("Generating I-CRE production and balance reports...")
    
    # Ensure output directory exists
    src.config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Calculate summaries
    production_summary = calculate_production_summary()
    balance_summary = calculate_balance_summary()
    
    # Generate output files
    production_output_path = src.config.OUTPUT_DIR / "icre_production.xlsx"
    balance_output_path = src.config.OUTPUT_DIR / "icre_balances.xlsx"
    
    # Write to Excel
    production_summary.to_excel(production_output_path, engine='openpyxl', index=False)
    balance_summary.to_excel(balance_output_path, engine='openpyxl', index=False)
    
    print(f"I-CRE Production report: {production_output_path}")
    print(f"I-CRE Balance report: {balance_output_path}")
    
    return production_output_path, balance_output_path

# =============================================================================
# CALL CODE GROUPING AND LOAN CATEGORY ANALYSIS
# =============================================================================

def add_call_code_grouping(df):
    """
    Add call code grouping to loan data.
    
    Args:
        df (pd.DataFrame): Loan data with fdiccatcd column
        
    Returns:
        pd.DataFrame: Data with 'Cleaned Call Code' column added
    """
    # Create mapping from individual call codes to groups
    call_code_mapping = {code: group for group, codes in src.config.FDIC_CALL_CODE_GROUPS.items() for code in codes}
    
    # Add cleaned call code grouping
    df_copy = df.copy()
    df_copy['Cleaned Call Code'] = df_copy['fdiccatcd'].map(call_code_mapping)
    
    return df_copy

def generate_total_cml_report(processed_data):
    """
    Generate Total CML report by call code groups.
    
    Args:
        processed_data (pd.DataFrame): Processed CRE data with call code grouping
        
    Returns:
        Path: Path to the generated total CML output file
    """
    print("Generating Total CML report...")
    
    # Group by cleaned call code and sum net balances
    total_cml = processed_data.groupby('Cleaned Call Code')['Net Balance'].sum().reset_index()
    
    # Ensure output directory exists
    src.config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Generate output file
    total_cml_output_path = src.config.OUTPUT_DIR / "total_cml.xlsx"
    total_cml.to_excel(total_cml_output_path, engine='openpyxl', index=False)
    
    print(f"Total CML report: {total_cml_output_path}")
    
    # Log summary
    for _, row in total_cml.iterrows():
        print(f"{row['Cleaned Call Code']}: ${row['Net Balance']:,.2f}")
    
    return total_cml_output_path

def generate_icre_detailed_report(processed_data):
    """
    Generate detailed I-CRE report with property type grouping.
    
    Args:
        processed_data (pd.DataFrame): Processed CRE data
        
    Returns:
        Path: Path to the generated I-CRE detailed output file
    """
    print("Generating detailed I-CRE report...")
    
    # Filter to I-CRE loans
    icre_data = processed_data[processed_data['fdiccatcd'].isin(['RENO', 'REMU'])].copy()
    
    # Add property type grouping if proptypdesc column exists
    if 'proptypdesc' in icre_data.columns:
        proptype_mapping = {code: group for group, codes in src.config.PROPERTY_TYPE_GROUPS.items() for code in codes}
        icre_data['Cleaned PropType'] = icre_data['proptypdesc'].map(proptype_mapping).fillna(icre_data['proptypdesc'])
    
    # Ensure output directory exists
    src.config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Generate output file
    icre_output_path = src.config.OUTPUT_DIR / "icre_detailed.xlsx"
    icre_data.to_excel(icre_output_path, engine='openpyxl', index=False)
    
    print(f"I-CRE detailed report: {icre_output_path}")
    print(f"I-CRE total balance: ${icre_data['Net Balance'].sum():,.2f}")
    
    return icre_output_path


def generate_construction_report(processed_data):
    """
    Generate Construction loans report with property type grouping.
    
    Args:
        processed_data (pd.DataFrame): Processed CRE data
        
    Returns:
        Path: Path to the generated Construction output file
    """
    print("Generating Construction report...")
    
    # Filter to Construction loans
    construction_data = processed_data[processed_data['Cleaned Call Code'] == 'Construction'].copy()
    
    # Add property type grouping if proptypdesc column exists
    if 'proptypdesc' in construction_data.columns:
        proptype_mapping = {code: group for group, codes in src.config.PROPERTY_TYPE_GROUPS.items() for code in codes}
        construction_data['Cleaned PropType'] = construction_data['proptypdesc'].map(proptype_mapping).fillna(construction_data['proptypdesc'])
    
    # Ensure output directory exists
    src.config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Generate output file
    construction_output_path = src.config.OUTPUT_DIR / "construction.xlsx"
    construction_data.to_excel(construction_output_path, engine='openpyxl', index=False)
    
    print(f"Construction report: {construction_output_path}")
    print(f"Construction total balance: ${construction_data['Net Balance'].sum():,.2f}")
    
    return construction_output_path

def generate_current_icre_report():
    """
    Generate current I-CRE loans report from daily loan data.
    This filters the full daily file for I-CRE loans and writes to icre.xlsx.
    
    Returns:
        Path: Path to the generated I-CRE output file
    """
    print("Generating current I-CRE report from daily data...")
    
    # Get current daily loan data
    main_loan_data = cdutils.acct_file_creation.core.query_df_on_date()
    
    # Filter to I-CRE loans only (using FDIC call codes from config)
    icre_call_codes = src.config.FDIC_CALL_CODE_GROUPS['I-CRE']  # ['RENO', 'REMU']
    icre_data = main_loan_data[main_loan_data['fdiccatcd'].isin(icre_call_codes)].copy()
    
    # Ensure output directory exists
    src.config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Generate output file
    icre_output_path = src.config.OUTPUT_DIR / "icre.xlsx"
    icre_data.to_excel(icre_output_path, engine='openpyxl', index=False)
    
    # Calculate total for validation
    total_balance = icre_data['Net Balance'].sum()
    
    print(f"Current I-CRE report: {icre_output_path}")
    print(f"Current I-CRE total balance: ${total_balance:,.2f} ({len(icre_data)} loans)")
    print(f"I-CRE call codes used: {icre_call_codes}")
    
    return icre_output_path

# =============================================================================
# MAIN PROCESSING PIPELINE
# =============================================================================

def process_cre_data():
    """
    Main processing function for CRE Reporting Board data.
    
    Returns:
        pd.DataFrame: Processed CRE data ready for output
    """
    print("Fetching data from COCC...")
    # Fetch data from database
    main_loan_data = cdutils.acct_file_creation.core.query_df_on_date()
    prop_data_dict = fetch_prop_data()
    
    # Join property tables
    print("Joining property tables...")
    prop_data = join_prop_tables(prop_data_dict['wh_prop'], prop_data_dict['wh_prop2'])
    
    # Convert column names to lowercase for consistency
    prop_data.columns = prop_data.columns.str.lower()
    
    # Enforce consistent data types for merge keys
    print("Enforcing data type consistency...")
    
    # Define schema for key columns to ensure consistent data types
    loan_schema = {'acctnbr': str}
    prop_schema = {'acctnbr': str, 'propnbr': str}
    
    # Apply schema enforcement
    main_loan_data = cdutils.input_cleansing.enforce_schema(main_loan_data, loan_schema)
    prop_data = cdutils.input_cleansing.enforce_schema(prop_data, prop_schema)
    
    # Filter to CRE loans only (before property merge for efficiency)
    print("Filtering to CRE loans only...")
    cre_loans = main_loan_data[main_loan_data['Category'] == 'CRE'].copy()
    print(f"Filtered from {len(main_loan_data)} total loans to {len(cre_loans)} CRE loans")
    
    # Consolidate loan data & property data (single property per loan)
    print("Consolidating loan and property data...")
    single_prop_data = consolidation_with_one_prop(cre_loans, prop_data)
    
    # Add call code grouping
    print("Adding call code grouping...")
    single_prop_data = add_call_code_grouping(single_prop_data)
    
    # multiple_prop_data = consolidation_with_multiple_props(main_loan_data, property_data)

    # Sort data by Total Exposure (descending) and account number
    single_prop_data = single_prop_data.sort_values(
        by=['Total Exposure', 'acctnbr'], 
        ascending=[False, True]
    )
    # multiple_prop_data = multiple_prop_data.sort_values(by=['Total Exposure','acctnbr'], ascending=[False, True])

    print(f"Processing complete. Final dataset has {len(single_prop_data)} records.")
    
    return single_prop_data

def generate_output(processed_data):
    """
    Generate the output Excel file for CRE Reporting Board.
    
    Args:
        processed_data (pd.DataFrame): Processed CRE data
        
    Returns:
        Path: Path to the generated output file
    """
    # Ensure output directory exists
    src.config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Create output file path
    output_file_path = src.config.OUTPUT_DIR / src.config.OUTPUT_FILENAME
    
    print(f"Writing output to: {output_file_path}")
    
    # Writing loan data with single property data to excel
    processed_data.to_excel(output_file_path, engine='openpyxl', index=False)
    
    # Writing loan data with multiple property data to excel (commented out - not currently used)
    # multiple_prop_data_file_path = src.config.OUTPUT_DIR / "multiple_property_per_loan.xlsx"
    # multiple_prop_data.to_excel(multiple_prop_data_file_path, engine='openpyxl', index=False)
    
    print(f"Output file created successfully: {output_file_path}")
    
    return output_file_path

def run_cre_reporting_pipeline():
    """
    Execute the complete CRE Reporting Board pipeline.
    
    Returns:
        dict: Dictionary containing paths to generated output files
    """
    try:
        print("=== CRE Reporting Board Pipeline ===")
        
        # Process the main CRE loader data
        print("\n1. Processing CRE Loader data...")
        processed_data = process_cre_data()
        
        # Generate CRE loader output
        print("\n2. Generating CRE Loader output...")
        cre_loader_path = generate_output(processed_data)
        
        # Generate call code analysis reports
        print("\n3. Generating Call Code Analysis reports...")
        total_cml_path = generate_total_cml_report(processed_data)
        icre_detailed_path = generate_icre_detailed_report(processed_data)
        construction_path = generate_construction_report(processed_data)
        
        # Generate current I-CRE report from daily data
        print("\n4. Generating current I-CRE report...")
        current_icre_path = generate_current_icre_report()
        
        # Generate I-CRE production and balance reports
        print("\n5. Generating I-CRE Production and Balance reports...")
        production_path, balance_path = generate_icre_reports()
        
        print("\n=== Pipeline Complete ===")
        
        return {
            'cre_loader': cre_loader_path,
            'total_cml': total_cml_path,
            'icre_detailed': icre_detailed_path,
            'construction': construction_path,
            'current_icre': current_icre_path,
            'icre_production': production_path,
            'icre_balances': balance_path
        }
        
    except Exception as e:
        print(f"Error in CRE Reporting pipeline: {str(e)}")
        raise