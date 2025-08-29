"""
New Loan Report LR Credit Configuration

Input Files: Database queries from COCC warehouse tables
Output Files: Excel report with NEW LOAN and CRA sheets
Tables: wh_acctcommon, wh_loans, wh_acctloan, wh_org, wh_prop, wh_prop2, househldacct
"""

import os
from pathlib import Path

# Report Info
REPORT_NAME = "New Loan Report LR Credit"
BUSINESS_LINE = "Credit Loan Review"
SCHEDULE = "Weekly"
OWNER = "Chad Doorley"

# Status
PROD_READY = False

# Environment & Paths
ENV = os.getenv('REPORT_ENV', 'dev')
BASE_PATH = Path(r"\\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Credit_Loan_Review\NewLoanReport_LR_Credit\Production") if ENV == 'prod' else Path(__file__).parent.parent
OUTPUT_DIR = BASE_PATH / "output"
INPUT_DIR = BASE_PATH / "input"

# Email Recipients
EMAIL_TO = [
    "paul.kocak@bcsbmail.com",
    "linda.clark@bcsbmail.com"
] if ENV == 'prod' else []
EMAIL_CC = [
    "chad.doorley@bcsbmail.com"
]

# SQLite database path for pkey lookup
PKEY_DB_PATH = Path(r"\\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Data_Analytics\R360\Production\assets")
