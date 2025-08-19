from typing import List
from pathlib import Path

import win32com.client as win32 # type: ignore


def email_out(recipients: List, bcc_recipients: List, attachment_path: Path) -> None:
    try:
        outlook = win32.Dispatch("Outlook.Application")
        message = outlook.CreateItem(0)
        # message.Display()
        message.To = ";".join(recipients)
        message.BCC = ";".join(bcc_recipients)
        message.Subject = f"Deposit Deep Dive"
        message.Body = "Hi Eddie, \n\nAttached is the monthly deposit deep dive report. Please let me know if you have any questions"
        message.Attachments.Add(str(attachment_path.absolute()))
        message.Send()
        outlook.Quit()
        print("Email sent!")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        outlook = None