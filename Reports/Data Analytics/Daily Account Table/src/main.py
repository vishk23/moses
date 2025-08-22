"""
Main entry point for your project.

Replace this docstring with a description of your project's purpose and logic.
"""

import src.config
import src._version
import cdutils.acct_file_creation.core # type: ignore
from datetime import datetime
import pandas as pd
from pathlib import Path

def main():
    print(f"Running {src._version.__version__}")
    print(f"Running {src.config.REPORT_NAME} for {src.config.BUSINESS_LINE}")
    print(f"Schedule: {src.config.SCHEDULE}")
    print(f"Owner: {src.config.OWNER}")
    print(f"Environment: {src.config.ENV}")
    print(f"Output directory: {src.config.OUTPUT_DIR}")
    # Add your main project logic here
    # Example: print('Hello, world!')
    df = cdutils.acct_file_creation.core.query_df_on_date()

    src.config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    filename = "daily_account_table.parquet"
    OUTPUT_PATH = src.config.OUTPUT_DIR / filename
    
    df.to_parquet(OUTPUT_PATH, index=False)
    print("Complete!")

if __name__ == "__main__":
    main()