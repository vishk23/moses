"""
Fetching data module. Aim is import all necessary fields up front, but if needed, you can define another function to be called here.

This uses a sliding window for the trailing 2 months, current and prior.

Usage:
    import src.cdutils.database
"""
import datetime
from typing import Dict

from sqlalchemy import text # type: ignore

import src.cdutils.database.connect

def fetch_data() -> Dict:
    """
    Fetch data from COCC in a sliding window fashion (trailing month end dates)
    """
    effdates = text("""
    SELECT DISTINCT
        a.EFFDATE
    FROM 
        COCCDM.WH_ACCTCOMMON a
    WHERE
        MONTHENDYN = 'Y'
    ORDER BY EFFDATE DESC
    """)

    queries = [
        {'key':'effdates', 'sql':effdates, 'engine':2},
    ]

    data = src.cdutils.database.connect.retrieve_data(queries)

    effdates = data['effdates'].copy()

    recent_me = effdates['effdate'][0]
    prior_me = effdates['effdate'][1]

    def main_query(monthend_date: datetime) -> Dict:
        """
        Takes in a date to query on and returns a dictionary with dataframes for each table.
        """
        wh_acctcommon = text(f"""
        SELECT
            a.EFFDATE,
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
            a.CONTRACTDATE
        FROM
            COCCDM.WH_ACCTCOMMON a
        WHERE
            (a.CURRACCTSTATCD IN ('ACT','NPFM')) AND
            (a.EFFDATE = TO_DATE('{monthend_date}', 'yyyy-mm-dd hh24:mi:ss'))
        """)

        wh_loans = text(f"""
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
            (a.RUNDATE = TO_DATE('{monthend_date}', 'yyyy-mm-dd hh24:mi:ss'))
        """)

        wh_acctloan = text(f"""
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
            (a.EFFDATE = TO_DATE('{monthend_date}', 'yyyy-mm-dd hh24:mi:ss'))
        """)

        wh_acct = text(f"""
        SELECT
            a.ACCTNBR,
            a.DATEMAT
        FROM
            COCCDM.WH_ACCT a
        WHERE
            (a.RUNDATE = TO_DATE('{monthend_date}', 'yyyy-mm-dd hh24:mi:ss'))
        """)

        queries = [
            {'key':'wh_acctcommon', 'sql':wh_acctcommon, 'engine':2},
            {'key':'wh_loans', 'sql':wh_loans, 'engine':2},
            {'key':'wh_acctloan', 'sql':wh_acctloan, 'engine':2},
            {'key':'wh_acct', 'sql':wh_acct, 'engine':2},
        ]

        data = src.cdutils.database.connect.retrieve_data(queries)
        return data

    prior_data = main_query(prior_me)
    current_data = main_query(recent_me)

    return prior_data, current_data 

