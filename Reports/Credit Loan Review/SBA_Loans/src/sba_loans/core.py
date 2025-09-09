import pandas as pd
from pathlib import Path
from deltalake import DeltaTable
import src.config
import src.sba_loans.fetch_data

def main_report_creation():
    # Get Lakehouse tables
    df = DeltaTable(src.config.SILVER / "account").to_pandas()
    wh_acctloan = DeltaTable(src.config.BRONZE / "wh_acctloan").to_pandas()
    wh_loans = DeltaTable(src.config.BRONZE / "wh_loans").to_pandas()

    # Filter to SBA loans and select relevant columns
    df = df[df['product'].str.contains('SBA', case=False, na=False)].copy()
    df = df[[
        'acctnbr',
        'product',
        'curracctstatcd',
        'ownersortname',
        'noteintrate',
        'Net Balance'
    ]].copy()
    df = df.rename(columns={
        'noteintrate': 'Interest Rate (%)',
        'Net Balance': 'Closing Balance'
    }).copy()

    # Select and rename relevant columns from wh_acctloan
    wh_acctloan = wh_acctloan[[
        'acctnbr',
        'currduedate',
        'sbaacctnbr'
    ]].copy()
    wh_acctloan['sbaacctnbr'] = wh_acctloan['sbaacctnbr'].astype(str)
    
    wh_acctloan = wh_acctloan.rename(columns={
        'currduedate': 'Next Installment Due Date (MM/DD/YYYY)'
    }).copy()
    wh_acctloan['Next Installment Due Date (MM/DD/YYYY)'] = pd.to_datetime(wh_acctloan['Next Installment Due Date (MM/DD/YYYY)'])
    wh_acctloan['acctnbr'] = wh_acctloan['acctnbr'].astype(str)

    # Select and rename relevant columns from wh_loans
    wh_loans = wh_loans[[
        'acctnbr',
        'intpaidtodate'
    ]].copy()
    wh_loans = wh_loans.rename(columns={
        'intpaidtodate': 'Interest Period To (MM/DD/YYYY)'
    }).copy()
    wh_loans['acctnbr'] = wh_loans['acctnbr'].astype(str)

    # Merge the DataFrames
    merged_df = df.merge(wh_acctloan, on='acctnbr', how='left').merge(wh_loans, how='left', on='acctnbr')

    # Fetch rtxnbal data
    rtxnbal_data = src.sba_loans.fetch_data.fetch_rtxnbal()
    rtxnbal = rtxnbal_data['wh_rtxnbal'].copy()

    # Convert 'amt' column to numeric type
    rtxnbal['amt'] = pd.to_numeric(rtxnbal['amt'], errors='coerce')
    rtxnbal['amt'] = rtxnbal['amt'].fillna(0)

    # Filter for 'PDSB' transaction types and group by account number
    advances_raw = rtxnbal[rtxnbal['rtxntypcd'] == 'PDSB'].copy()
    df_advances = advances_raw.groupby('acctnbr')['amt'].sum().reset_index()
    df_advances = df_advances.rename(columns={'amt': 'Advances'})
    df_advances['acctnbr'] = df_advances['acctnbr'].astype(str)

    # Filter for 'SPMT' transaction types and group by account number and balance category
    spmt_raw = rtxnbal[rtxnbal['rtxntypcd'] == 'SPMT'].copy()
    payments = spmt_raw.groupby(['acctnbr', 'baltypcd'])['amt'].sum()
    df_payments = payments.unstack(level='baltypcd').fillna(0).reset_index()
    df_payments = df_payments.rename(columns={
        'BAL': 'Principal Paid',
        'INT': 'Interest Paid'
    })
    df_payments['acctnbr'] = df_payments['acctnbr'].astype(str)
    df_payments['Principal Paid'] = df_payments['Principal Paid'] * -1
    df_payments['Interest Paid'] = df_payments['Interest Paid'] * -1

    # Ensure the key in the main DataFrame is also a string
    merged_df['acctnbr'] = merged_df['acctnbr'].astype(str)

    # Merge the advances and payments
    final_df = pd.merge(merged_df, df_advances, on='acctnbr', how='left')
    final_df = pd.merge(final_df, df_payments, on='acctnbr', how='left')
    final_df[['Advances', 'Principal Paid', 'Interest Paid']] = final_df[['Advances', 'Principal Paid', 'Interest Paid']].fillna(0)

    # Rename and reorder columns
    final_df = final_df.rename(columns={
        'acctnbr': 'SBA Loan Number',
        'Advances': 'Amount Disbursed This Period',
        'Interest Paid': 'Interest Payment',
        'Principal Paid': 'Principal Payment',
        'sbaacctnbr':'SBA Guarantee Account Number'
    }).copy()
    final_df = final_df[[
        'SBA Loan Number',
        'Next Installment Due Date (MM/DD/YYYY)',
        'Amount Disbursed This Period',
        'Interest Rate (%)',
        'Interest Payment',
        'Principal Payment',
        'Interest Period To (MM/DD/YYYY)',
        'Closing Balance',
        'product',
        'ownersortname',
        'curracctstatcd',
        'SBA Guarantee Account Number'
    ]].copy()

    return final_df
