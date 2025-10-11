import src.config
import cdutils.acct_file_creation.core # type: ignore
from datetime import datetime
import pandas as pd
from pathlib import Path
from deltalake import write_deltalake
from src.utils.parquet_io import add_load_timestamp, cast_all_null_columns_to_string
import src.bronze.fetch_data

def generate_bronze_tables():

    print("Start bronze table generation") 

    # wh_addr (address) ========================

    WH_ADDR_PATH = src.config.BRONZE / "wh_addr"
    WH_ADDR_PATH.mkdir(parents=True, exist_ok=True)

    data = src.bronze.fetch_data.fetch_wh_addr()
    wh_addr = data['wh_addr'].copy()
    wh_addr = add_load_timestamp(wh_addr)

    write_deltalake(WH_ADDR_PATH, wh_addr, mode='overwrite', schema_mode='merge')

    # wh_allroles ========================
    WH_ALLROLES_PATH = src.config.BRONZE / "wh_allroles"
    WH_ALLROLES_PATH.mkdir(parents=True, exist_ok=True)

    data = src.bronze.fetch_data.fetch_wh_allroles()
    wh_allroles = data['wh_allroles'].copy()
    wh_allroles = add_load_timestamp(wh_allroles)

    write_deltalake(WH_ALLROLES_PATH, wh_allroles, mode='overwrite', schema_mode='merge')

    # Org/Pers ========================
    WH_ORG_PATH = src.config.BRONZE / "wh_org"
    WH_ORG_PATH.mkdir(parents=True, exist_ok=True)
    WH_PERS_PATH = src.config.BRONZE / "wh_pers"
    WH_PERS_PATH.mkdir(parents=True, exist_ok=True)

    data = src.bronze.fetch_data.fetch_org_pers()
    wh_org = data['wh_org'].copy()
    wh_pers = data['wh_pers'].copy()
    wh_org = add_load_timestamp(wh_org)
    wh_pers = add_load_timestamp(wh_pers)

    write_deltalake(WH_ORG_PATH, wh_org, mode='overwrite', schema_mode='merge')
    write_deltalake(WH_PERS_PATH, wh_pers, mode='overwrite', schema_mode='merge')

    # DB Metadata Lookup ======================== 
    METADATA_PATH1 = src.config.BRONZE / "metadata_lookup_engine1"
    METADATA_PATH1.mkdir(parents=True, exist_ok=True)
    METADATA_PATH2 = src.config.BRONZE / "metadata_lookup_engine2"
    METADATA_PATH2.mkdir(parents=True, exist_ok=True)

    data = src.bronze.fetch_data.fetch_db_metadata()
    lookup_df1 = data['lookup_df1'].copy()
    lookup_df2 = data['lookup_df2'].copy()

    lookup_df1 = lookup_df1[[
        'owner',
        'table_name',
        'column_name',
        'data_type'
    ]].copy()

    lookup_df2 = lookup_df2[[
        'owner',
        'table_name',
        'column_name',
        'data_type'
    ]].copy()

    lookup_df1 = add_load_timestamp(lookup_df1)
    lookup_df1 = add_load_timestamp(lookup_df1)

    write_deltalake(METADATA_PATH1, lookup_df1, mode='overwrite', schema_mode='merge')
    write_deltalake(METADATA_PATH2, lookup_df2, mode='overwrite', schema_mode='merge')


    # Property ========================
    WH_PROP_PATH = src.config.BRONZE / "wh_prop"
    WH_PROP_PATH.mkdir(parents=True, exist_ok=True)
    WH_PROP2_PATH = src.config.BRONZE / "wh_prop2"
    WH_PROP2_PATH.mkdir(parents=True, exist_ok=True)

    data = src.bronze.fetch_data.fetch_prop()
    wh_prop = data['wh_prop'].copy()
    wh_prop2 = data['wh_prop2'].copy()

    wh_prop = cast_all_null_columns_to_string(wh_prop)
    wh_prop2 = cast_all_null_columns_to_string(wh_prop2)

    wh_prop = add_load_timestamp(wh_prop)
    wh_prop2 = add_load_timestamp(wh_prop2)

    write_deltalake(WH_PROP_PATH, wh_prop, mode='overwrite', schema_mode='merge')
    write_deltalake(WH_PROP2_PATH, wh_prop2, mode='overwrite', schema_mode='merge')

    # Insurance ======================== 
    ACCTPROPINS_PATH = src.config.BRONZE / "acctpropins"
    ACCTPROPINS_PATH.mkdir(parents=True, exist_ok=True)
    WH_INSPOLICY_PATH = src.config.BRONZE / "wh_inspolicy"
    WH_INSPOLICY_PATH.mkdir(parents=True, exist_ok=True)

    data = src.bronze.fetch_data.fetch_insurance()
    acctpropins = data['acctpropins'].copy()
    wh_inspolicy = data['wh_inspolicy'].copy()

    acctpropins = cast_all_null_columns_to_string(acctpropins)
    wh_inspolicy = cast_all_null_columns_to_string(wh_inspolicy)

    acctpropins = add_load_timestamp(acctpropins)
    wh_inspolicy = add_load_timestamp(wh_inspolicy)

    write_deltalake(ACCTPROPINS_PATH, acctpropins, mode='overwrite', schema_mode='merge')
    write_deltalake(WH_INSPOLICY_PATH, wh_inspolicy, mode='overwrite', schema_mode='merge')


    # Account data ========================
    WH_ACCTCOMMON_PATH = src.config.BRONZE / "wh_acctcommon"
    WH_ACCTCOMMON_PATH.mkdir(parents=True, exist_ok=True)
    WH_ACCTLOAN_PATH = src.config.BRONZE / "wh_acctloan"
    WH_ACCTLOAN_PATH.mkdir(parents=True, exist_ok=True)
    WH_LOANS_PATH = src.config.BRONZE / "wh_loans"
    WH_LOANS_PATH.mkdir(parents=True, exist_ok=True)

    data = src.bronze.fetch_data.fetch_account_data()
    wh_acctcommon = data['wh_acctcommon'].copy()
    wh_acctloan = data['wh_acctloan'].copy()
    wh_loans = data['wh_loans'].copy()

    wh_acctcommon = cast_all_null_columns_to_string(wh_acctcommon)
    wh_acctloan = cast_all_null_columns_to_string(wh_acctloan)
    wh_loans = cast_all_null_columns_to_string(wh_loans)

    wh_acctcommon = add_load_timestamp(wh_acctcommon)
    wh_acctloan = add_load_timestamp(wh_acctloan)
    wh_loans = add_load_timestamp(wh_loans)

    write_deltalake(WH_ACCTCOMMON_PATH, wh_acctcommon, mode='overwrite', schema_mode='merge')
    write_deltalake(WH_ACCTLOAN_PATH, wh_acctloan, mode='overwrite', schema_mode='overwrite')
    write_deltalake(WH_LOANS_PATH, wh_loans, mode='overwrite', schema_mode='merge')


    # ORGADDRUSE/PERSADDRUSE (Address Linking) ======================== 
    PERSADDRUSE_PATH = src.config.BRONZE / "persaddruse"
    PERSADDRUSE_PATH.mkdir(parents=True, exist_ok=True)
    ORGADDRUSE_PATH = src.config.BRONZE / "orgaddruse"
    ORGADDRUSE_PATH.mkdir(parents=True, exist_ok=True)

    data = src.bronze.fetch_data.fetch_addruse_tables()
    persaddruse = data['persaddruse'].copy()
    orgaddruse = data['orgaddruse'].copy()

    persaddruse = cast_all_null_columns_to_string(persaddruse)
    orgaddruse = cast_all_null_columns_to_string(orgaddruse)

    persaddruse = add_load_timestamp(persaddruse)
    orgaddruse = add_load_timestamp(orgaddruse)

    write_deltalake(PERSADDRUSE_PATH, persaddruse, mode='overwrite', schema_mode='merge')
    write_deltalake(ORGADDRUSE_PATH, orgaddruse, mode='overwrite', schema_mode='merge')


    # WH_RTXN (OSIBANK) ======================== 
    WH_RTXN_PATH = src.config.BRONZE / "wh_rtxn"
    WH_RTXNBAL_PATH = src.config.BRONZE / "wh_rtxnbal"
    WH_RTXN_PATH.mkdir(parents=True, exist_ok=True)
    WH_RTXNBAL_PATH.mkdir(parents=True, exist_ok=True)

    data = src.bronze.fetch_data.fetch_rtxn()
    wh_rtxn = data['wh_rtxn'].copy()
    wh_rtxnbal = data['wh_rtxnbal'].copy()

    wh_rtxn = cast_all_null_columns_to_string(wh_rtxn)
    wh_rtxnbal = cast_all_null_columns_to_string(wh_rtxnbal)

    wh_rtxn = add_load_timestamp(wh_rtxn)
    wh_rtxnbal = add_load_timestamp(wh_rtxnbal)

    write_deltalake(WH_RTXN_PATH, wh_rtxn, mode='overwrite', schema_mode='merge')
    write_deltalake(WH_RTXNBAL_PATH, wh_rtxnbal, mode='overwrite', schema_mode='merge')

    # WH_ACCTUSERFIELDS (OSIBANK) ======================== 
    WH_ACCTUSERFIELDS_PATH = src.config.BRONZE / "wh_acctuserfields"
    WH_ACCTUSERFIELDS_PATH.mkdir(parents=True, exist_ok=True)

    data = src.bronze.fetch_data.fetch_userfields()
    wh_acctuserfields = data['wh_acctuserfields'].copy()

    wh_acctuserfields = cast_all_null_columns_to_string(wh_acctuserfields)

    wh_acctuserfields = add_load_timestamp(wh_acctuserfields)

    write_deltalake(WH_ACCTUSERFIELDS_PATH, wh_acctuserfields, mode='overwrite', schema_mode='merge')

    # WH_ORGUSERFIELDS (OSIBANK)
    WH_ORGUSERFIELDS_PATH = src.config.BRONZE / "wh_orguserfields"
    WH_ORGUSERFIELDS_PATH.mkdir(parents=True, exist_ok=True)

    data = src.bronze.fetch_data.fetch_userfields()
    wh_orguserfields = data['wh_orguserfields'].copy()

    wh_orguserfields = cast_all_null_columns_to_string(wh_orguserfields)

    wh_orguserfields = add_load_timestamp(wh_orguserfields)

    write_deltalake(WH_ORGUSERFIELDS_PATH, wh_orguserfields, mode='overwrite', schema_mode='merge')

    # WH_PERSUSERFIELDS (OSIBANK)
    WH_PERSUSERFIELDS_PATH = src.config.BRONZE / "wh_persuserfields"
    WH_PERSUSERFIELDS_PATH.mkdir(parents=True, exist_ok=True)

    data = src.bronze.fetch_data.fetch_userfields()
    wh_persuserfields = data['wh_persuserfields'].copy()

    wh_persuserfields = cast_all_null_columns_to_string(wh_persuserfields)

    wh_persuserfields = add_load_timestamp(wh_persuserfields)

    write_deltalake(WH_PERSUSERFIELDS_PATH, wh_persuserfields, mode='overwrite', schema_mode='merge')

    # WH_INVR (OSIBANK)
    # TODO

    # ACCTGRPINVR (OSIBANK)
    # TODO

    # PERSPHONEVIEW ========================
    PERSPHONEVIEW_PATH = src.config.BRONZE / "persphoneview"
    PERSPHONEVIEW_PATH.mkdir(parents=True, exist_ok=True)

    data = src.bronze.fetch_data.fetch_phoneview()
    persphoneview = data['persphoneview'].copy()

    persphoneview = cast_all_null_columns_to_string(persphoneview)

    persphoneview = add_load_timestamp(persphoneview)

    write_deltalake(PERSPHONEVIEW_PATH, persphoneview, mode='overwrite', schema_mode='merge')

    # ORGPHONEVIEW ========================
    ORGPHONEVIEW_PATH = src.config.BRONZE / "orgphoneview"
    ORGPHONEVIEW_PATH.mkdir(parents=True, exist_ok=True)

    orgphoneview = data['orgphoneview'].copy()

    orgphoneview = cast_all_null_columns_to_string(orgphoneview)

    orgphoneview = add_load_timestamp(orgphoneview)

    write_deltalake(ORGPHONEVIEW_PATH, orgphoneview, mode='overwrite', schema_mode='merge')