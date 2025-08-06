"""
Data fetching module for CRE Reporting Board.

This module handles fetching data from COCC data mart for CRE portfolio analysis.
All database queries and data retrieval logic is contained here.

Usage:
    from src.cre_board_reporting.fetch_data import fetch_cre_data
"""

import cdutils.database.connect
from sqlalchemy import text
import src.config

def fetch_prop_data():
    """
    Fetch CRE portfolio data from COCC data mart.
    
    Returns:
        dict: Dictionary containing DataFrames for each table:
            - wh_prop: Property information
            - wh_prop2: Additional property details
    """
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

    queries = [
        {'key':'wh_prop', 'sql':wh_prop, 'engine':1},
        {'key':'wh_prop2', 'sql':wh_prop2, 'engine':1},
    ]

    data = cdutils.database.connect.retrieve_data(queries)
    
    # Cache data for development if enabled
    if hasattr(src.config, 'USE_CACHING') and src.config.USE_CACHING and hasattr(src.config, 'CACHE_DIR') and src.config.CACHE_DIR:
        cdutils.caching.cache_data(str(src.config.CACHE_DIR), data)
        
    return data

