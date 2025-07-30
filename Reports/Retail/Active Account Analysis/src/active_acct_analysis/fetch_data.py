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

def fetch_data():
    """
    Main data query
    """
    wh_agreement = text("""SELECT * FROM OSIBANK.WH_AGREEMENT a""")
    wh_org = text("""SELECT * FROM OSIBANK.WH_ORG""")
    wh_pers = text("""SELECT * FROM OSIBANK.WH_PERS""")
    cardagrementtyp = text("""SELECT a.AGREETYPCD, a.AGREETYPDESC FROM OSIBANK.CARDAGREEMENTTYP a""")

    queries = [
        {'key':'wh_agreement', 'sql':wh_agreement, 'engine':1},
        {'key':'wh_org', 'sql':wh_org, 'engine':1},
        {'key':'wh_pers', 'sql':wh_pers, 'engine':1},
        {'key':'cardagreementtyp', 'sql':cardagrementtyp, 'engine':1},
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data
