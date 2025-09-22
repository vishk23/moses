"""
CT Dashboard Configuration

Input Files: HTML exports from covenant/tickler tracking system saved as .xls files in assets/ folder
Output Files: CT_Covenant_Tracking.xlsx and CT_Tickler_Tracking.xlsx in output/ folder  
Tables: OSIBANK.WH_ACCTCOMMON, WH_ALLROLES, WH_ORG, WH_PERS for officer assignments

Usage:
- Run from repo
- Drop files into input folder from Credit Track (3 saved reports)
- Run python -m src.main from root of project

Recipients:
- Commercial Portfolio Managers shared mailbox
- Laura Stack

CC:
- Laurie Williams
- Hasan Ali
- Linda Sternfelt
"""

import os
from pathlib import Path

# Report Info
REPORT_NAME = "CT Dashboard"
BUSINESS_LINE = "Commercial Lending"
SCHEDULE = "Monthly"
OWNER = "Laurie Williams"

# Status
PROD_READY = True

# Environment & Paths
ENV = os.getenv('REPORT_ENV', 'dev')
BASE_PATH = Path(r"\\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Commercial_Lending\CT_Dashboard\Production") if ENV == 'prod' else Path(__file__).parent.parent
OUTPUT_DIR = BASE_PATH / "output"
INPUT_DIR = BASE_PATH / "input"  # HTML files go in input folder

# Email Recipients
EMAIL_TO = ["laurie.williams@bcsbmail.com"]  # Primary recipients for production
EMAIL_CC = ["businessintelligence@bcsbmail.com"]  # CC recipients for production
