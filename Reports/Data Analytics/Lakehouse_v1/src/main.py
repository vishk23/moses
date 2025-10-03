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
import src.bronze.core
import src.silver.core


def main():
    print(f"Running {src._version.__version__}")
    print(f"Running {src.config.REPORT_NAME} for {src.config.BUSINESS_LINE}")
    print(f"Schedule: {src.config.SCHEDULE}")
    print(f"Owner: {src.config.OWNER}")
    print(f"Environment: {src.config.ENV}")

    # # == Bronze ==
    # src.config.BRONZE.mkdir(parents=True, exist_ok=True)
    # src.bronze.core.generate_bronze_tables()

    # == Silver ==
    src.config.SILVER.mkdir(parents=True, exist_ok=True)
    src.silver.core.generate_silver_tables()

    # == Gold ==

if __name__ == "__main__":
    main()