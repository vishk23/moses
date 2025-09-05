# Core logic specific to project/report

import pandas as pd
from pathlib import Path
from deltalake import DeltaTable
import src.config
import src.sba_loans.fetch_data

def main_report_creation():
        
    # def main_report_creation():
    # Get Lakehouse tables
    df = DeltaTable(src.config.SILVER / "account").to_pandas()
    wh_acctloan = DeltaTable(src.config.BRONZE / "wh_acctloan").to_pandas()
    wh_loans = DeltaTable(src.config.BRONZE / "wh_loans").to_pandas()



    # Filter to SBA loans
    df = df[df['product'].str.contains('SBA',case=False,na=False)].copy()
    df = df[[
        'acctnbr',
        'product',
        'curracctstatcd',
        'ownersortname',
        'noteintrate',
        'Net Balance'
    ]].copy()
    df = df.rename(columns={
        'noteintrate':'Interest Rate (%)',
        'Net Balance':'Closing Balance'
    }).copy()

    wh_acctloan = wh_acctloan[[
        'acctnbr',
        'currduedate'
    ]].copy()

    wh_acctloan = wh_acctloan.rename(columns={
        'currduedate':'Next Installment Due Date (MM/DD/YYYY)'
    }).copy()
    wh_acctloan['Next Installment Due Date (MM/DD/YYYY)'] = pd.to_datetime(wh_acctloan['Next Installment Due Date (MM/DD/YYYY)']).copy()
    wh_acctloan['acctnbr'] = wh_acctloan['acctnbr'].astype(str)

    wh_loans = wh_loans[[
        'acctnbr',
        'intpaidtodate'
    ]].copy()

    wh_loans = wh_loans.rename(columns={
        'intpaidtodate':'Interest Period To (MM/DD/YYYY)'
    }).copy()
    wh_loans['acctnbr'] = wh_loans['acctnbr'].astype(str)

    merged_df = df.merge(wh_acctloan, on='acctnbr', how='left').merge(wh_loans, how='left', on='acctnbr')




    # %%
    rtxnbal_data = src.sba_loans.fetch_data.fetch_rtxnbal()

    # %%
    # rtxn = data['wh_rtxn'].copy()
    rtxnbal = rtxnbal_data['wh_rtxnbal'].copy()

    # %%
    # Convert 'amt' column to a numeric type. 
    # errors='coerce' will turn any non-numeric values into NaN (Not a Number)
    rtxnbal['amt'] = pd.to_numeric(rtxnbal['amt'], errors='coerce')

    # It's good practice to fill any resulting NaN values, for instance with 0
    rtxnbal['amt'] = rtxnbal['amt'].fillna(0)

    # %%
    # 1. Filter for 'PDSB' transaction types
    advances_raw = rtxnbal[rtxnbal['rtxntypcd'] == 'PDSB'].copy()

    # 2. Group by account number and sum the amount
    df_advances = advances_raw.groupby('acctnbr')['amt'].sum().reset_index()

    # 3. Rename the column for clarity
    df_advances = df_advances.rename(columns={'amt': 'Advances'})

    # 4. Convert acctnbr to string for merging
    df_advances['acctnbr'] = df_advances['acctnbr'].astype(str)

    # print("\n--- Advances DataFrame (df_advances) ---")
    # print(df_advances)

    # %%
    # 1. Filter for 'SPMT' transaction types
    spmt_raw = rtxnbal[rtxnbal['rtxntypcd'] == 'SPMT'].copy()

    # 2. Group by account and balance category, then sum the amounts
    payments = spmt_raw.groupby(['acctnbr', 'baltypcd'])['amt'].sum()

    # 3. Unstack the 'balcatcd' level to turn 'BAL' and 'INT' into columns
    df_payments = payments.unstack(level='baltypcd').fillna(0).reset_index()

    # 4. Rename columns for clarity
    df_payments = df_payments.rename(columns={
        'BAL': 'Principal Paid',
        'INT': 'Interest Paid'
    })

    # 5. Convert acctnbr to string for merging
    df_payments['acctnbr'] = df_payments['acctnbr'].astype(str)

    # print("\n--- Combined Payments DataFrame ---")
    # print(df_payments)

    # %%
    # Optional: Create two fully separate DataFrames as requested
    df_principal = df_payments[['acctnbr', 'Principal Paid']].copy()
    df_interest = df_payments[['acctnbr', 'Interest Paid']].copy()

    # print("\n--- Principal Paid DataFrame (df_principal) ---")
    # print(df_principal)

    # print("\n--- Interest Paid DataFrame (df_interest) ---")
    # print(df_interest)

    # %%
    # Ensure the key in the main DataFrame is also a string
    merged_df['acctnbr'] = merged_df['acctnbr'].astype(str)

    # 1. Merge the advances
    final_df = pd.merge(merged_df, df_advances, on='acctnbr', how='left')

    # 2. Merge the payments (using the combined df_payments is more efficient)
    final_df = pd.merge(final_df, df_payments, on='acctnbr', how='left')

    # 3. After merging, fill any NaN values with 0
    # This handles accounts that were in merged_df but had no payments/advances
    final_df[['Advances', 'Principal Paid', 'Interest Paid']] = final_df[['Advances', 'Principal Paid', 'Interest Paid']].fillna(0)

    final_df = final_df.rename(columns={
        'acctnbr':'SBA Loan Number',
        'Advances':'Amount Disbursed This Period',
        'Interest Paid':'Interest Payment',
        'Principal Paid':'Principal Payment'
    }).copy()

    final_df = final_df[[
        # Insert from below exact ordering of columns
    ]].copy()
    # Put into specific order below:
    # acctnbr
#     Next Installment Due Date (MM/DD/YYYY)  0 non-null      float64
#     Amount Disbursed This Period            0 non-null      float64
#     Interest Rate (%)                       0 non-null      float64
#     Interest Payment                        0 non-null      float64
#     Principal Payment                       0 non-null      float64
#     Interest Period To (MM/DD/YYYY)         0 non-null      float64
#     Closing Balance   
# product
# ownersortname
# curracctstatcd              

    # %%
    return final_df

    # %%




