"""
Provides information about the deposits and loans 
relevant to Nancy Cabral, David Ferreira, and George Mendros.

Input Files: None (database query)
Output Files: Portfolio_Report [Month Day Year].xlsx
Tables: WH_ACCTCOMMON, WH_ACCTLOAN, WH_PROP, WH_PROP2, WH_LOANS, WH_ACCTROLE
"""

import os
from pathlib import Path

# Report Info
REPORT_NAME = "SBRM_Portfolio"
BUSINESS_LINE = "Credit Loan Review"
SCHEDULE = "Manual"
OWNER = "Francine Ferguson"

# Status
PROD_READY = True

# Environment & Paths
ENV = os.getenv('REPORT_ENV', 'dev')
BASE_PATH = Path(r"\\00-DA1\Home\Share\Data & Analytics Initiatives\Project Management\Credit_Loan_Review\SBRM_Portfolio\Production") if ENV == 'prod' else Path(__file__).parent.parent
OUTPUT_DIR = BASE_PATH / "output"

# Email Recipients
EMAIL_TO = [
    "Nancy.Cabral@bcsbmail.com",
    "george.mendros@bcsbmail.com",
    "David.Ferreira@bcsbmail.com"
] if ENV == 'prod' else []
EMAIL_CC = ["chad.doorley@bcsbmail.com", "businessintelligence@bcsbmail.com"] if ENV == 'prod' else []

# Creates directories
