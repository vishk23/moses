from datetime import datetime
from pathlib import Path
from dateutil.relativedelta import relativedelta
import shutil

import pandas as pd # type: ignore

from src._version import __version__

def reset_month(production_flag: bool=False) -> None:
    """Reset monthly data and archive previous month.
    
    Archives current staging data and report, then initializes new empty
    staging file for the upcoming month.
    """
    if production_flag:
        BASE_PATH = Path(r'\\00-DA1\Home\Share\Line of Business_Shared Services\Indirect Lending\Dealer Reserve Recon\Production')
        assert "prod" in __version__, (f"Cannot run in production mode without 'prod' in the __version__")
    else:
        BASE_PATH = Path('.') 

    stamp: str = (datetime.now() - relativedelta(months=1)).strftime("%Y%m")
    staging: Path = BASE_PATH / Path('./assets/staging_data/current_month.csv')
    archive_staging: Path = BASE_PATH / Path('./output/archive/staging_data')

    processed: Path = BASE_PATH / Path('./assets/processed_files/')
    archive_processed: Path = BASE_PATH / Path('./output/archive/processed_files')

    report: Path = BASE_PATH / Path('./output/current_month_report.xlsx')
    archive_report: Path = BASE_PATH / Path('./output/archive/monthly_report')
    
    # Ensure archive directory exists
    archive_staging.mkdir(parents=True, exist_ok=True)
    archive_processed.mkdir(parents=True, exist_ok=True)
    archive_report.mkdir(parents=True, exist_ok=True)
    
    # Archive staging data
    if staging.exists():
        staging.replace(archive_staging / f"{stamp}_staging.csv")
    
    # Archive processed files
    if processed.exists() and any(processed.iterdir()):
        for file in processed.glob('*'):
            if file.is_file():
                destination_path = archive_processed / file.name
                shutil.move(str(file), str(destination_path))
                print(f"Moved: {file} -> {destination_path}")

    # Archive report
    if report.exists():
        report.replace(archive_report / f"{stamp}_report.xlsx")
    
if __name__ == '__main__':
    print(f"Initializing reset process [{__version__}]")
    reset_month(production_flag=True)
    # reset_month()
    print("Templates have been reset and current files have been archived!")
