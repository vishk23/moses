"""
Provides Commercial Lending Officer (CLO) active portfolio analysis organized 
by responsibility officer with subtotals and detailed loan information.
Includes risk ratings, SBA guarantees, and comprehensive Excel formatting.

Input Files: None (database query)
Output Files: CLO Active Portfolio [Month Day Year].xlsx
Tables: Active commercial loan portfolio, household accounts, user fields
"""

import os
from pathlib import Path

# Report Info
REPORT_NAME = "CLO Active Portfolio Officer Report"
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
