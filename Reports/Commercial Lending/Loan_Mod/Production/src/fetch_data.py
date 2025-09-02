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
    acctcommon = text("""
    SELECT 
        a.ACCTNBR,
        a.OWNERNAME,
        a.LOANOFFICER,
        a.EFFDATE, 
        a.MJACCTTYPCD, 
        a.PRODUCT, 
        a.CURRMIACCTTYPCD, 
        a.BOOKBALANCE,
        a.NOTEBAL,
        a.NOTEOPENAMT,
        a.CURRACCTSTATCD, 
        a.CONTRACTDATE,
        a.DATEMAT 
    FROM
        OSIBANK.WH_ACCTCOMMON a
    WHERE 
        a.CURRACCTSTATCD IN ('ACT','NPFM')
        AND a.MJACCTTYPCD IN ('CML')
    """)

    # AcctSubAcct
    acctsubacct = text("""
    SELECT 
        *
    FROM 
        OSIBANK.ACCTSUBACCT a
    WHERE
        a.BALCATCD = 'CMDF'
        AND BALTYPCD = 'FEE'
    """)
    
    # AcctLoanModHist
    acctloanmodhist = text("""
    SELECT
        *
    FROM
        OSIBANK.ACCTLOANMODHIST a
    """)
    
    # AcctLoanReason
    loanmodreason = text("""
    SELECT
        *
    FROM
        OSIBANK.LOANMODREASON a
    """)
    
    queries = [
        {'key':'acctcommon', 'sql':acctcommon, 'engine':1},
        {'key':'acctsubacct', 'sql':acctsubacct, 'engine':1},
        {'key':'acctloanmodhist', 'sql':acctloanmodhist, 'engine':1},
        {'key':'loanmodreason', 'sql':loanmodreason, 'engine':1},
        # {'key':'wh_pers', 'sql':wh_pers, 'engine':1},
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data
