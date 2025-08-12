# Database query - Transactions

import cdutils.database.connect # type: ignore
from sqlalchemy import text # type: ignore
from datetime import datetime, timedelta
from typing import Optional

def fetch_transactions_window(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    window_size_days: int = 365
) -> list:
    """
    Fetch transactions within a specified date window from the database.
    :param start_date: The start date for the transaction window. If None, defaults to today minus window size.
    :param end_date: The end date for the transaction window. If None, defaults to today.
    :param window_size_days: The number of days to look back from the end date.
    :return: A list of transactions within the specified date range.
    """
    
    if start_date is None:
        start_date = datetime.now() - timedelta(days=window_size_days)
    
    if end_date is None:
        end_date = datetime.now()

    query = text(f"""
        SELECT 
            * 
        FROM
            COCCDM.WH_RTXN a
        WHERE 
            (a.RUNDATE >= TO_DATE('{start_date.strftime('%Y-%m-%d')}', 'YYYY-MM-DD')) 
            AND (a.RUNDATE <= TO_DATE('{end_date.strftime('%Y-%m-%d')}', 'YYYY-MM-DD'))
            AND (a.CURRRTXNSTATCD = 'C')
        ORDER BY RUNDATE DESC
    """)

    queries = [
        {'key': 'query','sql': query,'engine':2}
    ]
    data = cdutils.database.connect.retrieve_data(queries)
    return data

def fetch_transactions_window_test(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    window_size_days: int = 365
) -> list:
    """
    Fetch transactions within a specified date window from the database.
    :param start_date: The start date for the transaction window. If None, defaults to today minus window size.
    :param end_date: The end date for the transaction window. If None, defaults to today.
    :param window_size_days: The number of days to look back from the end date.
    :return: A list of transactions within the specified date range.
    """
    
    if start_date is None:
        start_date = datetime.now() - timedelta(days=window_size_days)
    
    if end_date is None:
        end_date = datetime.now()

    query = text(f"""
        SELECT 
            * 
        FROM
            COCCDM.WH_RTXN a
        WHERE 
            (a.RUNDATE >= TO_DATE('{start_date.strftime('%Y-%m-%d')}', 'YYYY-MM-DD')) 
            AND (a.RUNDATE <= TO_DATE('{end_date.strftime('%Y-%m-%d')}', 'YYYY-MM-DD'))
            AND (a.CURRRTXNSTATCD = 'C')
        ORDER BY RUNDATE DESC
        FETCH FIRST 100000 ROWS ONLY
    """)

    queries = [
        {'key': 'query','sql': query,'engine':2}
    ]
    data = cdutils.database.connect.retrieve_data(queries)
    return data

### Fetching account data

def fetch_account_data(specified_date: Optional[datetime] = None):
    """
    Main data query
    """
    if specified_date is None:
        specified_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    else:
        assert isinstance(specified_date, datetime), "Specified date must be a datetime object"
        specified_date = specified_date.strftime('%Y-%m-%d %H:%M:%S')

    wh_acctcommon = text(f"""
    SELECT
        a.ACCTNBR,
        a.BRANCHNAME,
        a.PRIMARYOWNERCITY,
        a.PRIMARYOWNERSTATE,
        a.TAXRPTFORPERSNBR,
        a.TAXRPTFORORGNBR,
        a.MJACCTTYPCD,
        a.ACCTOFFICER,
        a.LOANOFFICER
    FROM
        COCCDM.WH_ACCTCOMMON a
    WHERE
        (a.CURRACCTSTATCD IN ('ACT','NPFM','DORM')) AND
        (a.EFFDATE = TO_DATE('{specified_date}', 'YYYY-MM-DD HH24:MI:SS'))
    """)

    queries = [
        {'key':'wh_acctcommon', 'sql':wh_acctcommon, 'engine':2},
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data
