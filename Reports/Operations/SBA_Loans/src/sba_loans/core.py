import pandas as pd
from pathlib import Path
from deltalake import DeltaTable
import src.config
import src.sba_loans.fetch_data
import cdutils.all_status_silver_acct.core
import numpy as np

def main_report_creation():
    # Get data from custom silver table that includes all accounts 
    # Reason is that the other one is only looking at active accounts
    df = cdutils.all_status_silver_acct.core.query_df_on_date()

    
    orgpersaddr_data = src.sba_loans.fetch_data.fetch_org_pers_addr()
    orgaddruse = orgpersaddr_data['orgaddruse'].copy()
    persaddruse = orgpersaddr_data['persaddruse'].copy()
    wh_addr = orgpersaddr_data['wh_addr'].copy()

    # Filter to SBA loans and select relevant columns
    # df = df[df['product'].str.contains('SBA', case=False, na=False)].copy()
    df = df[[
        'acctnbr',
        'ownersortname',
        'portfolio_key',
        'product',
        'mjaccttypcd',
        'currmiaccttypcd',
        'curracctstatcd',
        'loanofficer',
        'taxrptfororgnbr',
        'taxrptforpersnbr'
    ]].copy()



    # 
    orgaddruse = orgaddruse[orgaddruse['addrusecd'].isin(['PRI'])].copy()
    persaddruse = persaddruse[persaddruse['addrusecd'].isin(['PRI'])].copy()


# %%
    orgaddruse['orgnbr'] = orgaddruse['orgnbr'].astype(str)
    orgaddruse['addrnbr'] = orgaddruse['addrnbr'].astype(str)
    persaddruse['persnbr'] = persaddruse['persnbr'].astype(str)
    persaddruse['addrnbr'] = persaddruse['addrnbr'].astype(str)


    wh_addr = wh_addr[[
        'addrnbr',
        'text1',
        'text2',
        'text3',
        'text4',
        'text5',
        'cityname',
        'statecd',
        'zipcd'
    ]].copy()

    df['taxrptfororgnbr'] = np.where(df['taxrptfororgnbr'].isna(), np.nan, df['taxrptfororgnbr'].astype('Int64').astype(str))
    df['taxrptforpersnbr'] = np.where(df['taxrptforpersnbr'].isna(), np.nan, df['taxrptforpersnbr'].astype('Int64').astype(str))



    orgaddruse = orgaddruse[[
        'orgnbr',
        'addrnbr'
    ]].copy()

    persaddruse = persaddruse[[
        'persnbr',
        'addrnbr'
    ]].copy()

    wh_addr['addrnbr'] = wh_addr['addrnbr'].astype(str)

    orgaddruse = orgaddruse.merge(wh_addr, on='addrnbr', how='inner')


    df = df.merge(orgaddruse, left_on='taxrptfororgnbr', right_on='orgnbr', how='left')

    df = df.drop(columns=['taxrptfororgnbr','orgnbr','addrnbr']).copy()

    persaddruse = persaddruse.merge(wh_addr, on='addrnbr', how='inner')

    df = df.merge(persaddruse, left_on='taxrptforpersnbr', right_on='persnbr', how='left')

    df = df.drop(columns=['taxrptforpersnbr','addrnbr','persnbr']).copy()

    df_copy = df.copy()

    base_names = {col[:-2] for col in df_copy.columns if col.endswith('_x')}

    for base in base_names:
        col_x = f"{base}_x"
        col_y = f"{base}_y"

        if col_y in df_copy.columns:
            df_copy[base] = df_copy[col_x].fillna(df_copy[col_y])
            df_copy = df_copy.drop(columns=[col_x, col_y])

    final_df = df_copy[[
        'acctnbr',
        'ownersortname',
        'portfolio_key',
        'product',
        'mjaccttypcd',
        'currmiaccttypcd',
        'curracctstatcd',
        'loanofficer',
        'text1',
        'text2',
        'text3',
        'text4',
        'text5',
        'cityname',
        'statecd',
        'zipcd'
    ]].copy()

    return final_df

