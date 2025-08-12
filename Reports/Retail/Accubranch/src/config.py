"""
Configuration file for Accubranch project.

This file contains all project-specific settings and should be the only place
for configuration and environment logic.
"""

import os
from pathlib import Path

# Project metadata
REPORT_NAME = "Accubranch Analysis"
BUSINESS_LINE = "Retail"
SCHEDULE = "On-demand"
OWNER = "Data Analytics Team"

# Environment configuration
ENVIRONMENT = os.getenv('REPORT_ENV', 'dev')

# Base paths
PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"
INPUT_DIR = PROJECT_ROOT / "input"

# Ensure output directory exists
OUTPUT_DIR.mkdir(exist_ok=True)

# File paths
ACCOUNT_OUTPUT_FILE = OUTPUT_DIR / "account_data.csv"
TRANSACTION_OUTPUT_FILE = OUTPUT_DIR / "transaction.csv"
FIVE_YR_HISTORY_FILE = OUTPUT_DIR / "five_yr_history.csv"

# Email configuration
if ENVIRONMENT == 'prod':
    EMAIL_RECIPIENTS = [
        # Add production email recipients here
    ]
else:
    EMAIL_RECIPIENTS = [
        # Add development email recipients here
    ]

# Date configurations for historical analysis
HISTORICAL_YEARS = [
    {'year': 2020, 'date': '2020-12-31'},
    {'year': 2021, 'date': '2021-12-31'},
    {'year': 2022, 'date': '2022-12-30'},
    {'year': 2023, 'date': '2023-12-29'},
    {'year': 2024, 'date': '2024-12-31'},
]

# Account filtering configuration
EXCLUDE_ORG_TYPES = ["MUNI", "TRST"]
EXCLUDE_ACCOUNT_TYPES = ["CI07"]  # ACH Manager products

# Account type mappings
ACCOUNT_TYPE_MAPPING = {
    'CML': 'Commercial Loan',
    'MLN': 'Commercial Loan',
    'CNS': 'Consumer Loan',
    'MTG': 'Residential Loan',
    'CK': 'Checking',
    'SAV': 'Savings',
    'TD': 'CD'
}

# Loan and deposit account types
LOAN_ACCOUNT_TYPES = ['CML', 'MLN', 'CNS', 'MTG']
DEPOSIT_ACCOUNT_TYPES = ['CK', 'SAV', 'TD']
ALL_TARGET_ACCOUNT_TYPES = LOAN_ACCOUNT_TYPES + DEPOSIT_ACCOUNT_TYPES

# Small business loan officers
SMALL_BUSINESS_OFFICERS = ['EBL PROGRAM ADMIN', 'SBLC LOAN OFFICER']
