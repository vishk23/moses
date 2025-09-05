# Core logic specific to project/report

import pandas as pd
from pathlib import Path
from deltalake import DeltaTable
import src.config

def main_report_creation():
    # Get Lakehouse tables
    df = DeltaTable(src.config.SILVER / "account").to_pandas()
    wh_acctloan = DeltaTable(src.config.BRONZE / "wh_acctloan").to_pandas()
    wh_loans = DeltaTable(src.config.BRONZE / "wh_loans").to_pandas()

    # Need to get rtxn & wh_totalpaymentsdue

    # Filter to SBA loans
    df = df[df['product'].str.contains('SBA',case=False,na=False)].copy()
    df = df[[
        'acctnbr',
        'noteintrate',
        'Net Balance'
    ]].copy()
    df = df.rename(columns={
        'noteintrate':'Interest Rate (%)',
        'Net Balance':'Closing Balance'
    })

    wh_acctloan = wh_acctloan[[
        'acctnbr',
        'currduedate'
    ]].copy()

    wh_acctloan = wh_acctloan.rename(columns={
        'currduedate':'Next Installment Due Date (MM/DD/YYYY)'
    }).copy()
    wh_acctloan = pd.to_datetime(wh_acctloan['Next Installment Due Date (MM/DD/YYYY)']).copy()
    wh_acctloan['acctnbr'] = wh_acctloan['acctnbr'].astype(str)

    wh_loans = wh_loans[[
        'acctnbr',
        'intpaidtodate'
    ]].copy()

    wh_loans = wh_loans.rename(columns={
        'Interest Period To (MM/DD/YYYY)'
    }).copy()
    wh_loans['acctnbr'] = wh_loans['acctnbr'].astype(str)

    merged_df = df.merge(wh_acctloan, on='acctnbr', how='left').merge(wh_loans, how='left', on='acctnbr')
