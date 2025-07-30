"""
Main Entry Point
"""
from pathlib import Path
from typing import List
import argparse
from datetime import datetime

import pandas as pd # type: ignore

import src.fetch_data # type: ignore
import src.core_transform # type: ignore
import cdutils.pkey_sqlite # type: ignore
import cdutils.hhnbr # type: ignore
import cdutils.loans.calculations # type: ignore
import cdutils.inactive_date # type: ignore


def pkey():

    data = src.fetch_data.fetch_data()

    # # # Core transformation pipeline
    raw_data = src.core_transform.main_pipeline(data)

    # Raw data with pkey appended
    raw_data = cdutils.pkey_sqlite.add_pkey(raw_data)
    raw_data = cdutils.pkey_sqlite.add_ownership_key(raw_data)
    raw_data = cdutils.pkey_sqlite.add_address_key(raw_data)
    
    househldacct = data['househldacct'].copy()

    raw_data = cdutils.hhnbr.add_hh_nbr(raw_data, househldacct)
    loan_category_df = cdutils.loans.calculations.categorize_loans(raw_data)
    loan_category_df = loan_category_df[['acctnbr','Category']].copy()
    df = pd.merge(raw_data, loan_category_df, on='acctnbr', how='left')
    
    df = cdutils.inactive_date.append_inactive_date(df)
    
    return df