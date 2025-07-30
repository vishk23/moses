"""
Implements a logistic regrsesion pipeline to predict loan 
charge-offs based on borrower and loan characteristics.

Input Files: None (database query)
Output Files: CLO Active Portfolio [Month Day Year].xlsx
Tables: WH_ACCTCOMMON, WH_LOANS, WH_ACCTLOAN, HOUSEHLDACCT, WH_PERS,
        ACCTSTATISTICHIST, cdutils portfolio key pipeline
"""

import os
from pathlib import Path

# Report Info
REPORT_NAME = "ChargeOffModel"
BUSINESS_LINE = "Data Analytics"
SCHEDULE = "Quarterly"
OWNER = "Chad Doorley"

# Status
PROD_READY = True

# Environment & Paths
ENV = os.getenv('REPORT_ENV', 'dev')
BASE_PATH = Path(r"\\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Data_Analytics\ChargeOffModel\Production") if ENV == 'prod' else Path(__file__).parent.parent
OUTPUT_DIR = BASE_PATH / "output"

# Email Recipients
EMAIL_TO = [] if ENV == 'prod' else []
EMAIL_CC = ["chad.doorley@bcsbmail.com", "businessintelligence@bcsbmail.com"] if ENV == 'prod' else []

# Creates directories