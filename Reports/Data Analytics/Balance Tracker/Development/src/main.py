"""
Balance Tracker - revised
Developed by CD
"""
from pathlib import Path

import pandas as pd # type: ignore

import src.addition_fields
import src.balance_tracker_pipeline_v3
import src.excel_output
import src.fetch_data
import src.monthly_delta
from src._version import __version__
import cdutils.distribution # type: ignore

def main():
    # Fetch Data from COCC
    data_prior, data_current = src.fetch_data.fetch_data()

    _, data_prior_summary = src.balance_tracker_pipeline_v3.main_pipeline_bt(data_prior)
    full_data_current, data_current_summary = src.balance_tracker_pipeline_v3.main_pipeline_bt(data_current)

    # OUTPUT_PATH = Path('./output/data_prior_summary.xlsx')
    # data_prior_summary.to_excel(OUTPUT_PATH, engine='openpyxl', index=False)

    # OUTPUT_PATH = Path('./output/data_current_summary.xlsx')
    # data_current_summary.to_excel(OUTPUT_PATH, engine='openpyxl', index=False)

    monthly_delta = src.monthly_delta.creating_monthly_delta(data_prior_summary, data_current_summary)
    additional_fields = src.addition_fields.yield_and_unadvanced_creation(full_data_current)

    TEMPLATE_PATH = Path('./output/Portfolio_Balance_Tracker_2025YTD.xlsx')
    OUTPUT_PATH = Path('./output/Portfolio_Balance_Tracker_2025YTD.xlsx')
    # OUTPUT_PATH = Path('./output/Portfolio_Balance_Tracker_2025YTD_test.xlsx')

    src.excel_output.update_excel_template(TEMPLATE_PATH, monthly_delta, additional_fields, OUTPUT_PATH)

    # Distribution 
    recipients = [
        # "chad.doorley@bcsbmail.com"
        "Timothy.Chaves@bcsbmail.com",
        "John.Silva@bcsbmail.com",
        "Dawn.Young@bcsbmail.com",
        "Christopher.Alves@bcsbmail.com",
        "donna.oliveira@bcsbmail.com",
        "nancy.pimentel@bcsbmail.com",
        "Hasan.Ali@bcsbmail.com",
        "Michael.Patacao@bcsbmail.com",
        "Jeffrey.Pagliuca@bcsbmail.com",
        "Erin.Riendeau@bcsbmail.com",
        "donna.pavao@bcsbmail.com"
    ]
    bcc_recipients = [
        "chad.doorley@bcsbmail.com",
        "businessintelligence@bcsbmail.com"
    ]
    subject = f"Balance Tracker YTD - Through April 2025" 
    body = "Hi all, \n\nAttached is the Balance Tracker through the most recent month end. If you have any questions, please reach out to BusinessIntelligence@bcsbmail.com\n\n"
    attachment_paths = [OUTPUT_PATH]

    cdutils.distribution.email_out(
        recipients = recipients, 
        bcc_recipients = bcc_recipients, 
        subject = subject, 
        body = body, 
        attachment_paths = attachment_paths
        )



if __name__ == '__main__':
    print(f"Starting {__version__}")
    main()
    print("Complete!")

