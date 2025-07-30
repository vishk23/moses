"""
Early Payoff Report Component of Indirect Dealer Reserve Recon Process
"""
from typing import Dict
from pathlib import Path

import pandas as pd # type: ignore
import numpy as np # type: ignore
import win32com.client as win32 # type: ignore

import src.cdutils.database.fdic_recon
import src.transformations.joining
import src.transformations.calculations
from src._version import __version__
import src.config


def format_excel_file(file_path):
    # Formatting
    try:
        excel = win32.Dispatch("Excel.Application")
        excel.Visible = False
        workbook = excel.Workbooks.Open(str(file_path.absolute()))
        
        sheet = workbook.Worksheets("Sheet1")

        sheet.Columns.AutoFit()

        # Bold top row
        top_row = sheet.Rows(1)
        top_row.Font.Bold = True

        # Add bottom border to header row
        bottom_border = top_row.Borders(9)
        bottom_border.LineStyle = 1
        bottom_border.Weight = 2

        def format_columns():
            sheet.Columns("A:A").NumberFormat = "mm/dd/yyyy"
            sheet.Columns("H:H").NumberFormat = "mm/dd/yyyy"
            sheet.Columns("I:I").NumberFormat = "mm/dd/yyyy"
            sheet.Columns("J:J").NumberFormat = "mm/dd/yyyy"
            sheet.Columns("K:K").NumberFormat = "mm/dd/yyyy"

            sheet.Columns("L:L").NumberFormat = "0.00%"
            sheet.Columns("M:M").NumberFormat = "$#,##0.00"
            sheet.Columns("N:N").NumberFormat = "$#,##0.00"
            sheet.Columns("P:P").NumberFormat = "$#,##0.00"

        format_columns()

        # Freeze top row
        sheet.Application.ActiveWindow.SplitRow = 1
        sheet.Application.ActiveWindow.FreezePanes = True

        workbook.Save()
        workbook.Close()
        excel.Quit()
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        sheet = None
        workbook = None
        excel = None

def main_pipeline_early_payoff(data: Dict) -> pd.DataFrame:
    """
    Main data pipeline for early payoffs on AUTO loans originated by dealers. This ties back to the Call Report as a check.
    """

    # # Unpack data into dataframes
    wh_acctcommon = data['wh_acctcommon'].copy()
    wh_loans = data['wh_loans'].copy()
    wh_acctloan = data['wh_acctloan'].copy()
    wh_acct = data['wh_acct'].copy()
    acctsubacct = data['acctsubacct'].copy()

    current_date = wh_acctcommon['effdate'].iloc[0].strftime('%m%d%y')

    # Transforming the data
    main_loan_data = src.transformations.joining.join_loan_tables(wh_acctcommon, wh_acctloan, wh_loans, wh_acct)

    # # Calculated fields & data cleaning
    main_loan_data = src.transformations.calculations.append_total_exposure_field(main_loan_data)
    main_loan_data = src.transformations.calculations.cleaning_loan_data(main_loan_data)

    # Sort data
    df = main_loan_data.sort_values(by=['Total Exposure','acctnbr'], ascending=[False, True])

    # Limit scope to loans
    df = df[df['mjaccttypcd'].isin(['CML','MLN','MTG','CNS'])].copy()

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

    df = df[df['Category'] == 'Indirect'].copy()    
    df = df[df['curracctstatcd'] == 'CLS'].copy()

    datefields = ['closedate','contractdate']
    for field in datefields:
        df[field] = pd.to_datetime(df[field])

    filtered_df = df[(df['closedate'] - df['contractdate']) <= pd.Timedelta(days=90)]
    filtered_df = filtered_df.sort_values(by='closedate', ascending=False)


    filtered_df = filtered_df[(filtered_df['effdate'] - filtered_df['closedate']) <= pd.Timedelta(days=90)]

    filtered_df = filtered_df[['effdate','acctnbr','ownersortname','product','curracctstatcd','mjaccttypcd','currmiaccttypcd','origdate','contractdate','closedate','datemat','noteintrate','noteopenamt','bookbalance']].copy()

    # Adding the Dealer Flat/Split
    assert acctsubacct['acctnbr'].is_unique, "Duplicates in acctsubacct, fix"
    acctsubacct['origbal'] = pd.to_numeric(acctsubacct['origbal'])
    
    filtered_df = pd.merge(filtered_df, acctsubacct, on='acctnbr', how='left')

    filtered_df = filtered_df.rename(columns={'origbal':'chargeback_amt'}).copy()
    code_map = {'DLRS':'Dealer Split','DLRF':'Dealer Flat'}
    filtered_df['Category'] = filtered_df['balcatcd'].map(code_map)

    return filtered_df


def run_early_payoff():
    """Run the early payoff report using config-driven paths/settings."""
    OUTPUT_PATH = src.config.OUTPUT_DIR / "early_payoff_trailing90days.xlsx"
    data = src.cdutils.database.fdic_recon.fetch_data()
    early_payoffs = main_pipeline_early_payoff(data)
    early_payoffs.to_excel(OUTPUT_PATH, sheet_name='Sheet1', index=False)
    format_excel_file(OUTPUT_PATH)
    print(f"Running Early Payoff Report for {src.config.REPORT_NAME}")
    print(f"Output: {OUTPUT_PATH}")

if __name__ == '__main__':
    print(f"Starting early payoff [{__version__}]")
    run_early_payoff()
    print("Complete!")




