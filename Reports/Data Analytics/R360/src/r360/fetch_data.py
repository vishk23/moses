"""
Database Fetching Package

This package provides the ability to create custom SQL queries that can be used throughout the data pipeline.

Quick start:
    import src.cdutils.database

    # Simple data fetch
    data = src.cdutils.database.fetch_data()
"""

import cdutils.database.connect
from sqlalchemy import text # type: ignore
import pandas as pd # type: ignore

def fetch_data() -> dict[str, pd.DataFrame]:
    """
    Fetches data from SQL database

    Args:
        None
    
    Returns:

    """
    # acctcommon
    # engine 1
    acctcommon = text("""
    SELECT 
        a.ACCTNBR,
        a.OWNERSORTNAME,
        a.MJACCTTYPCD,
        a.CURRMIACCTTYPCD,
        a.CURRACCTSTATCD,
        a.TAXRPTFORPERSNBR,
        a.TAXRPTFORORGNBR,
        a.PRODUCT,
        a.BOOKBALANCE,
        a.NOTEINTRATE
    FROM 
        OSIBANK.WH_ACCTCOMMON a
    """)

    persaddruse = text("""
    SELECT 
        a.PERSNBR,
        a.ADDRNBR
    FROM 
        OSIBANK.PERSADDRUSE a
    WHERE
        a.ADDRUSECD IN ('PRI')
    """)

    orgaddruse = text("""
    SELECT 
        a.ORGNBR,
        a.ADDRNBR
    FROM 
        OSIBANK.ORGADDRUSE a
    WHERE
        a.ADDRUSECD IN ('PRI')
    """)

    wh_addr = text("""
    SELECT 
        a.ADDRNBR,
        a.TEXT1,
        a.TEXT2,
        a.TEXT3,
        a.CITYNAME,
        a.STATECD,
        a.ZIPCD
    FROM 
        OSIBANK.WH_ADDR a
    """)

    wh_allroles = text("""
    SELECT
        *
    FROM 
        OSIBANK.WH_ALLROLES a
    WHERE
        a.ACCTROLECD in ('OWN', 'GUAR', 'LNCO', 'Tax Owner')
    """)

    queries = [
        # {'key':'lookup_df', 'sql':lookup_df, 'engine':1},
        {'key':'acctcommon', 'sql':acctcommon, 'engine':1},
        {'key':'persaddruse', 'sql':persaddruse, 'engine':1},
        {'key':'orgaddruse', 'sql':orgaddruse, 'engine':1},
        {'key':'wh_addr', 'sql':wh_addr, 'engine':1},
        {'key':'wh_allroles', 'sql':wh_allroles, 'engine':1},
    ]

    data = cdutils.database.connect.retrieve_data(queries)
    return data