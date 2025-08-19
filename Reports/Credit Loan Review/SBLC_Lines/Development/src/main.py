"""
Main Entry Point
"""
from pathlib import Path
from typing import List
from datetime import datetime

import pandas as pd # type: ignore

import src.fetch_data # type: ignore
import src.core_transform # type: ignore
import cdutils.pkey_sqlite # type: ignore
import cdutils.hhnbr # type: ignore
import src.output_to_excel
import cdutils.loans.calculations # type: ignore
import cdutils.selo # type: ignore
import cdutils.inactive_date # type: ignore
from src._version import __version__


def main(production_flag: bool=False):
    if production_flag:
        BASE_PATH = Path(r'\\00-DA1\Home\Share\Line of Business_Shared Services')
        assert "prod" in __version__, (f"Cannot run in production mode without 'prod' in the __version__")
    else:
        BASE_PATH = Path('.')

    data = src.fetch_data.fetch_data()

    # # Core transformation pipeline
    raw_data = src.core_transform.main_pipeline(data)

    # Raw data with pkey appended
    raw_data = cdutils.pkey_sqlite.add_pkey(raw_data)
    raw_data = cdutils.pkey_sqlite.add_ownership_key(raw_data)
    raw_data = cdutils.pkey_sqlite.add_address_key(raw_data)

    # Household number
    househldacct = data['househldacct'].copy() 
    raw_data = cdutils.hhnbr.add_hh_nbr(raw_data, househldacct)

    # Categorize loans (if it's a deposit or other type of account, it will just return null)
    loan_category_df = cdutils.loans.calculations.categorize_loans(raw_data)
    loan_category_df = loan_category_df[['acctnbr','Category']].copy()
    df = pd.merge(raw_data, loan_category_df, on='acctnbr', how='left')

    # Add secondary lending officer
    df = cdutils.selo.append_selo(df)

    # Add inactive date
    df = cdutils.inactive_date.append_inactive_date(df)
    
    # Filter down columns
    df = df[[
        "effdate",
        "acctnbr",
        "loanofficer",
        "Secondary Lending Officer",
        "inactivedate",
        "availbalamt",
        "bookbalance",
        "ownersortname",
        "product",
        "riskratingcd",
        "contractdate"
    ]].copy()

    # Rename columns
    df = df.rename(columns={
        "effdate":"EFFDATE",
        "acctnbr":"ACCTNBR",
        "loanofficer":"Responsibility Officer",
        "inactivedate":"Inactive Date",
        "availbalamt":"Available Balance",
        "bookbalance":"Book Balance",
        "ownersortname":"Customer Name",
        "product":"Product Name",
        "riskratingcd":"Risk Rating",
        "contractdate":"Contract Date"
    }).copy()

    # Output to excel (raw data)
    OUTPUT_PATH = BASE_PATH / Path('./output/standard_report.xlsx')
    df.to_excel(OUTPUT_PATH, sheet_name='Sheet1', index=False)

    # Format excel
    src.output_to_excel.format_excel_file(OUTPUT_PATH)

    # Distribution
    # recipients = [
    #     # "chad.doorley@bcsbmail.com",
    # ]
    # bcc_recipients = [
    #     "chad.doorley@bcsbmail.com",
    #     "businessintelligence@bcsbmail.com"
    # ]
    # subject = f"File Name" 
    # body = "Hi, \n\nAttached is your requested report. If you have any questions, please reach out to BusinessIntelligence@bcsbmail.com \n\nThanks!"
    # attachment_paths = [OUTPUT_PATH]
    # cdutils.distribution.email_out(recipients, bcc_recipients, subject, body, attachment_paths)


if __name__ == '__main__':
    print(f"Starting [{__version__}]")
    # main(production_flag=True)
    main()
    print("Complete!")

