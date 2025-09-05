"""
Fetching data module. Aim is import all necessary fields up front, but if needed, you can define another function to be called here.

Usage:
    import src.cdutils.database

You need to set your own date that you want to see in effective date embedded in the SQL Query
"""

"""
Fetching data module. Aim is import all necessary fields up front, but if needed, you can define another function to be called here.

Usage:
    import src.cdutils.database

You need to set your own date that you want to see in effective date embedded in the SQL Query
"""

import cdutils.database.connect # type: ignore
from sqlalchemy import text # type: ignore
from datetime import datetime, timedelta
from typing import Optional, Tuple

# Define fetch data here using cdutils.database.connect
# There are often fetch_data.py files already in project if migrating
# This is an oracle DB so SQL syntax should match oracle.

def _get_trailing_month_dates() -> Tuple[datetime.date, datetime.date]:
    """
    Calculates the start and end date of the previous full month.
    
    Returns:
        A tuple containing the start date and end date of the trailing month.
    """
    today = datetime.today()
    # 1. Get the first day of the current month
    first_day_of_current_month = today.replace(day=1)
    # 2. Subtract one day to get the last day of the previous month
    end_of_trailing_month = first_day_of_current_month - timedelta(days=1)
    # 3. Get the first day of that previous month
    start_of_trailing_month = end_of_trailing_month.replace(day=1)
    
    return start_of_trailing_month, end_of_trailing_month


def fetch_advances():
    """
    Main data query for WH_RTXN.
    
    Filters for transactions in the trailing month that meet the criteria:
    - RTXNTYPCD = 'PDSB'
    - RTXNSTATCD = 'C'
    """
    # Define start & end dates for the trailing month
    start_date, end_date = _get_trailing_month_dates()

    # NOTE: Using bind parameters (:start_date, :end_date) is safer than f-strings.
    wh_rtxn = text("""
    SELECT
        a.*
    FROM
        COCCDM.WH_RTXN a
    WHERE
        a.RTXNTYPCD = 'PDSB'
        AND a.RTXNSTATCD = 'C'
        AND a.RUNDATE BETWEEN TO_DATE(:start_date, 'YYYY-MM-DD') AND TO_DATE(:end_date, 'YYYY-MM-DD')
    """)

    queries = [
        {
            'key': 'wh_rtxn',
            'sql': wh_rtxn.bindparams(
                start_date=start_date.strftime('%Y-%m-%d'),
                end_date=end_date.strftime('%Y-%m-%d')
            ),
            'engine': 2
        },
    ]

    data = cdutils.database.connect.retrieve_data(queries)
    return data


def fetch_payment_table():
    """
    Main data query for WH_TOTALPAYMENTSDUE.

    Filters for data within the trailing month based on RUNDATE.
    """
    # Define start & end dates for the trailing month
    start_date, end_date = _get_trailing_month_dates()
    
    # NOTE: Using bind parameters (:start_date, :end_date) is safer than f-strings.
    wh_totalpaymentsdue = text("""
    SELECT
        a.*
    FROM
        COCCDM.WH_TOTALPAYMENTSDUE a
    """)
#    WHERE
#        a.RUNDATE BETWEEN TO_DATE(:start_date, 'YYYY-MM-DD') AND TO_DATE(:end_date, 'YYYY-MM-DD')

    queries = [
        {
            'key': 'wh_totalpaymentsdue',
            'sql': wh_totalpaymentsdue,           ),
            'engine': 2
        },
    ]

# 'sql': wh_totalpaymentsdue.bindparams(
 #              start_date=start_date.strftime('%Y-%m-%d'),
 #               end_date=end_date.strftime('%Y-%m-%d')


    data = cdutils.database.connect.retrieve_data(queries)
    return data
