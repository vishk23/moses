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
    wh_addr = text(f"""
    SELECT
        *
    FROM
        OSIBANK.WH_ADDR a
    """)

    orgaddruse = text("""
    SELECT
        *
    FROM
        OSIBANK.ORGADDRUSE a
    """)

    persaddruse = text("""
    SELECT
        *
    FROM
        OSIBANK.PERSADDRUSE a
    """)    

    wh_org = text("""
    SELECT
        *
    FROM
        OSIBANK.WH_ORG a
    """)

    wh_pers = text("""
    SELECT
        *
    FROM
        OSIBANK.WH_PERS a
    """)

    queries = [
        {'key':'wh_addr', 'sql':wh_addr, 'engine':1},
        {'key':'orgaddruse', 'sql':orgaddruse, 'engine':1},
        {'key':'persaddruse', 'sql':persaddruse, 'engine':1},
        {'key':'wh_org', 'sql':wh_org, 'engine':1},
        {'key':'wh_pers', 'sql':wh_pers, 'engine':1},
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data

