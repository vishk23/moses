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
    
    vieworgtaxid = text(f"""
    SELECT
        *
    FROM
        OSIBANK.VIEWORGTAXID a
    """)

    queries = [
        {'key':'vieworgtaxid', 'sql':vieworgtaxid, 'engine':1}
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data
