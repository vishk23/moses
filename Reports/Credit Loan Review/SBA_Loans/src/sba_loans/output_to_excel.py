# output_to_excel.py

import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Font, Alignment, NamedStyle
from openpyxl.worksheet.dimensions import ColumnDimension
from pathlib import Path
from datetime import datetime

def export_df_to_excel(df, output_path):
    """
    Exports a Pandas DataFrame to an Excel file with auto-fitted column widths,
    bold headers, and a frozen top row. Additionally, formats specific columns
    according to the requirements.

    :param df: Pandas DataFrame to be exported.
    :param output_path: Path where the Excel file will be saved.
    """
    # Create a new workbook and select the active worksheet
    wb = Workbook()
    ws = wb.active

    # Convert the DataFrame to rows and append them to the worksheet
    for r in dataframe_to_rows(df, index=False, header=True):
        ws.append(r)

    # Define styles
    date_style = NamedStyle(name="date_style")
    date_style.number_format = "mm/dd/yyyy"
    wb.add_named_style(date_style)

    currency_style = NamedStyle(name="currency_style")
    currency_style.number_format = "$#,##0.00"
    wb.add_named_style(currency_style)

    percent_style = NamedStyle(name="percent_style")
    percent_style.number_format = "0.00%"
    wb.add_named_style(percent_style)

    # Apply styles to specific columns
    for col in ws.columns:
        column_letter = col[0].column_letter
        if column_letter in ['B', 'G']:
            for cell in col:
                cell.style = date_style
        elif column_letter in ['C', 'E', 'F', 'H']:
            for cell in col:
                cell.style = currency_style
        elif column_letter == 'D':
            for cell in col:
                cell.style = percent_style

    # Auto-fit column widths
    for col in ws.columns:
        max_length = 0
        column_letter = col[0].column_letter
        for cell in col:
            try:  # Necessary to avoid error on empty cells
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column_letter].width = adjusted_width

    # Bold the headers
    for cell in ws[1]:
        cell.font = Font(bold=True)

    # Freeze the top row
    ws.freeze_panes = 'A2'

    # Save the workbook
    wb.save(output_path)

