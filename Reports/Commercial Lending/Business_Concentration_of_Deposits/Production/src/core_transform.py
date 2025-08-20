"""
Core Transformations
"""
from typing import Dict
from pathlib import Path

import pandas as pd # type: ignore
import numpy as np # type: ignore

def group_and_summarize(df: pd.DataFrame, group_field: pd.DataFrame, sort_field: pd.DataFrame):
    """
    Groups the df by a field and sorts in descending order by the sort field. This is used for things like the Concentration of Credit/Deposit reports

    Args:
        df (pd.DataFrame)
        group_field (str): field in df that you want to group by
        sort_field (str): field in the df that you want to sort in descending order by (based on group total)

    Returns:
        df (pd.DataFrame)

    Tests/Assertions:
    - Postively assert that sort_field is numeric
    - Validate that the group_field has no null values
    - Assert df is not None
    """
    # Asserts
    assert df is not None, "df cannot be none"
    assert pd.api.types.is_numeric_dtype(df[sort_field]), f"Error: sort_field {sort_field} must be numeric"
    assert df[group_field].notnull().all(), f"Critical error: {group_field} contains null values and we are trying to group on it"

    pieces = []

    # Compute the total for each group based on sort_field and sort groups in descending order
    group_summaries = df.groupby(group_field)[sort_field].sum().sort_values(ascending=False)

    # Loop through each group
    for grp in group_summaries.index:
        grp_df = df[df[group_field] == grp]
        pieces.append(grp_df)

        # find the top ownername
        owner_total = grp_df.groupby("ownersortname")["notebal"].sum()
        top_owner = owner_total.idxmax()

        # Take the mode of the officer field
        officer_mode = grp_df["acctofficer"].mode()
        top_officer = officer_mode.iloc[0] if len(officer_mode) > 0 else ""

        # Take the mode of cash management officer
        cmo_mode = grp_df["Cash Management Officer"].mode()
        top_cmo = cmo_mode.iloc[0] if len(cmo_mode) > 0 else ""

        # Weighted Avg Rate
        if grp_df.empty or grp_df['notebal'].sum() == 0:
            weighted_avg = float('nan')
        else:
            weighted_avg = (grp_df['noteintrate'] * grp_df['notebal']).sum() / grp_df['notebal'].sum()

        # Build summary row
        summary = {}
        for col in df.columns:
            if col == group_field:
                summary[col] = grp
            elif col == "ownersortname":
                summary[col] = top_owner
            elif col == "acctofficer":
                summary[col] = top_officer
            elif col == "Cash Management Officer":
                summary[col] = top_cmo
            elif col == 'noteintrate':
                summary[col] = weighted_avg
            elif pd.api.types.is_numeric_dtype(df[col]):
                # Sum numeric columns
                summary[col] = grp_df[col].sum()
            else:
                summary[col] = ""
        pieces.append(pd.DataFrame([summary]))

        # Append a blank row
        blank_row = {col: "" for col in df.columns}
        pieces.append(pd.DataFrame([blank_row]))

    # Concatenate all pieces into one DataFrame
    result = pd.concat(pieces, ignore_index=True)
    return result

def main_pipeline(data: pd.DataFrame) -> pd.DataFrame:
    """
    Main data pipeline 
    """
    # # Set column types
    # numeric_cols = ['noteintrate','bookbalance','notebal']
    # for col in numeric_cols:
    #     df[col] = pd.to_numeric(df[col])

    cmo_col = "Cash Management Officer"

    if cmo_col not in data.columns:
        data[cmo_col] = ""
    else:
        data[cmo_col] = data[cmo_col].fillna("")


    data = data[[
        'portfolio_key',
        'acctnbr',
        'ownersortname',
        'product',
        'acctofficer',
        'Cash Management Officer',
        'notebal',
        'noteintrate',
        'contractdate',
        '3Mo_AvgBal',
        'TTM_AvgBal',
        'Year Ago Balance',
        'TTM_DAYS_OVERDRAWN',
        'TTM_NSF_COUNT',
        # 'YTD_DAYS_OVERDRAWN',
        # 'YTD_NSF_COUNT',
        'Latest_Month_Analyzed_Charges',
        'Latest_Month_Combined_Result',
        'Trailing_12M_Analyzed_Charges',
        'Trailing_12M_Combined_Result',
        'Latest_Month_ECR',
        # 'Trailing_12M_Avg_ECR',
        # 'Primary_Officer_Name_XAA',
        # 'Secondary_Officer_Name_XAA',
        # 'Treasury_Officer_Name_XAA'
    ]].copy()


    df = group_and_summarize(data, "portfolio_key", "notebal")

    df = df.rename(columns={
        'acctnbr':'Acct No.',
        'ownersortname':'Borrower Name',
        'notebal':'Current Balance',
        'noteintrate':'Interest Rate',
        'acctofficer':'Account Officer',
        'contractdate':'Acct Open Date',
        'Latest_Month_Analyzed_Charges':'Current Mo Analyzed Fees (Pre-ECR)',
        'Latest_Month_Combined_Result':'Current Mo Net Analyzed Fees (Post-ECR)',
        'Trailing_12M_Analyzed_Charges':'TTM Analyzed Fees (Pre-ECR)',
        'Trailing_12M_Combined_Result':'TTM Net Analyzed Fees (Post-ECR)',
        'Latest_Month_ECR':'Current ECR'
    }).copy()

    return df 


    




