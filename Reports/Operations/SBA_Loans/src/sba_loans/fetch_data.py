
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


def fetch_org_pers_addr():

    persaddruse = text("""
    SELECT
        a.*
    FROM
        OSIBANK.PERSADDRUSE a
    """)

    orgaddruse = text("""
    SELECT
        a.*
    FROM
        OSIBANK.ORGADDRUSE a
    """)

    wh_addr = text("""
    SELECT
        a.*
    FROM
        OSIBANK.WH_ADDR a
    """)
    queries = [
        # {
        #     'key': 'wh_rtxn',
        #     'sql': wh_rtxn.bindparams(
        #         start_date=start_date.strftime('%Y-%m-%d'),
        #         end_date=end_date.strftime('%Y-%m-%d')
        #     ),
        #     'engine': 2
        # },
        {
            'key': 'orgaddruse',
            'sql': orgaddruse,
            'engine': 1
        },
        {
            'key': 'persaddruse',
            'sql': persaddruse,
            'engine': 1
        },
        {
            'key': 'wh_addr',
            'sql': wh_addr,
            'engine': 1
        },
    ]

    data = cdutils.database.connect.retrieve_data(queries)
    return data


