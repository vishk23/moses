"""
Data fetching module for CRE Reporting Board.

This module handles fetching data from COCC data mart for CRE portfolio analysis.
All database queries and data retrieval logic is contained here.

Usage:
    from src.cre_board_reporting.fetch_data import fetch_cre_data
"""

import cdutils.database.connect
import cdutils.caching
from sqlalchemy import text
import src.config

def fetch_cre_data():
    """
    Fetch CRE portfolio data from COCC data mart.
    
    Returns:
        dict: Dictionary containing DataFrames for each table:
            - wh_acctcommon: Account common information
            - wh_loans: Loan details
            - wh_acctloan: Account loan specifics  
            - wh_acct: Account data
            - wh_prop: Property information
            - wh_prop2: Additional property details
    """
    
    wh_acctcommon = text("""
    SELECT
        a.ACCTNBR,
        a.OWNERSORTNAME,
        a.PRODUCT,
        a.NOTEOPENAMT,
        a.RATETYPCD,
        a.MJACCTTYPCD,
        a.CURRMIACCTTYPCD,
        a.CURRACCTSTATCD,
        a.NOTEINTRATE,
        a.BOOKBALANCE,
        a.NOTEBAL,
        a.RATETYPCD
    FROM
        COCCDM.WH_ACCTCOMMON a
    WHERE
        (a.CURRACCTSTATCD IN ('ACT','NPFM')) AND
        (a.MJACCTTYPCD IN ('CML','MLN')) AND
        (a.EFFDATE = (SELECT MAX(EFFDATE) FROM COCCDM.WH_ACCTCOMMON))
    """)

    wh_loans = text("""
    SELECT
        a.ACCTNBR,
        a.ORIGDATE,
        a.CURRTERM,
        a.LOANIDX,
        a.RCF,
        a.AVAILBALAMT,
        a.FDICCATDESC,
        a.ORIGBAL
    FROM
        COCCDM.WH_LOANS a
    WHERE
        (a.RUNDATE = (SELECT MAX(RUNDATE) FROM COCCDM.WH_LOANS))
    """)

    wh_acctloan = text("""
    SELECT
        a.ACCTNBR,
        a.CREDITLIMITAMT,
        a.ORIGINTRATE,
        a.MARGINFIXED,
        a.FDICCATCD,
        a.AMORTTERM,
        a.TOTALPCTSOLD,
        a.COBAL,
        a.CREDLIMITCLATRESAMT
    FROM
        COCCDM.WH_ACCTLOAN a
    WHERE
        (a.EFFDATE = (SELECT MAX(EFFDATE) FROM COCCDM.WH_ACCTLOAN))
    """)

    wh_acct = text("""
    SELECT
        a.ACCTNBR,
        a.DATEMAT
    FROM
        COCCDM.WH_ACCT a
    WHERE
        (a.RUNDATE = (SELECT MAX(RUNDATE) FROM COCCDM.WH_ACCT))
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

    queries = [
        {'key':'wh_acctcommon', 'sql':wh_acctcommon, 'engine':2},
        {'key':'wh_loans', 'sql':wh_loans, 'engine':2},
        {'key':'wh_acctloan', 'sql':wh_acctloan, 'engine':2},
        {'key':'wh_acct', 'sql':wh_acct, 'engine':2},
        {'key':'wh_prop', 'sql':wh_prop, 'engine':1},
        {'key':'wh_prop2', 'sql':wh_prop2, 'engine':1},
    ]

    data = cdutils.database.connect.retrieve_data(queries)
    
    # Cache data for development if enabled
    if hasattr(src.config, 'USE_CACHING') and src.config.USE_CACHING and hasattr(src.config, 'CACHE_DIR') and src.config.CACHE_DIR:
        cdutils.caching.cache_data(str(src.config.CACHE_DIR), data)
        
    return data

def validate_data(data):
    """
    Validate that all required data is present and has expected structure.
    
    Args:
        data (dict): Dictionary of DataFrames from fetch_cre_data()
        
    Returns:
        bool: True if validation passes
        
    Raises:
        ValueError: If validation fails
    """
    required_tables = ['wh_acctcommon', 'wh_loans', 'wh_acctloan', 'wh_acct', 'wh_prop', 'wh_prop2']
    
    for table in required_tables:
        if table not in data:
            raise ValueError(f"Missing required table: {table}")
        if data[table].empty:
            raise ValueError(f"Table {table} is empty")
            
    # Validate key fields are present
    if 'acctnbr' not in data['wh_acctcommon'].columns:
        raise ValueError("Missing acctnbr field in wh_acctcommon")
        
    return True
