# """
# Creating the deposit file
# """

# from pathlib import Path
# from datetime import datetime
# from dateutil.relativedelta import relativedelta # type: ignore

# from sqlalchemy import text # type: ignore
# import pandas as pd # type: ignore 

# import src.cdutils.database.connect
# import src.cdutils.caching
# import src.deposit_file

# def fetch_data():
#      # acctcommon
#     # engine 1
#     acctcommon = text("""
#     SELECT 
#         a.ACCTNBR, 
#         a.EFFDATE, 
#         a.MJACCTTYPCD, 
#         a.PRODUCT,
#         a.NOTEBAL,
#         a.NOTEMTDAVGBAL, 
#         a.CURRMIACCTTYPCD,  
#         a.ACCTOFFICER, 
#         a.OWNERSORTNAME, 
#         a.CURRACCTSTATCD, 
#         a.CONTRACTDATE 
#     FROM 
#         OSIBANK.WH_ACCTCOMMON a
#     WHERE 
#         a.CURRACCTSTATCD IN ('ACT','DORM','IACT') AND
#         a.MJACCTTYPCD IN ('TD','CK','SAV')
#     """)

#     # Need to define a range to encapsulate the trailing 12 month ends
#     current_date = datetime.now()
#     year_ago_date = current_date - relativedelta(years=1, months=1)
#     current_date = current_date.strftime('%Y-%m-%d')+' 00:00:00'
#     year_ago_date = year_ago_date.strftime('%Y-%m-%d')+' 00:00:00'

#     historical_acctcommon = text(f"""
#     SELECT 
#         a.ACCTNBR, 
#         a.EFFDATE,
#         a.MONTHENDYN,
#         a.NOTEMTDAVGBAL
#     FROM 
#         COCCDM.WH_ACCTCOMMON a
#     WHERE
#         a.CURRACCTSTATCD IN ('ACT','DORM','IACT') AND
#         a.MJACCTTYPCD IN ('TD','CK','SAV') AND
#         a.MONTHENDYN = 'Y' AND
#         a.EFFDATE BETWEEN TO_DATE('{year_ago_date}', 'yyyy-mm-dd hh24:mi:ss') AND TO_DATE('{current_date}', 'yyyy-mm-dd hh24:mi:ss')
#     """)

#     wh_deposit = text("""
#     SELECT 
#         a.ACCTNBR, 
#         a.YTDAVGBAL
#     FROM 
#         OSIBANK.WH_DEPOSIT a
#     """)

#     househldacct = text("""
#     SELECT 
#         a.HOUSEHOLDNBR, 
#         a.ACCTNBR
#     FROM 
#         OSIEXTN.HOUSEHLDACCT a
#     """)

#     acctstatistichist = text("""
#     SELECT 
#         *
#     FROM 
#         OSIBANK.ACCTSTATISTICHIST
#     """)

#     queries = [
#         {'key':'acctcommon', 'sql':acctcommon, 'engine':1},
#         {'key':'historical_acctcommon', 'sql':historical_acctcommon, 'engine':2},
#         {'key':'wh_deposit', 'sql':wh_deposit, 'engine':1},
#         {'key':'househldacct', 'sql':househldacct, 'engine':1},
#         {'key':'acctstatistichist', 'sql':acctstatistichist, 'engine':1},
#     ]

#     data = src.cdutils.database.connect.retrieve_data(queries)
#     return data

# def filter_on_trailing_months(historical_accounts: pd.DataFrame, trailing_months: int) -> pd.DataFrame:
#     """
#     Computes the trailing 3-month and 12-month averages for each despoit account

#     Args:
#         historical_accounts (pd.DataFrame): trailing 12 months of data

#     Returns:
#         df (pd.DataFrame): df with one row per account containing 3 month average and 12 month average
#     """
#     if "acctnbr" not in historical_accounts.columns:
#         raise ValueError("acctnbr missing")
#     if "effdate" not in historical_accounts.columns:
#         raise ValueError("effdate missing")

#     df = historical_accounts.copy()
    
#     df["effdate"] = pd.to_datetime(df["effdate"])

#     distinct_dates = df["effdate"].drop_duplicates().sort_values(ascending=False)

#     recent_dates = distinct_dates.head(trailing_months)

#     filtered_df = df[df["effdate"].isin(recent_dates)]

#     filtered_df = filtered_df.sort_values("effdate", ascending=False)

#     return filtered_df

# def 

