from datetime import datetime
import win32com.client as win32 # type: ignore
from pathlib import Path
import pandas as pd
from src.config import OUTPUT_DIR

"""
Autofits and formats excel file
"""

def format_excel_file(file_path):
    excel = None
    workbook = None

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

        # adding percent format to book to look % in book to look recon at the bottom
        last_row = sheet.UsedRange.Rows.Count
        cell = sheet.Cells(last_row, 4)
        cell.NumberFormat = "0.00%"

        # bolding book to look recon header
        btl_header = sheet.Cells(last_row - 2, 1)
        btl_header.Font.Bold = True

        # Freeze top row
        sheet.Application.ActiveWindow.SplitRow = 1
        sheet.Application.ActiveWindow.FreezePanes = True

        excel.DisplayAlerts = False
        workbook.Save()

        # print(f"Excel file saved with autofit at {file_path}")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if workbook is not None:
            workbook.Close(SaveChanges=False)
        if excel is not None:
            excel.Quit()


"""
Exports dataframe to excel file and bolds total rows
"""
def exportReport(final_df):
    
    today = datetime.today()

    # finding the month and year of report we should be making

    current_year = today.year
    current_month = today.month

    if current_month == 1:
        previous_month = 12
        year_of_previous_month = current_year - 1
    else:
        previous_month = current_month - 1
        year_of_previous_month = current_year

    previous_month = datetime(year_of_previous_month, previous_month, 1).strftime("%B")

    output_file_path = OUTPUT_DIR / Path("E Contract Summary " + previous_month + " " + str(year_of_previous_month) + ".xlsx")

    with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
        final_df.to_excel(writer, index=False, sheet_name='Sheet1')
        
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']

        bold_format = workbook.add_format({'bold': True})

        for row_num, (_, row) in enumerate(final_df.iterrows(), start=1):
            is_bold_row = 'total' in str(row['Dealer Name']).lower()

            for col_num, value in enumerate(row):
                if is_bold_row:
                    worksheet.write(row_num, col_num, value, bold_format)


    format_excel_file(output_file_path)

    print("Report generated")