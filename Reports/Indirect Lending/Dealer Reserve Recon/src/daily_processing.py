"""
Daily Processing Component of Indirect Dealer Reserve Recon Process
"""
import os
from pathlib import Path
from datetime import datetime

import pandas as pd # type: ignore

from src._version import __version__

def process_daily(production_flag: bool=False) -> None:
    """Process daily Excel files and append to staging table.
    
    Scans the daily_files directory for Excel files, appends their contents to
    the staging CSV, and moves processed files to the archive directory.
    
    Raises:
        FileNotFoundError: If required directories are missing
    """
    if production_flag:
        BASE_PATH = Path(r'\\00-DA1\Home\Share\Line of Business_Shared Services\Indirect Lending\Dealer Reserve Recon\Production')
        assert "prod" in __version__, (f"Cannot run in production mode without 'prod' in the __version__")
    else:
        BASE_PATH = Path('.') 

    DAILY_PATH: Path = BASE_PATH / Path('./assets/daily_files')
    STAGING_FILE: Path = BASE_PATH / Path('./assets/staging_data/current_month.csv')
    PROCESSED_PATH: Path = BASE_PATH / Path('./assets/processed_files')
    
    # Create directories if missing
    DAILY_PATH.mkdir(exist_ok=True)
    PROCESSED_PATH.mkdir(exist_ok=True)
    
    # Create staging file with header if not exists
    if not STAGING_FILE.exists():
        pd.DataFrame(columns=[
            'App #',
            'Name',
            'Dealer',
            'Charge back',
            'Contract Date',
            'Fund Date',
            'Pay-off Date',
            'Amt. Financed',
            'Buy Rate',
            'Contract Rate',
            'Rate Spread',
            'Term',
            'Score',
            'Dealer Split',
            'Dealer Flat',
            'Charge-back Amt.'
        ]).to_csv(STAGING_FILE, index=False)
    
    for daily_file in DAILY_PATH.glob('*.xlsx'):
        try:
            # Load daily data
            df: pd.DataFrame = pd.read_excel(daily_file, sheet_name='Dealer Reserve Report', header=2)
            df = df[~(df['App #'].isnull())].copy()
            df = df[~(df['Charge back'].isnull())].copy()
            
            # Append to staging
            df.to_csv(STAGING_FILE, mode='a', header=False, index=False)
            
            # Archive file
            processed_path: Path = PROCESSED_PATH / daily_file.name
            daily_file.rename(processed_path)
            
        except Exception as e:
            print(f"Error processing {daily_file}: {str(e)}")
            # Consider adding logging 
            


if __name__ == '__main__':
    print(f"Starting [{__version__}]")
    process_daily(production_flag=True)
    # process_daily()
    print("Processed daily files")

