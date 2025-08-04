"""
Main Entry Point
"""
from pathlib import Path

import pandas as pd # type: ignore

import src.fetch_data
import src.core_transform
import src.output_to_excel
import cdutils.pkey_sqlite # type: ignore
import cdutils.hhnbr # type: ignore
import cdutils.selo # type: ignore
import cdutils.loans.calculations # type: ignore
from src._version import __version__

def main(production_flag: bool=False):
    if production_flag:
        BASE_PATH = Path(r'\\00-DA1\Home\Share\Line of Business_Shared Services')
        assert "prod" in __version__, (f"Cannot run in production mode without 'prod' in the __version__")
    else:
        BASE_PATH = Path('.')
    
    data = src.fetch_data.fetch_data()

    # Core transformation pipeline
    raw_data = src.core_transform.main_pipeline(data)

    # Raw data with pkey appended
    raw_data = cdutils.pkey_sqlite.add_pkey(raw_data)

    # Attach HH number
    househldacct = data['househldacct'].copy()
    raw_data = cdutils.hhnbr.add_hh_nbr(raw_data, househldacct)

    # Attach secondary officer
    df = cdutils.selo.append_selo(raw_data)

    # Categorize loans
    df = cdutils.loans.calcuations.categorize_loans(df)

    # Filter down fields
    df = df[[
        'acctnbr',
        'ownersortname',
        'product',
        'mjaccttypcd',
        'currmiaccttypcd',
        'loanofficer',
        'branchname',
        'Secondary Lending Officer',
        'contractdate',
        'Net Balance',
        'creditlimitamt',
        'noteopenamt',
        'Category',
        'portfolio_key'
    ]].copy()

    df = df.rename(columns={'loanofficer':'Primary Officer','branchname': 'Branch Name', 'mjaccttypcd':'Major','currmiaccttypcd':'Minor'}).copy()

    # # Output to excel (raw data)
    OUTPUT_PATH = BASE_PATH / Path('./output/loan_report_branch_officer.xlsx')
    df.to_excel(OUTPUT_PATH, sheet_name='Sheet1', index=False)

    # # Format excel
    # src.output_to_excel.format_excel_file(OUTPUT_PATH)

if __name__ == '__main__':
    print(f"Starting [{__version__}]")
    # main(production_flag=True)
    main()
    print("Complete!")

