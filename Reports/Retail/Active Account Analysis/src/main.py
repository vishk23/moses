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
- Cross-sell opportunity analysis for retail interns
- Active account and agreement relationship mapping
- Customer engagement and product penetration insights
- Monthly reporting for retail department initiatives
"""
from pathlib import Path
from typing import List
from datetime import datetime

import pandas as pd # type: ignore

import src.config
import src.fetch_data # type: ignore
from cdutils import input_cleansing # type: ignore
from cdutils.acct_lookup_daily import daily_acct_table # type: ignore


def main():
    """Main report execution function for Active Account & Agreement Analysis"""
    
    # Ensure output directory exists
    src.config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"Environment: {src.config.ENV}")
    print(f"Output directory: {src.config.OUTPUT_DIR}")
    
    # Step 1: Load active accounts from daily_acct_file
    print("Loading active accounts...")
    active_accounts = daily_acct_table.get_daily_acct_table()
    print(f"Loaded {len(active_accounts)} active accounts")
    
    # Step 2: Load and prepare WH_ORG with deduplication and schema enforcement
    print("Loading WH_ORG...")
    data = src.fetch_data.fetch_data()
    wh_org = data['wh_org'].copy()
    
    # Enforce schema for WH_ORG - ensure orgnbr is string
    schema_wh_org = {
        'orgnbr': str,
        'orgname': str
    }
    wh_org = input_cleansing.enforce_schema(wh_org, schema_wh_org)
    
    # Deduplicate WH_ORG on primary key
    wh_org = wh_org.drop_duplicates(subset=['orgnbr'], keep='first')
    print(f"Loaded {len(wh_org)} unique organizations")
    
    # Step 3: Load and prepare WH_PERS with deduplication and schema enforcement
    print("Loading WH_PERS...")
    wh_pers = data['wh_pers'].copy()
    
    # Enforce schema for WH_PERS - ensure persnbr is string
    schema_wh_pers = {
        'persnbr': str,
        'firstname': str,
        'lastname': str
    }
    wh_pers = input_cleansing.enforce_schema(wh_pers, schema_wh_pers)
    
    # Deduplicate WH_PERS on primary key
    wh_pers = wh_pers.drop_duplicates(subset=['persnbr'], keep='first')
    print(f"Loaded {len(wh_pers)} unique persons")
    
    # Step 4: Load WH_AGREEMENTS
    print("Loading WH_AGREEMENTS...")
    wh_agreements = data['wh_agreements'].copy()
    
    # Enforce schema for WH_AGREEMENTS
    schema_wh_agreements = {
        'agrmntnbr': str,
        'ownerorgnbr': str,
        'ownerpersnbr': str,
        'agrmntstatcd': str
    }
    wh_agreements = input_cleansing.enforce_schema(wh_agreements, schema_wh_agreements)
    
    # Filter for active agreements only
    active_agreements = wh_agreements[wh_agreements['agrmntstatcd'] == 'A'].copy()
    print(f"Found {len(active_agreements)} active agreements")
    
    # Step 5: Load WH_ALLROLES to link agreements to accounts
    print("Loading WH_ALLROLES...")
    wh_allroles = data['wh_allroles'].copy()
    
    # Enforce schema for WH_ALLROLES
    schema_wh_allroles = {
        'acctnbr': str,
        'orgnbr': str,
        'persnbr': str
    }
    wh_allroles = input_cleansing.enforce_schema(wh_allroles, schema_wh_allroles)
    
    # Step 6: Link agreements to active accounts via WH_ALLROLES
    print("Linking agreements to active accounts...")
    
    # Convert account numbers to string for joining
    active_accounts['acctnbr'] = active_accounts['acctnbr'].astype(str)
    
    # Join active accounts with roles
    account_roles = pd.merge(
        active_accounts,
        wh_allroles,
        on='acctnbr',
        how='inner'
    )
    print(f"Found {len(account_roles)} account-role relationships")
    
    # Join with agreements via organization numbers
    agreements_with_accounts_org = pd.merge(
        account_roles,
        active_agreements,
        left_on='orgnbr',
        right_on='ownerorgnbr',
        how='inner'
    )
    
    # Join with agreements via person numbers
    agreements_with_accounts_pers = pd.merge(
        account_roles,
        active_agreements,
        left_on='persnbr',
        right_on='ownerpersnbr',
        how='inner'
    )
    
    # Combine both types of agreement linkages
    agreements_with_accounts = pd.concat([
        agreements_with_accounts_org,
        agreements_with_accounts_pers
    ], ignore_index=True)
    
    # Remove duplicates
    agreements_with_accounts = agreements_with_accounts.drop_duplicates()
    print(f"Found {len(agreements_with_accounts)} account-agreement relationships")
    
    # Step 7: Add organization and person names
    print("Adding organization and person names...")
    
    # Add organization names
    agreements_with_accounts = pd.merge(
        agreements_with_accounts,
        wh_org[['orgnbr', 'orgname']],
        left_on='ownerorgnbr',
        right_on='orgnbr',
        how='left',
        suffixes=('', '_owner')
    )
    
    # Add person names
    agreements_with_accounts = pd.merge(
        agreements_with_accounts,
        wh_pers[['persnbr', 'firstname', 'lastname']],
        left_on='ownerpersnbr',
        right_on='persnbr',
        how='left',
        suffixes=('', '_owner')
    )
    
    # Create a combined owner name field
    agreements_with_accounts['owner_name'] = agreements_with_accounts.apply(
        lambda row: row['orgname'] if pd.notna(row['orgname']) 
        else f"{row['firstname']} {row['lastname']}" if pd.notna(row['firstname']) and pd.notna(row['lastname'])
        else 'Unknown Owner',
        axis=1
    )
    
    # Step 8: Prepare final datasets
    print("Preparing final datasets...")
    
    # Active Accounts Dataset
    active_accounts_final = active_accounts.copy()
    
    # Active Agreements Dataset
    active_agreements_final = agreements_with_accounts[[
        'acctnbr', 'agrmntnbr', 'owner_name', 'ownerorgnbr', 'ownerpersnbr', 'agrmntstatcd'
    ]].copy()
    
    # Step 9: Output to Excel files
    print("Generating output files...")
    
    # Generate filename with current date
    today = datetime.today()
    date_str = f"{today.strftime('%B')} {today.day} {today.year}"
    
    # Output Active Accounts
    accounts_filename = f'Active Accounts {date_str}.xlsx'
    accounts_output_path = src.config.OUTPUT_DIR / accounts_filename
    active_accounts_final.to_excel(accounts_output_path, sheet_name='Active Accounts', index=False)
    print(f"Active accounts saved to: {accounts_output_path}")
    
    # Output Active Agreements
    agreements_filename = f'Active Agreements {date_str}.xlsx'
    agreements_output_path = src.config.OUTPUT_DIR / agreements_filename
    active_agreements_final.to_excel(agreements_output_path, sheet_name='Active Agreements', index=False)
    print(f"Active agreements saved to: {agreements_output_path}")
    
    # Summary statistics
    print(f"\nSummary:")
    print(f"- Active Accounts: {len(active_accounts_final)}")
    print(f"- Active Agreements: {len(active_agreements_final)}")
    print(f"- Unique Agreement Numbers: {active_agreements_final['agrmntnbr'].nunique()}")
    print(f"- Unique Account Numbers with Agreements: {active_agreements_final['acctnbr'].nunique()}")
    
    # Distribution (currently disabled - enable when recipients are determined)
    if src.config.EMAIL_TO:  # Only send emails if recipients are configured
        from cdutils import distribution # type: ignore
        
        email_subject = f"Active Account & Agreement Analysis - {date_str}"
        
        email_body = """Hi,

Attached are the Active Account and Agreement datasets for cross-sell analysis. 

The files include:
1. Active Accounts - Current active account portfolio
2. Active Agreements - Active agreements linked to accounts with owner information

If you have any questions, please reach out to BusinessIntelligence@bcsbmail.com

Thanks!"""
        
        distribution.email_out(
            recipients=src.config.EMAIL_TO, 
            bcc_recipients=src.config.EMAIL_CC, 
            subject=email_subject, 
            body=email_body, 
            attachment_paths=[accounts_output_path, agreements_output_path]
        )
        print(f"Email sent to {len(src.config.EMAIL_TO)} recipients with {len(src.config.EMAIL_CC)} CC")
    else:
        print(f"Development mode or no recipients configured - email not sent.")
        print(f"Output files: {accounts_output_path}, {agreements_output_path}")


if __name__ == '__main__':
    print("Starting Active Account & Agreement Analysis")
    main()
    print("Complete!")