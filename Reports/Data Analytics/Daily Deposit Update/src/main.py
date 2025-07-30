"""
Main Entry Point
"""
from pathlib import Path

import pandas as pd # type: ignore


import src.deposit_file
import src.output_to_excel
from src._version import __version__

def main(production_flag: bool=False):
    if production_flag:
        BASE_PATH = Path(r'\\00-DA1\Home\Share\Line of Business_Shared Services\Commercial Lending\Deposits\DailyDeposit')
        assert "prod" in __version__, (f"Cannot run in production mode without 'prod' in the __version__")
    else:
        BASE_PATH = Path('.')
    # Core transformation pipeline
    raw_data, daily_deposit_drop_in = src.deposit_file.deposit_dataset_execution()

    # Output to excel (raw_data -> Staging)
    OUTPUT_PATH = BASE_PATH / Path('./output/DailyDeposit_staging.xlsx')
    raw_data.to_excel(OUTPUT_PATH, sheet_name='Sheet1', index=False)

    # Output to excel (for the drop-in file to Commercial Credit drive)
    OUTPUT_PATH = BASE_PATH / Path('./output/DailyDeposit.xlsx')
    daily_deposit_drop_in.to_excel(OUTPUT_PATH, sheet_name='Sheet1', index=False)

    # Format excel
    src.output_to_excel.format_excel_file(OUTPUT_PATH)

    # Write to drop-in location
    try:
        OUTPUT_PATH.replace(Path(r'\\00-DA1\Home\Share\Line of Business_Shared Services\Commercial Lending\Deposits\DailyDeposit\DailyDeposit.xlsx'))
    except:
        print("Error replacing to drop-in location")
        
if __name__ == '__main__':
    print(f"Starting [{__version__}]")
    # main(production_flag=True)
    main()
    print("Complete!")

