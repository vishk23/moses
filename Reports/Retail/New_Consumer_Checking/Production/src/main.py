"""
New Business Checking
Developed by CD
[v1.0.5-prod] 
"""
from pathlib import Path
import os

import pandas as pd # type: ignore

import src.cdutils.database
from src._version import __version__

def main(production_flag: bool=False):
    if production_flag:
        BASE_PATH = Path(r'\\00-DA1\Home\Share\Line of Business_Shared Services\Retail Banking\New Consumer Checking\Production')
        assert "prod" in __version__, (f"Cannot run in production mode without 'prod' in the __version__")
    else:
        BASE_PATH = Path('.')
    data = src.cdutils.database.fetch_data()

    acctcommon = data['acctcommon'].copy()

    acctcommon = acctcommon[~acctcommon['taxrptforpersnbr'].isnull()]

    acctcommon = acctcommon[acctcommon['currmiaccttypcd'].isin(
        [
            'CK14',
            'CK02',
            'CK35',
            'CK04',
            'CK03',
            'CK05',
            'CK01',
            'CK06'
        ]
    )].copy()

    df = acctcommon.copy()
    
    FILE_PATH = BASE_PATH / Path('./output')
    os.makedirs(FILE_PATH, exist_ok=True)
    FILE_PATH = FILE_PATH / "consumer_deposits_tin_raw_data.xlsx"
    df.to_excel(FILE_PATH, engine='openpyxl', index=False)

if __name__ == "__main__":
    print(f"Starting new_consumer_checking [{__version__}]")
    main(production_flag=True)
    # main()
    print("Complete!")
