"""
Main Entry Point
"""
from pathlib import Path
from typing import List
import argparse
from datetime import datetime

import pandas as pd # type: ignore

import src.fetch_data # type: ignore
import src.core_transform
import src.output_to_excel
from src._version import __version__
import cdutils.pkey_sqlite # type: ignore
import cdutils.daily_deposit_staging # type: ignore
import cdutils.string_regex # type: ignore
import cdutils.distribution # type: ignore

def main(production_flag: bool=False):
    if production_flag:
        BASE_PATH = Path(r'\\00-DA1\Home\Share\Line of Business_Shared Services\Commercial_Lending\Status Page')
        assert "prod" in __version__, (f"Cannot run in production mode without 'prod' in the __version__")
    else:
        BASE_PATH = Path('.')


    # Define constants for validation
    REQUIRED_EMAIL_DOMAIN = '@bcsbmail.com'
    MAX_KEY_DIGITS = 12
    MAX_ACCOUNT_DIGITS = 20

    parser = argparse.ArgumentParser()
    parser.add_argument('--email', required=True)
    parser.add_argument('--key', type=int, required=True)
    parser.add_argument('--additions', nargs='*', type=int, default=[])
    parser.add_argument('--deletes', nargs='*', type=int, default=[])
    args = parser.parse_args()

    # Sanitization checks
    assert args.email.endswith(REQUIRED_EMAIL_DOMAIN), f"Email must end with {REQUIRED_EMAIL_DOMAIN}"
    assert len(str(args.key)) <= MAX_KEY_DIGITS, f"Key must have up to {MAX_KEY_DIGITS} digits"
    for num in args.additions:
        assert len(str(num)) <= MAX_ACCOUNT_DIGITS, f"Addition {num} has more than {MAX_ACCOUNT_DIGITS} digits"
    for num in args.deletes:
        assert len(str(num)) <= MAX_ACCOUNT_DIGITS, f"Delete {num} has more than {MAX_ACCOUNT_DIGITS} digits"
    
    # # Proceed with processing (example output)
    # print(f"Email: {args.email}")
    # print(f"Key: {args.key}")
    # print(f"Additions: {args.additions}")
    # print(f"Deletes: {args.deletes}")
    email = args.email
    key = args.key
    additions = args.additions
    deletes = args.deletes

    data = src.fetch_data.fetch_data()

    # # # Core transformation pipeline
    raw_data = src.core_transform.main_pipeline(data)

    # Raw data with pkey appended
    raw_data = cdutils.pkey_sqlite.add_pkey(raw_data)

    # # Filter on key
    filtered_data = src.core_transform.filtering_on_pkey(raw_data, key)

    # Additions/Deletes
    filtered_data = src.core_transform.apply_adds_deletes(raw_data, filtered_data, additions, deletes)

    # # Loan section
    cml, personal, _ = src.core_transform.loan_section(filtered_data)

    # # Deposits
    deposits, _ = src.core_transform.deposit_section(filtered_data)

    # # Household Title
    household_title = src.core_transform.household_title_logic(cml, personal, deposits)

    # Related entities
    dfs_for_related_entities = [cml, personal, deposits]
    related_entities = src.core_transform.related_entities(data, dfs_for_related_entities)

    # Relationship summary section
    dfs_for_summary_section = {
        'cml': cml, 
        'deposits': deposits}
     
    summary_section = src.core_transform.summary_section(dfs_for_summary_section)

    total_commitments = summary_section['total_commitments']
    total_outstanding = summary_section['total_outstanding']
    total_swap_exposure = summary_section['total_swap_exposure']
    deposit_balance = summary_section['deposit_balance']
    deposit_timeframe = summary_section['deposit_timeframe'] # Can't use copy with a string

    # Final data cleaning
    cml = src.core_transform.final_cml(cml)
    personal = src.core_transform.final_personal(personal)
    deposits = src.core_transform.final_deposits(deposits)

    # Output to Excel/Configuration
    current_date = filtered_data['effdate'].iloc[0].strftime("%m/%d/%Y")
    current_date_no_slash = current_date.replace("/","")
    normalized_customer_name = cdutils.string_regex.normalize_to_alnum_underscore(household_title)
    file_name = f"{current_date_no_slash}_{normalized_customer_name}.xlsx"

    SCRIPT_DIR = Path(__file__).parent
    PARENT_DIR = SCRIPT_DIR.parent
    TEMPLATE_PATH = PARENT_DIR / "assets" / "StatusPage_Template.xlsx"
    OUTPUT_PATH = PARENT_DIR / "output" / file_name

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    insertions = [
        (29, deposits),
        (25, personal),
        (21, cml),
        (4, related_entities, 'C'),
    ]

    cell_values = {
        'A1': household_title,
        'B6': deposit_balance,
        'B7': total_commitments,
        'B8': total_outstanding,
        'B11': total_swap_exposure,
        'A6': deposit_timeframe,
        'H3': 'CD Automation',
        'H2': current_date
    }

    src.output_to_excel.excel_mapping(
        template_path = TEMPLATE_PATH,
        output_path = OUTPUT_PATH,
        cell_values = cell_values,
        df_inserts = insertions
    )

    # # Distribute
    recipients = [
        # "chad.doorley@bcsbmail.com",
        email
    ]
    bcc_recipients = [
        "chad.doorley@bcsbmail.com",
        "businessintelligence@bcsbmail.com"
    ]
    subject = f"Status Page - {file_name}" 
    body = "Hi, \n\nAttached is your requested status page. If you have any questions, please reach out to BusinessIntelligence@bcsbmail.com \n\nThanks!"
    attachment_paths = [OUTPUT_PATH]
    cdutils.distribution.email_out(recipients, bcc_recipients, subject, body, attachment_paths)

if __name__ == '__main__':
    print(f"Starting [{__version__}]")
    # main(production_flag=True)
    main()
    print("Complete!")

