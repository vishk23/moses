"""
Fetching data module. Aim is import all necessary fields up front, but if needed, you can define another function to be called here.

Usage:
    import src.cdutils.database
"""

import cdutils.database.connect
from sqlalchemy import text # type: ignore

def fetch_data():
     # acctcommon
    # engine 1
    acctcommon = text("""
    SELECT
        a.ACCTNBR,
        a.PRODUCT,
        a.OWNERSORTNAME,
        a.LOANOFFICER,
        a.NOTEBAL,
        a.BOOKBALANCE,
        a.CURRACCTSTATCD,
        a.MJACCTTYPCD,
        a.EFFDATE
    FROM 
        COCCDM.WH_ACCTCOMMON_ME a
    WHERE
        CURRACCTSTATCD IN ('ACT','NPFM')
        AND MJACCTTYPCD IN ('CML','CNS','MTG')


    """)

    acctloan = text("""
    SELECT
        a.ACCTNBR,
        a.CURRDUEDATE,
        a.COBAL,
        a.TOTALPAYMENTSDUE,
        a.TOTALPIDUE,
        a.TOTALPCTSOLD,
        a.RISKRATINGCD
    FROM 
        COCCDM.WH_ACCTLOAN_ME a
    """)


    totalpaymentsdue = text("""
    SELECT
        *
    FROM 
        COCCDM.WH_TOTALPAYMENTSDUE a
    """)

    acctstatistichist = text("""
    SELECT 
        *
    FROM 
        OSIBANK.ACCTSTATISTICHIST
    """)

    queries = [
        {'key':'acctcommon', 'sql':acctcommon, 'engine':2},
        {'key':'acctloan', 'sql':acctloan, 'engine':2},
        {'key':'totalpaymentsdue', 'sql':totalpaymentsdue, 'engine':2},
        {'key':'acctstatistichist', 'sql':acctstatistichist, 'engine':1},
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data