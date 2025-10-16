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

def fetch_data():
    """
    Main data query
    """

    wh_rtxn = text(f"""
    SELECT
        *
    FROM
        COCCDM.WH_RTXN
    """)

    wh_rtxnbal = text(f"""
    SELECT
        r.*,
        b.*
    FROM
        COCCDM.WH_RTXN r
    JOIN
        COCCDM.WH_RTXNBAL b
    ON
        r.rtxnnbr = b.rtxnnbr
        AND r.rundate = b.rundate
    ORDER BY
        r.rundate DESC
    LIMIT 10000
    """)

    queries = [
        {'key':'wh_rtxn', 'sql':wh_rtxn, 'engine':2},
        {'key':'wh_rtxnbal', 'sql':wh_rtxnbal, 'engine':2},
    ]

    data = cdutils.database.connect.retrieve_data(queries)
    return data

def rtxn_check():
    """
    Verification query to reconcile account balances with transaction flows.
    Logic: Starting Balance (1/1/2025) + Sum(Transactions) = Ending Balance (Current)
    """

    verification_query = text("""
    WITH starting_balance AS (
        SELECT
            ACCTNBR,
            NOTEBAL AS start_bal,
            EFFDATE AS start_date
        FROM
            COCCDM.WH_ACCTCOMMON
        WHERE
            ACCTNBR = '1234'
            AND EFFDATE = '2025-01-01'
    ),
    ending_balance AS (
        SELECT
            ACCTNBR,
            NOTEBAL AS end_bal,
            EFFDATE AS end_date
        FROM
            COCCDM.WH_ACCTCOMMON
        WHERE
            ACCTNBR = '1234'
            AND EFFDATE = (
                SELECT MAX(EFFDATE)
                FROM COCCDM.WH_ACCTCOMMON
                WHERE ACCTNBR = '1234'
            )
    ),
    transaction_sum AS (
        SELECT
            ACCTNBR,
            SUM(TRANAMT) AS total_txn_amt,
            COUNT(DISTINCT ACCTNBR || '-' || SUBACCTNBR || '-' || RTXNNBR) AS txn_count,
            MIN(RUNDATE) AS first_txn_date,
            MAX(RUNDATE) AS last_txn_date
        FROM
            COCCDM.WH_RTXN
        WHERE
            ACCTNBR = '1234'
            AND RUNDATE >= '2025-01-01'
        GROUP BY
            ACCTNBR
    )
    SELECT
        s.ACCTNBR,
        s.start_bal,
        s.start_date,
        e.end_bal,
        e.end_date,
        t.total_txn_amt,
        t.txn_count,
        t.first_txn_date,
        t.last_txn_date,
        (s.start_bal + t.total_txn_amt) AS calculated_end_bal,
        e.end_bal AS actual_end_bal,
        (e.end_bal - (s.start_bal + t.total_txn_amt)) AS difference,
        CASE
            WHEN ABS(e.end_bal - (s.start_bal + t.total_txn_amt)) < 0.01 THEN 'MATCH'
            ELSE 'MISMATCH'
        END AS reconciliation_status
    FROM
        starting_balance s
    JOIN
        ending_balance e ON s.ACCTNBR = e.ACCTNBR
    LEFT JOIN
        transaction_sum t ON s.ACCTNBR = t.ACCTNBR
    """)

    queries = [
        {'key':'rtxn_verification', 'sql':verification_query, 'engine':2},
    ]

    data = cdutils.database.connect.retrieve_data(queries)
    return data
