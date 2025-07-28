"""
R360 Customer Relationship Keys - Main Entry Point

BUSINESS LOGIC EXTRACTED:

Data Sources & Relationships:
- fetch_data(): Pulls account common, address, and ownership data from OSIBANK warehouse tables
- Creates three distinct relationship key types for different business use cases

Business Rules:
- Portfolio Key = Groups by address OR ownership (comprehensive customer relationships)
- Address Key = Groups by address only (household analysis) 
- Ownership Key = Groups by ownership only (business concentration analysis)
- Uses Union-Find algorithm for efficient grouping of large datasets
- Maintains key persistence across daily runs using historical SQLite databases

Data Processing Flow:
1. Fetch account, address, and ownership data from multiple warehouse tables
2. Apply data cleaning and create hash keys for address and ownership
3. Use Union-Find algorithm to group accounts by specified criteria
4. Assign persistent keys using historical data
5. Store results in SQLite databases for downstream consumption
6. Output CSV files for debugging and validation

Key Business Information:
- Daily automated process feeding customer analytics across all business lines
- Enables 360-degree customer view for retail, commercial, and marketing teams
- Critical infrastructure for concentration of credit analysis and household insights
"""

from pathlib import Path
from datetime import datetime

import src.r360
import src.config
from src._version import __version__


def main():
    """Main report execution function"""
    print(f"Starting R360 Customer Relationship Keys [{__version__}]")
    print(f"Environment: {src.config.ENV.upper()} | Database Mode: {src.config.DATABASE_MODE}")
    
    # Show dev mode warnings if applicable
    if src.config.DEV_WARNINGS:
        print("\n" + "="*60)
        for warning in src.config.DEV_WARNINGS:
            print(warning)
        print("="*60 + "\n")
    
    # Show historical database configuration
    print("Historical Database Configuration:")
    for key_type, setting in src.config.HISTORICAL_DB_CONFIG.items():
        explanation = src.config.HISTORICAL_DB_HELP[setting]
        print(f"  {key_type.title()}: {setting} - {explanation}")
    print()
    
    # Create output directory
    src.config.OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Use configuration from config.py
    keys_to_generate = src.config.KEYS_TO_GENERATE
    output_config = src.config.OUTPUT_CONFIG
    historical_config = src.config.HISTORICAL_DB_CONFIG
    
    results = {}
    
    # Generate Portfolio Key (address OR ownership grouping)
    if keys_to_generate['portfolio']:
        print("\n=== Generating Portfolio Key (Address OR Ownership) ===")
        
        # Show historical database setting for this key type
        hist_setting = historical_config['portfolio']
        print(f"Historical DB Setting: {hist_setting} - {src.config.HISTORICAL_DB_HELP[hist_setting]}")
        
        # Pass database save setting (historical setting will be handled within the function based on config)
        portfolio_df = src.r360.portfolio_key(save_to_db=output_config['save_to_database'])
        results['portfolio'] = portfolio_df
        
        # Save detailed output
        if output_config['save_to_csv']:
            curr_date = datetime.now().strftime('%Y%m%d')
            output_file = src.config.OUTPUT_DIR / f"r360_portfolio_{curr_date}.csv"
            portfolio_df.to_csv(output_file, index=False)
            print(f"Portfolio key saved: {output_file}")
        
        if output_config['print_stats']:
            print(f"Total accounts: {len(portfolio_df):,}")
            print(f"Unique portfolio keys: {portfolio_df['portfolio_key'].nunique():,}")
        
        if output_config['save_to_database']:
            print("Portfolio keys saved to current.db")
        else:
            print("Portfolio keys NOT saved to database (dev mode safety)")

    # Generate Address Key (address only grouping)  
    if keys_to_generate['address']:
        print("\n=== Generating Address Key (Address Only) ===")
        
        # Show historical database setting for this key type
        hist_setting = historical_config['address']
        print(f"Historical DB Setting: {hist_setting} - {src.config.HISTORICAL_DB_HELP[hist_setting]}")
        
        # Pass database save setting (historical setting will be handled within the function based on config)
        address_df = src.r360.address_key(save_to_db=output_config['save_to_database'])
        results['address'] = address_df
        
        # Save detailed output
        if output_config['save_to_csv']:
            curr_date = datetime.now().strftime('%Y%m%d')
            output_file = src.config.OUTPUT_DIR / f"r360_address_{curr_date}.csv"
            address_df.to_csv(output_file, index=False)
            print(f"Address key saved: {output_file}")
        
        if output_config['print_stats']:
            print(f"Total accounts: {len(address_df):,}")
            print(f"Unique address keys: {address_df['portfolio_key'].nunique():,}")
        
        if output_config['save_to_database']:
            print("Address keys saved to address.db")
        else:
            print("Address keys NOT saved to database (dev mode safety)")

    # Generate Ownership Key (ownership only grouping)
    if keys_to_generate['ownership']:
        print("\n=== Generating Ownership Key (Ownership Only) ===")
        
        # Show historical database setting for this key type
        hist_setting = historical_config['ownership']
        print(f"Historical DB Setting: {hist_setting} - {src.config.HISTORICAL_DB_HELP[hist_setting]}")
        
        # Pass database save setting (historical setting will be handled within the function based on config)
        ownership_df = src.r360.ownership_key(save_to_db=output_config['save_to_database'])
        results['ownership'] = ownership_df
        
        # Save detailed output  
        if output_config['save_to_csv']:
            curr_date = datetime.now().strftime('%Y%m%d')
            output_file = src.config.OUTPUT_DIR / f"r360_ownership_{curr_date}.csv"
            ownership_df.to_csv(output_file, index=False)
            print(f"Ownership key saved: {output_file}")
        
        if output_config['print_stats']:
            print(f"Total accounts: {len(ownership_df):,}")
            print(f"Unique ownership keys: {ownership_df['portfolio_key'].nunique():,}")
        
        if output_config['save_to_database']:
            print("Ownership keys saved to ownership.db")
        else:
            print("Ownership keys NOT saved to database (dev mode safety)")
    
    print(f"\n=== R360 Processing Complete ===")
    print(f"Generated {len(results)} key type(s)")
    print(f"Environment: {src.config.ENV.upper()} | Database Operations: {'Enabled' if output_config['save_to_database'] else 'Disabled'}")
    
    if output_config['save_to_database']:
        print("Keys are stored in respective SQLite databases and available via cdutils")
    else:
        print("Keys were NOT saved to databases (dev mode safety - CSV files only)")
    
    return results


if __name__ == '__main__':
    main()





