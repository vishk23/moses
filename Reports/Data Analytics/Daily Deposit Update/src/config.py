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
OWNER = "Chad Doorley"

# Status
PROD_READY = True

# Environment
ENV = os.getenv('REPORT_ENV', 'dev')

# Staging Output Directory (for intermediate/staging files)
STAGING_OUTPUT_DIR = Path(r"\\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Data_Analytics\Daily_Deposit_Update\Production\output") if ENV == 'prod' else Path(__file__).parent.parent / "output"

# Drop-in/Final Output Directory (for drop-in file to business)
OUTPUT_DIR = Path(r"\\00-DA1\Home\Share\Line of Business_Shared Services\Commercial Lending\Deposits\DailyDeposit") if ENV == 'prod' else Path(__file__).parent.parent / "output"

# Input Directory (if needed)
INPUT_DIR = Path(__file__).parent.parent / "input"

# Email Recipients
EMAIL_TO = []  # List of primary recipients for production
EMAIL_CC = []  # List of CC recipients for production
