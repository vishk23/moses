"""
Using the lookup query to inspect the DB tables
"""

import cdutils.database.connect # type: ignore
from sqlalchemy import text # type: ignore

def fetch_acctstat_data():
    """
    Main data query
    """
    # Engine 1
    acctstatistichist = text("""
    SELECT 
        *
    FROM 
        OSIBANK.ACCTSTATISTICHIST
    """)

    doc = text("""
    SELECT 
        *
    FROM 
        OSIBANK.STATISTICTYP
    """)

    queries = [
        # {'key':'acctcommon', 'sql':acctcommon, 'engine':2},
        {'key':'acctstatistichist', 'sql':acctstatistichist, 'engine':1},
        {'key':'doc', 'sql':doc, 'engine':1}
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data