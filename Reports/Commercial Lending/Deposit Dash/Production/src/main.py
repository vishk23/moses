"""
Main Entry: Deposit Dash
Developed by CD
"""
from pathlib import Path
import datetime

import pandas as pd # type: ignore

from src._version import __version__
import cdutils.distribution # type: ignore
import src.output_to_excel

def main():
    # Read inputs
    file_path = r'\\00-da1\Home\Share\Line of Business_Shared Services\Commercial Lending\Deposits\DailyDeposit\DailyDeposit.xlsx'
    df1 = pd.read_excel(file_path)
    
    current_date = datetime.datetime.now().strftime("%m%d%y")

    # Output to excel (raw data)
    OUTPUT_PATH = Path(f'./output/DepositDash_{current_date}.xlsx')
    df1.to_excel(OUTPUT_PATH, sheet_name='Sheet1', index=False)

    src.output_to_excel.format_excel_file(OUTPUT_PATH)


    # Distribution
    recipients = [
        "commercial.portfolio.managers@bcsbmail.com",
        # "chad.doorley@bcsbmail.com"
    ]
    bcc_recipients = [
        "chad.doorley@bcsbmail.com",
        "businessintelligence@bcsbmail.com"
    ]
    subject = f"Monthly Deposit Report" 
    body = "Hi all, \n\nAttached is the Monthly Deposit report. If you have any questions, please reach out to BusinessIntelligence@bcsbmail.com\n"
    attachment_paths = [OUTPUT_PATH]

    cdutils.distribution.email_out(
        recipients = recipients, 
        bcc_recipients = bcc_recipients, 
        subject = subject, 
        body = body, 
        attachment_paths = attachment_paths
        )


if __name__ == "__main__":
    print(f"Running deposit dash [{__version__}]")
    main()
    print("Complete!")