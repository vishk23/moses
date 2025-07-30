"""
Active Account & Agreement Analysis - Main Entry Point

BUSINESS LOGIC EXTRACTED:

Data Sources & Relationships:
- daily_acct_file: Active accounts dataset (already available)
- WH_AGREEMENTS: Agreement data with OWNERORGNBR and OWNERPERSNBR
- WH_ALLROLES: Links agreements to active accounts via role relationships
- WH_ORG: Organization names (orgnbr matches OWNERORGNBR)
- WH_PERS: Person names (persnbr matches OWNERPERSNBR)

Business Rules:
- Active accounts linked to agreements through WH_ALLROLES
- Agreements filtered for active status only
- Organization and person names added from WH_ORG/WH_PERS
- Deduplication applied to org/pers tables on primary keys
- Primary keys enforced as string type for consistency

Data Processing Flow:
1. Load active accounts from daily_acct_file
2. Load and deduplicate WH_ORG and WH_PERS with schema enforcement
3. Load WH_AGREEMENTS and link to accounts via WH_ALLROLES
4. Filter for active agreements only
5. Add organization and person names
6. Output two datasets: active accounts and active agreements
7. Monthly delivery to Retail Department for cross-sell analysis

Business Intelligence Value:
- Cross-sell opportunity analysis for retail
- Active account and agreement relationship mapping
- Customer engagement and product penetration insights
- Monthly reporting for retail department initiatives
"""
from pathlib import Path
from typing import List
from datetime import datetime

import pandas as pd # type: ignore

import src.config
import src.active_acct_analysis.fetch_data # type: ignore
from cdutils import input_cleansing # type: ignore
from cdutils import deduplication # type: ignore
import cdutils.acct_file_creation.core # type: ignore


