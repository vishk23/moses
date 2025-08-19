"""
FDIC Recon: Full CML portfolio with Call codes
"""

from pathlib import Path
from typing import Dict

import pandas as pd # type: ignore
import numpy as np # type: ignore

import cdutils.joining # type: ignore
import cdutils.input_cleansing # type: ignore
import cdutils.loans.calculations # type: ignore
import src.transformations.joining
import src.transformations.calculations # type: ignore

def main_pipeline_bt(data: Dict):
    """
    Main data pipeline for the balance tracker. This ties back to the Call Report as a check.
    """

    # # Cache data for development
    # src.cdutils.caching.cache_data(r'C:\Users\w322800\Documents\cre_caching', data)
    
    # # Unpack data into dataframes
    wh_acctcommon = data['wh_acctcommon'].copy()
    wh_loans = data['wh_loans'].copy()
    wh_acctloan = data['wh_acctloan'].copy()
    wh_acct = data['wh_acct'].copy()

    current_date = wh_acctcommon['effdate'].iloc[0].strftime('%m%d%y')

    # Datatype manipulation
    acctcommon_schema = {'acctnbr':'str'}
    wh_acctcommon = cdutils.input_cleansing.enforce_schema(wh_acctcommon, acctcommon_schema)
    loans_schema = {'acctnbr':'str'}
    wh_loans = cdutils.input_cleansing.enforce_schema(wh_loans, loans_schema)
    acctloan_schema = {'acctnbr':'str'}
    wh_acctloan = cdutils.input_cleansing.enforce_schema(wh_acctloan, acctloan_schema)

    # Transforming the data
    main_loan_data = cdutils.joining.join_loan_tables(wh_acctcommon, wh_acctloan, wh_loans)
    # property_data = src.transformations.joining.join_prop_tables(wh_prop, wh_prop2)

    # # Calculated fields & data cleaning
    main_loan_data = cdutils.loans.calculations.append_total_exposure_field(main_loan_data)
    main_loan_data = cdutils.loans.calculations.cleaning_loan_data(main_loan_data)


    # Sort data
    df = main_loan_data.sort_values(by=['Total Exposure','acctnbr'], ascending=[False, True])
    # multiple_prop_data = multiple_prop_data.sort_values(by=['Total Exposure','acctnbr'], ascending=[False, True])
    # Limit scope to loans
    df = df[df['mjaccttypcd'].isin(['CML','MLN','MTG','CNS'])]

    # Original recon
    original_recon_amt = df['Net Balance'].sum()

    loan_category_df = cdutils.loans.calculations.categorize_loans(df)
    loan_category_df = loan_category_df[['acctnbr','Category']].copy()
    df = pd.merge(df, loan_category_df, on='acctnbr', how='left')
    adjusted_full_data = df.copy()

    final_df = df.groupby('Category')['Net Balance'].sum().reset_index()


    # Reconciliation Check
    original_recon_amt = round(original_recon_amt,2)
    assert original_recon_amt - round(final_df['Net Balance'].sum()) < abs(1), "Failed Reconciliation"

    final_df['Net Balance Rounded'] = (final_df['Net Balance'] / 1000).round() 
    
    return adjusted_full_data, final_df