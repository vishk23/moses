# Email Distribution Module

The `cdutils.distribution` module provides a clean, cross-platform way to send emails via Microsoft Outlook without requiring win32com dependencies.

## Features

- **Cross-platform support**: Works on Windows and macOS
- **No win32com dependency**: Uses PowerShell on Windows and AppleScript on macOS
- **Full email features**: Supports TO, CC, BCC recipients and file attachments
- **Outlook integration**: Opens emails in Outlook for review before sending
- **Backward compatibility**: Maintains support for legacy code

## Installation

No additional dependencies required! The module uses built-in system tools:
- Windows: PowerShell (included with Windows)
- macOS: AppleScript (included with macOS)

## Usage

### Basic Example

```python
import cdutils.distribution

# Send a simple email
cdutils.distribution.email_out(
    recipients=["user@example.com"],
    subject="Test Email",
    body="This is a test email."
)
```

### Full Example with All Features

```python
from pathlib import Path
import cdutils.distribution

# Send email with all recipient types and attachments
cdutils.distribution.email_out(
    recipients=["primary@example.com", "secondary@example.com"],
    cc_recipients=["manager@example.com"],
    bcc_recipients=["archive@example.com"],
    subject="Monthly Report - January 2024",
    body="""Hi Team,

Please find attached the monthly report for January 2024.

Key highlights:
- Revenue increased by 15%
- Customer satisfaction at 92%
- New product launch successful

Best regards,
Business Intelligence Team""",
    attachment_paths=[
        Path("reports/monthly_report.xlsx"),
        Path("reports/summary.pdf")
    ]
)
```

### Standard Report Pattern

This is the pattern used in our standardized reports:

```python
import cdutils.distribution
from pathlib import Path
import os

# Configuration (typically in config.py)
ENV = os.getenv('REPORT_ENV', 'dev')
EMAIL_TO = ["recipient@bcsbmail.com"] if ENV == 'prod' else []
EMAIL_CC = ["businessintelligence@bcsbmail.com"] if ENV == 'prod' else []

# After generating report
output_path = Path("output/report.xlsx")

if EMAIL_TO:  # Only send if recipients configured
    cdutils.distribution.email_out(
        recipients=EMAIL_TO,
        cc_recipients=EMAIL_CC,
        subject="Daily Report - Operations",
        body="""Hi,

Attached is the Daily Report. If you have any questions, please reach out to BusinessIntelligence@bcsbmail.com

Thanks!""",
        attachment_paths=[output_path]
    )
    print(f"Email sent to {len(EMAIL_TO)} recipients")
else:
    print("Development mode - email not sent")
```

## How It Works

### Windows
1. Creates a PowerShell script that uses Outlook COM objects
2. Sets all email properties (recipients, subject, body, attachments)
3. Opens the email in Outlook for review
4. User can review and click Send manually

### macOS
1. Creates an AppleScript that controls Microsoft Outlook
2. Sets all email properties
3. Opens the email in Outlook for review
4. User can review and click Send manually

### Other Platforms
Falls back to `mailto:` URL which opens the default email client with pre-filled fields (attachments must be added manually).

## Key Differences from win32com

1. **No Python dependencies**: Doesn't require `pywin32` package
2. **Display vs Send**: Opens email for review instead of sending immediately
3. **Better error handling**: Provides clear error messages
4. **Cross-platform**: Works on both Windows and macOS

## Migrating from win32com

If you have existing code using win32com, the migration is simple:

```python
# Old win32com code
import win32com.client
outlook = win32com.client.Dispatch("Outlook.Application")
mail = outlook.CreateItem(0)
mail.To = "user@example.com"
mail.Subject = "Test"
mail.Body = "Test email"
mail.Send()

# New cdutils code
import cdutils.distribution
cdutils.distribution.email_out(
    recipients=["user@example.com"],
    subject="Test",
    body="Test email"
)
```

## Notes

- Emails are opened for review, not sent automatically (for safety)
- The sender is set to "BusinessIntelligence@bcsbmail.com" when possible
- File paths are automatically converted to absolute paths
- Non-existent attachments generate warnings but don't stop execution