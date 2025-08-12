"""
Classifieds Report - Resolution Committee Package

Analyzes classified loan accounts (risk ratings 4 and 5) and tracks 
loan classification changes to maintain regulatory compliance and
support Resolution Committee decision-making.

Input Files: None
Output Files: YYYY-MM-DD_classifieds_report.xlsx
Tables: COCCDM.WH_ACCTCOMMON, COCCDM.WH_ACCTLOAN, COCCDM.WH_LOANS, COCCDM.WH_ACCT, OSIBANK.WH_ORG, OSIBANK.WH_PERS, OSIBANK.WH_PROP2
"""

import os
from pathlib import Path

# Report Info
REPORT_NAME = "Resolution Committee Classifieds Report"
BUSINESS_LINE = "Commercial Lending"
SCHEDULE = "Monthly"
OWNER = "Loan Review Team"

# Status
PROD_READY = True

# Environment & Paths
ENV = os.getenv('REPORT_ENV', 'dev')
BASE_PATH = Path(r"\\00-DA1\Home\Share\Data & Analytics Initiatives\Project Management\Credit_Loan_Review\Resolution Committee Automation\Classifieds\Production") if ENV == 'prod' else Path(__file__).parent.parent
OUTPUT_DIR = BASE_PATH / "output"
INPUT_DIR = BASE_PATH / "input"

# Email Recipients
EMAIL_TO = [] if ENV == 'prod' else []
EMAIL_CC = ["businessintelligence@bcsbmail.com"] if ENV == 'prod' else []

# Creates directories