"""
Deposit Deep Dive: Main Entry
"""

from datetime import datetime, timedelta
import json
import os
import time
from pathlib import Path

import pandas as pd # type: ignore
import numpy as np # type: ignore
# from win32com.client import Dispatch

import src.fetch_data
import cdutils.distribution # type: ignore
import src.output_to_excel
from src._version import __version__


#################################
def main(production_flag: bool=False):
    if production_flag:
        BASE_PATH = Path(r'\\00-DA1\Home\Share\Line of Business_Shared Services\Retail Banking\New Business Checking\Production')
        assert "prod" in __version__, (f"Cannot run in production mode without 'prod' in the __version__")
    else:
        BASE_PATH = Path('.')
    data = src.fetch_data.fetch_data()

   

    comparison_df = pd.merge(
        data['recent_acctcommon'], 
        data['prior_acctcommon'], 
        on=['acctofficer','acctnbr'], 
        how='outer',
        suffixes=('_recent', '_prior')
        )

    numeric_cols = ['bookbalance_recent','bookbalance_prior','notebal_recent','notebal_prior']
    for col in numeric_cols:
        comparison_df[col] = pd.to_numeric(comparison_df[col])


    #################################
    comparison_df['bookbalance_recent'] = comparison_df['bookbalance_recent'].fillna(0)
    comparison_df['bookbalance_prior'] = comparison_df['bookbalance_prior'].fillna(0)
    comparison_df['bookbalance_change'] = comparison_df['bookbalance_recent'] - comparison_df['bookbalance_prior']


    #################################
    comparison_df['bookbalance_change'] = comparison_df['bookbalance_change'].fillna(0)


    #################################


    #################################
    my_list = [
        'ANDREW RODRIGUES',
        'JEFFREY P. PAGLIUCA',
        'JOSHUA A. CAMARA',
        'WILLITTS S. MENDONCA',
        'ROGER A. CABRAL',
        'LAURA A. STACK'
        ]


    #################################
    # Most recent month end
    today = datetime.today()
    if today.day == 1:
        most_recent_month_end = today - timedelta(days=1)
    else:
        most_recent_month_end = today.replace(day=1) - timedelta(days=1)
    # most_recent_month_end_str = most_recent_month_end.strftime("%m/%d/%y")
    me_date_no_slash = most_recent_month_end.strftime("%m%d%y") # Month End date to append to file name

    OUTPUT_PATH = BASE_PATH / Path(f"./output/deposit_deep_dive_{me_date_no_slash}.xlsx")

    with pd.ExcelWriter(OUTPUT_PATH, engine='openpyxl') as writer:
        
        summary_df = comparison_df[comparison_df['acctofficer'].isin(my_list)].groupby('acctofficer').agg({
            'bookbalance_recent':'sum',
            'bookbalance_prior':'sum',
            'bookbalance_change': 'sum'
        }).reset_index()
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        for officer in my_list:
            officer_df = comparison_df[comparison_df['acctofficer'] == officer]
            officer_df.to_excel(writer, sheet_name=officer, index=False)

    src.output_to_excel.format_excel_file(OUTPUT_PATH)

    # Distribution
    recipients = [
        "eusebio.borges@bcsbmail.com",
        # "chad.doorley@bcsbmail.com"
    ]

    bcc_recipients = [
        "chad.doorley@bcsbmail.com",
        "businessintelligence@bcsbmail.com"
    ]
    subject = f"Monthly Deposit Deep Dive Report" 
    body = "Hi, \n\nAttached is the Deposit Deep Dive. If you have any questions, please reach out to BusinessIntelligence@bcsbmail.com\n"
    attachment_paths = [OUTPUT_PATH]

    cdutils.distribution.email_out(
        recipients = recipients, 
        bcc_recipients = bcc_recipients, 
        subject = subject, 
        body = body, 
        attachment_paths = attachment_paths
        )

if __name__ == '__main__':
    print(f"Starting deposit deep dive [{__version__}]")
    # main(production_flag=True)
    main()
    print("Complete!")
