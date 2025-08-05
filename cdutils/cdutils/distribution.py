from typing import List
from pathlib import Path

import win32com.client as win32 # type: ignore

# Usage
# # Distribution
# recipients = [
#     # "chad.doorley@bcsbmail.com"
#     "paul.kocak@bcsbmail.com",
#     "linda.clark@bcsbmail.com"
# ]
# cc_recipients = [
#     "manager@bcsbmail.com"
# ]
# bcc_recipients = [
#     "chad.doorley@bcsbmail.com"
# ]
# subject = f"Weekly Loan Report - {datetime.now().strftime('%m/%d/%Y')}" 
# body = "Hi all, \n\nAttached is the Weekly Loan Report with a 45 day lookback. Please let me know if you have any questions."
# attachment_paths = [OUTPUT_PATH]

def email_out(recipients: List, cc_recipients: List = None, bcc_recipients: List = None, subject: str = "", body: str = "", attachment_paths: List[Path] = None) -> None:
    # Gracefully handle empty or None recipients
    if not recipients or len(recipients) == 0:
        print("No recipients provided - email not sent")
        return
    
    # Handle None values for optional parameters
    if cc_recipients is None:
        cc_recipients = []
    if bcc_recipients is None:
        bcc_recipients = []
    if attachment_paths is None:
        attachment_paths = []
    
    try:
        outlook = win32.Dispatch("Outlook.Application")
        message = outlook.CreateItem(0)
        # message.Display()

        # Can't get this to work
        # desired_email = "BusinessIntelligence@bcsbmail.com"
        # for account in outlook.Session.Accounts:
        #     if account.SmtpAddress == desired_email:
        #         message.SendUsingAccount = account
        #         break
        #     else:
        #         print(f"Warning: Coudn't find {desired_email} in available Outlook Accounts")
        message.SentOnBehalfOfName = "BusinessIntelligence@bcsbmail.com"
        
        message.To = ";".join(recipients)
        if cc_recipients:
            message.CC = ";".join(cc_recipients)
        if bcc_recipients:
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