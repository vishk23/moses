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

def fetch_invr():
    """
    Main data query
    """
    
    wh_invr = text(f"""
    SELECT
        a.ACCTNBR,
        a.ACCTGRPNBR,
        a.INVRSTATCD,
        a.PCTOWNED,
        a.ORIGINVRRATE,
        a.CURRINVRRATE
    FROM
        OSIBANK.WH_INVR a
    """)
    
    acctgrpinvr = text(f"""
    SELECT
        a.ACCTGRPNBR,
        a.INVRORGNBR
    FROM
        OSIBANK.ACCTGRPINVR a
    """)

    queries = [
        {'key':'wh_invr', 'sql':wh_invr, 'engine':1},
        {'key':'acctgrpinvr', 'sql':acctgrpinvr, 'engine':1},
    ]

    data = cdutils.database.connect.retrieve_data(queries)
    return data



def fetch_acctsubacct():
    """
    Main data query
    """
    
    acctsubacct = text(f"""
    SELECT
        a.ACCTNBR,
        a.EFFDATE,
        a.ESCROWCUSHIONAMT,
        a.ALTERNATEESCPMTAMT
    FROM
        OSIBANK.ACCTSUBACCTCUSHION a
    """)
    
    queries = [
        {'key':'acctsubacct', 'sql':acctsubacct, 'engine':1},
    ]

    data = cdutils.database.connect.retrieve_data(queries)
    return data

def fetch_wh_acct():
    """
    Main data query
    """
    
    wh_acct = text(f"""
    SELECT
        a.ACCTNBR,
        a.NAICSCD,
        a.NAICSDESC
    FROM
        OSIBANK.WH_ACCT a
    """)
    
    queries = [
        {'key':'wh_acct', 'sql':wh_acct, 'engine':1},
    ]

    data = cdutils.database.connect.retrieve_data(queries)
    return data


def fetch_userfields():
    """Fetch account-level user fields."""

    wh_acctuserfields = text(f"""
    SELECT
        a.ACCTNBR,
        a.ACCTUSERFIELDCD,
        a.ACCTUSERFIELDVALUE,
        a.ACCTDATELASTMAINT
    FROM
        OSIBANK.WH_ACCTUSERFIELDS a
    """)

    queries = [
        {'key':'wh_acctuserfields', 'sql':wh_acctuserfields, 'engine':1},
    ]

    data = cdutils.database.connect.retrieve_data(queries)
    return data
