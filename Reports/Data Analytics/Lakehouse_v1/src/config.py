"""
Project Configuration Template

This file provides a template for configuring a new report or data pipeline project.
Fill in the placeholders below with your project's specific details.

Input Files: <describe input files or data sources>
Output Files: <describe output files or datasets>
Tables: <list relevant database tables or data sources>
"""

import os
from pathlib import Path

# Report Info
REPORT_NAME = "Lakehouse Transformation"
BUSINESS_LINE = "Data Engineering Team"
SCHEDULE = "Daily"
OWNER = "Chad Doorley"

# Status
PROD_READY = False

# Environment & Paths
ENV = os.getenv('REPORT_ENV', 'dev')
BASE_PATH = Path(r"\\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Data_Analytics\lakehouse") if ENV == 'prod' else Path(__file__).parent.parent
ACCOUNT_TABLE = BASE_PATH / "account"

# Email Recipients
EMAIL_TO = []  # List of primary recipients for production
EMAIL_CC = []  # List of CC recipients for production

# Add any additional configuration variables below as needed
