"""
Looks at Muni Statement pdfs and adds a larger margin to all pdfs
in the given directory

Input Files: pdfs in \\00-da1\Home\Share\Line of Business_Shared Services\Government Banking\Muni Statements\Production\Output\2025 - July
Output Files: \\00-da1\Home\Share\Line of Business_Shared Services\Government Banking\Muni Statements\Production\Output\2025 - July\Resized
Tables: None
"""

import os
from pathlib import Path
from datetime import date, timedelta

# Report Info
REPORT_NAME = "muni_pdf_resizer"
BUSINESS_LINE = "Government Banking"
SCHEDULE = "Monthly"
OWNER = "Government Banking team"

# Status
PROD_READY = True

# Environment & Paths
ENV = os.getenv('REPORT_ENV', 'dev')
BASE_PATH = Path(r"\\00-da1\Home\Share\Line of Business_Shared Services\Government Banking\Muni Statements\Production\Output") if ENV == 'prod' else Path(__file__).parent.parent

last_month = date.today().replace(day=1) - timedelta(1)             

INPUT_DIR = BASE_PATH / last_month.strftime("%Y - %B")
OUTPUT_DIR = INPUT_DIR / "resized"

# Email Recipients
EMAIL_TO = [] if ENV == 'prod' else []
EMAIL_CC = ["chad.doorley@bcsbmail.com", "businessintelligence@bcsbmail.com"] if ENV == 'prod' else []

# Creates directories