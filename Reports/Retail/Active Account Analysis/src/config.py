"""
Provides Active Account & Agreement Analysis for Retail Department cross-sell analysis.
Combines active accounts with agreements from WH_AGREEMENTS using WH_ALLROLES linkage.
Produces monthly datasets for retail interns to analyze cross-sell opportunities.

Input Files: None (database queries)
Output Files: Active Accounts and Agreements datasets
Tables: daily_acct_file, WH_AGREEMENTS, WH_ALLROLES, WH_ORG, WH_PERS
"""

import os
from pathlib import Path

# Report Info
REPORT_NAME = "Active Account Analysis"
BUSINESS_LINE = "Retail Banking"
SCHEDULE = "Monthly"
OWNER = "Stephanie Nordberg"

# Status
PROD_READY = True 

# Environment & Paths
ENV = os.getenv('REPORT_ENV', 'dev')
PROD_OUTPUT_PATH = Path(r"\\00-da1\Home\Share\Line of Business_Shared Services\Retail Banking\Active_Account_Agreement_Analysis")
BASE_PATH = PROD_OUTPUT_PATH if ENV == 'prod' else Path(__file__).parent.parent
OUTPUT_DIR = BASE_PATH / "output"
INPUT_DIR = BASE_PATH / "input"

# Email Recipients
EMAIL_TO = [] if ENV == 'prod' else []
EMAIL_CC = ["chad.doorley@bcsbmail.com", "businessintelligence@bcsbmail.com"] if ENV == 'prod' else []

