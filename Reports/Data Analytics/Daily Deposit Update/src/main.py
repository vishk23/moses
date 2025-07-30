"""
Main entry point for Daily Deposit Update project.

This script loads configuration from config.py and runs the main pipeline.
"""

import src.config
import src.deposit_file
import src.output_to_excel
from src._version import __version__

def main():
    print(f"Running {src.config.REPORT_NAME} for {src.config.BUSINESS_LINE}")
    print(f"Schedule: {src.config.SCHEDULE}")
    print(f"Owner: {src.config.OWNER}")
    print(f"Environment: {src.config.ENV}")
    print(f"Output directory: {src.config.OUTPUT_DIR}")
    print(f"Version: {__version__}")

    # Core transformation pipeline
    raw_data, daily_deposit_drop_in = src.deposit_file.deposit_dataset_execution()

    # Output to excel (raw_data -> Staging)
    staging_path = src.config.STAGING_OUTPUT_DIR / "DailyDeposit_staging.xlsx"
    raw_data.to_excel(staging_path, sheet_name='Sheet1', index=False)
    # Output to excel (for the drop-in file)
    dropin_path = src.config.OUTPUT_DIR / "DailyDeposit.xlsx"
    daily_deposit_drop_in.to_excel(dropin_path, sheet_name='Sheet1', index=False)

    # Format excel
    src.output_to_excel.format_excel_file(dropin_path)

    # Optionally, copy to production drop-in location if in prod
    if src.config.ENV == 'prod':
        try:
            prod_dropin = src.config.BASE_PATH / "DailyDeposit.xlsx"
            dropin_path.replace(prod_dropin)
            print(f"Wrote drop-in file to {prod_dropin}")
        except Exception as e:
            print(f"Error replacing to drop-in location: {e}")

if __name__ == '__main__':
    print(f"Starting [{__version__}]")
    main()
    print("Complete!")

