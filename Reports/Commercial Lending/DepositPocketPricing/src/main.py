"""
Main entry point for Deposit Pocket Pricing.

Simple workflow migrated from src_old:
- Read DepositPocketPricing.xlsx from INPUT_DIR
- Filter non-null open dates, select relevant columns
- Sort by open date
- Fill New Money 2 nulls with 0 and compute cumulative new money
- Write to output/deposit_pocket_pricing_raw.xlsx
"""

from pathlib import Path
import pandas as pd
import src.config

REQUIRED_COLUMNS = [
    'Region',
    'CLO',
    'Customer',
    'New Acct. Open Date',
    'New Acct Type',
    'New Money 2',
    'New Rate',
    'Source of Funds (What bank?)'
]


def main():
    print(f"Running {src.config.REPORT_NAME} for {src.config.BUSINESS_LINE}")
    print(f"Schedule: {src.config.SCHEDULE}")
    print(f"Environment: {src.config.ENV}")

    # Paths
    input_path = src.config.INPUT_DIR / 'DepositPocketPricing.xlsx'
    output_path = src.config.OUTPUT_DIR / 'deposit_pocket_pricing_raw.xlsx'

    # Ensure output dir exists
    src.config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    print(f"Reading input: {input_path}")
    df = pd.read_excel(input_path)

    # Filter rows with open date
    if 'New Acct. Open Date' not in df.columns:
        raise KeyError("Expected column 'New Acct. Open Date' not found in input file")

    df = df[~df['New Acct. Open Date'].isnull()].copy()

    # Select columns (only those present to avoid hard failure if extras missing)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise KeyError(f"Missing required columns: {missing}")

    df = df[REQUIRED_COLUMNS].copy()

    # Types and sort
    df['New Acct. Open Date'] = pd.to_datetime(df['New Acct. Open Date'], errors='coerce')
    df = df.sort_values(by='New Acct. Open Date').copy()

    # Money fields
    df['New Money 2'] = pd.to_numeric(df['New Money 2'], errors='coerce').fillna(0)
    df['Cumulative New Money'] = df['New Money 2'].cumsum()

    # Write
    print(f"Writing output: {output_path}")
    df.to_excel(output_path, engine='openpyxl', index=False)
    print("Complete!")


if __name__ == "__main__":
    main()