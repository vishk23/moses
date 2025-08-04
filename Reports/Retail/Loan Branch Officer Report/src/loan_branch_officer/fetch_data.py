"""
Fetching data module. Import all necessary fields up front.

This module handles data retrieval from the OSIBANK database tables
for the Loan Branch Officer Report.

Usage:
    import src.fetch_data
    data = src.fetch_data.fetch_data()
"""

import cdutils.database.connect
from sqlalchemy import text

def fetch_data():
    """
    Main data query for loan branch officer report.
    
    Returns:
        dict: Dictionary containing DataFrames for each query result
    """
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
        a.NOTEBAL,
        a.CONTRACTDATE,
        a.DATEMAT,
        a.TAXRPTFORORGNBR,
        a.TAXRPTFORPERSNBR,
        a.LOANOFFICER,
        a.BRANCHNAME
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
        a.FDICCATDESC,
        a.ORIGBAL,
        a.LOANLIMITYN
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

    househldacct = text("""
    SELECT
        a.ACCTNBR,
        a.HOUSEHOLDNBR,
        a.DATELASTMAINT
    FROM
        OSIEXTN.HOUSEHLDACCT a
    """)

    queries = [
        {'key': 'wh_acctcommon', 'sql': wh_acctcommon, 'engine': 1},
        {'key': 'wh_loans', 'sql': wh_loans, 'engine': 1},
        {'key': 'wh_acctloan', 'sql': wh_acctloan, 'engine': 1},
        {'key': 'househldacct', 'sql': househldacct, 'engine': 1},
    ]

    data = cdutils.database.connect.retrieve_data(queries)
    return data
