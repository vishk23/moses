"""
CRE Reporting Board - Main Entry Point

This script generates the CRE (Commercial Real Estate) loader data for board reporting.
It fetches loan portfolio data from COCC data mart, performs transformations, 
and creates consolidated reporting output.

Output: cre_loader.xlsx - Consolidated CRE portfolio data with property information
"""

import src.config
from src.cre_board_reporting.core import run_cre_reporting_pipeline
from src._version import __version__

def main():
    print(f"Starting {src.config.REPORT_NAME} [{__version__}]")
    print(f"Business Line: {src.config.BUSINESS_LINE}")
    print(f"Schedule: {src.config.SCHEDULE}")
    print(f"Owner: {src.config.OWNER}")
    print(f"Environment: {src.config.ENV}")
    print(f"Output directory: {src.config.OUTPUT_DIR}")
    print("-" * 50)
    
    try:
        # Run the CRE reporting pipeline
        output_path = run_cre_reporting_pipeline()
        
        print("-" * 50)
        print("CRE Reporting Board processing completed successfully!")
        print(f"Output file: {output_path}")
        
        # TODO: Add email distribution logic here if needed in production
        # if src.config.ENV == 'prod' and src.config.EMAIL_TO:
        #     send_email_with_attachment(output_path)
        
    except Exception as e:
        print(f"Error in CRE Reporting Board processing: {str(e)}")
        raise

if __name__ == "__main__":
    main()