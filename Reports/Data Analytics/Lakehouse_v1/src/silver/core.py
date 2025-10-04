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
import src.silver.customer_address_link.core
from src.utils.parquet_io import add_load_timestamp
import cdutils.orig_face_amt.core # type: ignore
import cdutils.customer_dim # type: ignore

def generate_silver_tables():
    # Account
    print("Start account")
    ACCOUNT_PATH = src.config.SILVER / "account"
    ACCOUNT_PATH.mkdir(parents=True, exist_ok=True)

    df = cdutils.acct_file_creation.core.query_df_on_date()
    # Pull in Active Accounts (create a clean customer_id for joining)
    # This is only build like this to provide compatability with exisiting reports
    # built on this table that join directly to taxrptfororgnbr and taxrptforpersnbr
    accts = df.copy()
    accts = cdutils.customer_dim.orgify(accts, 'taxrptfororgnbr')
    accts = accts.rename(columns={'customer_id':'org_id'}).copy()
    accts = cdutils.customer_dim.persify(accts, 'taxrptforpersnbr')
    accts['customer_id'] = accts['customer_id'].fillna(accts['org_id'])
    accts = accts[[
        'acctnbr',
        'customer_id'
    ]].copy()
    df = df.merge(accts, on='acctnbr', how='left')
    
    # Add macro type, Loan/Deposit/Other
    MACRO_TYPE_MAPPING = {
        'CML':'Loan',
        'MLN':'Loan',
        'CNS':'Loan',
        'MTG':'Loan',
        'CK':'Deposit',
        'SAV':'Deposit',
        'TD':'Deposit'
    }
    df['Macro Account Type'] = df['mjaccttypcd'].map(MACRO_TYPE_MAPPING).fillna('Other')
    
    # Set ACH manager products to other, they don't count as loans
    df.loc[df['currmiaccttypcd'] == 'CI07', 'Macro Account Type'] = 'Other'

    df = add_load_timestamp(df)

    write_deltalake(ACCOUNT_PATH, df, mode='overwrite', schema_mode='overwrite')
    print("Successfully wrote account data")

    

    # Address
    print("Starting address ...")
    ADDRESS_PATH = src.config.SILVER / "address"
    ADDRESS_PATH.mkdir(parents=True, exist_ok=True)

    df = src.silver.address.generate_address()
    df = add_load_timestamp(df)

    write_deltalake(ADDRESS_PATH, df, mode='overwrite', schema_mode='merge')
    print("Successfully wrote address data")

    # Property
    print("Starting property ...")
    PROPERTY_PATH = src.config.SILVER / "property"
    PROPERTY_PATH.mkdir(parents=True, exist_ok=True)
    ACCT_PROP_LINK_PATH = src.config.SILVER / "account_property_link"
    ACCT_PROP_LINK_PATH.mkdir(parents=True, exist_ok=True)

    acct_prop_link, property = src.silver.property.create_silver_prop_tables()

    ## Handle null columns
    property = src.utils.parquet_io.cast_all_null_columns_to_string(property)
    acct_prop_link = src.utils.parquet_io.cast_all_null_columns_to_string(acct_prop_link)
    
    property = add_load_timestamp(property)
    acct_prop_link = add_load_timestamp(acct_prop_link)
    
    write_deltalake(PROPERTY_PATH, property, mode='overwrite', schema_mode='merge')
    write_deltalake(ACCT_PROP_LINK_PATH, acct_prop_link, mode='overwrite', schema_mode='merge')
    print("Successfully wrote property data")

    # Insurance 
    print("Starting property ...")
    INSURANCE_PATH = src.config.SILVER / "insurance"
    INSURANCE_PATH.mkdir(parents=True, exist_ok=True)
    ACCT_PROP_INS_LINK_PATH = src.config.SILVER / "acct_prop_ins_link"
    ACCT_PROP_INS_LINK_PATH.mkdir(parents=True, exist_ok=True)

    insurance, acct_prop_ins_link = src.silver.insurance.generate_insurance_table()
    
    insurance = add_load_timestamp(insurance)
    acct_prop_ins_link = add_load_timestamp(acct_prop_ins_link)
    
    write_deltalake(INSURANCE_PATH, insurance, mode='overwrite', schema_mode='merge')
    write_deltalake(ACCT_PROP_INS_LINK_PATH, acct_prop_ins_link, mode='overwrite', schema_mode='merge')
    print("Successfully wrote insurance data")

    # Face Value
    print("Starting face value table generation ...")
    FACE_VALUE_PATH = src.config.SILVER / "face_value"
    FACE_VALUE_PATH.mkdir(parents=True, exist_ok=True)

    face_value = cdutils.orig_face_amt.core.query_orig_face_amt()
    
    face_value = add_load_timestamp(face_value)
    
    write_deltalake(FACE_VALUE_PATH, face_value, mode='overwrite', schema_mode='merge')
    print("Successfully wrote orig face value data")

    # Customer Dim 
    print("Starting customer dim (base) table generation ...")
    BASE_CUSTOMER_DIM = src.config.SILVER / "base_customer_dim"
    BASE_CUSTOMER_DIM.mkdir(parents=True, exist_ok=True)

    base_customer_dim = src.silver.customer_dim.core.generate_base_customer_dim_table()    
    base_customer_dim = add_load_timestamp(base_customer_dim)
    
    write_deltalake(BASE_CUSTOMER_DIM, base_customer_dim, mode='overwrite', schema_mode='overwrite')
    print("Successfully wrote base customer dim")

    # Customer Address Link 
    print("Starting customer address link table generation ...")
    CUSTOMER_ADDRESS_LINK = src.config.SILVER / "customer_address_link"
    CUSTOMER_ADDRESS_LINK.mkdir(parents=True, exist_ok=True)

    customer_address_link = src.silver.customer_address_link.core.generate_customer_address_link()    
    customer_address_link = add_load_timestamp(customer_address_link)
    
    write_deltalake(CUSTOMER_ADDRESS_LINK, customer_address_link, mode='overwrite', schema_mode='overwrite')
    print("Successfully wrote customer address link")

    # Pers Dim
    print("Starting pers dim table generation ...")
    PERS_DIM = src.config.SILVER / "pers_dim"
    PERS_DIM.mkdir(parents=True, exist_ok=True)

    pers_dim = src.silver.customer_dim.core.generate_pers_dim()    
    pers_dim = add_load_timestamp(pers_dim)
    
    write_deltalake(PERS_DIM, pers_dim, mode='overwrite', schema_mode='overwrite')
    print("Successfully wrote pers dim")

    # Org Dim
    print("Starting org dim table generation ...")
    ORG_DIM = src.config.SILVER / "org_dim"
    ORG_DIM.mkdir(parents=True, exist_ok=True)

    org_dim = src.silver.customer_dim.core.generate_org_dim()    
    org_dim = add_load_timestamp(org_dim)
    
    write_deltalake(ORG_DIM, org_dim, mode='overwrite', schema_mode='overwrite')
    print("Successfully wrote org dim")
