"""
Fetching data module. Aim is import all necessary fields up front, but if needed, you can define another function to be called here.

Usage:
    import src.cdutils.database

You need to set your own date that you want to see in effective date embedded in the SQL Query
"""

import cdutils.database.connect # type: ignore
from sqlalchemy import text # type: ignore

def fetch_data():
    """
    Main data query
    """
    wh_acctcommon = text(f"""
    SELECT
        a.EFFDATE,
        a.ACCTNBR,
        a.OWNERSORTNAME,
        a.PRODUCT,
        a.NOTEOPENAMT,
        a.RATETYPCD,
        a.MJACCTTYPCD,
        a.CURRMIACCTTYPCD,
        a.CURRACCTSTATCD,
        a.NOTEINTRATE,
        a.BOOKBALANCE,
        a.NOTEBAL,
        a.CONTRACTDATE,
        a.DATEMAT,
        a.TAXRPTFORORGNBR,
        a.TAXRPTFORPERSNBR
    FROM
        OSIBANK.WH_ACCTCOMMON a
    WHERE
        (a.CURRACCTSTATCD IN ('ACT','NPFM','DORM'))
    """)

    wh_loans = text(f"""
    SELECT
        a.ACCTNBR,
        a.ORIGDATE,
        a.CURRTERM,
        a.LOANIDX,
        a.RCF,
        a.AVAILBALAMT,
        a.FDICCATDESC,
        a.ORIGBAL,
        a.LOANLIMITYN
    FROM
        OSIBANK.WH_LOANS a
    """)

    wh_acctloan = text(f"""
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

    viewperstaxid = text("""
    SELECT
        a.PERSNBR,
        a.TAXID
    FROM
        OSIBANK.VIEWPERSTAXID a
    """)

    vieworgtaxid = text("""
    SELECT
        a.ORGNBR,
        a.TAXID
    FROM
        OSIBANK.VIEWORGTAXID a
    """)

    househldacct = text("""
    SELECT
        a.ACCTNBR,
        a.HOUSEHOLDNBR,
        a.DATELASTMAINT
    FROM
        OSIEXTN.HOUSEHLDACCT a
    """)

    househld = text("""
    SELECT
        a.HOUSEHOLDNBR,
        a.HOUSEHOLDTITLE,
        a.HEADOFHOUSENBR,
        a.HEADOFHOUSETYP
    FROM
        OSIEXTN.HOUSEHLD a
    """)

    acctloanlimithist = text("""
    SELECT
        a.ACCTNBR,
        a.INACTIVEDATE
    FROM
        OSIBANK.ACCTLOANLIMITHIST a
    """)

    wh_pers = text("""
    SELECT
        a.PERSNBR,
        a.PERSNAME
    FROM
        OSIBANK.WH_PERS a
    """)

    wh_org = text("""
    SELECT
        a.ORGNBR,
        a.ORGNAME
    FROM
        OSIBANK.WH_ORG a
    """)

    wh_allroles = text("""
    SELECT
        *
    FROM 
        OSIBANK.WH_ALLROLES a
    """)

    queries = [
        {'key':'wh_acctcommon', 'sql':wh_acctcommon, 'engine':1},
        {'key':'wh_loans', 'sql':wh_loans, 'engine':1},
        {'key':'wh_acctloan', 'sql':wh_acctloan, 'engine':1},
        {'key':'viewperstaxid', 'sql':viewperstaxid, 'engine':1},
        {'key':'vieworgtaxid', 'sql':vieworgtaxid, 'engine':1},
        {'key':'househldacct', 'sql':househldacct, 'engine':1},
        {'key':'househld', 'sql':househld, 'engine':1},
        {'key':'acctloanlimithist', 'sql':acctloanlimithist, 'engine':1},
        {'key':'wh_allroles', 'sql':wh_allroles, 'engine':1},
        {'key':'wh_pers', 'sql':wh_pers, 'engine':1},
        {'key':'wh_org', 'sql':wh_org, 'engine':1},
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data
