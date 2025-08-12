"""
Output to Excel
"""

import win32com.client as win32 # type: ignore


def format_excel_file(file_path):
    # Formatting
    try:
        excel = win32.Dispatch("Excel.Application")
        excel.Visible = False
        workbook = excel.Workbooks.Open(str(file_path.absolute()))

        new_loan_sheet = ['NEW LOAN']
        cra_sheet = ['CRA']

        for sheet in workbook.Sheets:

            sheet.Columns.AutoFit()

            # Bold top row
            top_row = sheet.Rows(1)
            top_row.Font.Bold = True

            # Add bottom border to header row
            bottom_border = top_row.Borders(9)
            bottom_border.LineStyle = 1
            bottom_border.Weight = 2

            # Freeze top row
            sheet.Application.ActiveWindow.SplitRow = 1
            sheet.Application.ActiveWindow.FreezePanes = True
            
            if sheet.Name in new_loan_sheet:
                def format_columns():
                    sheet.Columns("F:F").NumberFormat = "mm/dd/yyyy"
                    sheet.Columns("G:G").NumberFormat = "mm/dd/yyyy"

                    sheet.Columns("X:X").NumberFormat = "0.00%"
                    
                    sheet.Columns("L:L").NumberFormat = "$#,##0.00"
                    sheet.Columns("M:M").NumberFormat = "$#,##0.00"
                    sheet.Columns("N:N").NumberFormat = "$#,##0.00"
                    sheet.Columns("O:O").NumberFormat = "$#,##0.00"
                    sheet.Columns("P:P").NumberFormat = "$#,##0.00"
                    sheet.Columns("AA:AA").NumberFormat = "$#,##0.00"

                format_columns()
            
            if sheet.Name in cra_sheet:
                def format_columns():
                    sheet.Columns("B:B").NumberFormat = "mm/dd/yyyy"
                    sheet.Columns("W:W").NumberFormat = "mm/dd/yyyy"

                    sheet.Columns("U:U").NumberFormat = "0.00%"

                    sheet.Columns("E:E").NumberFormat = "$#,##0.00"

                format_columns()

        workbook.Save()
        workbook.Close()
        excel.Quit()

        # print(f"Excel file saved with autofit at {file_path}")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        sheet = None
        workbook = None
        excel = None
