"""
Lee & Mason Ins Tracking Extract
Developed by CD
v1.0.1-prod

This is the main entry point for the Lee & Mason Insurance Tracking Extract
It orchestrates the entire report generation:
- Data extraction from SQL database
- Data cleaning and transformation
- Excel report generation

Usage:
    python -m src.main
"""

from pathlib import Path

import pandas as pd # type: ignore

import src.transformations.joining
import src.cdutils.database
import src.cdutils.caching
import src.transformations.calculations
import src.transformations.filters

def main():
    # Fetch data from database
    data  = src.cdutils.database.fetch_data()

    # Unpack data
    wh_acctcommon = data['wh_acctcommon'].copy()
    wh_acctloan = data['wh_acctloan'].copy()
    wh_loans = data['wh_loans'].copy()
    acctpropins = data['acctpropins'].copy()
    wh_prop = data['wh_prop'].copy()
    wh_prop2 = data['wh_prop2'].copy()
    wh_inspolicy = data['wh_inspolicy'].copy()
    persaddruse = data['persaddruse'].copy()
    orgaddruse = data['orgaddruse'].copy()
    wh_addr = data['wh_addr'].copy()

    # # Caching
    # cache_path = Path(r'Z:\Chad Projects\Ad Hoc Reports\Lee_Mason_Ins_Tracking\Production\assets\caching')
    # src.cdutils.caching.cache_data(cache_path, data)

#    # Access cached data
#     wh_acctcommon = pd.read_csv(Path(r'Z:\Chad Projects\Ad Hoc Reports\Lee_Mason_Ins_Tracking\Production\assets\caching\wh_acctcommon.csv'))
#     wh_acctloan = pd.read_csv(Path(r'Z:\Chad Projects\Ad Hoc Reports\Lee_Mason_Ins_Tracking\Production\assets\caching\wh_acctloan.csv'))
#     wh_loans = pd.read_csv(Path(r'Z:\Chad Projects\Ad Hoc Reports\Lee_Mason_Ins_Tracking\Production\assets\caching\wh_loans.csv'))
#     acctpropins = pd.read_csv(Path(r'Z:\Chad Projects\Ad Hoc Reports\Lee_Mason_Ins_Tracking\Production\assets\caching\acctpropins.csv'))
#     wh_prop = pd.read_csv(Path(r'Z:\Chad Projects\Ad Hoc Reports\Lee_Mason_Ins_Tracking\Production\assets\caching\wh_prop.csv'))
#     wh_prop2 = pd.read_csv(Path(r'Z:\Chad Projects\Ad Hoc Reports\Lee_Mason_Ins_Tracking\Production\assets\caching\wh_prop2.csv'))
#     wh_inspolicy = pd.read_csv(Path(r'Z:\Chad Projects\Ad Hoc Reports\Lee_Mason_Ins_Tracking\Production\assets\caching\wh_inspolicy.csv'))
#     persaddruse = pd.read_csv(Path(r'Z:\Chad Projects\Ad Hoc Reports\Lee_Mason_Ins_Tracking\Production\assets\caching\persaddruse.csv'))
#     orgaddruse = pd.read_csv(Path(r'Z:\Chad Projects\Ad Hoc Reports\Lee_Mason_Ins_Tracking\Production\assets\caching\orgaddruse.csv'))
#     wh_addr = pd.read_csv(Path(r'Z:\Chad Projects\Ad Hoc Reports\Lee_Mason_Ins_Tracking\Production\assets\caching\wh_addr.csv'))

    # Data Cleaning & Transformations
    main_data = src.transformations.joining.join_loan_tables(wh_acctcommon, wh_acctloan, wh_loans)
    prop_data = src.transformations.joining.join_prop_tables(wh_prop, wh_prop2)
    main_data = src.transformations.joining.appending_owner_address(main_data, orgaddruse, persaddruse, wh_addr)
    main_data = src.transformations.calculations.append_total_exposure_field(main_data)
    main_data = src.transformations.calculations.cleaning_loan_data(main_data)
    merged_data = src.transformations.joining.consolidation_with_multiple_props(main_data, prop_data)
    insurance_merged = src.transformations.joining.merging_insurance_tables(acctpropins, wh_inspolicy)
    merged_data = src.transformations.joining.append_insurance_data_to_main(merged_data, insurance_merged)
    merged_data = src.transformations.filters.filtering_down_to_relevant_fields(merged_data)

    # Write out to excel
    output_path = Path("./output/lee_mason_extract.xlsx")
    merged_data.to_excel(output_path, engine='openpyxl', index=False)
    print(f"Report generation complete! File written to {output_path}")

if __name__ == '__main__':
    main()
    