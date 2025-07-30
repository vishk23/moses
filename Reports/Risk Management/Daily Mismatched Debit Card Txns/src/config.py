"""
This generates daily posting sheets by parsing txt 
files that are dropped in the input folder.

Input Files: .txt file in input directory
Output Files: Daily Posting Sheet [MM.DD.YY].xlsx
Tables: WH_ACCTCOMMON, WH_TOTALPAYMENTSDUE, WH_ACCTLOAN
"""

import os
from pathlib import Path

# Report Info
REPORT_NAME = "Daily Mismatched Debit Card Txns"
BUSINESS_LINE = "Risk Management"
SCHEDULE = "Daily"
OWNER = "Risk Management Team"

# Status
PROD_READY = True

# Environment & Paths
ENV = os.getenv('REPORT_ENV', 'dev')
BASE_PATH = Path(r"\\00-da1\Home\Share\Line of Business_Shared Services\Risk Management\Daily Mismatched Debit Card Txns") if ENV == 'prod' else Path(__file__).parent.parent
OUTPUT_DIR = BASE_PATH / "output"

# Email Recipients
EMAIL_TO = [] if ENV == 'prod' else []
EMAIL_CC = ["businessintelligence@bcsbmail.com"] if ENV == 'prod' else []

# Creates directories