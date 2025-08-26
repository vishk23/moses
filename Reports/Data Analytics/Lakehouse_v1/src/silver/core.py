import src.config
import cdutils.acct_file_creation.core # type: ignore
from datetime import datetime
import pandas as pd
from pathlib import Path
from deltalake import write_deltalake
import src.bronze.fetch_data
import src.silver.address

def generate_silver_tables():
    # Account
    print("Start account")
    ACCOUNT_PATH = src.config.SILVER / "account"
    ACCOUNT_PATH.mkdir(parents=True, exist_ok=True)

    df = cdutils.acct_file_creation.core.query_df_on_date()

    write_deltalake(ACCOUNT_PATH, df, mode='overwrite', schema_mode='merge')
    print("Successfully wrote account data")

    # Address
    print("Starting address ...")
    ADDRESS_PATH = src.config.SILVER / "address"
    ADDRESS_PATH.mkdir(parents=True, exist_ok=True)

    df = src.silver.address.generate_address()

    write_deltalake(ADDRESS_PATH, df, mode='overwrite', schema_mode='merge')
    print("Successfully wrote address data")


