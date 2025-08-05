"""
Loan Branch Officer Report - Configuration

This report provides loan portfolio information organized by branch and loan officer.

Input Files: None (database queries)
Output Files: loan_report_branch_officer.xlsx
Tables: OSIBANK.WH_ACCTCOMMON, OSIBANK.WH_LOANS, OSIBANK.WH_ACCTLOAN, OSIEXTN.HOUSEHLDACCT
"""

import os
from pathlib import Path

# Report Info
REPORT_NAME = "Loan Branch Officer Report"
BUSINESS_LINE = "Retail"
SCHEDULE = "Monthly"
OWNER = "Stephanie Nordberg"

# Status
PROD_READY = True

# Environment & Paths
ENV = os.getenv('REPORT_ENV', 'dev')
BASE_PATH = Path(r"\\00-da1\Home\Share\Line of Business_Shared Services\Retail Banking\EBL Loan Portfolio") if ENV == 'prod' else Path(__file__).parent.parent
OUTPUT_DIR = BASE_PATH / "Output"
INPUT_DIR = BASE_PATH / "input"

# Email Recipients
EMAIL_TO = []  # List of primary recipients for production
EMAIL_CC = ["businessintelligence@bcsbmail.com"]  # List of CC recipients for production

# Creates directories
OUTPUT_DIR.mkdir(exist_ok=True)
INPUT_DIR.mkdir(exist_ok=True)
