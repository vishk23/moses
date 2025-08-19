"""
Fetching data module. Aim is import all necessary fields up front, but if needed, you can define another function to be called here.

Usage:
    import src.cdutils.database
"""

import cdutils.database.connect
from sqlalchemy import text # type: ignore

def fetch_data_nov23():
     # acctcommon
    # engine 1
    acctcommon = text("""
    SELECT 
        a.ACCTNBR, 
        a.EFFDATE, 
        a.MJACCTTYPCD, 
        a.PRODUCT, 
        a.CURRMIACCTTYPCD, 
        a.BOOKBALANCE, 
        a.ACCTOFFICER, 
        a.OWNERSORTNAME, 
        a.CURRACCTSTATCD, 
        a.CONTRACTDATE, 
        a.BRANCHNAME,
        a.NOTEINTRATE,
        a.PRIMARYOWNERCITY,
        a.PRIMARYOWNERSTATE
    FROM 
        COCCDM.WH_ACCTCOMMON a
    WHERE 
        a.CURRACCTSTATCD IN ('ACT','DORM') AND
        (a.MJACCTTYPCD IN ('CK','SAV','TD')) AND
        (a.EFFDATE = TO_DATE('2023-11-01 00:00:00','yyyy-mm-dd hh24:mi:ss'))
    """)

    queries = [
        {'key':'acctcommon', 'sql':acctcommon, 'engine':2},
    ]

    data = cdutils.database.connect.retrieve_data(queries)
    return data


def fetch_data_dec24():
     # acctcommon
    acctcommon = text("""
    SELECT 
        a.ACCTNBR, 
        a.EFFDATE, 
        a.MJACCTTYPCD, 
        a.PRODUCT, 
        a.CURRMIACCTTYPCD, 
        a.BOOKBALANCE, 
        a.ACCTOFFICER, 
        a.OWNERSORTNAME, 
        a.CURRACCTSTATCD, 
        a.CONTRACTDATE, 
        a.BRANCHNAME,
        a.NOTEINTRATE,
        a.PRIMARYOWNERCITY,
        a.PRIMARYOWNERSTATE
    FROM 
        COCCDM.WH_ACCTCOMMON a
    WHERE 
        a.CURRACCTSTATCD IN ('ACT','DORM') AND
        (a.MJACCTTYPCD IN ('CK','SAV','TD')) AND
        (a.EFFDATE = TO_DATE('2024-12-31 00:00:00','yyyy-mm-dd hh24:mi:ss'))
    """)

    queries = [
        {'key':'acctcommon', 'sql':acctcommon, 'engine':2},
    ]

    data = cdutils.database.connect.retrieve_data(queries)
    return data

def fetch_data_ytd():
     # acctcommon
    # engine 1
    acctcommon = text("""
    SELECT 
        a.ACCTNBR, 
        a.EFFDATE, 
        a.MJACCTTYPCD, 
        a.PRODUCT, 
        a.CURRMIACCTTYPCD, 
        a.BOOKBALANCE, 
        a.ACCTOFFICER, 
        a.OWNERSORTNAME, 
        a.CURRACCTSTATCD, 
        a.CONTRACTDATE, 
        a.BRANCHNAME,
        a.NOTEINTRATE,
        a.PRIMARYOWNERCITY,
        a.PRIMARYOWNERSTATE
    FROM 
        COCCDM.WH_ACCTCOMMON_ME a
    WHERE 
        a.CURRACCTSTATCD IN ('ACT','DORM') AND
        (a.MJACCTTYPCD IN ('CK','SAV','TD')) AND
        (a.CONTRACTDATE >= TO_DATE('2025-01-01 00:00:00', 'yyyy-mm-dd hh24:mi:ss'))
    """)

    queries = [
        {'key':'acctcommon', 'sql':acctcommon, 'engine':2},
    ]

    data = cdutils.database.connect.retrieve_data(queries)
    return data