"""
Fetching data module. Aim is import all necessary fields up front, but if needed, you can define another function to be called here.

Usage:
    import src.cdutils.database

You need to set your own date that you want to see in effective date embedded in the SQL Query
"""

import src.cdutils.database.connect
from sqlalchemy import text # type: ignore

def fetch_data():
    wh_acctcommon = text("""
    SELECT
        a.EFFDATE,
        a.ACCTNBR,
        a.PRODUCT,
        a.ACCTOFFICER,
        a.OWNERSORTNAME,
        a.MJACCTTYPCD,
        a.CURRMIACCTTYPCD,
        a.CURRACCTSTATCD,
        a.NOTEINTRATE,
        a.BOOKBALANCE,
        a.NOTEBAL,
        a.CONTRACTDATE,
        a.CLOSEDATE
    FROM
        OSIBANK.WH_ACCTCOMMON a
    WHERE
        (a.CURRACCTSTATCD IN ('ACT','DORM')) AND
        (a.MJACCTTYPCD IN ('CK','SAV','TD'))
    """)

    queries = [
        {'key':'wh_acctcommon', 'sql':wh_acctcommon, 'engine':1},
    ]

    data = src.cdutils.database.connect.retrieve_data(queries)
    return data


