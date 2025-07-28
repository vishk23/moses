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
        a.ACCTNBR,
        a.BRANCHNAME,
        a.PRIMARYOWNERCITY,
        a.PRIMARYOWNERSTATE
    FROM
        OSIBANK.WH_ACCTCOMMON a
    WHERE
        (a.CURRACCTSTATCD IN ('ACT','NPFM','DORM'))
    """)



    queries = [
        {'key':'wh_acctcommon', 'sql':wh_acctcommon, 'engine':1},
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data
