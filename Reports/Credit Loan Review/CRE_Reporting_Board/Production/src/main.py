"""
FDIC Recon: Full CML portfolio with Call codes
"""

from pathlib import Path

import pandas as pd # type: ignore

import src.cdutils.database
import src.cdutils.caching
import src.transformations.joining
import src.transformations.calculations # type: ignore
from src._version import __version__

def main():
    # # Fetch Data from COCC
    data = src.cdutils.database.fetch_data()


    # # Cache data for development
    # src.cdutils.caching.cache_data(r'C:\Users\w322800\Documents\cre_caching', data)
    
    # # Unpack data into dataframes
    wh_acctcommon = data['wh_acctcommon'].copy()
    wh_loans = data['wh_loans'].copy()
    wh_acctloan = data['wh_acctloan'].copy()
    wh_acct = data['wh_acct'].copy()
    wh_prop = data['wh_prop'].copy()
    wh_prop2 = data['wh_prop2'].copy()

    # Transforming the data
    main_loan_data = src.transformations.joining.join_loan_tables(wh_acctcommon, wh_acctloan, wh_loans, wh_acct)
    property_data = src.transformations.joining.join_prop_tables(wh_prop, wh_prop2)

    # # Calculated fields & data cleaning
    main_loan_data = src.transformations.calculations.append_total_exposure_field(main_loan_data)
    main_loan_data = src.transformations.calculations.cleaning_loan_data(main_loan_data)

    # Consolidate loan data & property data
    single_prop_data = src.transformations.joining.consolidation_with_one_prop(main_loan_data, property_data)
    # multiple_prop_data = src.transformations.joining.consolidation_with_multiple_props(main_loan_data, property_data)

    # Sort data
    single_prop_data = single_prop_data.sort_values(by=['Total Exposure','acctnbr'], ascending=[False, True])
    # multiple_prop_data = multiple_prop_data.sort_values(by=['Total Exposure','acctnbr'], ascending=[False, True])

    # Writing loan data with single property data to excel
    single_prop_data_file_path = Path('./output/cre_loader.xlsx')
    single_prop_data.to_excel(single_prop_data_file_path, engine='openpyxl', index=False)


    # Writing loan data with multiple property data to excel
    # multiple_prop_data_file_path= Path(r'Z:\Chad Projects\Monthly Reports\Automated Linda Reports\NonOwnerOcc\Production\output\multiple_property_per_loan.xlsx')
    # multiple_prop_data.to_excel(multiple_prop_data_file_path, engine='openpyxl', index=False)

if __name__ == '__main__':
    print(f"Starting cre_loader [{__version__}]")
    main()
    print("Complete!")