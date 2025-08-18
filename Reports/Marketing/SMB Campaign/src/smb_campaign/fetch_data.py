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

    orgaddruse = text(f"""
    SELECT
        a.ADDRNBR,
        a.ADDRUSECD,
        a.ORGNBR
    FROM
        OSIBANK.ORGADDRUSE a
    """)

    wh_addr = text(f"""
    SELECT
        a.ADDRNBR,
        a.TEXT1,
        a.ADDRLINETYPCD1,
        a.ADDRLINETYPDESC1,
        a.TEXT2,
        a.ADDRLINETYPCD2,
        a.ADDRLINETYPDESC2,
        a.TEXT3,
        a.ADDRLINETYPCD3,
        a.ADDRLINETYPDESC3,
        a.CITYNAME,
        a.STATECD,
        a.ZIPCD
    FROM
        OSIBANK.WH_ADDR a
    """)    
    # vieworgtaxid = text(f"""
    # SELECT
    #     *
    # FROM
    #     OSIBANK.VIEWORGTAXID a
    # """)

    queries = [
        {'key':'wh_org', 'sql':wh_org, 'engine':1},
        {'key':'orgaddruse', 'sql':orgaddruse, 'engine':1},
        {'key':'wh_addr', 'sql':wh_addr, 'engine':1},
        
        # {'key':'vieworgtaxid', 'sql':vieworgtaxid, 'engine':1},
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data
