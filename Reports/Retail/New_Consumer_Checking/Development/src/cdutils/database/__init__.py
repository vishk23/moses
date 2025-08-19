"""
Fetching data module. Aim is import all necessary fields up front, but if needed, you can define another function to be called here.

Usage:
    import src.cdutils.database
"""

import src.cdutils.database.connect
from sqlalchemy import text # type: ignore

def fetch_data():
     # acctcommon
    # engine 1
    acctcommon = text("""
    SELECT 
        a.ACCTNBR,
        a.MJACCTTYPCD,
        a.CURRMIACCTTYPCD,
        a.PRODUCT,
        a.OWNERSORTNAME,
        a.CURRACCTSTATCD,
        a.CONTRACTDATE,
        a.DATEMAT,
        a.BOOKBALANCE,
        a.NOTEINTRATE,
        a.TAXRPTFORORGNBR,
        a.TAXRPTFORPERSNBR,
        a.BRANCHNAME,
        a.ACCTOFFICER,
        a.EFFDATE
    FROM 
        COCCDM.WH_ACCTCOMMON a
    WHERE
        (a.MONTHENDYN = 'Y') AND
        (a.EFFDATE >= ADD_MONTHS(SYSDATE, -24)) AND
        (a.MJACCTTYPCD IN ('TD','CK','SAV')) AND
        (a.CURRACCTSTATCD IN ('ACT','DORM')) AND
        (a.CURRMIACCTTYPCD IN (
            'CK14',
            'CK02',
            'CK35',
            'CK04',
            'CK03',
            'CK05',
            'CK01',
            'CK06'))
    """)

    queries = [
        {'key':'acctcommon', 'sql':acctcommon, 'engine':2},
    ]

    data = src.cdutils.database.connect.retrieve_data(queries)
    return data