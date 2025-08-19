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
        a.EFFDATE, 
        a.MJACCTTYPCD, 
        a.PRODUCT, 
        a.CURRMIACCTTYPCD, 
        a.BOOKBALANCE, 
        a.LOANOFFICER, 
        a.OWNERNAME, 
        a.CURRACCTSTATCD, 
        a.CONTRACTDATE, 
        a.NOTEBAL
    FROM 
        OSIBANK.WH_ACCTCOMMON a
    WHERE 
        a.CURRACCTSTATCD IN ('ACT','NPFM')
    """)

    acctloan = text("""
    SELECT 
        a.ACCTNBR, 
        a.COBAL, 
        a.CREDITLIMITAMT, 
        a.RISKRATINGCD, 
        a.TOTALPCTSOLD, 
        a.CREDLIMITCLATRESAMT
    FROM 
        OSIBANK.WH_ACCTLOAN a
    """)

    loans = text("""
    SELECT 
        a.ACCTNBR, 
        a.AVAILBALAMT
    FROM 
        OSIBANK.WH_LOANS a
    """)

    househldacct = text("""
    SELECT 
        a.HOUSEHOLDNBR, 
        a.ACCTNBR
    FROM 
        OSIEXTN.HOUSEHLDACCT a
    """)

    allroles = text("""
    SELECT 
        *
    FROM 
        OSIBANK.WH_ALLROLES a
    WHERE
        a.ACCTROLECD IN ('GUAR')
    """)

    pers = text("""
    SELECT 
        a.PERSNBR,
        a.FIRSTNAME,
        a.LASTNAME,
        a.DATEBIRTH,
        a.DEATHNOTIFICATIONDATE
    FROM 
        OSIBANK.PERS a
    """)

    viewperstaxid = text("""
    SELECT 
        *
    FROM 
        OSIBANK.VIEWPERSTAXID
    """)

    acctstatistichist = text("""
    SELECT 
        *
    FROM 
        OSIBANK.ACCTSTATISTICHIST
    """)

    acctloanlimithist = text("""
    SELECT 
        *
    FROM 
        OSIBANK.ACCTLOANLIMITHIST
    """)

    queries = [
        {'key':'acctcommon', 'sql':acctcommon, 'engine':1},
        {'key':'acctloan', 'sql':acctloan, 'engine':1},
        {'key':'loans', 'sql':loans, 'engine':1},
        {'key':'househldacct', 'sql':househldacct, 'engine':1},
        {'key':'allroles', 'sql':allroles, 'engine':1},
        {'key':'pers', 'sql':pers, 'engine':1},
        {'key':'viewperstaxid', 'sql':viewperstaxid, 'engine':1},
        {'key':'acctstatistichist', 'sql':acctstatistichist, 'engine':1},
        {'key':'acctloanlimithist', 'sql':acctloanlimithist, 'engine':1},
    ]

    data = src.cdutils.database.connect.retrieve_data(queries)
    return data