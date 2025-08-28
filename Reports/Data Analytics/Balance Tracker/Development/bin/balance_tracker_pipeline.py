"""
FDIC Recon: Full CML portfolio with Call codes
"""

from pathlib import Path

import pandas as pd # type: ignore
import numpy as np # type: ignore

import src.cdutils.database
import src.cdutils.caching
import src.transformations.joining
import src.transformations.calculations # type: ignore

def main():
    # # Fetch Data from COCC
    data = src.cdutils.database.fetch_data()


    # # Unpack data into dataframes
    wh_acctcommon = data['wh_acctcommon'].copy()
    wh_loans = data['wh_loans'].copy()
    wh_acctloan = data['wh_acctloan'].copy()
    wh_acct = data['wh_acct'].copy()

    current_date = wh_acctcommon['effdate'].iloc[0].strftime('%m%d%y')

    # Transforming the data
    main_loan_data = src.transformations.joining.join_loan_tables(wh_acctcommon, wh_acctloan, wh_loans, wh_acct)
    # property_data = src.transformations.joining.join_prop_tables(wh_prop, wh_prop2)

    # # Calculated fields & data cleaning
    main_loan_data = src.transformations.calculations.append_total_exposure_field(main_loan_data)
    main_loan_data = src.transformations.calculations.cleaning_loan_data(main_loan_data)

    # Consolidate loan data & property data
    # single_prop_data = src.transformations.joining.consolidation_with_one_prop(main_loan_data, property_data)
    # multiple_prop_data = src.transformations.joining.consolidation_with_multiple_props(main_loan_data, property_data)

    # Sort data
    df = main_loan_data.sort_values(by=['Total Exposure','acctnbr'], ascending=[False, True])
    # multiple_prop_data = multiple_prop_data.sort_values(by=['Total Exposure','acctnbr'], ascending=[False, True])

    # Limit scope to loans
    df = df[df['mjaccttypcd'].isin(['CML','MLN','MTG','CNS'])]

    # Original recon
    original_recon_amt = df['Net Balance'].sum()

    # Stratify the portfolio
    def cleaning_call_codes(df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleaning Stage for fdiccatcd
        - CML indirect get reclassified to AUTO
        - HOA gets its own category HOA
        - Tax Exempt Bonds become OTAL (other)
        - MTG loans are given their own code 'MTG', just for grouping purposes
        - Indirect Consumer loans originated by bank are put in Consumer/Other (CNOT)
        - Other/CML is the catch all for loans that don't have an FDIC code
        """
        df['fdiccatcd'] = np.where(df['currmiaccttypcd'].isin(['CM15','CM16']), 'AUTO', df['fdiccatcd'])
        df['fdiccatcd'] = np.where(df['currmiaccttypcd'].isin(['CM46','CM47']), 'HOA', df['fdiccatcd'])
        df['fdiccatcd'] = np.where(df['currmiaccttypcd'].isin(['CM45']), 'OTAL', df['fdiccatcd'])
        df['fdiccatcd'] = np.where(df['mjaccttypcd'].isin(['MTG']), 'MTG', df['fdiccatcd'])
        df['fdiccatcd'] = np.where(df['currmiaccttypcd'].isin(['IL09','IL10']), 'CNOT', df['fdiccatcd'])
        df['fdiccatcd'] = np.where(df['fdiccatcd'].isnull(), 'OTAL', df['fdiccatcd'])
        return df

    df = cleaning_call_codes(df) 

    fdic_groups = {
    # Note call codes have been adjusted in an earlier stage to stratify the portfolio
    'CRE': ['CNFM','OTCN','LAND','LNDV','RECN','REFI','REOE','REJU','REOW','RENO','REMU','OTAL','AGPR','REFM'],
    'C&I': ['CIUS'],
    'HOA': ['HOA'],
    'Residential': ['MTG'],
    'Consumer': ['CNOT','CNCR'],
    'Indirect': ['AUTO']
    }
    call_code_mapping = {code: group for group, codes in fdic_groups.items() for code in codes}
    df['Category'] = df['fdiccatcd'].map(call_code_mapping)

    final_df = df.groupby('Category')['Net Balance'].sum().reset_index()

    # Reconciliation Check
    original_recon_amt = round(original_recon_amt,2)
    assert original_recon_amt - round(final_df['Net Balance'].sum()) < abs(1), "Failed Reconciliation"

    final_df['Net Balance Rounded'] = (final_df['Net Balance'] / 1000).round() 
    
    # Writing full dataset to excel
    OUTPUT_PATH = Path(f'./output/loans_call_report_recon_{current_date}.xlsx')
    main_loan_data.to_excel(OUTPUT_PATH, engine='openpyxl', index=False)

    # Writing full dataset to excel
    OUTPUT_PATH = Path(f'./output/pipeline_output_{current_date}.xlsx')
    final_df.to_excel(OUTPUT_PATH, engine='openpyxl', index=False)

    # Writing loan data with multiple property data to excel
    # multiple_prop_data_file_path= Path(r'Z:\Chad Projects\Monthly Reports\Automated Linda Reports\NonOwnerOcc\Production\output\multiple_property_per_loan.xlsx')
    # multiple_prop_data.to_excel(multiple_prop_data_file_path, engine='openpyxl', index=False)

    print("Completed!")

if __name__ == '__main__':
    main()