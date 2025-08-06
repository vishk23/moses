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
OWNER = "Patrick Quinn"

# Status
PROD_READY = True

# Environment & Paths
ENV = os.getenv('REPORT_ENV', 'dev')
BASE_PATH = Path(r"\\00-da1\Home\Share\Line of Business_Shared Services\Risk Management\Daily Mismatched Debit Card Txns") if ENV == 'prod' else Path(__file__).parent.parent
INPUT_PATH = r"\\00-da1\\Home\\Share\\Line of Business_Shared Services\\Finance\\Accounting Daily\\245143 ATM Settlement Recon\\Input"
INPUT_FILE_PATH = INPUT_PATH + r"\\CO_VSUS FISERV SUSPECT REPORT FOR BALANCING_SETTLEMEN.txt"
OUTPUT_DIR = BASE_PATH / "output"

# Email Recipients
EMAIL_TO = [] if ENV == 'prod' else []
EMAIL_CC = ["businessintelligence@bcsbmail.com"] if ENV == 'prod' else []

# Creates directories