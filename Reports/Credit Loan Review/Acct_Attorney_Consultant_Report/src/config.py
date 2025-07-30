"""
Provides information of all extensions of credit to 
accountants, lawyers, consultants, appraisers, or similar 
individuals who have provided professional services to 
the institution since the last FDIC examination.

Input Files: None (database query)
Output Files: Acct_Attorney_Consultant [Month Day Year].xlsx
Tables: WH_ACCTCOMMON, WH_LOANS, WH_ACCTLOAN, HOUSEHLDACCT, 
        WH_PERS, WH_PERSUSERFIELDS, WH_ALLROLES, WH_PERS, portfoliokey
"""

import os
from pathlib import Path

# Report Info
REPORT_NAME = "Acct_Attorney_Consultant_Report"
BUSINESS_LINE = "Credit Loan Review"
SCHEDULE = "Manual"
OWNER = "Paul Kocak"

# Status
PROD_READY = True

# Environment & Paths
ENV = os.getenv('REPORT_ENV', 'dev')
BASE_PATH = Path(r"\\00-DA1\Home\Share\Data & Analytics Initiatives\Project Management\Credit_Loan_Review\Acct_Attorney_Consultant_Report\Production") if ENV == 'prod' else Path(__file__).parent.parent
OUTPUT_DIR = BASE_PATH / "output"

# Email Recipients
EMAIL_TO = [
    "paul.kocak@bcsbmail.com"
] if ENV == 'prod' else []
EMAIL_CC = ["chad.doorley@bcsbmail.com", "businessintelligence@bcsbmail.com"] if ENV == 'prod' else []

# Creates directories
