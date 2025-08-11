"""
Output to Excel formatting via COM
"""
from pathlib import Path
import win32com.client as win32  # type: ignore


def format_excel_file(file_path: Path):
    excel = None
    workbook = None
    try:
        excel = win32.Dispatch("Excel.Application")
        excel.Visible = False
        workbook = excel.Workbooks.Open(str(Path(file_path).absolute()))

        irregular = ['Irregular']

        for sheet in workbook.Sheets:
            sheet.Columns.AutoFit()

            # Bold top row
            top_row = sheet.Rows(1)
            top_row.Font.Bold = True

            # Bottom border on header
            bottom_border = top_row.Borders(9)
            bottom_border.LineStyle = 1
            bottom_border.Weight = 2

            # Freeze top row
            sheet.Application.ActiveWindow.SplitRow = 1
            sheet.Application.ActiveWindow.FreezePanes = True

            if sheet.Name not in irregular:
                sheet.Columns("G:G").NumberFormat = "mm/dd/yyyy"
                sheet.Columns("H:H").NumberFormat = "mm/dd/yyyy"
                sheet.Columns("L:L").NumberFormat = "mm/dd/yyyy"
            else:
                sheet.Columns("K:K").NumberFormat = "mm/dd/yyyy"
                sheet.Columns("I:I").NumberFormat = "0.00%"
                sheet.Columns("H:H").NumberFormat = "$#,##0.00"
                sheet.Columns("L:L").NumberFormat = "$#,##0.00"
                sheet.Columns("M:M").NumberFormat = "$#,##0.00"
                sheet.Columns("N:N").NumberFormat = "$#,##0.00"
                sheet.Columns("O:O").NumberFormat = "$#,##0.00"
                sheet.Columns("T:T").NumberFormat = "$#,##0.00"
                sheet.Columns("U:U").NumberFormat = "$#,##0.00"
                sheet.Columns("V:V").NumberFormat = "$#,##0.00"
                sheet.Columns("W:W").NumberFormat = "$#,##0.00"

        workbook.Save()
    finally:
        if workbook is not None:
            workbook.Close(SaveChanges=False)
        if excel is not None:
            excel.Quit()
