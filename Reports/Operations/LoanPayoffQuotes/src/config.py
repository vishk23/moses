"""
Take a prebuilt report and build a robust dashboard to share 
with executive management that breaks down loan payoff 
amounts & charges by major and minor.

Input Files: None (database query)
Output Files: CLO Active Portfolio [Month Day Year].xlsx
Tables: WH_ACCTCOMMON, portfoliokey pipeline
"""

import os
from pathlib import Path

# Report Info
REPORT_NAME = "LoanPayoffQuotes"
BUSINESS_LINE = "Operations"
SCHEDULE = "Monthly"
OWNER = "Kelly Abernathy"

# Status
PROD_READY = True

# Environment & Paths
ENV = os.getenv('REPORT_ENV', 'dev')
BASE_PATH = Path(r"\\00-DA1\Home\Share\Data & Analytics Initiatives\Project Management\Operations\LoanPayoffQuotes\Production") if ENV == 'prod' else Path(__file__).parent.parent
OUTPUT_DIR = BASE_PATH / "output"

# Email Recipients
EMAIL_TO = [] if ENV == 'prod' else []
EMAIL_CC = ["chad.doorley@bcsbmail.com", "businessintelligence@bcsbmail.com"] if ENV == 'prod' else []

# Creates directories