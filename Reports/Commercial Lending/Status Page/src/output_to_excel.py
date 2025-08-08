"""
Output to Excel
"""
import win32com.client as win32
import pandas as pd
from pathlib import Path

def col_num_to_letter(col_num):
    """Convert a column number (1-based) to Excel column letter(s), e.g., 1 -> A, 26 -> Z, 27 -> AA."""
    letters = ''
    while col_num > 0:
        col_num, remainder = divmod(col_num - 1, 26)
        letters = chr(65 + remainder) + letters
    return letters


def excel_mapping(template_path: Path, output_path: Path, cell_values: dict, df_inserts: list) -> None:
    """
    Write cell values and DataFrames to an Excel file using a template with pywin32.
    
    Args:
        template_path: Path to the Excel template file.
        output_path: Path where the modified Excel file will be saved.
        cell_values (dict): Dictionary mapping cell addresses (e.g., "A1") to values.
        df_inserts (list): List of tuples, each containing (start_row, df) or 
                          (start_row, df, start_col), specifying where to insert DataFrames.
    
    Raises:
        AssertionError: If input parameters do not meet expected conditions.
        Exception: If an error occurs during Excel operations.
    """
    # Validate input paths
    assert Path(template_path).is_file(), f"Template file does not exist: {template_path}"
    assert isinstance(cell_values, dict), "cell_values must be a dictionary"
    assert isinstance(df_inserts, list), "df_inserts must be a list"
    
    # Ensure output directory exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Delete the existing file in output path before running to avoid conflicts
    if output_path.exists():
        output_path.unlink()
       
    # Pre‑declare COM objects so we can safely close them in finally
    excel = None
    wb = None

    try:
        # Initialize Excel application
        excel = win32.Dispatch('Excel.Application')
        excel.Visible = False  # Run in background
        wb = excel.Workbooks.Open(str(template_path.absolute()))
        ws = wb.Worksheets(1)  # Use first worksheet

     # Write specific cell values
        for cell, value in cell_values.items():
            if not value:
                continue
            assert isinstance(cell, str), f"Cell address must be a string, got {cell}"
            # Coerce Path-like values to string to avoid COM type conversion issues
            if isinstance(value, Path):
                value = str(value)
            ws.Range(cell).Value = value
        
        for insertion in df_inserts:
            # Unpack tuple based on length
            if len(insertion) == 2:
                start_row, df = insertion
                start_col = 'A'  # Default to column A

            elif len(insertion) == 3:
                start_row, df, start_col = insertion

                # Convert integer start_col to letter if needed
                if isinstance(start_col, int):
                    start_col = col_num_to_letter(start_col)
            else:
                raise ValueError("Each insertion must be a tuple of 2 or 3 elements: (start_row, df, [start_col])")
            # Validate inputs
            assert isinstance(start_row, int) and start_row > 0, "start_row must be a positive integer"
            assert isinstance(start_col, str) and start_col.isalpha(), "start_col must be a string of letters (e.g., 'A', 'AA')"
            assert isinstance(df, pd.DataFrame), "df must be a pandas DataFrame"

            if df is None or df.empty:
                continue 
            
            # Get DataFrame dimensions
            num_rows = int(df.shape[0])
            num_cols = int(df.shape[1])
            
            # print(f"Inserting at: start_row = {start_row}, start_col = {start_col}, df.shape = {df.shape}")

            if num_rows > 0:
                ws.Range(f"{start_row}:{start_row + num_rows - 1}").Insert(-4121, 1) # Shift down

            start_cell = f"{start_col}{start_row}"
            # print(start_cell)
            # print(num_rows, num_cols)
            range_obj = ws.Range(start_cell).GetResize(num_rows, num_cols)
            # range_obj = ws.Range("A29").Resize(8, 7)
            # print(range_obj.Address)
            # Convert any Path objects inside the DataFrame to strings before writing to Excel
            if (df.dtypes == 'object').any():
                df_safe = df.astype(object).applymap(lambda x: str(x) if isinstance(x, Path) else x)
            else:
                df_safe = df
            # Provide data as a nested list for COM interop
            range_obj.Value = df_safe.values.tolist()

            # # Define the starting cell (e.g., "A5" or "H29")
            # start_cell = f"{start_col}{start_row}"
            # # Insert rows to accommodate the DataFrame
            # row_range = f"{start_row}:{start_row + num_rows - 1}"
            # ws.Rows(row_range).Insert(Shift=-4121)  # xlShiftDown constant
            # # Write the DataFrame to the specified range
            # ws.Range(start_cell).Resize(num_rows, num_cols).Value = df.values.tolist()
        
        # Set print area
        ws.PageSetup.Zoom = False
        ws.PageSetup.FitToPagesWide = 1
        ws.PageSetup.FitToPagesTall = 1

        excel.DisplayAlerts = False 
    # Save the workbook to the output path
        wb.SaveAs(str(output_path.absolute()))
    
    except Exception as e:
        print(f"Error occurred: {e}")
        raise
    
    finally:
        # Ensure workbook and Excel application are closed
        if wb is not None:
            wb.Close(SaveChanges=False)
        if excel is not None:
            excel.Quit()
