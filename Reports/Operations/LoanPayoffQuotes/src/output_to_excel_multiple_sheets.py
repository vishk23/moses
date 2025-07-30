"""
Output to Excel
"""

import win32com.client as win32 # type: ignore


def format_excel_file(file_path):
    excel = None
    workbook = None
    # Formatting
    try:
        excel = win32.Dispatch("Excel.Application")
        excel.Visible = False
        workbook = excel.Workbooks.Open(str(file_path.absolute()))

        summary_sheet = ['Summary']

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
            
            if sheet.Name not in summary_sheet:
                def format_columns():
                    sheet.Columns("F:F").NumberFormat = "mm/dd/yyyy"
                    sheet.Columns("M:M").NumberFormat = "mm/dd/yyyy"
                    sheet.Columns("T:T").NumberFormat = "mm/dd/yyyy"
                    sheet.Columns("AA:AA").NumberFormat = "mm/dd/yyyy"

                    sheet.Columns("K:K").NumberFormat = "0.00%"
                    sheet.Columns("Y:Y").NumberFormat = "0.00%"
                    
                    sheet.Columns("I:I").NumberFormat = "$#,##0.00"
                    sheet.Columns("J:J").NumberFormat = "$#,##0.00"
                    sheet.Columns("W:W").NumberFormat = "$#,##0.00"
                    sheet.Columns("X:X").NumberFormat = "$#,##0.00"
                    sheet.Columns("AE:AE").NumberFormat = "$#,##0.00"

                format_columns()
            
            if sheet.Name in summary_sheet:
                def format_columns():
                    sheet.Columns("B:B").NumberFormat = "$#,##0.00"
                    sheet.Columns("C:C").NumberFormat = "$#,##0.00"
                    sheet.Columns("D:D").NumberFormat = "$#,##0.00"

                format_columns()

        workbook.Save()

        # print(f"Excel file saved with autofit at {file_path}")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if workbook is not None:
            workbook.Close(SaveChanges=False)
        if excel is not None:
            excel.Quit()