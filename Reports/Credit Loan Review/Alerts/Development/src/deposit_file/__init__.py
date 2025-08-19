"""
Deposit File Creation
"""
from pathlib import Path

import pandas as pd # type: ignore

import src.deposit_file.create_deposit_dataset

def deposit_dataset_execution():
    data = src.deposit_file.create_deposit_dataset.fetch_data()

    # Unpack data
    acctcommon = data['acctcommon'].copy()
    acctstatistichist = data['acctstatistichist'].copy()
    wh_deposits = data['wh_deposit'].copy()
    historical_acctcommon = data['historical_acctcommon'].copy()

    # # Cache
    # file_path = Path(r'c:\Users\w322800\Documents\deposit_caching')
    # src.cdutils.caching.cache_data(file_path, data)

    # # Unpack cached data
    # acctcommon = pd.read_csv(Path(r'C:\Users\w322800\Documents\deposit_caching\acctcommon.csv'))
    # acctstatistichist = pd.read_csv(Path(r'C:\Users\w322800\Documents\deposit_caching\acctstatistichist.csv'))
    # wh_deposits = pd.read_csv(Path(r'C:\Users\w322800\Documents\deposit_caching\wh_deposit.csv'))
    # historical_acctcommon = pd.read_csv(Path(r'C:\Users\w322800\Documents\deposit_caching\historical_acctcommon.csv'))

    three_month_df = src.deposit_file.create_deposit_dataset.filter_on_trailing_months(historical_acctcommon, 3)
    # three_month_df.to_excel(Path('ThreeMonthCheck.xlsx',index=False))
    twelve_month_df = src.deposit_file.create_deposit_dataset.filter_on_trailing_months(historical_acctcommon, 12)
    # twelve_month_df.to_excel(Path('TwelveMonthCheck.xlsx',index=False))
    
    three_month_avg = src.deposit_file.create_deposit_dataset.average_balance_over_period(three_month_df, '3Mo_AvgBal')
    twelve_month_avg = src.deposit_file.create_deposit_dataset.average_balance_over_period(twelve_month_df, 'TTM_AvgBal')

    dod, nsf = src.deposit_file.create_deposit_dataset.filter_acctstatistichist(acctstatistichist)

    return src.deposit_file.create_deposit_dataset.quality_control_and_merging(acctcommon, wh_deposits, three_month_avg, twelve_month_avg, dod, nsf)
