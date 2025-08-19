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
        a.LOANOFFICER,
        a.ACCTOFFICER,
        a.BRANCHNAME,
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

    househldacct = text("""
    SELECT
        a.ACCTNBR,
        a.HOUSEHOLDNBR,
        a.DATELASTMAINT
    FROM
        OSIEXTN.HOUSEHLDACCT a
    """)

    queries = [
        {'key':'wh_acctcommon', 'sql':wh_acctcommon, 'engine':1},
        {'key':'wh_loans', 'sql':wh_loans, 'engine':1},
        {'key':'wh_acctloan', 'sql':wh_acctloan, 'engine':1},
        {'key':'househldacct', 'sql':househldacct, 'engine':1},
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data

def fetch_data_2024():
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
        a.LOANOFFICER,
        a.ACCTOFFICER,
        a.BRANCHNAME,
        a.NOTEBAL,
        a.CONTRACTDATE,
        a.DATEMAT,
        a.TAXRPTFORORGNBR,
        a.TAXRPTFORPERSNBR
    FROM
        COCCDM.WH_ACCTCOMMON a
    WHERE
        (a.CURRACCTSTATCD IN ('ACT','NPFM','DORM')) AND
        (a.EFFDATE = TO_DATE('2024-12-31 00:00:00', 'yyyy-mm-dd hh24:mi:ss'))

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
        COCCDM.WH_LOANS a
    WHERE
        (a.RUNDATE = TO_DATE('2024-12-31 00:00:00', 'yyyy-mm-dd hh24:mi:ss'))
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
        COCCDM.WH_ACCTLOAN a
    WHERE
        (a.EFFDATE = TO_DATE('2024-12-31 00:00:00', 'yyyy-mm-dd hh24:mi:ss'))

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
        {'key':'househldacct', 'sql':househldacct, 'engine':1},
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data

def fetch_data_2025():
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
        a.LOANOFFICER,
        a.ACCTOFFICER,
        a.BRANCHNAME,
        a.NOTEBAL,
        a.CONTRACTDATE,
        a.DATEMAT,
        a.TAXRPTFORORGNBR,
        a.TAXRPTFORPERSNBR
    FROM
        COCCDM.WH_ACCTCOMMON a
    WHERE
        (a.CURRACCTSTATCD IN ('ACT','NPFM','DORM')) AND
        (a.EFFDATE = TO_DATE('2025-03-31 00:00:00', 'yyyy-mm-dd hh24:mi:ss'))

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
        COCCDM.WH_LOANS a
    WHERE
        (a.RUNDATE = TO_DATE('2025-03-31 00:00:00', 'yyyy-mm-dd hh24:mi:ss'))
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
        COCCDM.WH_ACCTLOAN a
    WHERE
        (a.EFFDATE = TO_DATE('2025-03-31 00:00:00', 'yyyy-mm-dd hh24:mi:ss'))

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
        {'key':'househldacct', 'sql':househldacct, 'engine':1},
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data