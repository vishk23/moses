"""
Creating the deposit file
"""

from pathlib import Path
from datetime import datetime
from dateutil.relativedelta import relativedelta # type: ignore
from typing import Tuple

from sqlalchemy import text # type: ignore
import pandas as pd # type: ignore 

import src.cdutils.database.connect
import src.cdutils.caching
import src.deposit_file

def fetch_data():
     # acctcommon
    # engine 1
    acctcommon = text("""
    SELECT 
        a.ACCTNBR, 
        a.EFFDATE, 
        a.MJACCTTYPCD, 
        a.PRODUCT,
        a.NOTEBAL,
        a.NOTEMTDAVGBAL, 
        a.CURRMIACCTTYPCD,  
        a.ACCTOFFICER, 
        a.OWNERSORTNAME, 
        a.CURRACCTSTATCD, 
        a.CONTRACTDATE 
    FROM 
        OSIBANK.WH_ACCTCOMMON a
    WHERE 
        a.CURRACCTSTATCD IN ('ACT','DORM','IACT') AND
        a.MJACCTTYPCD IN ('TD','CK','SAV')
    """)

    # Need to define a range to encapsulate the trailing 12 month ends
    current_date = datetime.now()
    year_ago_date = current_date - relativedelta(years=1, months=1)
    current_date = current_date.strftime('%Y-%m-%d')+' 00:00:00'
    year_ago_date = year_ago_date.strftime('%Y-%m-%d')+' 00:00:00'

    historical_acctcommon = text(f"""
    SELECT 
        a.ACCTNBR, 
        a.EFFDATE,
        a.MONTHENDYN,
        a.NOTEMTDAVGBAL
    FROM 
        COCCDM.WH_ACCTCOMMON a
    WHERE
        a.CURRACCTSTATCD IN ('ACT','DORM','IACT') AND
        a.MJACCTTYPCD IN ('TD','CK','SAV') AND
        a.MONTHENDYN = 'Y' AND
        a.EFFDATE BETWEEN TO_DATE('{year_ago_date}', 'yyyy-mm-dd hh24:mi:ss') AND TO_DATE('{current_date}', 'yyyy-mm-dd hh24:mi:ss')
    """)

    wh_deposit = text("""
    SELECT 
        a.ACCTNBR, 
        a.YTDAVGBAL
    FROM 
        OSIBANK.WH_DEPOSIT a
    """)

    acctstatistichist = text("""
    SELECT 
        *
    FROM 
        OSIBANK.ACCTSTATISTICHIST
    """)

    househldacct = text("""
    SELECT 
        a.ACCTNBR,
        a.HOUSEHOLDNBR,
        a.DATELASTMAINT
    FROM 
        OSIEXTN.HOUSEHLDACCT a
    """)

    queries = [
        {'key':'acctcommon', 'sql':acctcommon, 'engine':1},
        {'key':'historical_acctcommon', 'sql':historical_acctcommon, 'engine':2},
        {'key':'wh_deposit', 'sql':wh_deposit, 'engine':1},
        {'key':'acctstatistichist', 'sql':acctstatistichist, 'engine':1},
        {'key':'househldacct', 'sql':househldacct, 'engine':1},
    ]

    data = src.cdutils.database.connect.retrieve_data(queries)
    return data

def filter_on_trailing_months(historical_accounts: pd.DataFrame, trailing_months: int) -> pd.DataFrame:
    """
    Computes the trailing 3-month and 12-month averages for each despoit account

    Args:
        historical_accounts (pd.DataFrame): trailing 12 months of data

    Returns:
        df (pd.DataFrame): df with one row per account containing 3 month average and 12 month average
    """
    if "acctnbr" not in historical_accounts.columns:
        raise ValueError("acctnbr missing")
    if "effdate" not in historical_accounts.columns:
        raise ValueError("effdate missing")

    df = historical_accounts.copy()
    
    df["effdate"] = pd.to_datetime(df["effdate"])
    df["notemtdavgbal"] = pd.to_numeric(df["notemtdavgbal"], errors="coerce")
    df["notemtdavgbal"] = df["notemtdavgbal"].fillna(0)

    distinct_dates = df["effdate"].drop_duplicates().sort_values(ascending=False)

    recent_dates = distinct_dates.head(trailing_months)

    filtered_df = df[df["effdate"].isin(recent_dates)]

    filtered_df = filtered_df.sort_values("effdate", ascending=False)

    return filtered_df

def get_year_ago_bal(historical_accounts: pd.DataFrame, trailing_months: int = 13) -> pd.DataFrame:
    """
    Gets the max value from effective date to 

    Args:
        historical_accounts (pd.DataFrame): trailing 12 months of data

    Returns:
        df (pd.DataFrame): df with one row per account containing 3 month average and 12 month average
    """
    ##### This needs work next focus session
    
    if "acctnbr" not in historical_accounts.columns:
        raise ValueError("acctnbr missing")
    if "effdate" not in historical_accounts.columns:
        raise ValueError("effdate missing")

    df = historical_accounts.copy()
    
    df["effdate"] = pd.to_datetime(df["effdate"])
    df["notemtdavgbal"] = pd.to_numeric(df["notemtdavgbal"], errors="coerce")

    distinct_dates = df["effdate"].drop_duplicates().sort_values(ascending=False)

    recent_dates = distinct_dates.head(trailing_months)
    min_date = recent_dates.min()
    filtered_df = df[df["effdate"] == min_date].copy()
    
    filtered_df["notemtdavgbal"] = filtered_df["notemtdavgbal"].fillna(0)
    filtered_df = filtered_df.rename(columns={'notemtdavgbal': 'Year Ago Balance'})
    filtered_df = filtered_df[['acctnbr','Year Ago Balance']].copy()
    return filtered_df

