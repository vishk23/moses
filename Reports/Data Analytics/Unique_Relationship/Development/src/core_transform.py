"""
Core Transformations
"""
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import pandas as pd # type: ignore
import numpy as np # type: ignore
from pandas.api.types import is_numeric_dtype

import cdutils.input_cleansing # type: ignore
import cdutils.deduplication # type: ignore
import cdutils.loans.calculations # type: ignore
import cdutils.joining # type: ignore
import cdutils.input_cleansing # type: ignore
import cdutils.loans.inactive_date # type:ignore
import cdutils.timezone # type: ignore 
import cdutils.daily_deposit_staging # type: ignore
import cdutils.summary_row # type: ignore

def main_pipeline(data: Dict) -> pd.DataFrame:
    """
    Main data pipeline for the balance tracker. This ties back to the Call Report as a check.
    """

    # # Cache data for development
    # src.cdutils.caching.cache_data(r'C:\Users\w322800\Documents\cre_caching', data)
    
    # # Unpack data into dataframes
    wh_acctcommon = data['wh_acctcommon'].copy()
    wh_loans = data['wh_loans'].copy()
    wh_acctloan = data['wh_acctloan'].copy()
    # need to pull out some more necessary fields from the data fetch process here

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

    # Consolidate loan data & property data
    # single_prop_data = src.transformations.joining.consolidation_with_one_prop(main_loan_data, property_data)
    # multiple_prop_data = src.transformations.joining.consolidation_with_multiple_props(main_loan_data, property_data)

    # Sort data
    df = main_loan_data.sort_values(by=['Total Exposure','acctnbr'], ascending=[False, True])
    # multiple_prop_data = multiple_prop_data.sort_values(by=['Total Exposure','acctnbr'], ascending=[False, True])

    df = df[df['mjaccttypcd'].isin(['CK','SAV','TD'])]

    return df