def main():
    # Ensure output directory exists
    src.config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Environment: {src.config.ENV}")
    print(f"Output directory: {src.config.OUTPUT_DIR}")

    # Step 1: Load active accounts from daily_acct_file
    print("Loading active accounts...")
    active_accounts = cdutils.acct_file_creation.core.query_df_on_date()
    print(f"Loaded {len(active_accounts)} active accounts")

    # Filter active_accounts by mjaccttypcd before any processing
    mjaccttypcd_keep = ['CK','SAV','TD','CML','MLN','MTG','CNS']
    active_accounts = active_accounts[active_accounts['mjaccttypcd'].isin(mjaccttypcd_keep)].copy()

    # Step 2: Load base data
    print("Loading base data...")
    data = src.active_acct_analysis.fetch_data.fetch_data()

    # Step 3: Load and prepare WH_ORG with deduplication
    print("Loading WH_ORG...")
    wh_org = data['wh_org'].copy()
    schema_wh_org = {'orgnbr': str, 'orgname': str}
    wh_org = input_cleansing.enforce_schema(wh_org, schema_wh_org)
    wh_org = deduplication.dedupe([{'df': wh_org, 'field': 'orgnbr'}])
    print(f"Loaded {len(wh_org)} unique organizations")

    # Step 4: Load and prepare WH_PERS with deduplication
    print("Loading WH_PERS...")
    wh_pers = data['wh_pers'].copy()
    schema_wh_pers = {'persnbr': str, 'persname': str}
    wh_pers = input_cleansing.enforce_schema(wh_pers, schema_wh_pers)
    wh_pers = deduplication.dedupe([{'df': wh_pers, 'field': 'persnbr'}])
    print(f"Loaded {len(wh_pers)} unique persons")

    # Step 5: Load WH_AGREEMENTS and filter for active agreements
    print("Loading WH_AGREEMENTS...")
    wh_agreements = data['wh_agreement'].copy()
    schema_wh_agreements = {
        'acctnbr': str, 'agreenbr': str, 'persnbr': str, 'ownerpersnbr': str, 'ownerorgnbr': str,
        'agrmntnbr': str, 'agrmntstatcd': str, 'agreetypcd': str
    }
    wh_agreements = input_cleansing.enforce_schema(wh_agreements, schema_wh_agreements)
    active_agreements = wh_agreements[
        (wh_agreements['inactivedate'].isnull()) |
        (wh_agreements['inactivedate'] > wh_agreements['rundate'])
    ].copy()
    print(f"Found {len(active_agreements)} active agreements out of {len(wh_agreements)} total")

    # Step 6: Merge in agreement type descriptions
    print("Merging in agreement type descriptions...")
    cardagreementtyp = data['cardagreementtyp'].copy()
    cardagreementtyp = cardagreementtyp.rename(columns={"AGREETYPCD": "agreetypcd", "AGREETYPDESC": "agreetypdesc"})
    active_agreements = pd.merge(
        active_agreements,
        cardagreementtyp[['agreetypcd', 'agreetypdesc']],
        on='agreetypcd', how='left'
    )

    # Step 7: Add owner name (org or pers)
    print("Adding owner names...")
    active_agreements = pd.merge(
        active_agreements,
        wh_org[['orgnbr', 'orgname']],
        left_on='ownerorgnbr', right_on='orgnbr', how='left', suffixes=('', '_org')
    )
    active_agreements = pd.merge(
        active_agreements,
        wh_pers[['persnbr', 'persname']],
        left_on='ownerpersnbr', right_on='persnbr', how='left', suffixes=('', '_pers')
    )
    active_agreements['owner_name'] = active_agreements.apply(
        lambda row: row['orgname'] if pd.notna(row['orgname'])
        else row['persname'] if pd.notna(row['persname'])
        else 'Unknown Owner', axis=1
    )
    active_agreements['owner_id'] = active_agreements.apply(
        lambda row: row['ownerorgnbr'] if pd.notna(row['ownerorgnbr']) and row['ownerorgnbr'] != ''
        else row['ownerpersnbr'], axis=1
    )

    # Step 8: One-hot encode agreement types by owner
    print("Building owner-agreement type matrix...")
    owner_agreement = active_agreements[['owner_id', 'owner_name', 'agreetypdesc']].drop_duplicates()
    owner_agreement['has_agreement'] = 'Y'
    summary = owner_agreement.pivot_table(
        index=['owner_id', 'owner_name'],
        columns='agreetypdesc',
        values='has_agreement',
        aggfunc='first',
        fill_value='N'
    ).reset_index()
    summary = summary.sort_values('owner_name').reset_index(drop=True)

    # Step 9: Output to Excel
    today = datetime.today()
    date_str = f"{today.strftime('%B')} {today.day} {today.year}"
    summary_filename = f'Agreement Owner Matrix {date_str}.xlsx'
    summary_output_path = src.config.OUTPUT_DIR / summary_filename
    summary.to_excel(summary_output_path, sheet_name='OwnerAgreementMatrix', index=False)
    print(f"Agreement owner matrix saved to: {summary_output_path}")

    # Output filtered active accounts with only the specified columns
    acct_cols = [
        'effdate', 'acctnbr', 'ownersortname', 'product', 'mjaccttypcd', 'currmiaccttypcd',
        'curracctstatcd', 'noteintrate', 'notebal', 'bookbalance', 'contractdate',
        'datemat', 'branchname', 'acctofficer', 'loanofficer', 'taxrptforpersnbr', 'taxrptfororgnbr', 'portfolio_key'
    ]
    active_accounts_out = active_accounts[acct_cols].copy()
    accounts_filename = f'Active Accounts {date_str}.xlsx'
    accounts_output_path = src.config.OUTPUT_DIR / accounts_filename
    active_accounts_out.to_excel(accounts_output_path, sheet_name='Active Accounts', index=False)
    print(f"Filtered active accounts saved to: {accounts_output_path}")

    print("\nSummary:")
    print(f"- Unique Owners: {len(summary)}")
    print(f"- Agreement Types: {list(summary.columns[2:])}")

if __name__ == '__main__':
    print("Starting Active Account & Agreement Analysis")
    main()
    print("Complete!")



