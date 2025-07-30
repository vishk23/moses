"""
Dealer Reserve Recon Project Configuration

Edit this file to set project-specific details and paths.
"""

import os
from pathlib import Path

# Report Info
REPORT_NAME = "Dealer Reserve Recon"
BUSINESS_LINE = "Indirect Lending"
SCHEDULE = "Daily"
OWNER = "<Project Owner or Team>"

# Status
PROD_READY = True

# Environment & Paths
ENV = os.getenv('REPORT_ENV', 'dev')
BASE_PATH = Path(r"\\00-DA1\Home\Share\Line of Business_Shared Services\Indirect Lending\Dealer Reserve Recon\Production") if ENV == 'prod' else Path(__file__).parent.parent
OUTPUT_DIR = BASE_PATH / "output"
INPUT_DIR = BASE_PATH / "input"
ASSETS_DIR = BASE_PATH / "assets"

# Email Recipients
EMAIL_TO = []  # List of primary recipients for production
EMAIL_CC = []  # List of CC recipients for production
