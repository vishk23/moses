"""
SWAP PNC Report Configuration

This file contains the configuration for the SWAP PNC Report,
a monthly report for the Credit Loan Review business line.

Report Owner: Business Intelligence
"""

import os
from pathlib import Path

# Hardcoded paths and report info for SWAP PNC workflow
REPORT_NAME = "SWAP PNC Report"
BUSINESS_LINE = "Credit Loan Review"
SCHEDULE = "Monthly"
OWNER = "Business Intelligence"

PROD_READY = True

# Environment & Paths
BASE_PATH = Path(__file__).parent.parent
ASSETS_FOLDER = BASE_PATH / "assets"
ARCHIVE_FOLDER = ASSETS_FOLDER / "archive"
STAGED_DATA_PATH = ASSETS_FOLDER / "staged_data" / "staged_data.csv"
OUTPUT_PATH = BASE_PATH / "output" / "swap_pnc_report.xlsx"

# Email Recipients
EMAIL_TO = ["Paul.Kocak@bcsbmail.com"]
EMAIL_BCC = ["chad.doorley@bcsbmail.com", "businessintelligence@bcsbmail.com"]

# Additional config variables as needed
