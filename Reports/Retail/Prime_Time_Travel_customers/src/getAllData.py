"""
Finding historical data for a given account number.
"""

import cdutils.database.connect # type: ignore
from sqlalchemy import text # type: ignore

def fetch_data_persuserfield():
    """
    Main data query
    """
    # Engine 1
    persuerfield = text(f"""
    SELECT 
        *
    FROM 
        OSIBANK.PERSUSERFIELD a
    WHERE
        a.USERFIELDCD  = 'PTTM' OR a.USERFIELDCD = 'PTTR' OR a.USERFIELDCD = 'PRTD'
    """)

    queries = [
        {'key':'PERSUSERFIELD', 'sql':persuerfield, 'engine':1},
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data['PERSUSERFIELD'].copy()


"""
Finding historical data for a given account number.
"""

def fetch_data_allroles():
    """
    Main data query
    """
    # Engine 1
    allroles = text(f"""
    SELECT 
        *
    FROM 
        OSIBANK.WH_ALLROLES 
    """)

    wh_pers = text(f"""
    SELECT 
        *
    FROM 
        OSIBANK.WH_PERS
    """)

    queries = [
        {'key':'WH_ALLROLES', 'sql':allroles, 'engine':1},
        {'key':'WH_PERS', 'sql':wh_pers, 'engine':1}
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data
