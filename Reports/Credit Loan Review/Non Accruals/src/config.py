"""
Non Accrual Report - Resolution Committee Package

Tracks all non-performing loans and reconciles month-over-month changes
for the Resolution Committee, increasing operational efficiency by
automating manual loan review tasks.

Input Files: None
Output Files: NonAccruals [Month Year].xlsx
Tables: WH_ACCTCOMMON, WH_TOTALPAYMENTSDUE, WH_ACCTLOAN
"""

import os
from pathlib import Path

# Report Info
REPORT_NAME = "Non Accruals"
BUSINESS_LINE = "Commercial Lending"
SCHEDULE = "Monthly"
OWNER = "Commercial Lending Team"

# Status
PROD_READY = True

# Environment & Paths
ENV = os.getenv('REPORT_ENV', 'dev')
BASE_PATH = Path(r"\\00-DA1\Home\Share\Data & Analytics Initiatives\Project Management\Credit_Loan_Review\Resolution Committee Automation\Non Accruals\Production") if ENV == 'prod' else Path(__file__).parent.parent
OUTPUT_DIR = BASE_PATH / "output"

# Email Recipients
EMAIL_TO = [] if ENV == 'prod' else []
EMAIL_CC = ["businessintelligence@bcsbmail.com"] if ENV == 'prod' else []

# Creates directories