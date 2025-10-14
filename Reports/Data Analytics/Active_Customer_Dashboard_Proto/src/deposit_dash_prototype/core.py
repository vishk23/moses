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
    # Main account table (current snapshot)
    current_df = DeltaTable(src.config.SILVER / "account").to_pandas()
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

    current_df['Macro Account Type'] = current_df['mjaccttypcd'].map(MACRO_TYPE_MAPPING)

    # Year end data (full snapshot)
    year_date = datetime(2024, 12, 31)
    year_end_df = cdutils.acct_file_creation.core.query_df_on_date(year_date)
    year_end_df['Macro Account Type'] = year_end_df['mjaccttypcd'].map(MACRO_TYPE_MAPPING)
    # Ensure effdate is set to snapshot date (adjust if query_df_on_date doesn't)
    year_end_df['effdate'] = year_date

    # Prior month end data (full snapshot)
    month_date = datetime(2025, 9, 30)
    month_end_df = cdutils.acct_file_creation.core.query_df_on_date(month_date)
    month_end_df['Macro Account Type'] = month_end_df['mjaccttypcd'].map(MACRO_TYPE_MAPPING)
    # Ensure effdate is set to snapshot date
    month_end_df['effdate'] = month_date

    # Union all snapshots (includes historical-only accounts)
    all_df = pd.concat([current_df, year_end_df, month_end_df], ignore_index=True, sort=False)

    # Define columns (based on account_proto_deriv; adjust as needed)
    dimension_columns = [
        'effdate', 'acctnbr', 'ownersortname', 'product', 'ratetypcd', 'mjaccttypcd',
        'currmiaccttypcd', 'curracctstatcd', 'contractdate', 'datemat', 'taxrptfororgnbr',
        'taxrptforpersnbr', 'loanofficer', 'acctofficer', 'origintrate', 'marginfixed',
        'fdiccatcd', 'loanidx', 'rcf', 'fdiccatdesc', 'loanlimityn', 'riskratingcd',
        'origdate', 'nextratechg', 'Category', 'inactivedate', 'branchname',
        'primaryownercity', 'primaryownerstate', 'primaryownerzipcd', 'portfolio_key',
        'Macro Account Type', 'ownership_key', 'address_key', 'householdnbr',
        'datelastmaint', 'noteintrate'  # Include rates if dimensional; move to fact if measures
    ]
    # Filter to existing columns only
    dimension_columns = [col for col in dimension_columns if col in all_df.columns]

    fact_columns = [
        'effdate', 'acctnbr', 'noteopenamt', 'bookbalance', 'notebal', 'creditlimitamt',
        'availbalamt', 'cobal', 'credlimitclatresamt', 'totalpctsold', 'amortterm',
        'currterm', 'origbal', 'Net Balance', 'Net Available', 'Net Collateral Reserve',
        'Total Exposure', 'orig_ttl_loan_amt'
    ]
    # Filter to existing columns only
    fact_columns = [col for col in fact_columns if col in all_df.columns]

    # Build dimension (no balances; dedup on key)
    dim_account = all_df[dimension_columns].drop_duplicates(subset=['effdate', 'acctnbr'])

    # Build fact (balances only)
    fact_balances = all_df[fact_columns]

    # Build portfolio from current (as before)
    portfolio = build_portfolio_dimension(current_df, portfolio_col="portfolio_key")

    return dim_account, fact_balances, portfolio


