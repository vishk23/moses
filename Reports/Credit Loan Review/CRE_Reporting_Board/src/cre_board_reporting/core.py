"""
Core business logic for CRE Reporting Board.

This module contains all the processing logic for generating the CRE loader file.
All data transformations, calculations, joining logic, and output generation happens here.
"""

import pandas as pd
from pathlib import Path
import src.config
from src.cre_board_reporting.fetch_data import fetch_cre_data, validate_data

# =============================================================================
# DATA TRANSFORMATION AND JOINING FUNCTIONS
# =============================================================================

def join_loan_tables(wh_acctcommon_me, wh_acctloan_me, wh_loans_me, wh_acct_me):
    """
    Merging core loan tables on acctnbr

    Args:
        wh_acctcommon_me (pd.DataFrame): (month end) from COCCDM
        wh_acctloan_me (pd.DataFrame): (month end) from COCCDM
        wh_loans_me (pd.DataFrame): (month end) from COCCDM
        wh_acct_me (pd.DataFrame): (month end) from COCCDM
    
    Returns:
        df (pd.DataFrame): Combined loan tables into a df
    """
    # Pre-merge validation
    assert wh_acctcommon_me['acctnbr'].is_unique, "Duplicates exist in wh_acctcommon"
    assert wh_acctloan_me['acctnbr'].is_unique, "Duplicates exist in wh_acctloan"
    assert wh_loans_me['acctnbr'].is_unique, "Duplicates exist in wh_loans"
    assert wh_acct_me['acctnbr'].is_unique, "Duplicates exist in wh_acct"

    # Merging
    df = pd.merge(wh_acctcommon_me, wh_acctloan_me, on='acctnbr', how='left')
    df = pd.merge(df, wh_loans_me, on='acctnbr', how='left')
    df = pd.merge(df, wh_acct_me, on='acctnbr', how='left')

    return df

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
    
    For loans with multiple properties, this takes the property with the 
    largest cumulative appraised value.
    
    Args:
        main_loan_data (pd.DataFrame): Consolidated loan data
        property_data (pd.DataFrame): Property data
        
    Returns:
        pd.DataFrame: Loan data with single property per loan
    """
    # Find the property with max appraised value for each account
    property_max = property_data.loc[
        property_data.groupby('acctnbr')['aprsvalueamt'].idxmax()
    ]
    
    # Merge with loan data
    single_prop_data = pd.merge(
        main_loan_data, 
        property_max, 
        on='acctnbr', 
        how='left'
    )
    
    return single_prop_data

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
# DATA CALCULATIONS AND CLEANING FUNCTIONS
# =============================================================================

def append_total_exposure_field(main_loan_data):
    """
    Calculate total exposure field for each loan.
    
    Total exposure = NOTEBAL + AVAILBALAMT (for revolving credit facilities)
    
    Args:
        main_loan_data (pd.DataFrame): Main loan dataset
        
    Returns:
        pd.DataFrame: Dataset with Total Exposure field added
    """
    # Fill NaN values in AVAILBALAMT with 0
    main_loan_data['availbalamt'] = main_loan_data['availbalamt'].fillna(0)
    
    # Calculate total exposure
    main_loan_data['Total Exposure'] = main_loan_data['notebal'] + main_loan_data['availbalamt']
    
    return main_loan_data

def cleaning_loan_data(main_loan_data):
    """
    Clean and standardize the loan data.
    
    Args:
        main_loan_data (pd.DataFrame): Raw loan data
        
    Returns:
        pd.DataFrame: Cleaned loan data
    """
    # Convert date fields to datetime (if they exist)
    date_fields = []
    for col in ['origdate', 'datemat']:
        if col in main_loan_data.columns:
            date_fields.append(col)
    
    if date_fields:
        for field in date_fields:
            main_loan_data[field] = pd.to_datetime(main_loan_data[field], errors='coerce')
    
    # Clean numeric fields
    numeric_fields = ['notebal', 'bookbalance', 'noteintrate', 'origintrate', 
                     'creditlimitamt', 'availbalamt', 'noteopenamt', 'origbal']
    
    for field in numeric_fields:
        if field in main_loan_data.columns:
            main_loan_data[field] = pd.to_numeric(main_loan_data[field], errors='coerce')
    
    # Clean string fields
    string_fields = ['ownersortname', 'product', 'fdiccatdesc', 'mjaccttypcd', 
                    'currmiaccttypcd', 'curracctstatcd']
    
    for field in string_fields:
        if field in main_loan_data.columns:
            main_loan_data[field] = main_loan_data[field].astype(str).str.strip()
    
    return main_loan_data

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
    data = fetch_cre_data()
    
    # Validate data
    validate_data(data)
    print(f"Data validation passed. Retrieved {len(data)} tables.")
    
    # Unpack data into dataframes
    wh_acctcommon = data['wh_acctcommon'].copy()
    wh_loans = data['wh_loans'].copy()
    wh_acctloan = data['wh_acctloan'].copy()
    wh_acct = data['wh_acct'].copy()
    wh_prop = data['wh_prop'].copy()
    wh_prop2 = data['wh_prop2'].copy()
    
    print(f"Processing {len(wh_acctcommon)} loan accounts...")
    
    # Transform the data
    print("Joining loan tables...")
    main_loan_data = join_loan_tables(wh_acctcommon, wh_acctloan, wh_loans, wh_acct)
    
    print("Joining property tables...")
    property_data = join_prop_tables(wh_prop, wh_prop2)
    
    # Calculate fields & data cleaning
    print("Calculating total exposure and cleaning data...")
    main_loan_data = append_total_exposure_field(main_loan_data)
    main_loan_data = cleaning_loan_data(main_loan_data)
    
    # Consolidate loan data & property data (single property per loan)
    print("Consolidating loan and property data...")
    single_prop_data = consolidation_with_one_prop(main_loan_data, property_data)
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
        Path: Path to the generated output file
    """
    try:
        # Process the data
        processed_data = process_cre_data()
        
        # Generate output
        output_path = generate_output(processed_data)
        
        return output_path
        
    except Exception as e:
        print(f"Error in CRE Reporting pipeline: {str(e)}")
        raise