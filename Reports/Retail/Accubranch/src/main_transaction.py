# %%
# Add project root to sys.path to import src modules from notebooks/
import sys
import os
from pathlib import Path

project_root = Path(os.getcwd()).parent
os.chdir(project_root)

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

print(f"Working directory: {os.getcwd()}")
print(f"Python path includes: {project_root}")


# %%
import src.transactions.fetch_data
import pandas as pd
import numpy as np
from datetime import datetime

# %%
start_date = datetime(2024, 6, 30)
end_date = datetime(2025, 6, 30)
data = src.transactions.fetch_data.fetch_transactions_window_test(start_date=start_date, end_date=end_date)

# %%
rtxn = data['query'].copy()

# %%
rtxn

# %%
# # Skip for now, takes 84 minutes to load (12MM records)
# full_year = src.transactions.fetch_data.fetch_transactions_window()

# %%
# full_year

# %%
# rtxn_full = full_year['query'].copy()

# %%
# rtxn_full.info()

# %%
# from pathlib import Path

# %%

acct_data = src.transactions.fetch_data.fetch_account_data(datetime(2025,6,30))

# %%
acct_data = acct_data['wh_acctcommon'].copy()

# %%
acct_data

# %%
rtxn.info()

# %%
acct_data.info()

# %%
merged_rtxn = pd.merge(rtxn, acct_data, on='acctnbr', how='left')

# %%
merged_rtxn

# %%
# Create Primary Key (Tax Owner of Account)
merged_rtxn['Customer Unique ID'] = np.where(
    merged_rtxn['taxrptfororgnbr'].isnull(), 
    'P' + merged_rtxn['taxrptforpersnbr'].fillna(0).astype(int).astype(str), 
    'O' + merged_rtxn['taxrptfororgnbr'].fillna(0).astype(int).astype(str)
)

# %%
datetime_series = pd.to_datetime(merged_rtxn['actdatetime'], errors='coerce')
merged_rtxn['Date of Transaction'] = datetime_series.dt.strftime('%Y-%m-%d')
merged_rtxn['Time of Transaction'] = datetime_series.dt.strftime('%H:%M:%S')

# %%
merged_rtxn

# %%
# Create Account Type mapping - Easier to understand, based on our major field
def map_account_type(acct_code:str):
    """
    Map mjaccttypcd to friendly Account Type
    """
    mapping = {
        'CML':'Commercial Loan',
        'MLN':'Commercial Loan',
        'CNS':'Consumer Loan',
        'MTG':'Residential Loan',
        'CK':'Checking',
        'SAV':'Savings',
        'TD':'CD'
    }
    return mapping.get(str(acct_code).upper(), 'Other')

merged_rtxn['Account Type'] = merged_rtxn['mjaccttypcd'].apply(map_account_type)

# %%
merged_rtxn

# %%
merged_rtxn['Account Type'] = np.where(
    (merged_rtxn['Account Type'] == 'Commercial Loan') & 
    (merged_rtxn['loanofficer'].isin(['EBL PROGRAM ADMIN','SBLC LOAN OFFICER'])),
    'Small Business Loan',
    merged_rtxn['Account Type']
    )

# %%
merged_rtxn = merged_rtxn.rename(columns={
    'branchname':'Branch of Transaction',
    'rtxntypdesc':'Type of Transaction',
    'rtxnsourcecd':'Type of Teller'
}).copy()

# %%
merged_rtxn.info()

# %%
merged_rtxn

# %%
rtxn_final = merged_rtxn[[
    'Customer Unique ID',
    'Date of Transaction',
    'Time of Transaction',
    'Branch of Transaction',
    'Type of Teller', # rxtnsourcecd
    'Type of Transaction', # rtxntypdesc
    'Account Type' 
]].copy()

# %%
rtxn_final

# %%
print(f"Working directory: {os.getcwd()}")
print(f"Python path includes: {project_root}")

# %%
RTXN_OUTPUT = Path('./output/transaction.csv')
rtxn_final.to_csv(RTXN_OUTPUT, index=False)

# %% [markdown]
# For full transaction history (12MM records) -> 84 minutes to query and would be 180 minutes to write file to network drive

# %%



