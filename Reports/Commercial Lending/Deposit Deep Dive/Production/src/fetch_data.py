"""
Fetching data module. Aim is import all necessary fields up front, but if needed, you can define another function to be called here.

Usage:
    import src.cdutils.database
"""

import src.cdutils.database.connect
from sqlalchemy import text # type: ignore

def fetch_data():
    effdates = text("""
    SELECT DISTINCT
        a.EFFDATE
    FROM 
        COCCDM.WH_ACCTCOMMON a
    WHERE
        MONTHENDYN = 'Y'
    ORDER BY EFFDATE DESC
    """)

    queries = [
        {'key':'effdates', 'sql':effdates, 'engine':2},
    ]

    data = src.cdutils.database.connect.retrieve_data(queries)

    effdates = data['effdates'].copy()

    recent_me = effdates['effdate'][0]
    prior_me = effdates['effdate'][1]

    recent_acctcommon = text(f"""
    SELECT 
        a.ACCTNBR,
        a.OWNERNAME,
        a.PRODUCT,
        a.LOANOFFICER,
        a.ACCTOFFICER,
        a.EFFDATE, 
        a.MJACCTTYPCD, 
        a.CURRMIACCTTYPCD,
        a.NOTEBAL,
        a.BOOKBALANCE,
        a.NOTEINTRATE,
        a.CURRACCTSTATCD, 
        a.CONTRACTDATE,
        a.DATEMAT,
        a.TAXRPTFORORGNBR,
        a.TAXRPTFORPERSNBR
    FROM 
        COCCDM.WH_ACCTCOMMON a
    WHERE
        a.EFFDATE = TO_DATE('{recent_me}', 'yyyy-mm-dd hh24:mi:ss')
        AND a.CURRACCTSTATCD IN ('ACT','DORM')
        AND a.MJACCTTYPCD IN ('CK','SAV','TD')
    """)

    prior_acctcommon = text(f"""
    SELECT 
        a.ACCTNBR,
        a.OWNERNAME,
        a.PRODUCT,
        a.LOANOFFICER,
        a.ACCTOFFICER,
        a.EFFDATE, 
        a.MJACCTTYPCD, 
        a.CURRMIACCTTYPCD,
        a.NOTEBAL,
        a.BOOKBALANCE,
        a.NOTEINTRATE,
        a.CURRACCTSTATCD, 
        a.CONTRACTDATE,
        a.DATEMAT,
        a.TAXRPTFORORGNBR,
        a.TAXRPTFORPERSNBR
    FROM 
        COCCDM.WH_ACCTCOMMON a
    WHERE
        a.EFFDATE = TO_DATE('{prior_me}', 'yyyy-mm-dd hh24:mi:ss')
        AND a.CURRACCTSTATCD IN ('ACT','DORM')
        AND a.MJACCTTYPCD IN ('CK','SAV','TD')
    """)

    queries = [
        {'key':'recent_acctcommon', 'sql':recent_acctcommon, 'engine':2},
        {'key':'prior_acctcommon', 'sql':prior_acctcommon, 'engine':2}
    ]

    data = src.cdutils.database.connect.retrieve_data(queries)
    return data