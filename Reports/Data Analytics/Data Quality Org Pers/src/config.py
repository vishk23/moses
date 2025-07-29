"""
Data Quality ETL Pipeline - Organization & Person Data Consolidation

A comprehensive ETL pipeline for cleaning and consolidating customer data from 
WH_PERS (person) and WH_ORG (organization) tables, generating unified snapshots 
of customer records linked to active accounts.

Input Files: Excel files in data/inputs/org/ and data/inputs/pers/ (optional)
Output Files: org_final_[timestamp].xlsx, pers_final_[timestamp].xlsx
Tables: WH_ORG, WH_PERS, ORGADDRUSE, PERSADDRUSE, WH_ADDR, WH_ALLROLES
"""

import os
from pathlib import Path

# Report Info
REPORT_NAME = "Data Quality Org Pers"
BUSINESS_LINE = "Data Analytics"
SCHEDULE = "On-Demand"
OWNER = "Janet Silva"

# Status
PROD_READY = True

# Environment & Paths
ENV = os.getenv('REPORT_ENV', 'dev')

# Production path for automated refresh
PROD_OUTPUT_PATH = Path(r"\\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Data_Analytics\Data Quality\Data Quality\Automated Refresh")

# Base paths depending on environment
if ENV == 'prod':
    BASE_PATH = PROD_OUTPUT_PATH
    OUTPUT_DIR = PROD_OUTPUT_PATH
    INPUT_DIR = PROD_OUTPUT_PATH / "inputs"
    ARCHIVE_DIR = PROD_OUTPUT_PATH / "archive"
else:
    # Development mode - use local project structure
    BASE_PATH = Path(__file__).parent.parent
    OUTPUT_DIR = BASE_PATH / "outputs"
    INPUT_DIR = BASE_PATH / "data" / "inputs"
    ARCHIVE_DIR = BASE_PATH / "data" / "archive"

# Email Recipients
EMAIL_TO = ["janet.silva@bcsbmail.com"] if ENV == 'prod' else []
EMAIL_CC = ["chad.doorley@bcsbmail.com", "businessintelligence@bcsbmail.com"] if ENV == 'prod' else []
