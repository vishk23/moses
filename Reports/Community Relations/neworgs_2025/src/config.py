"""
Project Configuration Template

This file provides a template for configuring a new report or data pipeline project.
Fill in the placeholders below with your project's specific details.

Usage:
run from monorepo (here) through runner or cd to neworgs_2025/
python -m src.main
"""

import os
from pathlib import Path

# Report Info
REPORT_NAME = "New Orgs YTD (2025)"
BUSINESS_LINE = "Community Relations"
SCHEDULE = "Weekly (Monday)"
OWNER = "Jeff Bradley"

# Status
PROD_READY = True 

# Environment & Paths
ENV = os.getenv('REPORT_ENV', 'dev')
BASE_PATH = Path(r"<\\network\path\to\production\folder>") if ENV == 'prod' else Path(__file__).parent.parent
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
