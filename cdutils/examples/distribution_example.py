"""
Example usage of the cdutils.distribution module for sending emails via Outlook.

This example demonstrates various ways to use the email_out function with different
recipient configurations.
"""

from pathlib import Path
from datetime import datetime
import cdutils.distribution


def example_basic_email():
    """Send a basic email with TO recipients only."""
    cdutils.distribution.email_out(
        recipients=["user@example.com"],
        subject="Test Email - Basic",
        body="This is a basic test email with TO recipients only."
    )
    print("Basic email sent!")


def example_email_with_cc():
    """Send an email with TO and CC recipients."""
    cdutils.distribution.email_out(
        recipients=["primary@example.com"],
        cc_recipients=["manager@example.com", "team@example.com"],
        subject="Test Email - With CC",
        body="This email includes CC recipients for visibility."
    )
    print("Email with CC sent!")


def example_email_with_all_fields():
    """Send an email with TO, CC, BCC recipients and attachments."""
    # Create a sample file for attachment
    sample_file = Path("sample_report.txt")
    sample_file.write_text("Sample report content")
    
    try:
        cdutils.distribution.email_out(
            recipients=["recipient1@example.com", "recipient2@example.com"],
            cc_recipients=["cc1@example.com", "cc2@example.com"],
            bcc_recipients=["businessintelligence@bcsbmail.com"],
            subject=f"Daily Report - {datetime.now().strftime('%Y-%m-%d')}",
            body="""Hi Team,

Please find attached today's report.

Best regards,
Business Intelligence Team""",
            attachment_paths=[sample_file]
        )
        print("Full email with attachments sent!")
    finally:
        # Clean up
        if sample_file.exists():
            sample_file.unlink()


def example_report_distribution():
    """Example of typical report distribution pattern."""
    # This pattern is commonly used in standardized reports
    
    # Configuration (typically from config.py)
    ENV = "prod"  # or os.getenv('REPORT_ENV', 'dev')
    EMAIL_TO = ["report.recipient@bcsbmail.com"] if ENV == "prod" else []
    EMAIL_CC = ["businessintelligence@bcsbmail.com"] if ENV == "prod" else []
    
    # Report output
    report_path = Path("monthly_report.xlsx")
    
    if EMAIL_TO:  # Only send if recipients configured
        subject = f"Monthly Report - {datetime.now().strftime('%B %Y')}"
        body = """Hi,

Attached is the Monthly Report. If you have any questions, please reach out to BusinessIntelligence@bcsbmail.com

Thanks!"""
        
        cdutils.distribution.email_out(
            recipients=EMAIL_TO,
            cc_recipients=EMAIL_CC,
            subject=subject,
            body=body,
            attachment_paths=[report_path] if report_path.exists() else []
        )
        print(f"Report sent to {len(EMAIL_TO)} recipients with {len(EMAIL_CC)} CC")
    else:
        print("Development mode - email not sent")


if __name__ == "__main__":
    print("cdutils.distribution Examples")
    print("=" * 40)
    
    # Uncomment the example you want to run:
    
    # example_basic_email()
    # example_email_with_cc()
    # example_email_with_all_fields()
    # example_report_distribution()
    
    print("\nNote: Uncomment the example function you want to run in the main block.")