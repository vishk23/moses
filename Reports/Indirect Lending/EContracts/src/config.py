"""
Provides Indirect Lending with a summary of all EContracts.

Input Files: Daily funding reports and monthly Book to Looks
Output Files: E Contract Summary [Month Year].xlsx
"""

import os
from pathlib import Path

# Report Info
REPORT_NAME = "EContracts"
BUSINESS_LINE = "Indirect Lending"
SCHEDULE = "Monthly"
OWNER = "Marlene Braganca"

# Status
PROD_READY = True

# Environment & Paths
ENV = os.getenv('REPORT_ENV', 'dev')
BASE_PATH = Path(r"\\00-da1\Home\Share\Line of Business_Shared Services\Indirect Lending\E Contract Summary Report\Production") if ENV == 'prod' else Path(__file__).parent.parent
OUTPUT_DIR = BASE_PATH / "output"
INPUT_DIR = BASE_PATH / "input"

# Email Recipients
EMAIL_TO = [] if ENV == 'prod' else []
EMAIL_CC = ["chad.doorley@bcsbmail.com", "businessintelligence@bcsbmail.com"] if ENV == 'prod' else []

# Creates directories
