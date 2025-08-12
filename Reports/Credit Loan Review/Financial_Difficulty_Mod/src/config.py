"""
Financial Difficulty Modifications Report - Resolution Committee Package

Tracks financial difficulty modifications (TDR - Troubled Debt Restructuring)
for loan accounts, supporting the Resolution Committee's decision-making 
process and regulatory compliance requirements.

Input Files: None
Output Files: YYYY-MM-DD_FDM_report.xlsx
Tables: COCCDM.WH_ACCTCOMMON, COCCDM.WH_ACCTLOAN, OSIBANK.WH_ACCTUSERFIELDS
"""

import os
from pathlib import Path

# Report Info
REPORT_NAME = "Resolution Committee Financial Difficulty Modifications Report"
BUSINESS_LINE = "Commercial Lending"
SCHEDULE = "Monthly"
OWNER = "Loan Review Team"

# Status
PROD_READY = True

# Environment & Paths
ENV = os.getenv('REPORT_ENV', 'dev')
BASE_PATH = Path(r"\\00-DA1\Home\Share\Data & Analytics Initiatives\Project Management\Credit_Loan_Review\Resolution Committee Automation\Financial Difficulty Modifications\Production") if ENV == 'prod' else Path(__file__).parent.parent
OUTPUT_DIR = BASE_PATH / "output"


# Email Recipients
EMAIL_TO = [] if ENV == 'prod' else []
EMAIL_CC = ["businessintelligence@bcsbmail.com"] if ENV == 'prod' else []

# Creates directories