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

def fetch_data():
    """
    Main data query
    """
    
    query = text("""
    SELECT
        a.ACCTNBR,
        a.EFFDATE,    
        a.NOTEOPENAMT,
        la.CREDITLIMITAMT,
        ln.LOANLIMITYN,
        CASE
            WHEN UPPER(ln.LOANLIMITYN) = 'Y' THEN COALESCE(la.CREDITLIMITAMT, 0)
                ELSE COALESCE(a.NOTEOPENAMT, 0)
        END AS facevalue
    FROM
        COCCDM.WH_ACCTCOMMON a
    INNER JOIN
        COCCDM.WH_ACCTLOAN la
        ON a.ACCTNBR = la.ACCTNBR
        AND a.EFFDATE = la.EFFDATE
    INNER JOIN
        COCCDM.WH_LOANS ln
        ON a.ACCTNBR = ln.ACCTNBR
        AND a.EFFDATE = ln.RUNDATE
    WHERE
        (a.ACCTNBR, a.EFFDATE) IN (
            SELECT
                ACCTNBR,
                MIN(EFFDATE)
            FROM
                COCCDM.WH_ACCTCOMMON
            GROUP BY
                ACCTNBR
        )
    """)

    queries = [
        {'key':'query', 'sql':query, 'engine':2},
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data
