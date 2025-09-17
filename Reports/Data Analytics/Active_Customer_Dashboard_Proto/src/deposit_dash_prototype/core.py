# Core logic specific to project/report
#

from deltalake import DeltaTable
import pandas as pd
from pathlib import Path
import src.config
import cdutils.acct_file_creation.core # type: ignore
from src.utils.parquet_io import add_load_timestamp
from datetime import datetime
import numpy as np


def build_portfolio_dimension(df: pd.DataFrame, portfolio_col: str = "portfolio_key") -> pd.DataFrame:
    """
    Create a portfolio-level dimension table.

    Expects columns:
      - portfolio key:      portfolio_col (default 'portfolio_key')
      - product:            'product'
      - Macro Account Type: 'Macro Account Type' (values like 'Loan' / 'Deposit')
      - Net Balance:        'Net Balance'
      - account number:     'acctnbr'
      - tax fields:         'taxrptfororgnbr', 'taxrptforpersnbr'
    """

    # --- Normalize helpful helper columns ---
    df = df.copy()

    # Numeric balance
    df["__net_bal__"] = pd.to_numeric(df["Net Balance"], errors="coerce")

    # Macro Account Type normalized to lower-case strings
    mat = df["Macro Account Type"].astype(str).str.casefold()
    df["__is_loan__"] = mat.eq("loan")
    df["__is_deposit__"] = mat.eq("deposit")

    # Muni presence logic
    df["__is_muni__"] = (
        df["product"].str.contains("muni", case=False, na=False) &
        (~df["product"].str.contains("Community", case=False, na=False))
    )

    g = df.groupby(portfolio_col, dropna=False)

    # --- Muni presence (Y/N) ---
    muni_present = g["__is_muni__"].any().map({True: "Y", False: "N"})
    muni_present.name = "Muni_Present"

    # --- Category ---
    # if taxrptfororgnbr is all null -> 'Consumer'
    # elif taxrptforpersnbr is all null -> 'Business'
    # else 'Mixed'
    org_all_null  = g["taxrptfororgnbr"].apply(lambda s: s.isna().all())
    pers_all_null = g["taxrptforpersnbr"].apply(lambda s: s.isna().all())
    category = np.where(org_all_null, "Consumer",
                        np.where(pers_all_null, "Business", "Mixed"))
    category = pd.Series(category, index=org_all_null.index, name="Category")

    # --- Balances ---
    loan_bal = g.apply(lambda x: x.loc[x["__is_loan__"], "__net_bal__"].sum(min_count=1)).fillna(0.0)
    loan_bal.name = "Total loan Balance"

    dep_bal = g.apply(lambda x: x.loc[x["__is_deposit__"], "__net_bal__"].sum(min_count=1)).fillna(0.0)
    dep_bal.name = "Total deposit Balance"

    # --- Unique counts ---
    uniq_loans = g.apply(lambda x: x.loc[x["__is_loan__"], "acctnbr"].nunique(dropna=True))
    uniq_loans.name = "Unique Loans"

    uniq_deps = g.apply(lambda x: x.loc[x["__is_deposit__"], "acctnbr"].nunique(dropna=True))
    uniq_deps.name = "Unique Deposits"

    # --- Assemble dimension ---
    dim = pd.concat(
        [muni_present, category, loan_bal, dep_bal, uniq_loans, uniq_deps],
        axis=1
    ).reset_index()

    return dim

# Example usage:
# dim_table = build_portfolio_dimension(df, portfolio_col="portfolio_key")
# display(dim_table.head())



def main_pipeline():
# Main account table
    df = DeltaTable(src.config.SILVER / "account").to_pandas()
# Create loans/deposits distinction
    MACRO_TYPE_MAPPING = {
        'CML':'Loan',
        'MLN':'Loan',
        'CNS':'Loan',
        'MTG':'Loan',
        'CK':'Deposit',
        'SAV':'Deposit',
        'TD':'Deposit'
    }


    df['Macro Account Type'] = df['mjaccttypcd'].map(MACRO_TYPE_MAPPING)
    

    # # Year end data
    specified_date = datetime(2024, 12, 31)
    year_end_df = cdutils.acct_file_creation.core.query_df_on_date(specified_date)

    # # Prior month end data
    specified_date = datetime(2025, 8, 31)
    month_end_df = cdutils.acct_file_creation.core.query_df_on_date(specified_date)

    year_end_df = year_end_df[[
        'acctnbr',
        'Net Balance'
    ]].copy()

    month_end_df = month_end_df[[
        'acctnbr',
        'Net Balance'
    ]].copy()

    merged_history_df = year_end_df.merge(month_end_df, how='outer', on='acctnbr', suffixes=('_prior_year','_prior_month'))

    merged_history_df = merged_history_df.fillna(0)

    df = df.merge(merged_history_df, how='left', on='acctnbr').copy()

    portfolio = build_portfolio_dimension(df, portfolio_col="portfolio_key")

    return df, portfolio

# Absent of proper portfolio silver dimension table
# Separate field for presence of Muni (Y/N)
# We group by portfolio key and come up with a dimension
# Example: portfolio key is primary key and then I have a calculated field (agg, probably lambda function)
    - Category
        - if taxrptfororgnbr is all null, 'Consumer', if taxrptforpersnbr is all null, 'Business'
        - else, 'Mixed'
    - Total loan Balance
        - sum up 'Net Balance' on records (acctnbr) where df['Macro Account Type'] = Loan
    - Total deposit Balance
        - sum up 'Net Balance' on records (acctnbr) where df['Macro Account Type'] = Deposit
    - Unique Loans
        - nunique Loans (use logic above)
    - Unqiue Deposits
        - nunique deposits (use logic above)
