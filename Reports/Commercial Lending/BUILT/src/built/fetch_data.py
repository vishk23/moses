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
    
    wh_invr = text("""
    SELECT
        a.ACCTNBR,
        a.ACCTGRPNBR,
        a.INVRSTATCD,
        a.PCTOWNED,
        a.ORIGINVRRATE,
        a.CURRINVRRATE,
        a.DATELASTMAINT
    FROM
        OSIBANK.WH_INVR a
    """)
    
    acctgrpinvr = text("""
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



# Define fetch data here using cdutils.database.connect
# There are often fetch_data.py files already in project if migrating
def fetch_inactive_date_data():
    """
    Main data query
    """
    acctloanlimithist = text("""
    SELECT
        a.ACCTNBR,
        a.INACTIVEDATE
    FROM
        OSIBANK.ACCTLOANLIMITHIST a
    WHERE
        a.CREDITLIMITAMT != 0
    """)
    # vieworgtaxid = text(f"""
    # SELECT
    #     *
    # FROM
    #     OSIBANK.VIEWORGTAXID a
    # """)

    queries = [
        {'key':'acctloanlimithist', 'sql':acctloanlimithist, 'engine':1},

        # {'key':'vieworgtaxid', 'sql':vieworgtaxid, 'engine':1},
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data


def fetch_orgpersrole():
    """
    Fetch controlling person data from WH_ORGPERSROLE
    """
    query = text("""
    SELECT
        *
    FROM
        OSIBANK.WH_ORGPERSROLE a
    """)

    queries = [
        {'key':'wh_orgpersrole', 'sql':query, 'engine':1},
    ]

    data = cdutils.database.connect.retrieve_data(queries)
    return data

def fetch_holdbacks():
    """
    Fetch latest balamt for holdback subaccounts (BALCATCD='HOLD') from ACCTSUBACCT and ACCTBALHIST.
    """
    query = text("""
    SELECT
        acctnbr,
        subacctnbr,
        balcatcd,
        balamt
    FROM (
        SELECT
            a.acctnbr,
            a.subacctnbr,
            a.balcatcd,
            h.balamt,
            h.effdate,
            ROW_NUMBER() OVER (PARTITION BY a.acctnbr, a.subacctnbr ORDER BY h.effdate DESC) AS rn
        FROM
            OSIBANK.ACCTSUBACCT a
        INNER JOIN
            OSIBANK.ACCTBALHIST h ON a.acctnbr = h.acctnbr AND a.subacctnbr = h.subacctnbr
        WHERE
            a.BALCATCD = 'HOLD'
    )
    WHERE rn = 1
    """)

    queries = [
        {'key':'holdbacks', 'sql':query, 'engine':1},
    ]

    data = cdutils.database.connect.retrieve_data(queries)
    return data
