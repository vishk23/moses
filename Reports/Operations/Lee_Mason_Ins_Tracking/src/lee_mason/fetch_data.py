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

    acctpropins = text("""
    SELECT 
        *
    FROM 
        OSIBANK.ACCTPROPINS a
    """)

    wh_prop = text("""
    SELECT
        a.ACCTNBR,
        a.PROPNBR,
        a.PROPADDR1,
        a.PROPADDR2,
        a.PROPCITY,
        a.PROPSTATE,
        a.PROPZIP,
        a.APRSVALUEAMT,
        a.APRSDATE
    FROM
        OSIBANK.WH_PROP a
    """)

    wh_prop2 = text("""
    SELECT
        a.ACCTNBR,
        a.PROPTYPDESC,
        a.PROPNBR,
        a.PROPDESC
    FROM
        OSIBANK.WH_PROP2 a
    """)

    # Need more insurance tables
    wh_inspolicy = text("""
    SELECT
        *
    FROM
        OSIBANK.WH_INSPOLICY
    """)


    queries = [
        {'key':'acctpropins', 'sql':acctpropins, 'engine':1},
        {'key':'wh_prop', 'sql':wh_prop, 'engine':1},
        {'key':'wh_prop2', 'sql':wh_prop2, 'engine':1},
        {'key':'wh_inspolicy', 'sql':wh_inspolicy, 'engine':1},
    ]

    data = cdutils.database.connect.retrieve_data(queries)
    return data


