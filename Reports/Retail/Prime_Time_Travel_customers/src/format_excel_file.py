import win32com.client as win32 # type: ignore

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


        # format_columns()

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