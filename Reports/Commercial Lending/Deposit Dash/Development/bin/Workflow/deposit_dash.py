"""
= Project Name: Deposit Dash Report =
= Status: Completed =
v1.0.0 
File_path:
\\10.161.85.66\Home\Share\Data & Analytics Initiatives\Project Management\Chad Projects\Monthly Reports\Deposit Dash\


= Overview =
Goal: Assist the portfolio managers with understanding deposit balances and trends for their teams and lenders that they assist.
 
Key Stakeholder: Hasan Ali

= Milestones =
- [x] Build in Alteryx
- [x] Recode to automated execution

= Notes =

"""


from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd
from pathlib import Path
import datetime
from win32com.client import Dispatch

def main():
    # Read inputs
    file_path = r'\\10.161.85.66\Home\Share\Line of Business_Shared Services\Commercial Credit\Deposits\DailyDeposit\DailyDeposit.xlsx'
    df1 = pd.read_excel(file_path)

    wb = Workbook()
    ws = wb.active

    for r in dataframe_to_rows(df1, index=False, header=True):
        ws.append(r)

    current_date = datetime.datetime.now().strftime("%m%d%y")


    directory = Path(r'\\10.161.85.66\Home\Share\Data & Analytics Initiatives\Project Management\Chad Projects\Monthly Reports\Deposit Dash\Production\Output')
    filename = f"DepositDash_{current_date}.xlsx"
    full_path = directory / filename

    wb.save(full_path)
    wb.close()
    print(f"Written to {full_path}")

    excel = Dispatch('Excel.Application')

    wb = excel.Workbooks.Open(full_path)

    sheet_name = "Sheet"
    sheet = wb.Sheets(sheet_name)

    #Autofit column in active sheet
    sheet.Columns.AutoFit()

    # Bold top row
    top_row = sheet.Rows(1)
    top_row.Font.Bold = True

    # Add bottom border to header row
    bottom_border = top_row.Borders(9)
    bottom_border.LineStyle = 1
    bottom_border.Weight = 2

    # Short Date
    sheet.Columns(15).NumberFormat = "mm/dd/yyy"
    sheet.Columns(16).NumberFormat = "mm/dd/yyy"

    # Freeze top row
    sheet.Application.ActiveWindow.SplitRow = 1
    sheet.Application.ActiveWindow.FreezePanes = True

    #Save changes in a new file
    wb.Save()

    wb.Close()
    excel.Quit()
    print(f"Formatting Completed!")

    # Email
    recipients = [
        # "commercial.portfolio.managers@bcsbmail.com",
        "chad.doorley@bcsbmail.com"
    ]
    bcc_recipients = [
        "chad.doorley@bcsbmail.com"
    ]
    outlook = Dispatch("Outlook.Application")
    message = outlook.CreateItem(0)
    # message.Display()
    message.To = ";".join(recipients)
    message.BCC = ";".join(bcc_recipients)
    message.Subject = f"Deposit Dash PMs"
    message.Body = "Hi all, \n\nAttached is the monthly deposit report for the most recent month end. Please let me know if you have any questions"
    message.Attachments.Add(str(full_path))
    message.Send()
    print("Email sent!")


if __name__ == "__main__":
    main()