"""
Email distribution module for sending reports via Outlook.

This module provides functionality to send emails with attachments through Outlook
using native system integration without win32com dependencies.
"""

import subprocess
import platform
import os
import tempfile
import json
from typing import List, Optional, Union
from pathlib import Path


def email_out(
    recipients: List[str], 
    cc_recipients: Optional[List[str]] = None,
    bcc_recipients: Optional[List[str]] = None, 
    subject: str = "", 
    body: str = "", 
    attachment_paths: Optional[List[Union[str, Path]]] = None
) -> None:
    """
    Send an email via Outlook using native system integration.
    
    This function creates an email draft in Outlook with all specified parameters.
    On Windows, it uses PowerShell to interact with Outlook.
    On macOS, it uses AppleScript to interact with Microsoft Outlook.
    
    Args:
        recipients: List of email addresses for TO field
        cc_recipients: Optional list of email addresses for CC field
        bcc_recipients: Optional list of email addresses for BCC field
        subject: Email subject line
        body: Email body text
        attachment_paths: Optional list of file paths (str or Path objects) for attachments
        
    Example:
        email_out(
            recipients=["user1@example.com", "user2@example.com"],
            cc_recipients=["manager@example.com"],
            subject="Daily Report",
            body="Please find attached the daily report.",
            attachment_paths=[Path("report.xlsx")]
        )
    """
    # Initialize optional parameters
    cc_recipients = cc_recipients or []
    bcc_recipients = bcc_recipients or []
    attachment_paths = attachment_paths or []
    
    # Convert all paths to absolute paths
    absolute_paths = []
    for path in attachment_paths:
        abs_path = Path(path).absolute()
        if abs_path.exists():
            absolute_paths.append(str(abs_path))
        else:
            print(f"Warning: Attachment not found: {abs_path}")
    
    # Determine platform and send accordingly
    system = platform.system()
    
    try:
        if system == "Windows":
            _send_windows_outlook(recipients, cc_recipients, bcc_recipients, subject, body, absolute_paths)
        elif system == "Darwin":  # macOS
            _send_macos_outlook(recipients, cc_recipients, bcc_recipients, subject, body, absolute_paths)
        else:
            print(f"Platform {system} is not directly supported. Opening default email client...")
            _send_mailto(recipients, cc_recipients, bcc_recipients, subject, body)
            if absolute_paths:
                print("Please attach the following files manually:")
                for path in absolute_paths:
                    print(f"  - {path}")
    except Exception as e:
        print(f"Error preparing email: {str(e)}")
        raise


def _send_windows_outlook(recipients, cc_recipients, bcc_recipients, subject, body, attachment_paths):
    """Send email using PowerShell on Windows."""
    # Create PowerShell script
    ps_script = '''
Add-Type -AssemblyName Microsoft.Office.Interop.Outlook
$outlook = New-Object -ComObject Outlook.Application
$mail = $outlook.CreateItem(0)

# Set recipients
$mail.To = @"
{to}
"@

# Set CC if provided
{cc_line}

# Set BCC if provided
{bcc_line}

# Set subject and body
$mail.Subject = @"
{subject}
"@
$mail.Body = @"
{body}
"@

# Set sender
try {{
    $mail.SentOnBehalfOfName = "BusinessIntelligence@bcsbmail.com"
}} catch {{
    # Ignore if can't set sender
}}

# Add attachments
{attachments}

# Display the email (change to .Send() to send immediately)
$mail.Display()
    '''.format(
        to=';'.join(recipients),
        cc_line=f'$mail.CC = "{";".join(cc_recipients)}"' if cc_recipients else '# No CC recipients',
        bcc_line=f'$mail.BCC = "{";".join(bcc_recipients)}"' if bcc_recipients else '# No BCC recipients',
        subject=subject.replace('"', '""'),
        body=body.replace('"', '""'),
        attachments='\n'.join([f'$mail.Attachments.Add("{path}")' for path in attachment_paths])
    )
    
    # Save script to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ps1', delete=False, encoding='utf-8') as f:
        f.write(ps_script)
        script_path = f.name
    
    try:
        # Execute PowerShell script
        result = subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode == 0:
            print("Email prepared successfully in Outlook!")
        else:
            print(f"PowerShell error: {result.stderr}")
            
    finally:
        # Clean up temporary file
        try:
            os.unlink(script_path)
        except:
            pass


def _send_macos_outlook(recipients, cc_recipients, bcc_recipients, subject, body, attachment_paths):
    """Send email using AppleScript on macOS."""
    # Escape special characters for AppleScript
    def escape_applescript(text):
        return text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
    
    # Build the AppleScript
    script_lines = [
        'tell application "Microsoft Outlook"',
        f'    set newMessage to make new outgoing message with properties {{subject:"{escape_applescript(subject)}", content:"{escape_applescript(body)}"}}'
    ]
    
    # Add recipients
    script_lines.append('    tell newMessage')
    
    for recipient in recipients:
        script_lines.append(f'        make new to recipient with properties {{email address:{{address:"{recipient}"}}}}')
    
    for recipient in cc_recipients:
        script_lines.append(f'        make new cc recipient with properties {{email address:{{address:"{recipient}"}}}}')
    
    for recipient in bcc_recipients:
        script_lines.append(f'        make new bcc recipient with properties {{email address:{{address:"{recipient}"}}}}')
    
    # Add attachments
    for path in attachment_paths:
        script_lines.append(f'        make new attachment with properties {{file:POSIX file "{path}"}}')
    
    # Open the message window
    script_lines.extend([
        '        open',
        '    end tell',
        'end tell'
    ])
    
    applescript = '\n'.join(script_lines)
    
    # Execute AppleScript
    result = subprocess.run(
        ["osascript", "-e", applescript],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("Email prepared successfully in Outlook!")
    else:
        print(f"AppleScript error: {result.stderr}")


def _send_mailto(recipients, cc_recipients, bcc_recipients, subject, body):
    """Fallback method using mailto: URL."""
    import urllib.parse
    
    # Build mailto URL
    mailto = "mailto:" + ";".join(recipients) if recipients else "mailto:"
    
    params = []
    if cc_recipients:
        params.append(f"cc={';'.join(cc_recipients)}")
    if bcc_recipients:
        params.append(f"bcc={';'.join(bcc_recipients)}")
    if subject:
        params.append(f"subject={urllib.parse.quote(subject)}")
    if body:
        # Limit body length for URL
        truncated_body = body[:500] + "..." if len(body) > 500 else body
        params.append(f"body={urllib.parse.quote(truncated_body)}")
    
    if params:
        mailto += "?" + "&".join(params)
    
    # Open default email client
    system = platform.system()
    if system == "Windows":
        os.startfile(mailto)
    elif system == "Darwin":
        subprocess.run(["open", mailto])
    else:
        subprocess.run(["xdg-open", mailto])


# Backward compatibility wrapper
def email_out_legacy(recipients: List, bcc_recipients: List, subject: str, body: str, attachment_paths: List[Path]) -> None:
    """Legacy function signature for backward compatibility."""
    email_out(
        recipients=recipients,
        bcc_recipients=bcc_recipients,
        subject=subject,
        body=body,
        attachment_paths=attachment_paths
    )