"""
Payroll and Vendor Report - Analyzes government banking payroll and vendor transactions, 
tracking check numbers and amounts over a 30-day period for reconciliation and monitoring.

Input Files: None
Output Files: payroll_report.txt, vendor_report.csv
Tables: COCCDM.WH_RTXN
"""

import os
from pathlib import Path

# Report Info
REPORT_NAME = "Payroll and Vendor Report"
BUSINESS_LINE = "Government Banking"
SCHEDULE = "As Needed"
OWNER = "Government Banking Team"

# Status
PROD_READY = True

# Environment & Paths
ENV = os.getenv('REPORT_ENV', 'dev')
BASE_PATH = Path(r"\\00-DA1\Home\Share\Line of Business_Shared Services\Government Banking\Municipal Banking Reports") if ENV == 'prod' else Path(__file__).parent.parent
OUTPUT_DIR = BASE_PATH  / "Output"


# Email Recipients
EMAIL_TO = [] if ENV == 'prod' else []
EMAIL_CC = ["businessintelligence@bcsbmail.com"] if ENV == 'prod' else []

# Creates directories