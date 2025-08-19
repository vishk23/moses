"""
Business Deposit Account: Custom Date Range 
"""


from pathlib import Path
from typing import List

import pandas as pd # type: ignore

import src.fetch_data
import src.cdutils.input_cleansing
from src._version import __version__
import src.output_to_excel
import cdutils.distribution # type: ignore


def main(production_flag: bool=False):
    if production_flag:
        BASE_PATH = Path(r'\\00-DA1\Home\Share\Line of Business_Shared Services')
        assert "prod" in __version__, (f"Cannot run in production mode without 'prod' in the __version__")
    else:
        BASE_PATH = Path('.')
    data = src.fetch_data.fetch_data_ytd()

    acctcommon = data['acctcommon'].copy()

    # Custom list of minors (Business Deposits)
    minors = [
        'CK24', # 1st Business Checking
        'CK12', # Business Checking
        'CK25', # Simple Business Checking
        'CK30', # Business Elite Money Market
        'CK19', # Business Money Market
        'CK22', # Business Premium Plus MoneyMkt
        'CK23', # Premium Business Checking
        'CK40', # Community Assoc Reserve
        'CD67', # Commercial Negotiated Rate
        'CD01', # 1 Month Business CD
        'CD07', # 3 Month Business CD
        'CD17', # 6 Month Business CD
        'CD31', # 1 Year Business CD
        'CD35', # 1 Year Business CD
        'CD37', # 18 Month Business CD
        'CD38', # 2 Year Business CD
        'CD50', # 3 Year Business CD
        'CD53', # 4 Year Business CD
        'CD59', # 5 Year Business CD
        'CD76', # 9 Month Business CD
        'CD84', # 15 Month Business CD
        'CD95', # Business <12 Month Simple CD
        'CD96', # Business >12 Month Simple CD
        'CK28', # Investment Business Checking
        'CK33', # Specialty Business Checking
        'CK34', # ICS Shadow - Business - Demand
        'SV06' # Business Select High Yield
    ]

    acctcommon_schema = {
        'noteintrate': float,
        'bookbalance': float
    }

    acctcommon = src.cdutils.input_cleansing.enforce_schema(acctcommon, acctcommon_schema).copy()



    def filter_to_business_deposits(df: pd.DataFrame, minors: List) -> pd.DataFrame:
        """
        Filter the total deposit account dataset to specific business minors
        """
        df = df[df['currmiaccttypcd'].isin(minors)].copy()
        return df

    df_filtered = filter_to_business_deposits(acctcommon, minors)

    df_filtered = df_filtered.sort_values(by='contractdate').copy()

    
    # df_filtered['contractdate'] = pd.to_datetime(df_filtered['contractdate']).dt.strftime('%m/%d/%Y')
    # df_filtered['effdate'] = pd.to_datetime(df_filtered['effdate']).dt.strftime('%m/%d/%Y')

    # Write out to excel
    OUTPUT_PATH = Path('./output/business_deposit_report_2025_YTD.xlsx')
    df_filtered.to_excel(OUTPUT_PATH, sheet_name='Sheet1', engine='openpyxl', index=False)

    src.output_to_excel.format_excel_file(OUTPUT_PATH)

    # Usage
    recipients = [
        # "chad.doorley@bcsbmail.com"
        "hasan.ali@bcsbmail.com",
        "becky.velazquez@bcsbmail.com"
    ]
    bcc_recipients = [
        "chad.doorley@bcsbmail.com",
        "businessintelligence@bcsbmail.com"
    ]
    subject = f"Business Deposits YTD (as of most recent Month End)" 
    body = "Hi all, \n\nAttached is the Business Deposits YTD report. If you have any questions, please reach out to BusinessIntelligence@bcsbmail.com\n"
    attachment_paths = [OUTPUT_PATH]

    cdutils.distribution.email_out(
        recipients = recipients, 
        bcc_recipients = bcc_recipients, 
        subject = subject, 
        body = body, 
        attachment_paths = attachment_paths
        )

if __name__ == '__main__':
    print(f"Starting YTD Business Deposit Report [{__version__}]")
    # main(production_flag=True)
    main()
    print("Complete!")







