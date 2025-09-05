"""
Fetching data module. Aim is import all necessary fields up front, but if needed, you can define another function to be called here.

Usage:
    import src.cdutils.database

You need to set your own date that you want to see in effective date embedded in the SQL Query
"""

import cdutils.database.connect # type: ignore
from sqlalchemy import text # type: ignore
from datetime import datetime
from typing import Optional

# Define fetch data here using cdutils.database.connect
# There are often fetch_data.py files already in project if migrating
# This is an oracle DB so SQL syntax should match oracle.

def fetch_advances():
    """
    Main data query
    """
    # This needs to be the trailing month. So whatever month we are in, it should be 
    # Define current month and start & end dates
    # In the SQL query, we need to create a BETWEEN on a.RUNDATE

    wh_rtxn = text(f"""
    SELECT
        *
    FROM
        COCCDM.WH_RTXN a
    """)

    queries = [
        {'key':'wh_rtxn', 'sql':wh_rtxn, 'engine':2},
    ]

    data = cdutils.database.connect.retrieve_data(queries)
    return data


def fetch_payment_table():
    """
    Main data query
    """
    # This needs to be the trailing month. So whatever month we are in, it should be 
    # Define current month and start & end dates
    # In the SQL query, we need to create a BETWEEN on a.RUNDATE

    wh_totalpaymentsdue = text(f"""
    SELECT
        *
    FROM
        COCCDM.WH_TOTALPAYMENTSDUE a
    """)

    queries = [
        {'key':'wh_totalpaymentsdue', 'sql':wh_totalpaymentsdue, 'engine':2},
    ]

    data = cdutils.database.connect.retrieve_data(queries)
    return data