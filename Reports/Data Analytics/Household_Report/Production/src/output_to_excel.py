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
            sheet.Columns("J:J").NumberFormat = "mm/dd/yyyy"
            sheet.Columns("K:K").NumberFormat = "mm/dd/yyyy"

            # sheet.Columns("I:I").NumberFormat = "0.00%"
            
            # sheet.Columns("J:J").NumberFormat = "$#,##0.00"
            # sheet.Columns("K:K").NumberFormat = "$#,##0.00"

        format_columns()

        # Freeze top row
        sheet.Application.ActiveWindow.SplitRow = 1
        sheet.Application.ActiveWindow.FreezePanes = True


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
