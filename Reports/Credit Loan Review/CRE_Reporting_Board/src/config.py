"""
CRE Reporting Board Configuration

This project generates the CRE (Commercial Real Estate) loader data for board reporting.
It fetches loan portfolio data from COCC data mart and performs transformations 
to create consolidated reporting output.

Input Files: COCC Data Mart queries (wh_acctcommon, wh_loans, wh_acctloan, wh_acct, wh_prop, wh_prop2)
Output Files: cre_loader.xlsx - Consolidated CRE portfolio data with property information
Tables: COCCDM.WH_* tables, OSIBANK.WH_PROP* tables
"""

import os
from pathlib import Path

# Report Info
REPORT_NAME = "CRE Reporting Board"
BUSINESS_LINE = "Credit Loan Review"
SCHEDULE = "Monthly"
OWNER = "Linda Sternfelt"

# Status
PROD_READY = True

# Environment & Paths
ENV = os.getenv('REPORT_ENV', 'dev')
BASE_PATH = Path(r"\\") if ENV == 'prod' else Path(__file__).parent.parent
OUTPUT_DIR = BASE_PATH / "output"
INPUT_DIR = BASE_PATH / "input"

# Email Recipients
EMAIL_TO = [""]  # Primary recipient for production
EMAIL_CC = []  # List of CC recipients for production

# Database configuration
USE_CACHING = ENV == 'dev'  # Enable caching for development
CACHE_DIR = Path(__file__).parent.parent / "cache" if USE_CACHING else None

# Output file configuration
OUTPUT_FILENAME = "cre_loader.xlsx"
