"""
Rate Scraping Report - Automated daily collection of interest rates from multiple external 
sources (FRED, CME, FHLB) for treasury management and loan pricing decisions.

Input Files: None (external API/web scraping)
Output Files: Rate_Report_MMM_DD_YY_HHMM.xlsx and .pdf
Tables: None
"""

import os
from pathlib import Path

# Report Info
REPORT_NAME = "Rate Scraping Report"
BUSINESS_LINE = "Operations"
SCHEDULE = "Daily"
OWNER = "Operations Team"

# Status
PROD_READY = True

# Environment & Paths
ENV = os.getenv('REPORT_ENV', 'dev')
BASE_PATH = Path(__file__).parent.parent
OUTPUT_DIR = BASE_PATH / "output"


# Email Recipients
EMAIL_TO = [
    "Kelly.Abernathy@bcsbmail.com",
    "Taylor.Willbanks@bcsbmail.com",
    "Josephine.Willard@bcsbmail.com",
    "Patty.DeSimone@bcsbmail.com",
    "Zachary.Cabral@bcsbmail.com",
    "Tanner.Vickery@bcsbmail.com"
] if ENV == 'prod' else []
EMAIL_CC = ["businessintelligence@bcsbmail.com"] if ENV == 'prod' else []

#Public API key for FRED
API_KEY  = "ac15589a824557b5b4d2260b45438215"