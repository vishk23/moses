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
from src.utils.date_helpers import get_all_required_dates
from typing import List, Dict


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
    loan_bal = g.apply(lambda x: x.loc[x["__is_loan__"], "__net_bal__"].sum(min_count=1), include_groups=False).fillna(0.0)
    loan_bal.name = "Total loan Balance"

    dep_bal = g.apply(lambda x: x.loc[x["__is_deposit__"], "__net_bal__"].sum(min_count=1), include_groups=False).fillna(0.0)
    dep_bal.name = "Total deposit Balance"

    # --- Unique counts ---
    uniq_loans = g.apply(lambda x: x.loc[x["__is_loan__"], "acctnbr"].nunique(dropna=True), include_groups=False)
    uniq_loans.name = "Unique Loans"

    uniq_deps = g.apply(lambda x: x.loc[x["__is_deposit__"], "acctnbr"].nunique(dropna=True), include_groups=False)
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


def fetch_snapshot(date: datetime, macro_type_mapping: dict) -> pd.DataFrame:
    """
    Fetch account snapshot for a given date and apply macro type mapping.

    Args:
        date: Target date for snapshot
        macro_type_mapping: Dict mapping mjaccttypcd to Macro Account Type

    Returns:
        DataFrame with snapshot data, effdate set, and Macro Account Type added
    """
    df = cdutils.acct_file_creation.core.query_df_on_date(date)
    df['Macro Account Type'] = df['mjaccttypcd'].map(macro_type_mapping)
    df['effdate'] = date  # Ensure effdate is set to requested date
    return df


def main_pipeline():
    """
    Main ETL pipeline - fetches multi-period account snapshots and builds dimensional model.

    Returns:
        Tuple of (dim_account, fact_balances, portfolio)
    """

    # Define macro type mapping
    MACRO_TYPE_MAPPING = {
        'CML':'Loan',
        'MLN':'Loan',
        'CNS':'Loan',
        'MTG':'Loan',
        'CK':'Deposit',
        'SAV':'Deposit',
        'TD':'Deposit'
    }

    # Get all required dates dynamically
    dates = get_all_required_dates()

    print(f"Fetching data for multiple time periods...")
    print(f"  Current date: {dates['current'].strftime('%Y-%m-%d')}")
    print(f"  Prior day: {dates['prior_day'].strftime('%Y-%m-%d')}")
    print(f"  Prior month-end: {dates['prior_month_end'].strftime('%Y-%m-%d')}")
    print(f"  Prior quarter-end: {dates['prior_quarter_end'].strftime('%Y-%m-%d')}")
    print(f"  Prior year-end: {dates['prior_year_end'].strftime('%Y-%m-%d')}")
    print(f"  Trailing 16 months: {dates['trailing_16_months'][0].strftime('%Y-%m-%d')} to {dates['trailing_16_months'][-1].strftime('%Y-%m-%d')}")
    print(f"  Prior 8 business days: {dates['prior_8_days'][0].strftime('%Y-%m-%d')} to {dates['prior_8_days'][-1].strftime('%Y-%m-%d')}")

    # Fetch current snapshot from Silver lakehouse (already in memory)
    print("Fetching current snapshot from SILVER/account...")
    current_df = DeltaTable(src.config.SILVER / "account").to_pandas()
    current_df['Macro Account Type'] = current_df['mjaccttypcd'].map(MACRO_TYPE_MAPPING)
    # Note: effdate should already be set in Silver table

    # Collect all snapshots to union
    all_snapshots = [current_df]

    # Fetch all unique dates (dedupe to avoid duplicate queries)
    unique_dates = set()

    # Add key period dates
    unique_dates.add(dates['prior_day'])
    unique_dates.add(dates['prior_month_end'])
    unique_dates.add(dates['prior_quarter_end'])
    unique_dates.add(dates['prior_year_end'])

    # Add trailing 16 months
    for month_end in dates['trailing_16_months']:
        unique_dates.add(month_end)

    # Add prior 8 business days
    for day in dates['prior_8_days']:
        unique_dates.add(day)

    # Remove current date if already in Silver (avoid duplicate)
    unique_dates.discard(dates['current'])

    # Sort dates for cleaner logging
    unique_dates_sorted = sorted(unique_dates, reverse=True)

    print(f"Fetching {len(unique_dates_sorted)} historical snapshots...")

    # Fetch all historical snapshots
    for i, date in enumerate(unique_dates_sorted, 1):
        print(f"  [{i}/{len(unique_dates_sorted)}] Fetching {date.strftime('%Y-%m-%d')}...")
        snapshot = fetch_snapshot(date, MACRO_TYPE_MAPPING)
        all_snapshots.append(snapshot)

    # Union all snapshots
    print("Unioning all snapshots...")
    all_df = pd.concat(all_snapshots, ignore_index=True, sort=False)

    print(f"Total records across all periods: {len(all_df):,}")
    print(f"Unique accounts: {all_df['acctnbr'].nunique():,}")
    print(f"Unique dates: {all_df['effdate'].nunique()}")

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


