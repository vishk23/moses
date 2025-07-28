import unittest
import cdutils.distribution
from datetime import datetime
from pathlib import Path


class TestDistribution(unittest.TestCase):
    def setUp(self):
        """Set up test email parameters."""
        self.recipients = ["chad.doorley@bcsbmail.com"]
        self.cc_recipients = ["businessintelligence@bcsbmail.com"]
        self.bcc_recipients = ["chad.doorley@bcsbmail.com"]
        self.subject = f"Testing - {datetime.now().strftime('%m/%d/%Y')}" 
        self.body = "Hi - Testing the email distribution module."
        self.attachment_paths = []

    def test_send_basic(self):
        """Test basic email sending with TO recipients only."""
        try:
            cdutils.distribution.email_out(
                recipients=self.recipients,
                subject=self.subject,
                body=self.body
            ) 
        except Exception as e:
            self.fail(f"email_out raised exception: {str(e)}")

    def test_send_with_cc(self):
        """Test email sending with TO and CC recipients."""
        try:
            cdutils.distribution.email_out(
                recipients=self.recipients,
                cc_recipients=self.cc_recipients,
                subject=self.subject + " (with CC)",
                body=self.body
            ) 
        except Exception as e:
            self.fail(f"email_out raised exception: {str(e)}")

    def test_send_with_all_recipients(self):
        """Test email sending with TO, CC, and BCC recipients."""
        try:
            cdutils.distribution.email_out(
                recipients=self.recipients,
                cc_recipients=self.cc_recipients,
                bcc_recipients=self.bcc_recipients,
                subject=self.subject + " (with CC and BCC)",
                body=self.body,
                attachment_paths=self.attachment_paths
            ) 
        except Exception as e:
            self.fail(f"email_out raised exception: {str(e)}")

    def test_legacy_function(self):
        """Test backward compatibility with legacy function signature."""
        try:
            cdutils.distribution.email_out_legacy(
                recipients=self.recipients,
                bcc_recipients=self.bcc_recipients,
                subject=self.subject + " (legacy)",
                body=self.body,
                attachment_paths=self.attachment_paths
            ) 
        except Exception as e:
            self.fail(f"email_out_legacy raised exception: {str(e)}")

    def test_send_with_attachment(self):
        """Test email sending with attachment (if test file exists)."""
        # Create a temporary test file
        test_file = Path("test_attachment.txt")
        test_file.write_text("This is a test attachment.")
        
        try:
            cdutils.distribution.email_out(
                recipients=self.recipients,
                cc_recipients=self.cc_recipients,
                subject=self.subject + " (with attachment)",
                body=self.body,
                attachment_paths=[test_file]
            ) 
        except Exception as e:
            self.fail(f"email_out raised exception: {str(e)}")
        finally:
            # Clean up test file
            if test_file.exists():
                test_file.unlink()


if __name__ == '__main__':
    unittest.main()