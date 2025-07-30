"""
Provides Commercial Lending Officer (CLO) active portfolio analysis organized 
by responsibility officer with subtotals and detailed loan information.

Input Files: None (database query)
Output Files: CLO Active Portfolio [Month Day Year].xlsx
Tables: WH_ACCTCOMMON, WH_LOANS, WH_ACCTLOAN, 
        HOUSEHLDACCT, WH_ACCTUSERFIELDS, portfoliokey
"""

import os
from pathlib import Path

# Report Info
REPORT_NAME = "CLO_ActivePortfolio_Officer_Report"
BUSINESS_LINE = "Commercial Lending"
SCHEDULE = "Manual"
OWNER = "Commercial Lending Team"

# Status
PROD_READY = True

# Environment & Paths
ENV = os.getenv('REPORT_ENV', 'dev')
BASE_PATH = Path(r"\\00-DA1\Home\Share\Data & Analytics Initiatives\Project Management\Commercial_Lending\CLO_ActivePortfolio_Officer_Report\Production") if ENV == 'prod' else Path(__file__).parent.parent
OUTPUT_DIR = BASE_PATH / "output"
INPUT_DIR = BASE_PATH / "input"

# Email Recipients
EMAIL_TO = [] if ENV == 'prod' else []
EMAIL_CC = ["chad.doorley@bcsbmail.com", "businessintelligence@bcsbmail.com"] if ENV == 'prod' else []

# Creates directories