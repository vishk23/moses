import pandas as pd
from pathlib import Path
from deltalake import DeltaTable
import src.config
import src.sba_loans.fetch_data
import cdutils.all_status_silver_acct.core

def main_report_creation():
    # Get data from custom silver table that includes all accounts 
    # Reason is that the other one is only looking at active accounts
    df = cdutils.all_status_silver_acct.core.query_df_on_date()

    # Get Lakehouse tables
    address = DeltaTable(src.config.BRONZE / "wh_addr").to_pandas()
    
    orgpersaddr_data = src.sba_loans.fetch_data.fetch_org_pers_addr()
    orgaddruse = orgpersaddr_data['orgaddruse'].copy()
    persaddruse = orgpersaddr_data['persaddruse'].copy()

    # Filter to SBA loans and select relevant columns
    df = df[df['product'].str.contains('SBA', case=False, na=False)].copy()
    df = df[[
        'acctnbr',
        'ownersortname',
        'portfolio_key',
        'product',
        'mjaccttypcd',
        'currmiaccttypcd',
        'curracctstatcd',
        'loanofficer',
    ]].copy()



    # 
    orgaddruse = orgaddruse[orgaddruse['addrusecd'].isin(['PRI'])].copy()
    persaddruse = persaddruse[persaddruse['addrusecd'].isin(['PRI'])].copy()


    # %%
    orgaddruse['orgnbr'] = orgaddruse['orgnbr'].astype(str)
    orgaddruse['addrnbr'] = orgaddruse['addrnbr'].astype(str)

    cleaned_address['addrnbr'] = cleaned_address['addrnbr'].astype(str)

    # %%
    merged_address = pd.merge(orgaddruse, cleaned_addr, on='addrnbr', how='inner')


    return final_df
