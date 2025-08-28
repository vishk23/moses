import src.config
import cdutils.acct_file_creation.core # type: ignore
from datetime import datetime
import pandas as pd
from pathlib import Path
from deltalake import write_deltalake
import src.silver.address
import src.silver.property
import src.utils.parquet_io

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

    # Property
    print("Starting property ...")
    PROPERTY_PATH = src.config.SILVER / "property"
    PROPERTY_PATH.mkdir(parents=True, exist_ok=True)
    ACCT_PROP_LINK_PATH = src.config.SILVER / "account_property_link"
    ACCT_PROP_LINK_PATH.mkdir(parents=True, exist_ok=True)

    acct_prop_link, property = src.silver.property.create_silver_prop_tables()

    # Handle null columns
    property = src.utils.parquet_io.cast_all_null_columns_to_string(property)
    acct_prop_link = src.utils.parquet_io.cast_all_null_columns_to_string(acct_prop_link)
    
    write_deltalake(PROPERTY_PATH, property, mode='overwrite', schema_mode='merge')
    write_deltalake(ACCT_PROP_LINK_PATH, acct_prop_link, mode='overwrite', schema_mode='merge')
    print("Successfully wrote property data")
