"""
New Business Checking
Developed by CD
[v1.0.5-prod] 
"""
from pathlib import Path

import pandas as pd # type: ignore

import src.cdutils.database
from src._version import __version__

def main(production_flag: bool=False):
    if production_flag:
        BASE_PATH = Path(r'\\00-DA1\Home\Share\Line of Business_Shared Services\Retail Banking\New Business Checking\Production')
        assert "prod" in __version__, (f"Cannot run in production mode without 'prod' in the __version__")
    else:
        BASE_PATH = Path('.')
    data = src.cdutils.database.fetch_data()

    acctcommon = data['acctcommon'].copy()

    acctcommon = acctcommon[~acctcommon['taxrptfororgnbr'].isnull()]

    acctcommon = acctcommon[(acctcommon['product'].str.contains('Business',case=False, na=False)) | (acctcommon['product'].str.contains('IOLTA',case=False,na=False)) | (acctcommon['product'].str.contains('Community',case=False,na=False)) | (acctcommon['product'].str.contains('Commercial',case=False,na=False)) | (acctcommon['product'].str.contains('BCSB Internal Holdback Savings',case=False,na=False))].copy()

    df = acctcommon.copy()
    FILE_PATH = BASE_PATH / Path('./Output/business_deposits_tin_raw_data.xlsx')
    df.to_excel(FILE_PATH, engine='openpyxl', index=False)

if __name__ == "__main__":
    print(f"Starting new_business_checking [{__version__}]")
    main(production_flag=True)
    # main()
    print("Complete!")
