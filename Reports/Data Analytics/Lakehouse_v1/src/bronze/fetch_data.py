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
def fetch_wh_addr():
    """
    Main data query
    """

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
        {'key':'wh_addr', 'sql':wh_addr, 'engine':1},
        
        # {'key':'vieworgtaxid', 'sql':vieworgtaxid, 'engine':1},
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data

def fetch_wh_allroles():
    """
    Main data query
    """

    wh_allroles = text(f"""
    SELECT
        *
    FROM
        OSIBANK.WH_ALLROLES a
    """)    

    queries = [
        {'key':'wh_allroles', 'sql':wh_allroles, 'engine':1},
        
        # {'key':'vieworgtaxid', 'sql':vieworgtaxid, 'engine':1},
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data


def fetch_org_pers():
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
        
        # {'key':'vieworgtaxid', 'sql':vieworgtaxid, 'engine':1},
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data

"""
Using the lookup query to inspect the DB tables
"""

def fetch_db_metadata():
    """
    Main data query
    """
    # Engine 1
    lookup_df1 = text("""
    SELECT 
        *
    FROM 
        sys.all_tab_columns col
    """)

    # Engine 2
    lookup_df2 = text("""
    SELECT 
        *
    FROM 
        sys.all_tab_columns col
    """)

    queries = [
        # {'key':'acctcommon', 'sql':acctcommon, 'engine':2},
        {'key':'lookup_df1', 'sql':lookup_df1, 'engine':1},
        {'key':'lookup_df2', 'sql':lookup_df2, 'engine':2},
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data
