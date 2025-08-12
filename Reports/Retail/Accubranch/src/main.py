"""
Main entry point for Accubranch Analysis project.

This module orchestrates the generation of both account data and transaction data
for AccuBranch analysis. It can be run as a module: python -m src.main

The process includes:
1. Account data processing and 5-year historical analysis
2. Transaction data processing for specified date windows
3. Output generation to CSV files
"""
import sys
import os
from pathlib import Path

# Add project root to sys.path for imports
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Change to project root directory
os.chdir(project_root)

import src.config as config
import src._version as version
import src.accubranch.core as accubranch_core
import src.transactions.core as transaction_core


def main():
    """
    Main execution function for Accubranch analysis.
    """
    print(f"Starting {config.REPORT_NAME}")
    print(f"Version: {version.__version__}")
    print(f"Environment: {config.ENVIRONMENT}")
    print(f"Business Line: {config.BUSINESS_LINE}")
    print(f"Schedule: {config.SCHEDULE}")
    print(f"Owner: {config.OWNER}")
    print(f"Working directory: {os.getcwd()}")
    print(f"Output directory: {config.OUTPUT_DIR}")
    print("-" * 50)
    
    try:
        # Process account data and historical analysis
        print("Processing account data...")
        accubranch_core.process_account_data()
        print("✓ Account data processing completed")
        
        # Process transaction data
        print("Processing transaction data...")
        transaction_core.process_transaction_data()
        print("✓ Transaction data processing completed")
        
        print("-" * 50)
        print("Accubranch analysis completed successfully!")
        print(f"Output files generated:")
        print(f"  - {config.ACCOUNT_OUTPUT_FILE}")
        print(f"  - {config.TRANSACTION_OUTPUT_FILE}")
        print(f"  - {config.FIVE_YR_HISTORY_FILE}")
        
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
