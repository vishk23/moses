"""
Core Transformations
"""
from typing import Dict
from pathlib import Path

import pandas as pd # type: ignore
import numpy as np # type: ignore


def main_pipeline(data: Dict) -> pd.DataFrame:
    """
    Main data pipeline 
    """
    # Extract data
    acctcommon = data['acctcommon'].copy()
    acctloan = data['acctloan'].copy()
    loans = data['loans'].copy()
    prop = data['prop'].copy()
    prop2 = data['prop2'].copy()

    # %%
    def filter_acctcommon(df):
        df = df.loc[df['mjaccttypcd'] == 'CML'].copy()
        df = df.loc[df['curracctstatcd'].isin(['ACT','NPFM'])].copy()
        return df

    # %%
    acctcommon = filter_acctcommon(acctcommon)

    assert acctcommon['acctnbr'].is_unique, "Duplicates found"
    assert acctloan['acctnbr'].is_unique, "Duplicates found"
    assert loans['acctnbr'].is_unique, "Duplicates found"

    def merging_loan_data(acctcommon, acctloan, loans):
        merged_df = pd.merge(acctcommon, acctloan, how='left', on='acctnbr')
        merged_df = pd.merge(merged_df, loans, how='left', on='acctnbr')
        return merged_df

    merged_df = merging_loan_data(acctcommon, acctloan, loans)

    def dedupe_prop(df):
        df = df.sort_values(by='aprsvalueamt', ascending=False).drop_duplicates(subset='acctnbr', keep='first').copy()
        return df

    def dedupe_prop2(df):
        df = df.sort_values(by='propvalue', ascending=False).drop_duplicates(subset='acctnbr', keep='first').copy()
        return df

    prop = dedupe_prop(prop)
    prop2 = dedupe_prop2(prop2)

    assert prop['acctnbr'].is_unique, "Duplicates found"
    assert prop2['acctnbr'].is_unique, "Duplicates found"

    def merging_core_with_prop(df, prop, prop2):
        merged_df = pd.merge(df, prop, how='left', on='acctnbr')
        merged_df = pd.merge(merged_df, prop2, how='left', on='acctnbr')
        return merged_df

    merged_df = merging_core_with_prop(merged_df, prop, prop2)

    merged_df['prepayment_penalty'] = np.where(merged_df['prepaycharge'] > 0, 'Y', 'N')

    return merged_df

    


def main_pipeline_multiple_prop(data: Dict) -> pd.DataFrame:
    """
    Main data pipeline for multiple prop
    """
    acctcommon = data['acctcommon'].copy()
    acctloan = data['acctloan'].copy()
    loans = data['loans'].copy()
    prop = data['prop'].copy()
    prop2 = data['prop2'].copy()


    # %%
    def filter_acctcommon(df):
        df = df.loc[df['mjaccttypcd'] == 'CML'].copy()
        df = df.loc[df['curracctstatcd'].isin(['ACT','NPFM'])].copy()
        return df

    acctcommon = filter_acctcommon(acctcommon)

    # %%
    assert acctcommon['acctnbr'].is_unique, "Duplicates found"
    assert acctloan['acctnbr'].is_unique, "Duplicates found"
    assert loans['acctnbr'].is_unique, "Duplicates found"

    def merging_loan_data(acctcommon, acctloan, loans):
        merged_df = pd.merge(acctcommon, acctloan, how='left', on='acctnbr')
        merged_df = pd.merge(merged_df, loans, how='left', on='acctnbr')
        return merged_df

    merged_df = merging_loan_data(acctcommon, acctloan, loans)

    # %%
    # assert prop['acctnbr'].is_unique, "Duplicates found"
    # assert prop2['acctnbr'].is_unique, "Duplicates found"

    # %%
    def merging_core_with_prop(df, prop, prop2):
        merged_df = pd.merge(df, prop, how='left', on='acctnbr')
        merged_df = pd.merge(merged_df, prop2, how='left', on='acctnbr')
        return merged_df

    merged_df = merging_core_with_prop(merged_df, prop, prop2)

    # %%
    merged_df['prepayment_penalty'] = np.where(merged_df['prepaycharge'] > 0, 'Y', 'N')

    return merged_df


