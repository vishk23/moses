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
import os

# Project metadata
REPORT_NAME = "Patch Dashboard"
BUSINESS_LINE = "IT"
SCHEDULE = "Monthly"
OWNER = "IT Department"
PROD_READY = False

# Environment & Paths
ENV = os.getenv('REPORT_ENV', 'dev')
BASE_PATH = Path(r"\\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\IT\Patch Management") if ENV == 'prod' else Path(__file__).parent.parent
OUTPUT_DIR = BASE_PATH / "output"
INPUT_DIR = BASE_PATH / "input"

# Email Recipients
EMAIL_TO = []  # List of primary recipients for production
EMAIL_CC = []  # List of CC recipients for production

