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


def fetch_prop():
    """
    Main data query
    """
    # Engine 1
    wh_prop = text("""
    SELECT 
        *
    FROM 
        OSIBANK.WH_PROP a
    """)

    wh_prop2 = text("""
    SELECT 
        *
    FROM 
        OSIBANK.WH_PROP2 a 
    """)

    queries = [
        # {'key':'acctcommon', 'sql':acctcommon, 'engine':2},
        {'key':'wh_prop', 'sql':wh_prop, 'engine':1},
        {'key':'wh_prop2', 'sql':wh_prop2, 'engine':1},
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data

def fetch_insurance():
    """
    Main data query
    """
    acctpropins = text("""
    SELECT 
        *
    FROM 
        OSIBANK.ACCTPROPINS a
    """)

    wh_inspolicy = text("""
    SELECT
        *
    FROM
        OSIBANK.WH_INSPOLICY a
    """)


    queries = [
        {'key':'acctpropins', 'sql':acctpropins, 'engine':1},
        {'key':'wh_inspolicy', 'sql':wh_inspolicy, 'engine':1},
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data

def fetch_account_data():
    """
    Main data query
    """
    
    wh_acctcommon = text(f"""
    SELECT
        *
    FROM
        OSIBANK.WH_ACCTCOMMON a
    """)

    wh_loans = text(f"""
    SELECT
        *
    FROM
        OSIBANK.WH_LOANS a
    """)

    wh_acctloan = text(f"""
    SELECT
        *
    FROM
        OSIBANK.WH_ACCTLOAN a
    """)

    queries = [
        {'key':'wh_acctcommon', 'sql':wh_acctcommon, 'engine':1},
        {'key':'wh_loans', 'sql':wh_loans, 'engine':1},
        {'key':'wh_acctloan', 'sql':wh_acctloan, 'engine':1},
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data


def fetch_addruse_tables():
    """
    Main data query
    """
    persaddruse = text("""
    SELECT 
        *
    FROM 
        OSIBANK.PERSADDRUSE a
    """)

    orgaddruse = text("""
    SELECT
        *
    FROM
        OSIBANK.ORGADDRUSE a
    """)


    queries = [
        {'key':'persaddruse', 'sql':persaddruse, 'engine':1},
        {'key':'orgaddruse', 'sql':orgaddruse, 'engine':1},
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data

def fetch_rtxn():
    """
    Main data query
    """

    wh_rtxn = text("""
    SELECT
        *
    FROM
        OSIBANK.WH_RTXN a
    """)

    wh_rtxnbal = text("""
    SELECT
        *
    FROM
        OSIBANK.WH_RTXNBAL a
    """)

    queries = [
        {'key':'wh_rtxn', 'sql':wh_rtxn, 'engine':1},
        {'key':'wh_rtxnbal', 'sql':wh_rtxnbal, 'engine':1},
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data

def fetch_userfields():
    """
    Main data query
    """

    wh_acctuserfields = text("""
    SELECT
        *
    FROM
        OSIBANK.WH_ACCTUSERFIELDS a
    """)

    wh_orguserfields = text("""
    SELECT
        *
    FROM
        OSIBANK.WH_ORGUSERFIELDS a
    """)

    wh_persuserfields = text("""
    SELECT
        *
    FROM
        OSIBANK.WH_PERSUSERFIELDS a
    """)


    queries = [
        {'key':'wh_acctuserfields', 'sql':wh_acctuserfields, 'engine':1},
        {'key':'wh_orguserfields', 'sql':wh_orguserfields, 'engine':1},
        {'key':'wh_persuserfields', 'sql':wh_persuserfields, 'engine':1},
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data

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
        a.CURRINVRRATE,
        a.DATELASTMAINT
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

def fetch_phone():
    """
    Main data query
    """
    persphone = text("""
    SELECT
        *
    FROM
        OSIBANK.PERSPHONE a
    """)

    orgphone = text("""
    SELECT
        *
    FROM
        OSIBANK.ORGPHONE a
    """)


    queries = [
        {'key':'persphone', 'sql':persphone, 'engine':1},
        {'key':'orgphone', 'sql':orgphone, 'engine':1},

    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data
