"""
Fetching data module. Aim is import all necessary fields up front, but if needed, you can define another function to be called here.

Usage:
    import src.cdutils.database

You need to set your own date that you want to see in effective date embedded in the SQL Query
"""

import cdutils.database.connect # type: ignore
from sqlalchemy import text # type: ignore
from typing import Optional
from datetime import datetime, timedelta
import pandas as pd

def fetch_data(specified_date: Optional[datetime] = None):
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
        a.CLOSEDATE,
        a.TAXRPTFORORGNBR,
        a.TAXRPTFORPERSNBR,
        a.LOANOFFICER,
        a.ACCTOFFICER
    FROM
        COCCDM.WH_ACCTCOMMON a
    WHERE
        (a.CONTRACTDATE >= TO_DATE('{datetime(2020, 1, 1)}''YYYY-MM-DD HH24:MI:SS')) AND
        (a.EFFDATE = TO_DATE('{specified_date}', 'YYYY-MM-DD HH24:MI:SS'))
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
        a.LOANLIMITYN,
        a.NEXTRATECHG
    FROM
        COCCDM.WH_LOANS a
    WHERE
        a.RUNDATE = TO_DATE('{specified_date}', 'YYYY-MM-DD HH24:MI:SS')
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
        a.CREDLIMITCLATRESAMT,
        a.RISKRATINGCD
    FROM
        COCCDM.WH_ACCTLOAN a
    WHERE
        a.EFFDATE = TO_DATE('{specified_date}', 'YYYY-MM-DD HH24:MI:SS')
    """)

    househldacct = text("""
    SELECT
        a.ACCTNBR,
        a.HOUSEHOLDNBR,
        a.DATELASTMAINT
    FROM
        OSIEXTN.HOUSEHLDACCT a
    """)

    wh_pers = text("""
    SELECT
        *
    FROM
        OSIBANK.WH_PERS a
    """)    

    queries = [
        {'key':'wh_acctcommon', 'sql':wh_acctcommon, 'engine':2},
        {'key':'wh_loans', 'sql':wh_loans, 'engine':2},
        {'key':'wh_acctloan', 'sql':wh_acctloan, 'engine':2},
        {'key':'househldacct', 'sql':househldacct, 'engine':1},
        {'key':'wh_pers', 'sql':wh_pers, 'engine':1},
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data
