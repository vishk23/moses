"""
Main entry point for New Loan Report LR Credit.

This report generates a weekly loan report with a 45-day lookback for new loans,
providing both NEW LOAN and CRA sections for Credit Loan Review team.
"""

from pathlib import Path
from datetime import datetime
import pandas as pd

import src.config
import src._version
from src.new_loan_credit_lr import fetch_data, core


def main():
    print(f"Running {src._version.__version__}")
    print(f"Running {src.config.REPORT_NAME} for {src.config.BUSINESS_LINE}")
    print(f"Schedule: {src.config.SCHEDULE}")
    print(f"Owner: {src.config.OWNER}")
    print(f"Environment: {src.config.ENV}")
    print(f"Output directory: {src.config.OUTPUT_DIR}")
    
    # Ensure output directory exists
    src.config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Fetch data from database
    print("Fetching data from database...")
    data = fetch_data.fetch_data()
    
    # Process data through main pipeline
    print("Processing data...")
    new_loan_page, cra_page = core.main_pipeline(data)
    
    # Generate output filename with current date
    current_date = datetime.now().strftime('%Y%m%d')
    filename = f'Loan_Report_45_day_lookback_{current_date}.xlsx'
    output_path = src.config.OUTPUT_DIR / filename
    
    # Write to Excel with multiple sheets
    print(f"Writing output to: {output_path}")
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        new_loan_page.to_excel(writer, sheet_name='NEW LOAN', index=False)
        cra_page.to_excel(writer, sheet_name='CRA', index=False)
    
    # Format Excel file (if in production environment)
    if src.config.ENV == 'prod':
        format_excel_file(output_path)
    
    # Send email distribution (if in production environment)
    if src.config.ENV == 'prod' and src.config.PROD_READY:
        send_email_distribution(output_path)
    
    print("Report generation complete!")


def format_excel_file(file_path: Path):
    """
    Format the Excel file for better presentation.
    Only works on Windows with Excel installed.
    """
    try:
        import win32com.client as win32
        
        excel = win32.Dispatch("Excel.Application")
        excel.Visible = False
        workbook = excel.Workbooks.Open(str(file_path.absolute()))
        
        for sheet in workbook.Sheets:
            # Auto-fit columns
            sheet.Columns.AutoFit()
            
            # Bold and format header row
            top_row = sheet.Rows(1)
            top_row.Font.Bold = True
            
            # Add bottom border to header row
            bottom_border = top_row.Borders(9)  # xlEdgeBottom
            bottom_border.LineStyle = 1
            bottom_border.Weight = 2
        
        workbook.Save()
        workbook.Close()
        excel.Quit()
        print("Excel formatting applied successfully")
        
    except ImportError:
        print("Excel formatting skipped - win32com not available")
    except Exception as e:
        print(f"Excel formatting failed: {e}")


def send_email_distribution(output_path: Path):
    """
    Send email with the report attachment.
    Only works on Windows with Outlook installed.
    """
    try:
        import win32com.client as win32
        
        subject = f"Weekly Loan Report - {datetime.now().strftime('%m/%d/%Y')}"
        body = "Hi all,\n\nAttached is the Weekly Loan Report with a 45 day lookback. Please let me know if you have any questions."
        
        outlook = win32.Dispatch("Outlook.Application")
        message = outlook.CreateItem(0)  # olMailItem
        
        message.To = ";".join(src.config.EMAIL_TO)
        message.CC = ";".join(src.config.EMAIL_CC)
        message.Subject = subject
        message.Body = body
        
        # Add attachment
        absolute_path = str(output_path.absolute())
        message.Attachments.Add(absolute_path)
        
        message.Send()
        outlook.Quit()
        print("Email sent successfully!")
        
    except ImportError:
        print("Email distribution skipped - win32com not available")
    except Exception as e:
        print(f"Email distribution failed: {e}")


if __name__ == "__main__":
    main()