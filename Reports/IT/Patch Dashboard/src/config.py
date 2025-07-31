"""
Patch Dashboard Project Configuration

- REPORT_NAME: Patch Dashboard
- BUSINESS_LINE: IT
- SCHEDULE: Monthly
- OWNER: IT Department
- DESCRIPTION: Cleans and aggregates raw patch data from ManageEngine for PowerBI dashboarding.

Edit paths and settings as needed for your environment.
"""
from pathlib import Path

# Project metadata
REPORT_NAME = "Patch Dashboard"
BUSINESS_LINE = "IT"
SCHEDULE = "Monthly"
OWNER = "IT Department"
PROD_READY = False

# Input/output directories
PROJECT_ROOT = Path(__file__).parent.parent
INPUT_DIR = PROJECT_ROOT / "data"  # Place raw ManageEngine exports here
OUTPUT_DIR = PROJECT_ROOT / "outputs"

# Example: Add any other config variables needed for your ETL/cleaning
# e.g. COLUMN_MAP = {...}
