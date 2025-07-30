"""
Daily Deposit Update Project Configuration

Edit this file to set project-specific details and paths.
"""

import os
from pathlib import Path

# Report Info
REPORT_NAME = "Daily Deposit Update"
BUSINESS_LINE = "Data Analytics"
SCHEDULE = "Daily"
OWNER = "<Project Owner or Team>"

# Status
PROD_READY = True

# Environment & Paths
ENV = os.getenv('REPORT_ENV', 'dev')
BASE_PATH = Path(r"\\00-DA1\Home\Share\Line of Business_Shared Services\Commercial Lending\Deposits\DailyDeposit") if ENV == 'prod' else Path(__file__).parent.parent
STAGING_OUTPUT_DIR = BASE_PATH / "output"  # Staging output directory (can be changed)
OUTPUT_DIR = BASE_PATH / "output"           # Final output directory (can be changed)
INPUT_DIR = BASE_PATH / "input"

# Email Recipients
EMAIL_TO = []  # List of primary recipients for production
EMAIL_CC = []  # List of CC recipients for production
