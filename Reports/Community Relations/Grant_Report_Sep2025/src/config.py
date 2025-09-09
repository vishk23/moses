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
REPORT_NAME = "Grant Request Report (Sep 2025)"
BUSINESS_LINE = "Community Relations"
SCHEDULE = "On-Demand"
OWNER = "Jeff Bradley"

# Status
PROD_READY = False

# Environment & Paths
ENV = os.getenv('REPORT_ENV', 'dev')
BASE_PATH = Path(r"\\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Community Relations\Grant Report Sep2025") if ENV == 'prod' else Path(__file__).parent.parent
OUTPUT_DIR = BASE_PATH / "output"
INPUT_DIR = BASE_PATH / "input"

# Lakehouse
LAKEHOUSE_PATH = Path(r"C:\Users\w322800\Documents\lakehouse") 

# Bronze
BRONZE = LAKEHOUSE_PATH / "bronze"

# Silver
SILVER = LAKEHOUSE_PATH / "silver"

# Gold
GOLD = BASE_PATH / "gold"

# Email Recipients
EMAIL_TO = [] if ENV == 'prod' else [] # List of primary recipients for production
EMAIL_CC = []  # List of CC recipients for production

# Add any additional configuration variables below as needed
