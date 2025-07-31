"""
Deposit File Creation
"""
from pathlib import Path
from datetime import datetime
from dateutil.relativedelta import relativedelta

import pandas as pd # type: ignore

import src.deposit_file.create_deposit_dataset

def deposit_dataset_execution():
    data = src.deposit_file.create_deposit_dataset.fetch_data()

    # Unpack data
    acctcommon = data['acctcommon'].copy()
    acctstatistichist = data['acctstatistichist'].copy()
    wh_deposits = data['wh_deposit'].copy()
    historical_acctcommon = data['historical_acctcommon'].copy()
    househldacct = data['househldacct']


    three_month_df = src.deposit_file.create_deposit_dataset.filter_on_trailing_months(historical_acctcommon, 3)
    # three_month_df.to_excel(Path('ThreeMonthCheck.xlsx',index=False))
    twelve_month_df = src.deposit_file.create_deposit_dataset.filter_on_trailing_months(historical_acctcommon, 12)
    # twelve_month_df.to_excel(Path('TwelveMonthCheck.xlsx',index=False))

    year_ago_bal = src.deposit_file.create_deposit_dataset.get_year_ago_bal(historical_acctcommon)
    # Example usage

    three_month_avg = src.deposit_file.create_deposit_dataset.average_balance_over_period(three_month_df, '3Mo_AvgBal')
    twelve_month_avg = src.deposit_file.create_deposit_dataset.average_balance_over_period(twelve_month_df, 'TTM_AvgBal')

    # Current date
    current_date = datetime.now()
    
    # TTM: Trailing Twelve Months
    start_date_ttm = (current_date - relativedelta(years=1)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_date_ttm = current_date
    dod_ttm, nsf_ttm = src.deposit_file.create_deposit_dataset.filter_acctstatistic(acctstatistichist, start_date_ttm, end_date_ttm, prefix="TTM")
    
    # YTD: Year-to-Date
    start_date_ytd = datetime(current_date.year, 1, 1)
    end_date_ytd = current_date
    dod_ytd, nsf_ytd = src.deposit_file.create_deposit_dataset.filter_acctstatistic(acctstatistichist, start_date_ytd, end_date_ytd, prefix="YTD")
    

    df = src.deposit_file.create_deposit_dataset.quality_control_and_merging(
        acctcommon, 
        wh_deposits, 
        three_month_avg, 
        twelve_month_avg, 
        year_ago_bal, 
        dod_ttm, 
        nsf_ttm,
        dod_ytd,
        nsf_ytd
    )
    
    df = src.deposit_file.create_deposit_dataset.add_householdnbr(df, househldacct)

    # Match to existing daily deposit (but there are more columns here that could be used)
    rename_mapping = {
        "mjaccttypcd":"MAJOR",
        "currmiaccttypcd":"MINOR",
        "product":"PRODUCT",
        "curracctstatcd":"STATUS",
        "acctnbr":"ACCTNBR",
        "ownersortname":"OWNERNAME",
        "acctofficer":"ACCTOFFICER",
        "notebal":"NOTEBAL",
        "TTM_AvgBal":"TTM Average Balance",
        "TTM_DAYS_OVERDRAWN":"TTM Overdrafts",
        "ytdavgbal":"YTDAVGBAL",
        "YTD_DAYS_OVERDRAWN":"YTD Overdrafts",
        "effdate":"EFFDATE",
        "contractdate":"CONTRACTDATE",
        "householdnbr":"HOUSEHOLDNBR"

    }

    desired_order = [
        "MAJOR",
        "MINOR",
        "PRODUCT",
        "STATUS",
        "ACCTNBR",
        "OWNERNAME",
        "ACCTOFFICER",
        "NOTEBAL",
        "TTM Average Balance",
        "TTM Overdrafts",
        "YTDAVGBAL",
        "YTD Overdrafts",
        "HOUSEHOLDNBR",
        "EFFDATE",
        "CONTRACTDATE"
    ]

    dropin_deposit_df = df.rename(columns=rename_mapping).loc[:,desired_order].copy()

    return df, dropin_deposit_df
