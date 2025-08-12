"""
Business logic for CT Dashboard (Covenant & Tickler tracking)
"""
import pandas as pd  # type: ignore
import numpy as np
from pathlib import Path

import src.config
from src.ct_dashboard import fetch_cocc_data as fetch_data
from src.ct_dashboard import ingest  
from src.ct_dashboard import rel_entity_officer
from src.ct_dashboard import output_to_excel_multiple_sheets


def get_mode(series):
    """
    Get mode of a pandas series, handling cases where there might be multiple modes.
    Returns the first mode if multiple exist, or None if series is empty.
    """
    series_clean = series.dropna()
    if len(series_clean) == 0:
        return None
    
    unique_values = pd.Series(series_clean.unique())
    mode_result = unique_values.mode()
    
    return mode_result.iloc[0] if len(mode_result) > 0 else None


def merge_with_mode(df_dict, cocc_data_grouped, rel_entity_grouped):
    """
    Merge dataframes with officer data from COCC and related entities.
    
    Args:
        df_dict: Dictionary of dataframes from ingest process
        cocc_data_grouped: COCC officer data grouped by customer name
        rel_entity_grouped: Related entity officer data as fallback
        
    Returns:
        Dictionary of merged dataframes with officer assignments
    """
    merged_dict = {}
    
    for key, df in df_dict.items():
        # Merge with primary officer data
        merged_df = df.merge(cocc_data_grouped, on='customer_name', how='left')
        
        # Merge with related entity officer data (fallback)
        merged_df = merged_df.merge(rel_entity_grouped, on='customer_name', how='left')
        
        # Handle datetime fields
        date_fields = ['period_date', 'due_date', 'report_date']
        for field in date_fields:
            if field in merged_df.columns:
                merged_df[field] = pd.to_datetime(merged_df[field], errors='coerce')
        
        # Sort by period date
        if 'period_date' in merged_df.columns:
            merged_df = merged_df.sort_values(by='period_date', ascending=True)
        
        # Use related entity officer as fallback when primary is null
        if 'Loan Officer' in merged_df.columns and 'Loan Officer_related' in merged_df.columns:
            merged_df['Loan Officer_final'] = np.where(
                merged_df['Loan Officer'].isnull(), 
                merged_df['Loan Officer_related'], 
                merged_df['Loan Officer']
            )
        else:
            merged_df['Loan Officer_final'] = merged_df.get('Loan Officer', '')
        
        # Select final columns
        final_columns = [
            'customer_name',
            'Loan Officer_final',
            'Deposit Officer', 
            'item_name',
            'required_value',
            'actual_value',
            'period_date',
            'due_date',
            'days_past_due',
            'interval',
            'comments',
            'report_date'
        ]
        
        # Only include columns that exist
        available_columns = [col for col in final_columns if col in merged_df.columns]
        merged_df = merged_df[available_columns].copy()
        
        # Rename final officer column
        if 'Loan Officer_final' in merged_df.columns:
            merged_df = merged_df.rename(columns={'Loan Officer_final': 'Loan Officer'})
        
        merged_dict[key] = merged_df
    
    return merged_dict


def process_ct_dashboard():
    """
    Main processing function for CT Dashboard.
    
    1. Ingests HTML files from input folder
    2. Fetches officer data from COCC database  
    3. Merges data and enriches with officer assignments
    4. Outputs formatted Excel files for covenants and ticklers
    """
    print("Processing CT Dashboard files...")
    
    # Step 1: Ingest HTML files
    print("Ingesting HTML files from input folder...")
    files = ingest.process_xls_files()
    
    if not files:
        print("No files found to process. Please place .xls files in the input folder.")
        return
    
    print(f"Found {len(files)} report types: {list(files.keys())}")
    
    # Step 2: Fetch COCC officer data
    print("Fetching officer data from COCC...")
    cocc_data = fetch_data.fetch_data()
    
    if 'wh_acctcommon' not in cocc_data:
        print("Warning: No COCC account data found")
        cocc_data_grouped = pd.DataFrame(columns=['customer_name', 'Loan Officer', 'Deposit Officer'])
    else:
        wh_acctcommon = cocc_data['wh_acctcommon'].copy()
        
        # Group by customer and get mode of officer assignments
        cocc_data_grouped = wh_acctcommon.groupby('ownersortname').agg({
            'loanofficer': get_mode,
            'acctofficer': get_mode
        }).reset_index()
        
        cocc_data_grouped = cocc_data_grouped.rename(columns={
            'ownersortname': 'customer_name',
            'loanofficer': 'Loan Officer', 
            'acctofficer': 'Deposit Officer'
        })
    
    # Step 3: Get related entity officer data (fallback)
    print("Fetching related entity officer data...")
    rel_entity_grouped = rel_entity_officer.create_officer_df()
    
    # Step 4: Merge all data
    print("Merging data with officer assignments...")
    cleaned_dict = merge_with_mode(files, cocc_data_grouped, rel_entity_grouped)
    
    # Step 5: Generate outputs
    print("Generating Excel outputs...")
    
    # Covenant tracking
    covenant_sheets = {}
    if 'covenants_past_due' in cleaned_dict:
        covenant_sheets['Past Due'] = cleaned_dict['covenants_past_due']
    if 'covenants_in_default' in cleaned_dict:
        covenant_sheets['In Default'] = cleaned_dict['covenants_in_default']
    
    if covenant_sheets:
        covenant_output_path = src.config.OUTPUT_DIR / 'CT_Covenant_Tracking.xlsx'
        print(f"Writing covenant tracking to: {covenant_output_path}")
        
        with pd.ExcelWriter(covenant_output_path, engine="openpyxl") as writer:
            for sheet_name, df in covenant_sheets.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        # Format Excel file
        output_to_excel_multiple_sheets.format_excel_file(covenant_output_path)
    
    # Tickler tracking  
    tickler_sheets = {}
    if 'ticklers_past_due' in cleaned_dict:
        tickler_sheets['Past Due'] = cleaned_dict['ticklers_past_due']
    
    if tickler_sheets:
        tickler_output_path = src.config.OUTPUT_DIR / 'CT_Tickler_Tracking.xlsx'
        print(f"Writing tickler tracking to: {tickler_output_path}")
        
        with pd.ExcelWriter(tickler_output_path, engine="openpyxl") as writer:
            for sheet_name, df in tickler_sheets.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        # Format Excel file
        output_to_excel_multiple_sheets.format_excel_file(tickler_output_path)
    
    print(f"CT Dashboard processing complete. Output files saved to: {src.config.OUTPUT_DIR}")