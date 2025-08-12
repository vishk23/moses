"""
Main Entry Point
"""
from pathlib import Path
from datetime import datetime

import pandas as pd # type: ignore

import src.cdutils.database.fdic_recon
import src.cdutils.database.generic_query
import src.core_transform
import src.distribution
import src.output_to_excel
from src._version import __version__
import src.output_to_excel_multiple_sheets

def main(production_flag: bool=False):
    if production_flag:
        BASE_PATH = Path(r'\\00-DA1\Home\Share\Line of Business_Shared Services')
        assert "prod" in __version__, (f"Cannot run in production mode without 'prod' in the __version__")
    else:
        BASE_PATH = Path('.')
    data = src.cdutils.database.generic_query.fetch_data()

    # Create early payoff report
    new_loan_page, cra_page = src.core_transform.main_pipeline(data)

    # Output to excel
    current_date = datetime.now().strftime('%Y%m%d')
    file_path = BASE_PATH / Path('./output')
    file_name = f'Loan_Report_45_day_lookback_{current_date}.xlsx'
    OUTPUT_PATH = file_path / file_name
    with pd.ExcelWriter(OUTPUT_PATH, mode='w', engine='openpyxl') as writer:
        new_loan_page.to_excel(writer, sheet_name='NEW LOAN', index=False)
        cra_page.to_excel(writer, sheet_name='CRA', index=False)


    # Format excel
    src.output_to_excel_multiple_sheets.format_excel_file(OUTPUT_PATH)

    # Distribution
    recipients = [
        # "chad.doorley@bcsbmail.com"
        "paul.kocak@bcsbmail.com",
        "linda.clark@bcsbmail.com"
    ]
    bcc_recipients = [
        "chad.doorley@bcsbmail.com"
    ]
    subject = f"Weekly Loan Report - {datetime.now().strftime('%m/%d/%Y')}" 
    body = "Hi all, \n\nAttached is the Weekly Loan Report with a 45 day lookback. Please let me know if you have any questions."
    attachment_paths = [OUTPUT_PATH]
    
    src.distribution.email_out(recipients, bcc_recipients, subject, body, attachment_paths)

if __name__ == '__main__':
    print(f"Starting [{__version__}]")
    # main(production_flag=True)
    main()
    print("Complete!")

