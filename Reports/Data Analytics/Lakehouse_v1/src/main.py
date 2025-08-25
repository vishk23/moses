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
from deltalake import write_deltalake


def main():
    print(f"Running {src._version.__version__}")
    print(f"Running {src.config.REPORT_NAME} for {src.config.BUSINESS_LINE}")
    print(f"Schedule: {src.config.SCHEDULE}")
    print(f"Owner: {src.config.OWNER}")
    print(f"Environment: {src.config.ENV}")
    # Add your main project logic here
    # Example: print('Hello, world!')

    # DB -> silver
    ## Daily Acccount Table
    df = cdutils.acct_file_creation.core.query_df_on_date()

    src.config.ACCOUNT_TABLE.mkdir(parents=True, exist_ok=True)
    write_deltalake(str(src.config.ACCOUNT_TABLE), df, mode='overwrite', schema_mode='merge')
    print("Successfully wrote account data")

if __name__ == "__main__":
    main()