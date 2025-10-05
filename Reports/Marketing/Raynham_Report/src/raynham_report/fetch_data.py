"""
Fetching data module. Aim is import all necessary fields up front, but if needed, you can define another function to be called here.

Usage:
    import src.cdutils.database

You need to set your own date that you want to see in effective date embedded in the SQL Query
"""

import cdutils.database.connect # type: ignore
from sqlalchemy import text # type: ignore
from datetime import datetime
from typing import Optional

# Define fetch data here using cdutils.database.connect
# There are often fetch_data.py files already in project if migrating

def fetch_data():
    """
    Main data query
    """
    
    wh_org = text(f"""
    SELECT
        *
    FROM
        OSIBANK.WH_ORG a
    """)
    wh_pers = text(f"""
    SELECT
        *
    FROM
        OSIBANK.WH_PERS a
    """)

    queries = [
        {'key':'wh_org', 'sql':wh_org, 'engine':1},
        {'key':'wh_pers', 'sql':wh_pers, 'engine':1},
    ]

    data = cdutils.database.connect.retrieve_data(queries)
    return data



def fetch_rtxn_data():
    """
    Main data query
    """
    # transacted = text("""
    # SELECT
    #     *
    # FROM
    #     COCCDM.WH_RTXN a
    # WHERE
    #     a.ORGNBR = 204
    #     AND a.RTXNSOURCECD = 'ONLI'
    #     AND a.RUNDATE >= SYSDATE - 90
    # """)
    transacted = text("""
    SELECT
        DISTINCT a.ACCTNBR
    FROM
        COCCDM.WH_RTXN a
    WHERE
        a.ORGNBR = 204
        AND a.RTXNSOURCECD = 'ONLI'
        AND a.RUNDATE >= SYSDATE - 90
    """)

    # SELECT
    #     *
    # FROM
    #     OSIBANK.VIEWORGTAXID a
    # """)

    queries = [
        {'key':'transacted', 'sql':transacted, 'engine':2},
        # {'key':'vieworgtaxid', 'sql':vieworgtaxid, 'engine':1},
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data
