"""
Using the lookup query to inspect the DB tables
"""

import cdutils.database.connect # type: ignore
from sqlalchemy import text # type: ignore

def fetch_data():
    """
    Main data query
    """
    # Engine 1
    lookup_df = text("""
    SELECT 
        *
    FROM 
        sys.all_tab_columns col
    """)

    queries = [
        # {'key':'acctcommon', 'sql':acctcommon, 'engine':2},
        {'key':'lookup_df', 'sql':lookup_df, 'engine':1},
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data
