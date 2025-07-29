#!/usr/bin/env python3
"""
Main script for data quality ETL pipeline.
Chains together functions to create consolidated org_final and pers_final dataframes.
Run with: python -m src.main
"""

import pandas as pd
from pathlib import Path
import sys
from datetime import datetime
import os

import src.data_quality.core
import src.data_quality.fetch_data # type: ignore
import cdutils.acct_file_creation.core # type: ignore
import src.config as config

def create_acct_df():
    """
    This is a blackbox function that returns the active accounts snapshot.
    """
    return cdutils.acct_file_creation.core.query_df_on_date()

def load_database_tables():
    """
    In production, this would connect to the database and load the required tables.
    """
    return src.data_quality.fetch_data.fetch_data()

def create_org_final(data, acct_df):
    """
    Create the final organization dataframe with addresses, filtered to active accounts.
    
    Args:
        data: Dictionary containing database tables (wh_org, orgaddruse, wh_addr, wh_allroles, vieworgtaxid)
        acct_df: DataFrame with active account numbers
        
    Returns:
        DataFrame: Final organization data with addresses, filtered to active accounts
    """
    print("Creating org_final dataframe...")
    
    # Step 0: Update organization tax information with view table if available
    wh_org_updated = data['wh_org']
    if 'vieworgtaxid' in data and data['vieworgtaxid'] is not None:
        print("  Step 0: Updating tax information from VIEWORGTAXID...")
        wh_org_updated = src.data_quality.core.merge_org_with_view_taxid(
            data['wh_org'], 
            data['vieworgtaxid']
        )
    else:
        print("  Step 0: No VIEWORGTAXID table found, skipping tax updates...")
    
    # Step 1: Create organization table with addresses
    print("  Step 1: Merging WH_ORG with addresses...")
    org_with_address = src.data_quality.core.create_org_table_with_address(
        wh_org_updated, 
        data['orgaddruse'], 
        data['wh_addr']
    )
    print(f"    Organizations with addresses: {len(org_with_address):,} records")
    
    # Step 2: Filter to only organizations linked to active accounts
    print("  Step 2: Filtering to active accounts...")
    org_final = src.data_quality.core.filter_to_active_accounts(
        acct_df, 
        data['wh_allroles'], 
        org_with_address=org_with_address
    )
    print(f"    Final organizations: {len(org_final):,} records")
    
    return org_final

def create_pers_final(data, acct_df):
    """
    Create the final person dataframe with addresses, filtered to active accounts.
    
    Args:
        data: Dictionary containing database tables (wh_pers, persaddruse, wh_addr, wh_allroles, viewperstaxid)
        acct_df: DataFrame with active account numbers
        
    Returns:
        DataFrame: Final person data with addresses, filtered to active accounts
    """
    print("Creating pers_final dataframe...")
    
    # Step 0: Update person tax information with view table if available
    wh_pers_updated = data['wh_pers']
    if 'viewperstaxid' in data and data['viewperstaxid'] is not None:
        print("  Step 0: Updating tax information from VIEWPERSTAXID...")
        wh_pers_updated = src.data_quality.core.merge_pers_with_view_taxid(
            data['wh_pers'], 
            data['viewperstaxid']
        )
    else:
        print("  Step 0: No VIEWPERSTAXID table found, skipping tax updates...")
    
    # Step 1: Create person table with addresses
    print("  Step 1: Merging WH_PERS with addresses...")
    pers_with_address = src.data_quality.core.create_pers_table_with_address(
        wh_pers_updated, 
        data['persaddruse'], 
        data['wh_addr']
    )
    print(f"    Persons with addresses: {len(pers_with_address):,} records")
    
    # Step 2: Filter to only persons linked to active accounts
    print("  Step 2: Filtering to active accounts...")
    pers_final = src.data_quality.core.filter_to_active_accounts(
        acct_df, 
        data['wh_allroles'], 
        pers_with_address=pers_with_address
    )
    print(f"    Final persons: {len(pers_final):,} records")
    
    return pers_final