def average_balance_over_period(df: pd.DataFrame, col_output_name: str) -> pd.DataFrame:
    """
    Create an average for the "notemtdavgbal" column, to get trailing average
    """
    grouped_df = df.groupby('acctnbr')['notemtdavgbal'].mean().reset_index()

    grouped_df = grouped_df.rename(columns={'notemtdavgbal': col_output_name})
    return grouped_df

def filter_acctstatistic(acctstatistic: pd.DataFrame, start_date: datetime, end_date: datetime, prefix: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Filters the account statistics DataFrame for a given date range and computes
    the sum of statistic_count for DOD and NSF statistic types, grouped by account number.
    
    Parameters:
    - acctstatistic: pd.DataFrame - Input DataFrame with account statistics (columns: 'acctnbr', 'yearnbr', 
      'monthcd', 'statistictypecd', 'statistic_count').
    - start_date: datetime - Start date of the period (inclusive).
    - end_date: datetime - End date of the period (inclusive).
    - prefix: str - Prefix for output column names (e.g., 'TTM' for trailing twelve months, 'YTD' for year-to-date).
    
    Returns:
    - tuple[pd.DataFrame, pd.DataFrame]: Two DataFrames:
        - DOD DataFrame with columns 'acctnbr' and '{prefix}_DAYS_OVERDRAWN'.
        - NSF DataFrame with columns 'acctnbr' and '{prefix}_NSF_COUNT'.
    """
    # Create a copy to avoid modifying the input DataFrame
    df = acctstatistic.copy()
    
    # Create statistic_date from yearnbr and monthcd (first day of the month)
    df['statistic_date'] = pd.to_datetime(
        df['yearnbr'].astype(str) + '-' +
        df['monthcd'].astype(str).str.zfill(2) + '-01'
    )
    
    # Filter for rows within the specified date range
    df = df[(df['statistic_date'] >= start_date) & (df['statistic_date'] <= end_date)].copy()
    
    # DOD: Filter, group, and sum statistic_count
    dod = df[df['statistictypcd'] == "DOD"].copy()
    dod_grouped = dod.groupby('acctnbr')['statisticcount'].sum().reset_index()
    dod_grouped = dod_grouped.rename(columns={'statisticcount': f"{prefix}_DAYS_OVERDRAWN"})
    
    # NSF: Filter, group, and sum statistic_count
    nsf = df[df['statistictypcd'] == "NSF"].copy()
    nsf_grouped = nsf.groupby('acctnbr')['statisticcount'].sum().reset_index()
    nsf_grouped = nsf_grouped.rename(columns={'statisticcount': f"{prefix}_NSF_COUNT"})
    
    # Return the two DataFrames
    return dod_grouped, nsf_grouped

def quality_control_and_merging(
        acctcommon: pd.DataFrame, 
        wh_deposits: pd.DataFrame, 
        three_month_avg: pd.DataFrame, 
        twelve_month_avg: pd.DataFrame,
        year_ago_bal: pd.DataFrame,
        dod_ttm: pd.DataFrame, 
        nsf_ttm: pd.DataFrame,
        dod_ytd: pd.DataFrame,
        nsf_ytd: pd.DataFrame,
        ) -> pd.DataFrame:
    """
    Bringing all the fields together to build daily deposit dataset
    """

    assert wh_deposits['acctnbr'].is_unique, "Duplicates exist"
    assert three_month_avg['acctnbr'].is_unique, "Duplicates exist"
    assert twelve_month_avg['acctnbr'].is_unique, "Duplicates exist"
    assert year_ago_bal['acctnbr'].is_unique, "Duplicates exist"
    assert dod_ttm['acctnbr'].is_unique, "Duplicates exist"
    assert nsf_ttm['acctnbr'].is_unique, "Duplicates exist"
    assert dod_ytd['acctnbr'].is_unique, "Duplicates exist"
    assert nsf_ytd['acctnbr'].is_unique, "Duplicates exist"

    df = pd.merge(acctcommon, wh_deposits, on='acctnbr', how='left')
    df = pd.merge(df, three_month_avg, on='acctnbr', how='left')
    df = pd.merge(df, twelve_month_avg, on='acctnbr', how='left')
    df = pd.merge(df, year_ago_bal, on='acctnbr', how='left')
    df = pd.merge(df, dod_ttm, on='acctnbr', how='left')
    df = pd.merge(df, nsf_ttm, on='acctnbr', how='left')
    df = pd.merge(df, dod_ytd, on='acctnbr', how='left')
    df = pd.merge(df, nsf_ytd, on='acctnbr', how='left')


    numeric_cols = ['notebal','notemtdavgbal','ytdavgbal','3Mo_AvgBal','TTM_AvgBal','Year Ago Balance','TTM_DAYS_OVERDRAWN','TTM_NSF_COUNT','YTD_DAYS_OVERDRAWN','YTD_NSF_COUNT']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col])
        df[col] = df[col].fillna(0)
    return df


def add_householdnbr(df, househldacct):
    """
    Mergine acctcommon & household dataframes
    """
    househldacct = househldacct.sort_values(by='datelastmaint', ascending=False).drop_duplicates(subset='acctnbr', keep='first').copy()
    assert househldacct['acctnbr'].is_unique, "Duplicates found"
    merged_df = pd.merge(df, househldacct, on='acctnbr', how='left')
    return merged_df


    
