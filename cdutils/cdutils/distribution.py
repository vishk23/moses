from typing import List, Optional, Union
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

def email_out(
    recipients: List[str],
    cc_recipients: Optional[List[str]] = None,
    bcc_recipients: Optional[List[str]] = None,
    subject: str = "",
    body: str = "",
    attachment_paths: Optional[List[Union[str, Path]]] = None,
) -> None:
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
        #         print(f"Warning: Couldn't find {desired_email} in available Outlook Accounts")
        message.SentOnBehalfOfName = "BusinessIntelligence@bcsbmail.com"

        # Ensure all addresses are strings
        recipients = [str(r) for r in recipients]
        cc_recipients = [str(r) for r in cc_recipients] if cc_recipients else []
        bcc_recipients = [str(r) for r in bcc_recipients] if bcc_recipients else []

        message.To = ";".join(recipients)
        if cc_recipients:
            message.CC = ";".join(cc_recipients)
        if bcc_recipients:
            message.BCC = ";".join(bcc_recipients)
        message.Subject = str(subject)
        message.Body = str(body)

        for file_path in attachment_paths:
            # Normalize to string absolute path; accept str or Path
            p = Path(file_path)
            absolute_path = str(p.resolve())
            # Optional existence check to avoid cryptic COM errors
            if not p.exists():
                print(f"Warning: attachment not found, skipping -> {absolute_path}")
                continue
            # Use positional arg; COM expects Source as first parameter
            message.Attachments.Add(absolute_path)
        message.Send()
        outlook.Quit()
        print("Email sent!")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        outlook = None