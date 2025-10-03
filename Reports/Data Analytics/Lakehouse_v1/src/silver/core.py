import src.config
import cdutils.acct_file_creation.core # type: ignore
from datetime import datetime
import pandas as pd
from pathlib import Path
from deltalake import write_deltalake
import src.silver.address
import src.silver.property
import src.utils.parquet_io
import src.silver.insurance
import src.silver.customer_dim.core
from src.utils.parquet_io import add_load_timestamp
import cdutils.orig_face_amt.core # type: ignore

def generate_silver_tables():
    # # Account
    # print("Start account")
    # ACCOUNT_PATH = src.config.SILVER / "account"
    # ACCOUNT_PATH.mkdir(parents=True, exist_ok=True)

    # df = cdutils.acct_file_creation.core.query_df_on_date()
    # df = add_load_timestamp(df)

    # write_deltalake(ACCOUNT_PATH, df, mode='overwrite', schema_mode='merge')
    # print("Successfully wrote account data")

    # # Address
    # print("Starting address ...")
    # ADDRESS_PATH = src.config.SILVER / "address"
    # ADDRESS_PATH.mkdir(parents=True, exist_ok=True)

    # df = src.silver.address.generate_address()
    # df = add_load_timestamp(df)

    # write_deltalake(ADDRESS_PATH, df, mode='overwrite', schema_mode='merge')
    # print("Successfully wrote address data")

    # # Property
    # print("Starting property ...")
    # PROPERTY_PATH = src.config.SILVER / "property"
    # PROPERTY_PATH.mkdir(parents=True, exist_ok=True)
    # ACCT_PROP_LINK_PATH = src.config.SILVER / "account_property_link"
    # ACCT_PROP_LINK_PATH.mkdir(parents=True, exist_ok=True)

    # acct_prop_link, property = src.silver.property.create_silver_prop_tables()

    # ## Handle null columns
    # property = src.utils.parquet_io.cast_all_null_columns_to_string(property)
    # acct_prop_link = src.utils.parquet_io.cast_all_null_columns_to_string(acct_prop_link)
    
    # property = add_load_timestamp(property)
    # acct_prop_link = add_load_timestamp(acct_prop_link)
    
    # write_deltalake(PROPERTY_PATH, property, mode='overwrite', schema_mode='merge')
    # write_deltalake(ACCT_PROP_LINK_PATH, acct_prop_link, mode='overwrite', schema_mode='merge')
    # print("Successfully wrote property data")

    # # Insurance 
    # print("Starting property ...")
    # INSURANCE_PATH = src.config.SILVER / "insurance"
    # INSURANCE_PATH.mkdir(parents=True, exist_ok=True)
    # ACCT_PROP_INS_LINK_PATH = src.config.SILVER / "acct_prop_ins_link"
    # ACCT_PROP_INS_LINK_PATH.mkdir(parents=True, exist_ok=True)

    # insurance, acct_prop_ins_link = src.silver.insurance.generate_insurance_table()
    
    # insurance = add_load_timestamp(insurance)
    # acct_prop_ins_link = add_load_timestamp(acct_prop_ins_link)
    
    # write_deltalake(INSURANCE_PATH, insurance, mode='overwrite', schema_mode='merge')
    # write_deltalake(ACCT_PROP_INS_LINK_PATH, acct_prop_ins_link, mode='overwrite', schema_mode='merge')
    # print("Successfully wrote insurance data")

    # # Face Value
    # print("Starting face value table generation ...")
    # FACE_VALUE_PATH = src.config.SILVER / "face_value"
    # FACE_VALUE_PATH.mkdir(parents=True, exist_ok=True)

    # face_value = cdutils.orig_face_amt.core.query_orig_face_amt()
    
    # face_value = add_load_timestamp(face_value)
    
    # write_deltalake(FACE_VALUE_PATH, face_value, mode='overwrite', schema_mode='merge')
    # print("Successfully wrote orig face value data")

    # Customer Dim 
    print("Starting face value table generation ...")
    BASE_CUSTOMER_DIM = src.config.SILVER / "base_customer_dim"
    BASE_CUSTOMER_DIM.mkdir(parents=True, exist_ok=True)

    base_customer_dim = src.silver.customer_dim.core.generate_base_customer_dim_table()    
    base_customer_dim = add_load_timestamp(base_customer_dim)
    
    write_deltalake(BASE_CUSTOMER_DIM, base_customer_dim, mode='overwrite', schema_mode='overwrite')
    print("Successfully wrote base customer dim")