"""
Fetching data module. Aim is import all necessary fields up front, but if needed, you can define another function to be called here.

Usage:
    import src.cdutils.database

You need to set your own date that you want to see in effective date embedded in the SQL Query
"""

import cdutils.database.connect # type: ignore
from sqlalchemy import text # type: ignore
from typing import Optional
from datetime import datetime

def fetch_data(specified_date: Optional[datetime] = None):
    """
    Main data query
    """
    if specified_date is None:
        specified_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    else:
        assert isinstance(specified_date, datetime), "Specified date must be a datetime object"
        specified_date = specified_date.strftime('%Y-%m-%d %H:%M:%S')

    wh_acctcommon = text(f"""
    SELECT
        a.ACCTNBR,
        a.BRANCHNAME,
        a.PRIMARYOWNERCITY,
        a.PRIMARYOWNERSTATE
    FROM
        COCCDM.WH_ACCTCOMMON a
    WHERE
        (a.CURRACCTSTATCD IN ('ACT','NPFM','DORM')) AND
        (a.EFFDATE = TO_DATE('{specified_date}', 'YYYY-MM-DD HH24:MI:SS'))
    """)

    queries = [
        {'key':'wh_acctcommon', 'sql':wh_acctcommon, 'engine':2},
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data
