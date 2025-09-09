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
REPORT_NAME = "SBA Loans"
BUSINESS_LINE = "Credit/Loan Review - SBLC"
SCHEDULE = "Monthly"
OWNER = "Joan Medeiros"

# Status
PROD_READY = True 

# Environment & Paths
ENV = os.getenv('REPORT_ENV', 'dev')
BASE_PATH = Path(r"\\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Credit_Loan_Review\SBA_Loans") if ENV == 'prod' else Path(__file__).parent.parent
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
