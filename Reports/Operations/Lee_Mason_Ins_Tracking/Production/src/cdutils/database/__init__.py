"""
Database Fetching Package

This package provides the ability to create custom SQL queries that can be used throughout the data pipeline.

Quick start:
    import src.cdutils.database

    # Simple data fetch
    data = src.cdutils.database.fetch_data()
"""

import src.cdutils.database.connect
from sqlalchemy import text # type: ignore
import pandas as pd # type: ignore

def fetch_data() -> pd.DataFrame:
    wh_acctcommon = text("""
    SELECT
        a.ACCTNBR,
        a.EFFDATE,
        a.OWNERSORTNAME,
        a.NOTEBAL,
        a.BOOKBALANCE,
        a.MJACCTTYPCD,
        a.CURRMIACCTTYPCD,
        a.PRODUCT,
        a.CURRACCTSTATCD,
        a.TAXRPTFORPERSNBR,
        a.TAXRPTFORORGNBR,
        a.LOANOFFICER,
        a.ACCTOFFICER,
        a.CONTRACTDATE,
        a.NOTEOPENAMT,
        a.NOTEINTRATE
    FROM
        OSIBANK.WH_ACCTCOMMON a
    WHERE
        (a.CURRACCTSTATCD IN ('ACT','NPFM','DORM')) AND
        (a.MJACCTTYPCD IN ('CML','MLN','MTG'))
    """)

    wh_loans = text("""
    SELECT
        a.ACCTNBR,
        a.ORIGDATE,
        a.CURRTERM,
        a.LOANIDX,
        a.RCF,
        a.AVAILBALAMT,
        a.FDICCATDESC
    FROM
        OSIBANK.WH_LOANS a
    """)

    acctpropins = text("""
    SELECT 
        *
    FROM 
        OSIBANK.ACCTPROPINS a
    """)

    wh_acctloan = text("""
    SELECT
        a.ACCTNBR,
        a.CREDITLIMITAMT,
        a.ORIGINTRATE,
        a.MARGINFIXED,
        a.FDICCATCD,
        a.AMORTTERM,
        a.TOTALPCTSOLD,
        a.COBAL,
        a.CREDLIMITCLATRESAMT
    FROM
        OSIBANK.WH_ACCTLOAN a
    """)

    acctloanlimithist = text("""
    SELECT
        a.ACCTNBR,
        a.INACTIVEDATE
    FROM
        OSIBANK.ACCTLOANLIMITHIST a
    """)

    wh_prop = text("""
    SELECT
        a.ACCTNBR,
        a.PROPNBR,
        a.PROPADDR1,
        a.PROPADDR2,
        a.PROPCITY,
        a.PROPSTATE,
        a.PROPZIP,
        a.APRSVALUEAMT,
        a.APRSDATE
    FROM
        OSIBANK.WH_PROP a
    """)

    wh_prop2 = text("""
    SELECT
        a.ACCTNBR,
        a.PROPTYPDESC,
        a.PROPNBR,
        a.PROPDESC
    FROM
        OSIBANK.WH_PROP2 a
    """)

    orgaddruse = text("""
    SELECT
        a.ORGNBR,
        a.ADDRNBR
    FROM
        OSIBANK.ORGADDRUSE a
    WHERE
        a.ADDRUSECD IN ('PRI')
    """)

    persaddruse = text("""
    SELECT
        a.PERSNBR,
        a.ADDRNBR
    FROM
        OSIBANK.PERSADDRUSE a
    WHERE
        a.ADDRUSECD IN ('PRI')
    """)

    wh_addr = text("""
    SELECT
        a.ADDRNBR,
        a.TEXT1,
        a.TEXT2,
        a.TEXT3,
        a.CITYNAME,
        a.STATECD,
        a.ZIPCD
    FROM
        OSIBANK.WH_ADDR a
    """)

    # Need more insurance tables
    wh_inspolicy = text("""
    SELECT
        *
    FROM
        OSIBANK.WH_INSPOLICY
    """)


    queries = [
        {'key':'wh_acctcommon', 'sql':wh_acctcommon, 'engine':1},
        {'key':'wh_loans', 'sql':wh_loans, 'engine':1},
        {'key':'wh_acctloan', 'sql':wh_acctloan, 'engine':1},
        {'key':'acctpropins', 'sql':acctpropins, 'engine':1},
        {'key':'acctloanlimithist', 'sql':acctloanlimithist, 'engine':1},
        {'key':'wh_prop', 'sql':wh_prop, 'engine':1},
        {'key':'wh_prop2', 'sql':wh_prop2, 'engine':1},
        {'key':'orgaddruse', 'sql':orgaddruse, 'engine':1},
        {'key':'persaddruse', 'sql':persaddruse, 'engine':1},
        {'key':'wh_addr', 'sql':wh_addr, 'engine':1},
        {'key':'wh_inspolicy', 'sql':wh_inspolicy, 'engine':1},
    ]

    data = src.cdutils.database.connect.retrieve_data(queries)
    return data