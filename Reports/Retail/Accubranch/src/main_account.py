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

from pathlib import Path
from typing import List
import argparse
from datetime import datetime

import numpy as np
import pandas as pd # type: ignore

import src.additional_fields
import src.fetch_data # type: ignore
import src.core_transform # type: ignore
import cdutils.pkey_sqlite # type: ignore
import cdutils.hhnbr # type: ignore
import cdutils.loans.calculations
import cdutils.inactive_date
import cdutils.input_cleansing
import src.data_cleaning_main
# Current (doesn't really work without)
# data = src.fetch_data.fetch_data()



# %%
data2020 = src.data_cleaning_main.run_data_cleaning_pipeline(
    as_of_date=datetime(2020, 12, 31),
    data_source="production",
    exclude_org_types=["MUNI","TRST"]
)

data2021 = src.data_cleaning_main.run_data_cleaning_pipeline(
    as_of_date=datetime(2021, 12, 31),
    data_source="production",
    exclude_org_types=["MUNI","TRST"]
)

data2022 = src.data_cleaning_main.run_data_cleaning_pipeline(
    as_of_date=datetime(2022, 12, 30),
    data_source="production",
    exclude_org_types=["MUNI","TRST"]
)

data2023 = src.data_cleaning_main.run_data_cleaning_pipeline(
    as_of_date=datetime(2023, 12, 29),
    data_source="production",
    exclude_org_types=["MUNI","TRST"]
)

data2024 = src.data_cleaning_main.run_data_cleaning_pipeline(
    as_of_date=datetime(2024, 12, 31),
    data_source="production",
    exclude_org_types=["MUNI","TRST"]
)

# %%
import src.annual_deposit_history


dataframes = [data2020, data2021, data2022, data2023, data2024]
dates = ['2020-12-31', '2021-12-31', '2022-12-31', '2023-12-31','2024-12-31']
five_yr_history = src.annual_deposit_history.create_time_series_analysis(dataframes, dates)

# %%
FIVE_YR_HISTORY = Path('./output/five_yr_history.csv')
five_yr_history.to_csv(FIVE_YR_HISTORY, index=False)

# %% [markdown]
# ### Data Requirment #1: 5 Year History of Branches
# - Complete

# %%
data_current = src.data_cleaning_main.run_data_cleaning_pipeline(
    as_of_date=datetime(2025, 6, 30),
    data_source="production",
    exclude_org_types=["MUNI","TRST"]
)

# %%
# Create Primary Key (Tax Owner of Account)
data_current['Primary Key'] = np.where(
    data_current['taxrptfororgnbr'].isnull(), 
    'P' + data_current['taxrptforpersnbr'].astype(str), 
    'O' + data_current['taxrptfororgnbr'].astype(str)
)

# %%
# Create Address field
def concat_address(text1, text2, text3):
    parts = [str(p).strip() for p in [text1, text2, text3] if p and str(p).strip()]
    return ' '.join(parts) if parts else pd.NA

data_current['Address'] = data_current.apply(
    lambda row: concat_address(row.get('text1'), row.get('text2'), row.get('text3')),
    axis=1
)

# %%
# Filter to Loans & Deposits
data_current = data_current[data_current['mjaccttypcd'].isin(['CML','MLN','CNS','MTG','CK','SAV','TD'])].copy()

# %%
# Exclude ACH Manager products (coded as CML)
data_current = data_current[~data_current['currmiaccttypcd'].isin(['CI07'])].copy()

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

data_current['Account Type'] = data_current['mjaccttypcd'].apply(map_account_type)

# %%
data_current['Account Type'] = np.where(
    (data_current['Account Type'] == 'Commercial Loan') & 
    (data_current['loanofficer'].isin(['EBL PROGRAM ADMIN','SBLC LOAN OFFICER'])),
    'Small Business Loan',
    data_current['Account Type']
    )

# %%
data_current['orig_ttl_loan_amt'] = np.where(
    data_current['mjaccttypcd'].isin(['CML','MLN','MTG','CNS']),
    data_current['orig_ttl_loan_amt'],
    pd.NA
)

# %%
data_current['Business/Individual'] = np.where(
    data_current['taxrptfororgnbr'].isnull(),
    'Individual',
    'Business'
)

# %%
data_current = data_current.rename(columns={
    'cityname':'City',
    'statecd':'State',
    'zipcd':'Zip',
    'branchname':'Branch Associated',
    'contractdate':'Date Account Opened',
    'Net Balance':'Current Balance',
    'orig_ttl_loan_amt':'Original Balance (Loans)',
    'datebirth':'Date of Birth'
}).copy()

# %%
data_current_final = data_current[[
    'Primary Key',
    'Address',
    'City',
    'State',
    'Zip',
    'Branch Associated',
    'Account Type',
    'Date Account Opened',
    'Current Balance',
    'Original Balance (Loans)',
    'Date of Birth'
]].copy()

# %%
data_current_final

# %%
ACCOUNT_OUTPUT = Path('./output/account_data.csv')
data_current_final.to_csv(ACCOUNT_OUTPUT, index=False)

# %%



