"""
Prime Time Travel Customers Report

Analyzes Prime Time Travel customers by identifying customers with PTTM/PTTR/PRTD flags and calculating their deposit and loan balances.

Input Files: None (fetched from database)
Output Files: Prime Time Travel Customers [Month Day Year].xlsx
Tables: persuserfield, WH_ALLROLES, WH_PERS, portfoliokey
"""

import os
from pathlib import Path

# Report Info
REPORT_NAME = "Prime_Time_Travel_customers"
BUSINESS_LINE = "Retail"
SCHEDULE = "Monthly"
OWNER = "Stephanie Nordberg"

# Status
PROD_READY = True

# Environment & Paths
ENV = os.getenv('REPORT_ENV', 'dev')
if ENV == 'prod':
    BASE_PATH = Path(r'\\00-da1\Home\Share\Line of Business_Shared Services\Retail Banking\Prime_Time_Travel_customers\Production')
else:
    BASE_PATH = Path(__file__).parent.parent
OUTPUT_DIR = BASE_PATH / "output"

# Email Recipients
EMAIL_TO = [] if ENV == 'prod' else []
EMAIL_CC = ["businessintelligence@bcsbmail.com"] if ENV == 'prod' else []

# Creates directories