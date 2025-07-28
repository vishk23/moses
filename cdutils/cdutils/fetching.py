import src.cdutils.database.connect
import src.cdutils.caching
from sqlalchemy import text # type: ignore

def fetch_data():
    wh_acctcommon = text("""
    SELECT
        a.ACCTNBR,
        a.EFFDATE,
        a.DATEMAT,
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
        a.TAXRPTFORPERSNBR,
        a.TAXRPTFORORGNBR,
        a.LOANOFFICER,
        a.ACCTOFFICER,
        a.CONTRACTDATE
    FROM
        OSIBANK.WH_ACCTCOMMON a
    WHERE
        (a.CURRACCTSTATCD IN ('ACT','NPFM','DORM'))
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
    """)

    wh_org = text("""
    SELECT
        a.ORGNBR,
        a.ORGNAME
    """)

    queries = [
        {'key':'wh_acctcommon', 'sql':wh_acctcommon, 'engine':1},
        # {'key':'wh_loans', 'sql':wh_loans, 'engine':1},
        # {'key':'wh_acctloan', 'sql':wh_acctloan, 'engine':1},
        # {'key':'viewperstaxid', 'sql':viewperstaxid, 'engine':1},
        # {'key':'vieworgtaxid', 'sql':vieworgtaxid, 'engine':1},
        # {'key':'househldacct', 'sql':househldacct, 'engine':1},
        # {'key':'househld', 'sql':househld, 'engine':1},
        # {'key':'acctloanlimithist', 'sql':acctloanlimithist, 'engine':1},
    ]

    data = src.cdutils.database.connect.retrieve_data(queries)
    return data