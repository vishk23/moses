# Core logic specific to project/report

import cdutils.deduplication # type: ignore
from deltalake import DeltaTable
import src.config
import pandas as pd
from pathlib import Path
from datetime import datetime
import src.neworgs_2025.fetch_data

def main_pipeline():
    accts = DeltaTable(src.config.SILVER / "account").to_pandas()
    accts = accts[accts['taxrptforpersnbr'].isna()].copy()

    org_data = DeltaTable(src.config.BRONZE / "wh_org").to_pandas()

    # Dedupe org table
    if 'wh_org' in org_data:
        dedupe_list = [{'df': org_data['wh_org'], 'field': 'orgnbr'}]
        org_data['wh_org'] = cdutils.deduplication.dedupe(dedupe_list)

    org_data = org_data[[
        'orgnbr',
        'orgname',
        'orgtypcd',
        'orgtypcddesc'
    ]].copy() 

    ## loans/deposit categorization
    # Account type mappings
    MACRO_TYPE_MAPPING = {
        'CML': 'Loan',
        'MLN': 'Loan',
        'CNS': 'Loan',
        'MTG': 'Loan',
        'CK': 'Deposit',
        'SAV': 'Deposit',
        'TD': 'Deposit'
    }

    accts['Macro Account Type'] = accts['mjaccttypcd'].map(MACRO_TYPE_MAPPING)
    accts = accts[~(accts['Macro Account Type'].isna())].copy()

    summary_df = accts.pivot_table(
        index='taxrptfororgnbr',
        columns='Macro Account Type',
        aggfunc={
            'Net Balance':'sum',
            'acctnbr':'nunique'
        },
        fill_value=0
    )

    summary_df.columns = ['_'.join(col) for col in summary_df.columns]   
    summary_df = summary_df.reset_index()
    summary_df['taxrptfororgnbr'] = summary_df['taxrptfororgnbr'].astype(int).astype(str)

    summary_df = summary_df.rename(columns={
        'taxrptfororgnbr':'taxrptfororgnbr',
        'Net Balance_Deposit':'Deposit Balance',
        'Net Balance_Loan':'Loan Balance',
        'acctnbr_Deposit':'Unique Deposit Accounts',
        'acctnbr_Loan':'Unique Loan Accounts'
    }).copy()

    # Get other entity details
    entity_details = accts.groupby('taxrptfororgnbr').agg(
        primaryownercity=('primaryownercity', 'first'),
        primaryownerstate=('primaryownerstate','first'),
        branchname=('branchname','first'),
        earliest_opendate=('contractdate','min'),
        latest_opendate=('contractdate','max'),
    ).reset_index()

    entity_details['taxrptfororgnbr'] = entity_details['taxrptfororgnbr'].astype(int).astype(str)
    # Merge two acct summary tables
    summary_df = pd.merge(entity_details, summary_df, on='taxrptfororgnbr', how='inner')
    summary_df = summary_df[summary_df['latest_opendate'] >= datetime(2025,1,1)]

    org_data['orgnbr'] = org_data['orgnbr'].astype(str)

    merged_df = pd.merge(org_data, summary_df, left_on='orgnbr', right_on='taxrptfororgnbr', how='inner')
    merged_df = merged_df.drop(columns=['taxrptfororgnbr']).copy()
    merged_df['Total Accounts'] = merged_df['Unique Deposit Accounts'] + merged_df['Unique Loan Accounts']

    raw_taxid = src.neworgs_2025.fetch_data.fetch_data()

    vieworgtaxid = raw_taxid['vieworgtaxid'].copy()

    assert vieworgtaxid['orgnbr'].is_unique, "Duplicates"

    vieworgtaxid = vieworgtaxid[['orgnbr','taxid']].copy()

    vieworgtaxid['orgnbr'] = vieworgtaxid['orgnbr'].astype(str)

    merged_df = pd.merge(merged_df, vieworgtaxid, on='orgnbr', how='left')

    return merged_df