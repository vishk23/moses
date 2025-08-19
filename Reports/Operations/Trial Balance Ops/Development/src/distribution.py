from typing import List
from pathlib import Path

import win32com.client as win32 # type: ignore


def email_out(recipients: List, bcc_recipients: List, subject: str, body: str, attachment_paths: Path) -> None:
    try:
        outlook = win32.Dispatch("Outlook.Application")
        message = outlook.CreateItem(0)
        # message.Display()
        message.To = ";".join(recipients)
        message.BCC = ";".join(bcc_recipients)
        message.Subject = subject
        message.Body = body

        for file_path in attachment_paths:
            absolute_path = str(Path(file_path).absolute())
            message.Attachments.Add(absolute_path)
        message.Send()
        outlook.Quit()
        print("Email sent!")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        outlook = None