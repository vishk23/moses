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
SCHEDULE = "Semi-Annual"
OWNER = "Linda Sternfelt"

# Status
PROD_READY = True

# Environment & Paths
ENV = os.getenv('REPORT_ENV', 'dev')
BASE_PATH = Path(r"\\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Credit_Loan_Review\CRE_Reporting_Board\Production") if ENV == 'prod' else Path(__file__).parent.parent
OUTPUT_DIR = BASE_PATH / "output"
INPUT_DIR = BASE_PATH / "input"

# Email Recipients
EMAIL_TO = [""]  # Primary recipient for production
EMAIL_CC = []  # List of CC recipients for production


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
    'Autobody/Gas Station': ['Autobody/Gas Station','Gas Station and Convenience St','Auto-Truck Repair','Car Wash'],
    'Retail': ['Retail - Big Box Store','Shopping Plaza','Strip Plaza','General Retail','Dealership'],
    'Hospitality': ['Hotel/Motel','Hospitality/Event Space','Assisted Living'],
    'Recreation': ['Outdoor Recreation','Indoor Recreational','Golf Course','Marina'],
    'Industrial': ['Manufacturing','Warehouse','Industrial','Seafood Processing Plant','Solar Farm'],
    'Land': ['Land - Unimproved','Land - Improved','Parking Lot'],
    'Mixed Use': ['Mixed Use (Retail/Office)','Mixed Use (Retail/Residential)','Mixed Use (Office/Residential)'],
    'Multi Family': ['Apartment Building','Multi Family'],
    'General Office': ['Office - Professional','Office- General'],
    'Medical Office': ['Office - Medical'],
    'Restaurant': ['Restaurant'],
    'Residential': ['1-4 Fam Res - Non Own Occ','1 Family Residential - Own Occ','2 Family Residential - Own Occ','Condominium'],
    'Storage': ['Self Storage'],
    'Educational': ['Educational Facilities','Day Care'],
    'Religious': ['Church'],
    'Funeral': ['Funeral Home'],
    'Real Estate Related': ['Real Estate - Business','Real Estate - Bus&Bus Assets','Real Estate - Personal & Bus','Real Estate - Pers&Bus Assets'],
    'Business Assets': ['All Business Assets','Bus Assets w/Accts Receivable','UCC - ABA','UCC- Equipment','Assignment of Leases/Rents'],
    'Secured Deposits': ['Savings - Partially Secured','Passbook/Savings Secured'],
    'Vehicles': ['Vehicle - Business','Boat'],
    'Contractor': ['General Contractor','Outdoor Dealers'],
    'Securities': ['Marketable Securities','SBA Loan'],
    'Other': ['Commercial - Other']
}
