"""
Report Generator
Developed by CD

This generates the cumulative monthly report from the staging data (all the daily files that have been processed)
"""

from pathlib import Path
from typing import List, Any

import pandas as pd # type: ignore
import numpy as np # type: ignore
import win32com.client as win32 # type: ignore

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
            sheet.Columns("E:E").NumberFormat = "mm/dd/yyyy"
            sheet.Columns("F:F").NumberFormat = "mm/dd/yyyy"
            sheet.Columns("G:G").NumberFormat = "mm/dd/yyyy"
            sheet.Columns("I:I").NumberFormat = "0.00%"
            sheet.Columns("J:J").NumberFormat = "0.00%"
            sheet.Columns("K:K").NumberFormat = "0.00%"
            sheet.Columns("H:H").NumberFormat = "$#,##0.00"
            sheet.Columns("N:N").NumberFormat = "$#,##0.00"
            sheet.Columns("O:O").NumberFormat = "$#,##0.00"
            sheet.Columns("P:P").NumberFormat = "$#,##0.00"
            sheet.Columns("Q:Q").NumberFormat = "$#,##0.00"

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


def generate_report() -> None:
    """Generate formatted cumulative report from staging data using config-driven paths."""
    STAGING_FILE: Path = src.config.ASSETS_DIR / "staging_data" / "current_month.csv"
    MAPPING_FILE: Path = src.config.ASSETS_DIR / "mapping_dealer_accounts.xlsx"
    REPORT_PATH: Path = src.config.OUTPUT_DIR / "current_month_report.xlsx"

    # Load data with validation
    if not STAGING_FILE.exists():
        raise FileNotFoundError(f"Staging file not found: {STAGING_FILE}")

    df: pd.DataFrame = pd.read_csv(STAGING_FILE)
    dealer_mapping: pd.DataFrame = pd.read_excel(MAPPING_FILE)

    # Format all names as uppercase
    df['Name'] = df['Name'].str.upper()

    # Merge with mapping data
    merged_df: pd.DataFrame = pd.merge(
        df, 
        dealer_mapping, 
        on='Dealer', 
        how='outer'
    )

    # Date formatting
    date_cols = ['Contract Date','Fund Date','Pay-off Date']
    for col in date_cols:
        if col in merged_df.columns:
            merged_df[col] = pd.to_datetime(merged_df[col], errors='coerce')
        else:
            raise KeyError(f"Required date column '{col}' not found")
        
    # Numeric columns to float
    numeric_cols = ['Amt. Financed','Dealer Split','Dealer Flat','Charge-back Amt.']
    for col in numeric_cols:
        merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce').fillna(0)

    # Create calculated column for total
    merged_df['Total'] = merged_df['Dealer Split'] + merged_df['Dealer Flat'] - merged_df['Charge-back Amt.']

    try:
        amt_idx = merged_df.columns.get_loc('Amt. Financed')
        split_idx = merged_df.columns.get_loc('Dealer Split')
        flat_idx = merged_df.columns.get_loc('Dealer Flat')
        chargeback_idx = merged_df.columns.get_loc('Charge-back Amt.')
        total_idx = merged_df.columns.get_loc('Total')
        name_idx = merged_df.columns.get_loc('Name')
    except KeyError as e:
        raise KeyError(f"Missing required column: {e}")

    # Create formatted output
    output: List[List[Any]] = []

    # Add header
    output.append(merged_df.columns.tolist())

    # Process dealers
    for dealer, group in merged_df.groupby('Dealer'):
        group = group.sort_values(by=['Charge back','Fund Date'], ascending=[True,True])
        for col in date_cols:
            group.loc[:, col] = group[col]
        # Create subtitle based on available mapping
        account_number = group['Account Number'].iloc[0]
        if pd.isna(account_number):
            subtitle_text = f"{dealer}: Account Number Not Mapped!"
        else:
            subtitle_text = f"{dealer}: Dealer Reserve DDA {account_number:.0f}"
            
        # Subtitle row
        subtitle: List[Any] = [''] * len(merged_df.columns)
        subtitle[name_idx] = subtitle_text
        output.append(subtitle)
        
        # Data rows
        output.extend(group.values.tolist())
        
        # Subtotal
        subtotal = [''] * len(merged_df.columns)
        subtotal[amt_idx] = group['Amt. Financed'].sum()
        subtotal[split_idx] = group['Dealer Split'].sum()
        subtotal[flat_idx] = group['Dealer Flat'].sum()
        subtotal[chargeback_idx] = group['Charge-back Amt.'].sum()
        subtotal[total_idx] = group['Total'].sum()
        subtotal[total_idx] = float(np.where(subtotal[total_idx] < 0, 0, subtotal[total_idx]))
        output.append(subtotal)
        
        # Blank line
        output.append([''] * len(merged_df.columns))

    # Create DataFrame and save
    report_df: pd.DataFrame = pd.DataFrame(output)
    report_df = report_df.drop(columns=[16])
    report_df[17] = np.where(report_df[1] == "", report_df[17], "")

    # Create Grand Total Row
    cols_to_sum = [7,13,14,15,17]
    subtotal_mask = report_df[17].ne("")
    subtotal_df = report_df[subtotal_mask]
    subtotal_df_numeric = subtotal_df.apply(pd.to_numeric, errors='coerce')
    total_values = subtotal_df_numeric[cols_to_sum].sum()
    total_row = pd.Series([""] * len(report_df.columns), index=report_df.columns)
    total_row[cols_to_sum] = total_values
    df_with_total = pd.concat([report_df, total_row.to_frame().T], ignore_index=True)
    df_with_total.iloc[-1, 2] = "Grand Total"
    df_with_total.loc[0, 17] = "Total"

    # Export to Excel
    df_with_total.to_excel(REPORT_PATH, index=False, header=False)

    # Format Excel file
    format_excel_file(REPORT_PATH)

    # Log the report generation
    print(f"Report generated: {REPORT_PATH}")
    print(f"Report details: {df_with_total.describe()}")
    print(f"Missing values in report: {df_with_total.isnull().sum()}")

if __name__ == '__main__':
    print(f"Starting [{__version__}]")
    generate_report()
    print("Complete!")