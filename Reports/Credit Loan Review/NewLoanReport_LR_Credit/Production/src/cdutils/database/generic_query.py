"""
Fetching data module. Aim is import all necessary fields up front, but if needed, you can define another function to be called here.

Usage:
    import src.cdutils.database

You need to set your own date that you want to see in effective date embedded in the SQL Query
"""

import src.cdutils.database.connect
from sqlalchemy import text # type: ignore

def fetch_data():
        # acctcommon
    # engine 2
    wh_acctcommon = text("""
    SELECT 
        a.ACCTNBR,
        a.LOANOFFICER,
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
        a.CURRMIACCTTYPCD,
        a.NAMEADDR1,
        a.NAMEADDR2,
        a.NAMEADDR3,
        a.PRIMARYOWNERCITY,
        a.PRIMARYOWNERSTATE,
        a.PRIMARYOWNERZIPCD,
        a.NOTEOPENAMT
    FROM 
        COCCDM.WH_ACCTCOMMON_TEMP a
    """)

    wh_loans = text("""
    SELECT
        a.ACCTNBR,
        a.ORIGDATE,
        a.ORIGBAL,
        a.FDICCATDESC,
        a.RUNDATE,
        a.AVAILBALAMT
    FROM
        COCCDM.WH_LOANS_TEMP a
    """)

    wh_acctloan = text("""
    SELECT
        a.ACCTNBR,
        a.MININTRATE,
        a.FDICCATCD,
        a.PROPNBR,
        a.TOTALPCTSOLD,
        a.RISKRATINGCD,
        a.COBAL,
        a.CREDLIMITCLATRESAMT
    FROM
        COCCDM.WH_ACCTLOAN_TEMP a
    """)

    wh_org = text("""
    SELECT
        a.ORGNBR,
        a.NAICSCD,
        a.NAICSCDDESC
    FROM
        COCCDM.WH_ORG a
    """)

    wh_prop = text("""
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
        a.PROPZIP,
        a.PROPTYPECD
    FROM
        COCCDM.WH_PROP a
    """)

    wh_prop2 = text("""
    SELECT
        a.ACCTNBR,
        a.PROPNBR,
        a.PROPDESC,
        a.PROPTYPDESC
    FROM
        COCCDM.WH_PROP2 a
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
        {'key':'wh_acctcommon', 'sql':wh_acctcommon, 'engine':2},
        {'key':'wh_loans', 'sql':wh_loans, 'engine':2},
        {'key':'wh_acctloan', 'sql':wh_acctloan, 'engine':2},
        {'key':'wh_org', 'sql':wh_org, 'engine':2},
        {'key':'wh_prop', 'sql':wh_prop, 'engine':2},
        {'key':'wh_prop2', 'sql':wh_prop2, 'engine':2},
        {'key':'househldacct', 'sql':househldacct, 'engine':1},
    ]

    data = src.cdutils.database.connect.retrieve_data(queries)
    return data


