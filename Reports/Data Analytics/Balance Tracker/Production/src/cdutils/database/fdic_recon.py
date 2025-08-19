"""
Fetching data module. Aim is import all necessary fields up front, but if needed, you can define another function to be called here.

Usage:
    import src.cdutils.database

You need to set your own date that you want to see in effective date embedded in the SQL Query
"""

import src.cdutils.database.connect
from sqlalchemy import text # type: ignore

def fetch_data_dec24():
    wh_acctcommon = text("""
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
        a.NOTEBAL
    FROM
        COCCDM.WH_ACCTCOMMON a
    WHERE
        (a.CURRACCTSTATCD IN ('ACT','NPFM')) AND
        (a.EFFDATE = TO_DATE('2024-12-31 00:00:00', 'yyyy-mm-dd hh24:mi:ss'))
    """)

    wh_loans = text("""
    SELECT
        a.ACCTNBR,
        a.ORIGDATE,
        a.CURRTERM,
        a.LOANIDX,
        a.RCF,
        a.AVAILBALAMT,
        a.FDICCATDESC,
        a.ORIGBAL
    FROM
        COCCDM.WH_LOANS a
    WHERE
        (a.RUNDATE = TO_DATE('2024-12-31 00:00:00', 'yyyy-mm-dd hh24:mi:ss'))
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
        COCCDM.WH_ACCTLOAN a
    WHERE
        (a.EFFDATE = TO_DATE('2024-12-31 00:00:00', 'yyyy-mm-dd hh24:mi:ss'))
    """)

    wh_acct = text("""
    SELECT
        a.ACCTNBR,
        a.DATEMAT
    FROM
        COCCDM.WH_ACCT a
    WHERE
        (a.RUNDATE = TO_DATE('2024-12-31 00:00:00', 'yyyy-mm-dd hh24:mi:ss'))
    """)

    queries = [
        {'key':'wh_acctcommon', 'sql':wh_acctcommon, 'engine':2},
        {'key':'wh_loans', 'sql':wh_loans, 'engine':2},
        {'key':'wh_acctloan', 'sql':wh_acctloan, 'engine':2},
        {'key':'wh_acct', 'sql':wh_acct, 'engine':2},
    ]

    data = src.cdutils.database.connect.retrieve_data(queries)
    return data


def fetch_data_jan25():
    wh_acctcommon = text("""
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
        a.NOTEBAL
    FROM
        COCCDM.WH_ACCTCOMMON a
    WHERE
        (a.CURRACCTSTATCD IN ('ACT','NPFM')) AND
        (a.EFFDATE = TO_DATE('2025-01-31 00:00:00', 'yyyy-mm-dd hh24:mi:ss'))
    """)

    wh_loans = text("""
    SELECT
        a.ACCTNBR,
        a.ORIGDATE,
        a.CURRTERM,
        a.LOANIDX,
        a.RCF,
        a.AVAILBALAMT,
        a.FDICCATDESC,
        a.ORIGBAL
    FROM
        COCCDM.WH_LOANS a
    WHERE
        (a.RUNDATE = TO_DATE('2025-01-31 00:00:00', 'yyyy-mm-dd hh24:mi:ss'))
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
        COCCDM.WH_ACCTLOAN a
    WHERE
        (a.EFFDATE = TO_DATE('2025-01-31 00:00:00', 'yyyy-mm-dd hh24:mi:ss'))
    """)

    wh_acct = text("""
    SELECT
        a.ACCTNBR,
        a.DATEMAT
    FROM
        COCCDM.WH_ACCT a
    WHERE
        (a.RUNDATE = TO_DATE('2025-01-31 00:00:00', 'yyyy-mm-dd hh24:mi:ss'))
    """)

    queries = [
        {'key':'wh_acctcommon', 'sql':wh_acctcommon, 'engine':2},
        {'key':'wh_loans', 'sql':wh_loans, 'engine':2},
        {'key':'wh_acctloan', 'sql':wh_acctloan, 'engine':2},
        {'key':'wh_acct', 'sql':wh_acct, 'engine':2},
    ]

    data = src.cdutils.database.connect.retrieve_data(queries)
    return data