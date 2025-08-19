"""
Main Entry Point
"""
from pathlib import Path
from datetime import datetime
import os
import shutil
import stat

import pandas as pd # type: ignore

import src.cdutils.database.fdic_recon
import src.cdutils.database.generic_query
import src.core_transform
import src.output_to_excel
from src._version import __version__

def main(production_flag: bool=False):
    if production_flag:
        BASE_PATH = Path('.')
        assert "prod" in __version__, (f"Cannot run in production mode without 'prod' in the __version__")
    else:
        BASE_PATH = Path('.')
    data = src.cdutils.database.generic_query.fetch_data()

    # Create early payoff report
    raw_data = src.core_transform.main_pipeline(data)

    # Output to excel (raw data)
    current_date = datetime.now().strftime('%Y%m%d')
    file_path = Path('./output')
    file_name = f'Household_Report_{current_date}.xlsx'
    OUTPUT_PATH = file_path / file_name
    raw_data.to_excel(OUTPUT_PATH, sheet_name='Sheet1', index=False)

    # Format excel
    src.output_to_excel.format_excel_file(OUTPUT_PATH)

    # Place in end user file
    # Move to CLO_Share folder and make read-only
    destination_path = Path(r'\\00-berlin\CLO_Share\Data Analytics\Household Report\Household Report.xlsx')
    try:
        if os.path.exists(destination_path):
            os.chmod(destination_path, stat.S_IWRITE)
        shutil.copy(OUTPUT_PATH, destination_path)
        os.chmod(destination_path, stat.S_IREAD)
    except Exception as e:
        print(f"Error occured: {e}")

if __name__ == '__main__':
    print(f"Starting [{__version__}]")
    main(production_flag=True)
    # main()
    print("Complete!")

