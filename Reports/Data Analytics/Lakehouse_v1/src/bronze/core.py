import src.config
import cdutils.acct_file_creation.core # type: ignore
from datetime import datetime
import pandas as pd
from pathlib import Path
from deltalake import write_deltalake

def generate_bronze_tables():
    # wh_addr (address)
    print("Start bronze table generation")
    WH_ADDR_PATH = src.config.BRONZE / "wh_addr"
    WH_ADDR_PATH.mkdir(parents=True, exist_ok=True)

    data = src.bronze.fetch_data.fetch_wh_addr()
    wh_addr = data['wh_addr'].copy()

    write_deltalake(WH_ADDR_PATH, wh_addr, mode='overwrite', schema_mode='merge')
    print("Successfully wrote wh_addr")

    # wh_allroles
    print("Start bronze table generation")
    WH_ALLROLES_PATH = src.config.BRONZE / "wh_allroles"
    WH_ALLROLES_PATH.mkdir(parents=True, exist_ok=True)

    data = src.bronze.fetch_data.fetch_wh_allroles()
    wh_allroles = data['wh_allroles'].copy()

    write_deltalake(WH_ALLROLES_PATH, wh_allroles, mode='overwrite', schema_mode='merge')

    # Org
    WH_ORG_PATH = src.config.BRONZE / "wh_org"
    WH_ORG_PATH.mkdir(parents=True, exist_ok=True)
    WH_PERS_PATH = src.config.BRONZE / "wh_pers"
    WH_PERS_PATH.mkdir(parents=True, exist_ok=True)

    data = src.bronze.fetch_data.fetch_org_pers()
    wh_org = data['wh_org'].copy()
    wh_pers = data['wh_org'].copy()

    write_deltalake(WH_ORG_PATH, wh_org, mode='overwrite', schema_mode='merge')
    write_deltalake(WH_PERS_PATH, wh_org, mode='overwrite', schema_mode='merge')

    # DB Metadata Lookup
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

    write_deltalake(METADATA_PATH1, lookup_df1, mode='overwrite', schema_mode='merge')
    write_deltalake(METADATA_PATH2, lookup_df2, mode='overwrite', schema_mode='merge')