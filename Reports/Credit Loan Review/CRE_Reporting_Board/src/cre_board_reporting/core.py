"""
Core business logic for CRE Reporting Board.

This module contains all the processing logic for generating the CRE loader file.
All data transformations, calculations, joining logic, and output generation happens here.
"""

import pandas as pd
from pathlib import Path
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
    
    # Consolidate loan data & property data (single property per loan)
    print("Consolidating loan and property data...")
    single_prop_data = consolidation_with_one_prop(main_loan_data, prop_data)
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