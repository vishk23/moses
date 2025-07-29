# %%
## Memorializing this as the easy way to lookup accounts


# %%
"""
Main Entry Point
"""
from pathlib import Path
from typing import List
import argparse
from datetime import datetime

import pandas as pd # type: ignore

import cdutils.inactive_date
import cdutils.loans.calculations
import cdutils.acct_lookup_daily.src.fetch_data # type: ignore
import cdutils.acct_lookup_daily.src.core_transform # type: ignore
import cdutils.pkey_sqlite # type: ignore
import cdutils.hhnbr # type: ignore

def create_daily_acct_table():
    data = cdutils.acct_lookup.src.fetch_data.fetch_data()

    # # # Core transformation pipeline
    raw_data = cdutils.acct_lookup.src.core_transform.main_pipeline(data)

    # Raw data with pkey appended
    raw_data = cdutils.pkey_sqlite.add_pkey(raw_data)
    raw_data = cdutils.pkey_sqlite.add_ownership_key(raw_data)
    raw_data = cdutils.pkey_sqlite.add_address_key(raw_data)

    # %%
    househldacct = data['househldacct'].copy()
    raw_data = cdutils.hhnbr.add_hh_nbr(raw_data, househldacct)

    # %%
    raw_data

    # %%

    # %%
    loan_category_df = cdutils.loans.calculations.categorize_loans(raw_data)

    # %%
    loan_category_df = loan_category_df[['acctnbr','Category']].copy()

    # %%
    df = pd.merge(raw_data, loan_category_df, on='acctnbr', how='left')

    # %%
    df

    # %%

    df = cdutils.inactive_date.append_inactive_date(df)

    # %%
    return df 
# %%



