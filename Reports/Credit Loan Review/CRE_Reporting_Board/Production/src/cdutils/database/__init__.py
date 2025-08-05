"""
Fetching data module. Aim is import all necessary fields up front, but if needed, you can define another function to be called here.

Usage:
    import src.cdutils.database
"""

import src.cdutils.database.connect
from sqlalchemy import text # type: ignore

def fetch_data():
    wh_acctcommon = text("""
    SELECT
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
        a.RATETYPCD
    FROM
        COCCDM.WH_ACCTCOMMON a
    WHERE
        (a.CURRACCTSTATCD IN ('ACT','NPFM')) AND
        (a.MJACCTTYPCD IN ('CML','MLN')) AND
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
        a.ORIGBAL,
        a.NEXTRATECHG
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

    queries = [
        {'key':'wh_acctcommon', 'sql':wh_acctcommon, 'engine':2},
        {'key':'wh_loans', 'sql':wh_loans, 'engine':2},
        {'key':'wh_acctloan', 'sql':wh_acctloan, 'engine':2},
        {'key':'wh_acct', 'sql':wh_acct, 'engine':2},
        {'key':'wh_prop', 'sql':wh_prop, 'engine':1},
        {'key':'wh_prop2', 'sql':wh_prop2, 'engine':1},
    ]

    data = src.cdutils.database.connect.retrieve_data(queries)
    return data

def fetch_data_2023():
    wh_acctcommon = text("""
    SELECT
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
        (a.MJACCTTYPCD IN ('CML')) AND
        (a.EFFDATE = TO_DATE('2023-12-29 00:00:00', 'yyyy-mm-dd hh24:mi:ss'))
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
        (a.RUNDATE = TO_DATE('2023-12-29 00:00:00', 'yyyy-mm-dd hh24:mi:ss'))
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
        (a.EFFDATE = TO_DATE('2023-12-29 00:00:00', 'yyyy-mm-dd hh24:mi:ss'))
    """)

    wh_acct = text("""
    SELECT
        a.ACCTNBR,
        a.DATEMAT
    FROM
        COCCDM.WH_ACCT a
    WHERE
        (a.RUNDATE = TO_DATE('2023-12-29 00:00:00', 'yyyy-mm-dd hh24:mi:ss'))
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

    queries = [
        {'key':'wh_acctcommon', 'sql':wh_acctcommon, 'engine':2},
        {'key':'wh_loans', 'sql':wh_loans, 'engine':2},
        {'key':'wh_acctloan', 'sql':wh_acctloan, 'engine':2},
        {'key':'wh_acct', 'sql':wh_acct, 'engine':2},
        {'key':'wh_prop', 'sql':wh_prop, 'engine':1},
        {'key':'wh_prop2', 'sql':wh_prop2, 'engine':1},
    ]

    data = src.cdutils.database.connect.retrieve_data(queries)
    return data

def fetch_data_2022():
    wh_acctcommon = text("""
    SELECT
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
        (a.MJACCTTYPCD IN ('CML')) AND
        (a.EFFDATE = TO_DATE('2022-12-30 00:00:00', 'yyyy-mm-dd hh24:mi:ss'))
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
        (a.RUNDATE = TO_DATE('2022-12-30 00:00:00', 'yyyy-mm-dd hh24:mi:ss'))
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
        (a.EFFDATE = TO_DATE('2022-12-30 00:00:00', 'yyyy-mm-dd hh24:mi:ss'))
    """)

    wh_acct = text("""
    SELECT
        a.ACCTNBR,
        a.DATEMAT
    FROM
        COCCDM.WH_ACCT a
    WHERE
        (a.RUNDATE = TO_DATE('2022-12-30 00:00:00', 'yyyy-mm-dd hh24:mi:ss'))
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

    queries = [
        {'key':'wh_acctcommon', 'sql':wh_acctcommon, 'engine':2},
        {'key':'wh_loans', 'sql':wh_loans, 'engine':2},
        {'key':'wh_acctloan', 'sql':wh_acctloan, 'engine':2},
        {'key':'wh_acct', 'sql':wh_acct, 'engine':2},
        {'key':'wh_prop', 'sql':wh_prop, 'engine':1},
        {'key':'wh_prop2', 'sql':wh_prop2, 'engine':1},
    ]

    data = src.cdutils.database.connect.retrieve_data(queries)
    return data
