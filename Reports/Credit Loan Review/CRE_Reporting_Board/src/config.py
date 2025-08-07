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

# I-CRE Analysis Years
ICRE_ANALYSIS_YEARS = [2024, 2023, 2022]

# FDIC Call Code grouping configuration
FDIC_CALL_CODE_GROUPS = {
    '1-4 Fam Construction': ['CNFM'],
    'Construction': ['OTCN','LAND','LNDV','RECN'],
    '1-4 Family': ['REFI','REOE','REJU'],
    'OwnerOcc': ['REOW'],
    'I-CRE': ['RENO','REMU'],
    'C&I': ['CIUS'],
    'Other': ['OTAL','AGPR','REFM','LENO']
}

# Property type grouping configuration
PROPERTY_TYPE_GROUPS = {
    'Autobody/Gas Station': ['Autobody/Gas Station','Gas Station and Convenience St','Auto-Truck Repair'],
    'Other': ['Other','Commercial - Other'],
    'Retail': ['Retail - Big Box Store','Shopping Plaza','Strip Plaza','Dry Cleaner/Laundromat','General Retail'],
    'Hospitality': ['Hotel/Motel','Hospitality/Event Space'],
    'Recreation': ['Outdoor Recreation','Indoor Recreational'],
    'Industrial': ['Manufacturing','Warehouse'],
    'Land': ['Land - Unimproved','Land - Improved'],
    'Mixed Use': ['Mixed Use (Retail/Office)','Mixed Use (Retail/Residential)','Mixed Use (Office/Residential)'],
    'Multi Family': ['Apartment Building'],
    'General Office': ['Office - Professional','Office- General'],
    'Medical Office': ['Office - Medical'],
    'Restaurant': ['Restaurant']
}
