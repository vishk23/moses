"""
Business Deposit Account: Custom Date Range 
"""


from pathlib import Path
from typing import List

import pandas as pd # type: ignore

import src.cdutils.database
import src.cdutils.input_cleansing


def main():
    data = src.cdutils.database.fetch_data_custom()

    acctcommon = data['acctcommon'].copy()

    # Custom list of minors (Business)
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
    OUTPUT_PATH = Path('./output/business_deposit_report_custom_date_range.xlsx')
    df_filtered.to_excel(OUTPUT_PATH, sheet_name='Sheet1', engine='openpyxl', index=False)
    print("Complete!")

if __name__ == '__main__':
    main()






