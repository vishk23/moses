"""
R360 Configuration

The R360 (Relationship 360) system creates centralized customer keys for better 
understanding of customer relationships across the Bank. Generates three key types:
- Portfolio Key: Groups by address OR ownership (comprehensive relationships)
- Address Key: Groups by address only (households)  
- Ownership Key: Groups by ownership only (business relationships)

Input Files: None (database queries)
Output Files: r360_portfolio_YYYYMMDD.csv, r360_address_YYYYMMDD.csv, r360_ownership_YYYYMMDD.csv
Database Storage: current.db, address.db, ownership.db (SQLite)
Tables: OSIBANK.WH_ACCTCOMMON, PERSADDRUSE, ORGADDRUSE, WH_ADDR, WH_ALLROLES

"""

import os
from pathlib import Path

# Report Info
REPORT_NAME = "R360 Customer Relationship Keys"
BUSINESS_LINE = "Cross-Functional (All Business Lines)"
SCHEDULE = "Daily"
OWNER = "Data Analytics Team"

# Status
PROD_READY = True

# Environment & Paths
ENV = os.environ.get('REPORT_ENV') or 'dev'
BASE_PATH = Path(r"\\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Data_Analytics\R360\Production") if ENV == 'prod' else Path(__file__).parent.parent
OUTPUT_DIR = BASE_PATH / "output"
INPUT_DIR = BASE_PATH / "input"

# No email distribution - this is a data pipeline that feeds other systems
EMAIL_TO = []
EMAIL_CC = []

# Creates directories
OUTPUT_DIR.mkdir(exist_ok=True)
INPUT_DIR.mkdir(exist_ok=True)

# Database paths for SQLite files
DB_DIR = BASE_PATH if ENV == 'prod' else Path(__file__).parent.parent / "assets"
DB_DIR.mkdir(exist_ok=True)

# Business Rules Configuration

# IOLTA addresses to exclude from address grouping
EXCLUDED_ADDRESSES = [
    '-grcQPptQrw=',  # IOLTA address hash
    'ShNDlbk0gXo=',  # IOLTA address hash
    'uA9lf4xIAz8='   # 29 Broadway hash (problematic shared address)
]

# IOLTA CIF numbers to exclude from ownership grouping
EXCLUDED_CIFS = [
    'O500',  # RI BAR IOLTA
    'O501',  # MA IOLTA Committee
    'nan'    # No roles
]

# Account role codes that define ownership relationships
OWNERSHIP_ROLE_CODES = [
    'OWN',        # Owner
    'GUAR',       # Guarantor
    'LNCO',       # Loan Co-signer
    'Tax Owner'   # Tax Owner
]

# Address use codes for primary addresses
PRIMARY_ADDRESS_CODES = ['PRI']  # Primary address use code

# R360 Processing Configuration

# Track which keys to generate (can comment out specific ones)
KEYS_TO_GENERATE = {
    'portfolio': True,    # Comprehensive relationships (address OR ownership)
    'address': False,     # Household relationships (address only)  
    'ownership': False,   # Business relationships (ownership only)
}

# Historical database configuration for key persistence
# Set to True to use historical data, False to generate fresh keys, None to skip entirely
# You can modify these settings regardless of environment for testing different scenarios
HISTORICAL_DB_CONFIG = {
    'portfolio': True,    # Default: Generate fresh keys in dev, change to True to use historical
    'address': False,      # Default: Generate fresh keys in dev, change to True to use historical
    'ownership': False,    # Default: Generate fresh keys in dev, change to True to use historical
}

# Override historical config for production (can be customized as needed)
if ENV == 'prod':
    HISTORICAL_DB_CONFIG = {
        'portfolio': True,     # Production: Use historical for key persistence
        'address': False,       # Production: Use historical for key persistence  
        'ownership': False,     # Production: Use historical for key persistence
    }

# Environment-aware database configuration
if ENV == 'dev':
    # Safe dev testing mode - skip database operations to avoid conflicts
    DATABASE_MODE = 'local'
    SAVE_TO_DATABASE = False  # Override: Skip database writes in dev
else:
    # Production mode - full database operations
    DATABASE_MODE = 'production'
    SAVE_TO_DATABASE = True

def print_environment_info():
    """Print environment configuration info - call when needed."""
    if ENV == 'dev':
        print(f"DEV MODE: Database operations disabled for safe testing")
        print(f"DEV MODE: CSV outputs will go to local directory: {OUTPUT_DIR}")
        print(f"DEV MODE: Historical database config: {HISTORICAL_DB_CONFIG}")
    else:
        print(f"PROD MODE: Full database operations enabled")
        print(f"PROD MODE: CSV outputs will go to network directory: {OUTPUT_DIR}")
        print(f"PROD MODE: Historical database config: {HISTORICAL_DB_CONFIG}")

# Only print during actual execution, not during discovery
if __name__ == "__main__":
    print_environment_info()

# Configuration for output and database operations
OUTPUT_CONFIG = {
    'save_to_csv': True,               # Save CSV files to output directory
    'save_to_database': SAVE_TO_DATABASE,  # Environment-aware database saving
    'print_stats': True,               # Print statistics about generated keys
}

# Dev mode warnings and safety checks
if ENV == 'dev':
    DEV_WARNINGS = [
        "DEV MODE ACTIVE - Database writes disabled",
        "CSV files will be saved locally only", 
        f"Historical database settings: {HISTORICAL_DB_CONFIG}",
        "Modify HISTORICAL_DB_CONFIG in config.py to test with historical data",
        "Use REPORT_ENV=prod for production database operations"
    ]
else:
    DEV_WARNINGS = []

# Historical database behavior explanation
HISTORICAL_DB_HELP = {
    True: "Use historical database for key persistence (maintains existing relationships)",
    False: "Generate fresh keys without historical data (relationships may change)", 
    None: "Skip historical database operations entirely (safe for dev testing)"
}