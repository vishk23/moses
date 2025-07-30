"""
Finding historical data for a given account number.
"""

import cdutils.database.connect # type: ignore
from sqlalchemy import text # type: ignore

def fetch_data_historical_acctcommon(acctnbr):
    """
    Main data query
    """
    # Engine 1
    acctcommon_hist = text(f"""
    SELECT 
        a.ACCTNBR,
        a.PRODUCT,
        a.EFFDATE
    FROM 
        COCCDM.WH_ACCTCOMMON a
    WHERE
        a.ACCTNBR = {acctnbr}
        
    """)

    queries = [
        {'key':'wh_acctcommon', 'sql':acctcommon_hist, 'engine':2},
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data
