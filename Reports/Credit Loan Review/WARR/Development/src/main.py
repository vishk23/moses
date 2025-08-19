"""
Main Entry Point
"""
from pathlib import Path

import pandas as pd # type: ignore

import src.cdutils.database.fdic_recon
import src.cdutils.database.generic_query
import src.core_transform
import src.output_to_excel
from src._version import __version__

def main(production_flag: bool=False):
    if production_flag:
        BASE_PATH = Path(r'\\00-DA1\Home\Share\Line of Business_Shared Services')
        assert "prod" in __version__, (f"Cannot run in production mode without 'prod' in the __version__")
    else:
        BASE_PATH = Path('.')
    data = src.cdutils.database.generic_query.fetch_data()

    # Core transformation pipeline
    raw_data = src.core_transform.main_pipeline(data)

    # Output to excel (raw data)
    OUTPUT_PATH = BASE_PATH / Path('./output/standard_report.xlsx')
    raw_data.to_excel(OUTPUT_PATH, sheet_name='Sheet1', index=False)

    # Format excel
    src.output_to_excel.format_excel_file(OUTPUT_PATH)

if __name__ == '__main__':
    print(f"Starting [{__version__}]")
    # main(production_flag=True)
    main()
    print("Complete!")

