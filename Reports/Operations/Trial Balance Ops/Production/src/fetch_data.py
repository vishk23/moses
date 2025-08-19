"""
Fetching data module. Aim is import all necessary fields up front, but if needed, you can define another function to be called here.

Usage:
    import src.cdutils.database

You need to set your own date that you want to see in effective date embedded in the SQL Query
"""

import src.cdutils.database.connect
from sqlalchemy import text # type: ignore

def fetch_data():
    acctcommon = text("""
    SELECT 
        a.ACCTNBR,
        a.MJACCTTYPCD,
        a.CURRMIACCTTYPCD,
        a.PRODUCT,
        a.CURRACCTSTATCD,
        a.NOTEINTRATE,
        a.NOTENEXTRATECHANGEDATE,
        a.NOTERATECHANGECALPERCD,
        a.NOTEOPENAMT,
        a.NOTEBAL,
        a.BOOKBALANCE,
        a.NOTEINTCALCSCHEDNBR,
        a.CALCBALTYPCD,
        a.INTMETHCD,
        a.RATETYPCD,
        a.INTBASE,
        a.DATEMAT,
        a.CONTRACTDATE,
        a.OWNERNAME
    FROM 
        COCCDM.WH_ACCTCOMMON_ME a
    """)

    # Acctloan, engine 2
    acctloan = text("""
    SELECT 
        a.ACCTNBR, 
        a.COBAL,
        a.ESCBAL, 
        a.PURPCD,
        a.FDICCATCD,
        a.DATE1STPMTDUE,
        a.MINRATECHANGEDOWN, 
        a.MAXRATECHANGEDOWN, 
        a.PREPAYCHARGE,
        a.LASTPAYMENTDATE,
        a.NOTEACCRUEDINT
    FROM 
        COCCDM.WH_ACCTLOAN_ME a
    """)

    loans = text("""
    SELECT 
        a.ACCTNBR, 
        a.AVAILBALAMT,
        a.INTPAIDTODATE,
        a.FDICCATDESC,
        a.LOANIDX
    FROM 
        COCCDM.WH_LOANS_ME a
    """)

    prop = text("""
    SELECT
        a.ACCTNBR,
        a.PROPNBR,
        a.APRSVALUEAMT,
        a.APRSDATE,
        a.PROPADDR1,
        a.PROPADDR2,
        a.PROPADDR3,
        a.PROPCITY,
        a.PROPSTATE,
        a.PROPZIP
    FROM
        OSIBANK.WH_PROP a
    """)

    prop2 = text("""
    SELECT
        a.ACCTNBR,
        a.PROPTYPDESC,
        a.PROPNBR,
        a.PROPVALUE,
        a.PROPTYPCD,
        a.PROPDESC
    FROM
        OSIBANK.WH_PROP2 a
    """)

    queries = [
        {'key':'acctcommon', 'sql':acctcommon, 'engine':2},
        {'key':'acctloan', 'sql': acctloan, 'engine':2},
        {'key':'loans', 'sql': loans, 'engine':2},
        {'key':'prop', 'sql': prop, 'engine':1},
        {'key':'prop2', 'sql': prop2, 'engine':1},
    ]

    data = src.cdutils.database.connect.retrieve_data(queries)
    return data