def main():
    """
    Main entry point for the data quality ETL pipeline.
    """
    # Ensure all necessary directories exist (moved from config.py)
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    config.INPUT_DIR.mkdir(parents=True, exist_ok=True)
    config.ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    (config.INPUT_DIR / "org").mkdir(parents=True, exist_ok=True)
    (config.INPUT_DIR / "pers").mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("Data Quality ETL Pipeline - Customer Data Consolidation")
    print("=" * 60)
    
    # Environment information
    env_msg = "PRODUCTION" if config.ENV == 'prod' else "DEVELOPMENT"
    print(f"🌐 Environment: {env_msg}")
    print(f"📁 Output Directory: {config.OUTPUT_DIR}")
    print(f"📥 Input Directory: {config.INPUT_DIR}")
    if config.ENV == 'prod':
        print(f"📋 Production Path: {config.PROD_OUTPUT_PATH}")
    print()
    
    try:
        # Load required data once upfront
        print("Loading database tables...")
        data = load_database_tables()
        
        print("Creating active accounts dataframe...")
        acct_df = create_acct_df()
        
        # Create final dataframes using the loaded data
        org_final = create_org_final(data, acct_df)
        pers_final = create_pers_final(data, acct_df)
        
        # Check for input files to merge with Janet's data
        print("\n" + "-" * 40)
        print("CHECKING FOR INPUT FILES")
        print("-" * 40)
        
        # Use config paths for input files
        org_input_dir = config.INPUT_DIR / "org"
        pers_input_dir = config.INPUT_DIR / "pers"
        
        # Note: process_input_files() may need to be updated to accept these paths
        # For now, temporarily change to the input directory
        original_cwd = Path.cwd()
        try:
            # Change to the input directory's parent if it exists
            if config.INPUT_DIR.exists():
                os.chdir(config.INPUT_DIR.parent)
            
            input_status = src.data_quality.core.process_input_files()
        finally:
            os.chdir(original_cwd)
        
        # Merge with org input file if it exists
        if input_status['has_org_input']:
            print("\nMerging org data with input file...")
            org_final = src.data_quality.core.merge_with_input_file(
                org_final, org_input_dir, "org"
            )
            # Archive the processed file
            print("Archiving org input file...")
            src.data_quality.core.archive_input_file(org_input_dir, "org")
        
        # Merge with pers input file if it exists
        if input_status['has_pers_input']:
            print("\nMerging pers data with input file...")
            pers_final = src.data_quality.core.merge_with_input_file(
                pers_final, pers_input_dir, "pers"
            )
            # Archive the processed file
            print("Archiving pers input file...")
            src.data_quality.core.archive_input_file(pers_input_dir, "pers")
        
        # Summary statistics
        print("\n" + "=" * 40)
        print("PIPELINE SUMMARY")
        print("=" * 40)
        print(f"Organizations processed: {len(org_final):,}")
        print(f"Persons processed: {len(pers_final):,}")
        print(f"Total customer records: {len(org_final) + len(pers_final):,}")
        
        # Column information
        print(f"\nOrganization columns: {len(org_final.columns)} fields")
        print(f"Person columns: {len(pers_final.columns)} fields")
        
        # Save to outputs directory using config
        print(f"\nSaving results to {config.OUTPUT_DIR}/...")
        config.OUTPUT_DIR.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        org_final.to_excel(config.OUTPUT_DIR / f"org_final_{timestamp}.xlsx", index=False)
        pers_final.to_excel(config.OUTPUT_DIR / f"pers_final_{timestamp}.xlsx", index=False)
        
        # In production mode, also save without timestamp for automated access
        if config.ENV == 'prod':
            org_final.to_excel(config.OUTPUT_DIR / "org_final_latest.xlsx", index=False)
            pers_final.to_excel(config.OUTPUT_DIR / "pers_final_latest.xlsx", index=False)
            print("Also saved latest versions without timestamp for automated access.")
        
        print("✅ Pipeline completed successfully!")
        
        # Environment status
        env_msg = "PRODUCTION" if config.ENV == 'prod' else "DEVELOPMENT"
        print(f"📍 Running in {env_msg} mode")
        print(f"📁 Output location: {config.OUTPUT_DIR}")
        
        return org_final, pers_final
        
    except NotImplementedError as e:
        print(f"❌ Implementation needed: {e}")
        print("\nNext steps:")
        print("1. Implement create_acct_df() function")
        print("2. Implement load_database_tables() function")
        print("3. Configure database connections")
        sys.exit(1)
        
    except ValueError as e:
        if "dtype mismatch" in str(e):
            print(f"❌ Data type mismatch error: {e}")
            print("\nThis error has been fixed with automatic type conversion.")
            print("Please try running the pipeline again.")
        else:
            print(f"❌ Data validation error: {e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Pipeline failed: {e}")
        import traceback
        print("\nFull error details:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()