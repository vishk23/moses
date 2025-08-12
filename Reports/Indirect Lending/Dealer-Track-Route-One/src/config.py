"""
Dealer Track - Route One Reconciliation Report - Reconciles data between Dealer Track and Route One systems,
ensuring data consistency and identifying discrepancies in indirect lending operations.

Input Files: dtevault.xlsx, funding.xlsx, routeonevault.xlsx (with month/year identifiers)
Output Files: [MonthYear] DL Reconciliation Report.xlsx
Tables: Dealer Track and Route One system data
"""

import os
from pathlib import Path

# Report Info
REPORT_NAME = "Dealer Track - Route One Reconciliation Report"
BUSINESS_LINE = "Indirect Lending"
SCHEDULE = "Monthly"
OWNER = "Indirect Lending Team"

# Status
PROD_READY = True

# Environment & Paths
ENV = os.getenv('REPORT_ENV', 'dev')
BASE_PATH = Path(r"\\00-DA1\Home\Share\Line of Business_Shared Services\Indirect Lending\DealerTrack-RouteOne Recon\Production") if ENV == 'prod' else Path(__file__).parent.parent
OUTPUT_DIR = BASE_PATH / "Output"
INPUT_DIR = BASE_PATH / "Input"

# Email Recipients
EMAIL_TO = [] if ENV == 'prod' else []
EMAIL_CC = [""] if ENV == 'prod' else []

# Creates directories