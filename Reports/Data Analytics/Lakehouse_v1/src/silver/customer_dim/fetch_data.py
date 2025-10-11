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

def fetch_taxid_data():
    """
    Main data query
    """
    vieworgtaxid = text(f"""
    SELECT
        *
    FROM
        OSIBANK.VIEWORGTAXID a
    """)

    viewperstaxid = text(f"""
    SELECT
        *
    FROM
        OSIBANK.VIEWPERSTAXID a
    """)

    ## Below two tables are not needed because they are already in bronze layer    
    # wh_org = text(f"""
    # SELECT
    #     *
    # FROM
    #     OSIBANK.WH_ORG a
    # """)

    # wh_pers = text(f"""
    # SELECT
    #     *
    # FROM
    #     OSIBANK.WH_PERS a
    # """)

    queries = [
        {'key':'vieworgtaxid', 'sql':vieworgtaxid, 'engine':1},
        {'key':'viewperstaxid', 'sql':viewperstaxid, 'engine':1},
        # {'key':'wh_org', 'sql':wh_org, 'engine':1},
        # {'key':'wh_pers', 'sql':wh_pers, 'engine':1},
    ]

    data = cdutils.database.connect.retrieve_data(queries)
    return data

def fetch_pers_data():
    """
    Main data query
    """

    pers = text("""
    SELECT
        a.PERSNBR,
        a.FIRSTNAMEUPPER,
        a.LASTNAMEUPPER
    FROM
        OSIBANK.PERS a
    """)    

    queries = [
        {'key':'pers', 'sql':pers, 'engine':1},
    ]

    data = cdutils.database.connect.retrieve_data(queries)
    return data


def fetch_org_data():
    """
    Main data query
    """

    org = text("""
    SELECT
        a.ORGNBR,
        a.PARENTORGNBR,
        a.CTRLPERSNBR
    FROM
        OSIBANK.ORG a
    """)    

    queries = [
        {'key':'org', 'sql':org, 'engine':1},
    ]

    data = cdutils.database.connect.retrieve_data(queries)
    return data

