"""
Account data fetching module for Accubranch project.

This module contains SQL queries and data retrieval functions for account-related data.
"""

import cdutils.database.connect # type: ignore
from sqlalchemy import text # type: ignore
from datetime import datetime
from typing import Optional

def fetch_data(specified_date: Optional[datetime] = None):
    """
    Main data query for account information.
    
    Parameters:
    -----------
    specified_date : datetime, optional
        Date for which to fetch account data. Defaults to current datetime.
        
    Returns:
    --------
    dict
        Dictionary containing multiple DataFrames with account data
    """
    if specified_date is None:
        specified_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    else:
        assert isinstance(specified_date, datetime), "Specified date must be a datetime object"
        specified_date = specified_date.strftime('%Y-%m-%d %H:%M:%S')

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
        a.TAXRPTFORPERSNBR,
        a.LOANOFFICER,
        a.ACCTOFFICER
    FROM
        COCCDM.WH_ACCTCOMMON a
    WHERE
        (a.CURRACCTSTATCD IN ('ACT','NPFM','DORM')) AND
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
        a.LOANLIMITYN
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
