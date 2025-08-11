import cdutils.database.connect # type: ignore
from sqlalchemy import text # type: ignore

def fetch_data():
    """
    Main data query
    """
    wh_acctcommon = text(f"""
    SELECT
        a.OWNERSORTNAME,
        a.LOANOFFICER,
        a.ACCTOFFICER
    FROM
        OSIBANK.WH_ACCTCOMMON a
    WHERE
        (a.CURRACCTSTATCD IN ('ACT','NPFM','DORM'))
        AND (a.MJACCTTYPCD IN ('CML','MLN','CK','SAV','TD'))
        AND (a.CURRMIACCTTYPCD != 'CI07')
    """)

    queries = [
        {'key':'wh_acctcommon', 'sql':wh_acctcommon, 'engine':1},
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data