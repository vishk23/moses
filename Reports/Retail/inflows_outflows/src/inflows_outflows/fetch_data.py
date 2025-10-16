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

def fetch_data():
    """
    Main data query
    """

    wh_rtxn = text(f"""
    SELECT
        *
    FROM
        COCCDM.WH_RTXN
    """)

    wh_rtxnbal = text(f"""
    SELECT
        r.*,
        b.*
    FROM
        COCCDM.WH_RTXN r
    JOIN
        COCCDM.WH_RTXNBAL b
    ON
        r.rtxnnbr = b.rtxnnbr
        AND r.rundate = b.rundate
    ORDER BY
        r.rundate DESC
    LIMIT 10000
    """)

    queries = [
        {'key':'wh_rtxn', 'sql':wh_rtxn, 'engine':2},
        {'key':'wh_rtxnbal', 'sql':wh_rtxnbal, 'engine':2},
    ]

    data = cdutils.database.connect.retrieve_data(queries)
    return data
