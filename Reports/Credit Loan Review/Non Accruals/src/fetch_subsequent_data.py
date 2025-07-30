"""
Fetching data module. Aim is import all necessary fields up front, but if needed, you can define another function to be called here.

Usage:
    import src.cdutils.database

You need to set your own date that you want to see in effective date embedded in the SQL Query
"""

import cdutils.database.connect # type: ignore
from sqlalchemy import text # type: ignore

def fetch_subsequent_data(effdate1, effdate2):

    first_acctcommon_query = text(f"""
    SELECT 
        COCCDM.WH_ACCTCOMMON.ACCTNBR, 
        COCCDM.WH_ACCTCOMMON.MJACCTTYPCD, 
        COCCDM.WH_ACCTCOMMON.CURRMIACCTTYPCD, 
        COCCDM.WH_ACCTCOMMON.PRODUCT, 
        COCCDM.WH_ACCTCOMMON.CURRACCTSTATCD, 
        COCCDM.WH_ACCTCOMMON.BOOKBALANCE, 
        COCCDM.WH_ACCTCOMMON.LOANOFFICER, 
        COCCDM.WH_ACCTCOMMON.OWNERSORTNAME, 
        COCCDM.WH_ACCTCOMMON.EFFDATE 
    FROM
        COCCDM.WH_ACCTCOMMON
    WHERE 
        COCCDM.WH_ACCTCOMMON.EFFDATE = TO_DATE('{effdate1}','yyyy-mm-dd hh24:mi:ss')
    """)

    second_acctcommon_query = text(f"""
    SELECT 
        COCCDM.WH_ACCTCOMMON.ACCTNBR, 
        COCCDM.WH_ACCTCOMMON.MJACCTTYPCD, 
        COCCDM.WH_ACCTCOMMON.CURRMIACCTTYPCD, 
        COCCDM.WH_ACCTCOMMON.PRODUCT, 
        COCCDM.WH_ACCTCOMMON.CURRACCTSTATCD, 
        COCCDM.WH_ACCTCOMMON.BOOKBALANCE, 
        COCCDM.WH_ACCTCOMMON.LOANOFFICER, 
        COCCDM.WH_ACCTCOMMON.OWNERSORTNAME, 
        COCCDM.WH_ACCTCOMMON.EFFDATE 
    FROM
        COCCDM.WH_ACCTCOMMON
    WHERE 
        COCCDM.WH_ACCTCOMMON.EFFDATE = TO_DATE('{effdate2}','yyyy-mm-dd hh24:mi:ss')
    """)

    first_acctloan_query = text(f"""
    SELECT 
        COCCDM.WH_ACCTLOAN.ACCTNBR, 
        COCCDM.WH_ACCTLOAN.COBAL, 
        COCCDM.WH_ACCTLOAN.NEXTDUEDATE, 
        COCCDM.WH_ACCTLOAN.RISKRATINGCD, 
        COCCDM.WH_ACCTLOAN.NOTEACCRUEDINT,
        COCCDM.WH_ACCTLOAN.TOTALPI, 
        COCCDM.WH_ACCTLOAN.TOTALPIDUE, 
        COCCDM.WH_ACCTLOAN.CURRDUEDATE, 
        COCCDM.WH_ACCTLOAN.TOTALPAYMENTSDUE
    FROM 
        COCCDM.WH_ACCTLOAN 
    WHERE 
        COCCDM.WH_ACCTLOAN.EFFDATE = TO_DATE('{effdate1}','yyyy-mm-dd hh24:mi:ss')
    """)  

    second_acctloan_query = text(f"""
    SELECT 
        COCCDM.WH_ACCTLOAN.ACCTNBR, 
        COCCDM.WH_ACCTLOAN.COBAL, 
        COCCDM.WH_ACCTLOAN.NEXTDUEDATE, 
        COCCDM.WH_ACCTLOAN.RISKRATINGCD, 
        COCCDM.WH_ACCTLOAN.NOTEACCRUEDINT,
        COCCDM.WH_ACCTLOAN.TOTALPI, 
        COCCDM.WH_ACCTLOAN.TOTALPIDUE, 
        COCCDM.WH_ACCTLOAN.CURRDUEDATE, 
        COCCDM.WH_ACCTLOAN.TOTALPAYMENTSDUE
    FROM 
        COCCDM.WH_ACCTLOAN 
    WHERE 
        COCCDM.WH_ACCTLOAN.EFFDATE = TO_DATE('{effdate2}','yyyy-mm-dd hh24:mi:ss')
    """)  

    queries = [
        {'key':'wh_acctcommon', 'sql':first_acctcommon_query, 'engine':2},
        {'key':'wh_acctcommon2', 'sql':second_acctcommon_query, 'engine':2},
        {'key':'wh_acctloan', 'sql':first_acctloan_query, 'engine':2},
        {'key':'wh_acctloan2', 'sql':second_acctloan_query, 'engine':2},
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data
