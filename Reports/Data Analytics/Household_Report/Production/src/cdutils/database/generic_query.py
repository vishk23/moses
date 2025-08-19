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
        a.ACCTNBR,
        a.LOANOFFICER,
        a.ACCTOFFICER,
        a.OWNERSORTNAME,
        a.PRODUCT,
        a.CURRACCTSTATCD,
        a.NOTEBAL,
        a.BOOKBALANCE,
        a.NOTEINTRATE,
        a.DATEMAT,
        a.TAXRPTFORORGNBR,
        a.TAXRPTFORPERSNBR,
        a.CONTRACTDATE,
        a.MJACCTTYPCD,
        a.CURRMIACCTTYPCD
    FROM 
        OSIBANK.WH_ACCTCOMMON a
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
        {'key':'wh_acctcommon', 'sql':wh_acctcommon, 'engine':1},
        {'key':'househldacct', 'sql':househldacct, 'engine':1},
    ]

    data = src.cdutils.database.connect.retrieve_data(queries)
    return data


