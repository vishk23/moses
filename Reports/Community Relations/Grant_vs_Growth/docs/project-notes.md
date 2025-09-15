Objective:
Extract loan and deposit growth in different regions and plot against our grants/Foundation 

Usage:
- notebook only for now.

# 2025-09-12
I think this is historically about 10% of NI.
- or operating profits, not sure exactly

Ideally 1 graph
All loans/deposits (Year end figures)
- break out by the regions that CPG uses

----

Roadmap:
- Pull in full data
    - For different year ends
    - Bounce off of balance tracker and other things for accuracy
- Apply region mapping
    - Need to categorize all branches to region
- Get annual totals (group by)
- Consolidate df with giving data (years as columns should match)
- Plot this
    - figure out optimal way to show this all on one graph


I was thinking matplotlib, but might as well do powerBI. Maybe I start with matplotlib.

df should be year end dates as the rows. The columns would be the regions and loans/deposits (and there should be a total too), like a double column index in a pivot table. This should be whatever is going to load cleanly into both matplotlib and PowerBI

Idea for graph is time on X axis

---

test2.6.py is the graph that he wants
- now just need the numbers

Unique branches
array(['BCSB - MUNI FALL RIVER BRANCH', 'BCSB - MUNI MAIN OFFICE',
       'BCSB - MAIN OFFICE', "BCSB - COMM'L LENDING- TAUNTON",
       "BCSB - COMM'L LENDING - WARWICK",
       "BCSB - COMM'L LENDING - PROVIDENCE",
       "BCSB - COMM'L LENDING - FALL RIVER",
       'BCSB - MUNI ATTLEBORO BRANCH',
       "BCSB - COMM'L LENDING - PAWTUCKET",
       "BCSB - COMM'L LENDING - CANDLEWORKS",
       'BCSB - MUNI NORTH RAYNHAM BRANCH',
       "BCSB - COMM'L LENDING - DARTMOUTH",
       'BCSB - MUNI DARTMOUTH BRANCH', 'BCSB - DEPOSIT OPERATIONS',
       'BCSB - NO ATTLEBORO BRANCH', 'BRISTOL COUNTY SAVINGS BANK',
       "BCSB - COMM'L LENDING - ATTLEBORO", 'BCSB - BEACON SECURITY CORP',
       'BCSB - MUNI NB ASHLEY BLVD BRANCH', 'BCSB - CUMBERLAND',
       'BCSB - NB ASHLEY BLVD BRANCH', 'BCSB - MUNI CANDLEWORKS BRANCH',
       'BCSB - ATTLEBORO BRANCH', 'BCSB - MUNI COUNTY STREET BRANCH',
       'BCSB - REHOBOTH BRANCH', 'BCSB - PAWTUCKET BRANCH',
       'BCSB - MUNI NO ATTLEBORO BRANCH',
       'BCSB - MUNI EAST FREETOWN BRANCH',
       'BCSB - MUNI RAYNHAM CENTER BRANCH', 'BCSB - DARTMOUTH BRANCH',
       'BCSB - EAST FREETOWN BRANCH', "BCSB - CMM'L LENDING - FNB-RI",
       'BCSB - RAYNHAM CENTER BRANCH', 'BCSB - FALL RIVER BRANCH',
       'BCSB - MUNI REHOBOTH BRANCH', 'BCSB - CANDLEWORKS BRANCH',
       'BCSB - MUNI PAWTUCKET BRANCH', "BCSB - COMM'L LENDING - FRANKLIN",
       'BCSB - FRANKLIN BRANCH', 'BCSB - COUNTY STREET BRANCH',
       'BCSB - RESIDENTIAL MTG - DARTMOUTH',
       'BCSB - RESIDENTIAL MTG - PAWTUCKET', 'BCSB - MUNI GREENVILLE',
       'BCSB - CONS INST LENDING- TAUNTON',
       'BCSB - RESIDENTIAL MTG - ATTLEBORO',
       'BCSB - RESIDENTIAL MTG - FALL RIVER', 'BCSB - GREENVILLE',
       'BCSB - NORTH RAYNHAM BRANCH', 'BCSB - RESIDENTIAL MTG - CAPE COD',
       'BCSB - CONS INST LENDING - DARTMOUTH',
       'BCSB - RESIDENTIAL MTG- TAUNTON',
       'BCSB - RESIDENTIAL MTG - FRANKLIN',
       'BCSB - CONS INST LENDING - ATTLEBORO',
       'BCSB - RESI LENDING - WARWICK',
       'BCSB - SMALL BUSINESS LOAN CENTER', 'BCSB - CONTACT CENTER',
       'BCSB - CONS INST LENDING - FALL RIVER',
       'BCSB - TAUNTON HIGH SCHOOL',
       'BCSB - CONS INST LENDING - FRANKLIN',
       'BCSB - CONS INST LENDING - PAWTUCKET',
       'BCSB - CONS INST LENDING - FNB-RI', 'BCSB - MUNI CUMBERLAND',
       'BCSB - RESI LENDING - NEW BEDFORD', 'BCSB - INDIRECT LENDING',
       'BCSB - RESIDENTIAL MTG - FNB-RI',
       'BCSB - MUNI ATTLEBORO HIGH SCHOOL',
       'BCSB - ATTLEBORO HIGH SCHOOL', 'BCSB - MUNI TAUNTON HIGH SCHOOL'],
      dtype=object)


Deposit mapping for other project:
region_mapping = {
    # Greater Attleboro
    'BCSB - ATTLEBORO BRANCH': 'Greater Attleboro',
    'BCSB - ATTLEBORO HIGH SCHOOL': 'Greater Attleboro', 
    'BCSB - FRANKLIN BRANCH': 'Greater Attleboro',
    'BCSB - NO ATTLEBORO BRANCH': 'Greater Attleboro',
    'BCSB - REHOBOTH BRANCH': 'Greater Attleboro',
    # RI
    'BCSB - GREENVILLE': 'RI',
    'BCSB - PAWTUCKET BRANCH': 'RI',
    'BCSB - CUMBERLAND': 'RI',
    # Taunton
    'BCSB - CONTACT CENTER': 'Taunton',
    'BCSB - COUNTY STREET BRANCH': 'Taunton',
    'BCSB - DEPOSIT OPERATIONS': 'Taunton',
    'BCSB - MAIN OFFICE': 'Taunton',
    'BCSB - NORTH RAYNHAM BRANCH': 'Taunton',
    'BCSB - RAYNHAM CENTER BRANCH': 'Taunton',
    'BCSB - TAUNTON HIGH SCHOOL':'Taunton', # New
    # South Coast
    'BCSB - DARTMOUTH BRANCH': 'South Coast',
    'BCSB - EAST FREETOWN BRANCH': 'South Coast',
    'BCSB - FALL RIVER BRANCH': 'South Coast',
    'BCSB - CANDLEWORKS BRANCH': 'South Coast',  
    'BCSB - NB ASHLEY BLVD BRANCH': 'South Coast',
}


Mapping:

region_map = {
    # ——— Attleboro/Taunton ———
    'BCSB - MUNI MAIN OFFICE': 'Attleboro/Taunton',
    'BCSB - MAIN OFFICE': 'Attleboro/Taunton',
    "BCSB - COMM'L LENDING- TAUNTON": 'Attleboro/Taunton',
    'BCSB - MUNI ATTLEBORO BRANCH': 'Attleboro/Taunton',
    'BCSB - DEPOSIT OPERATIONS': 'Attleboro/Taunton',
    'BCSB - NO ATTLEBORO BRANCH': 'Attleboro/Taunton',
    'BRISTOL COUNTY SAVINGS BANK': 'Attleboro/Taunton',
    "BCSB - COMM'L LENDING - ATTLEBORO": 'Attleboro/Taunton',
    'BCSB - BEACON SECURITY CORP': 'Attleboro/Taunton',
    'BCSB - ATTLEBORO BRANCH': 'Attleboro/Taunton',
    'BCSB - MUNI COUNTY STREET BRANCH': 'Attleboro/Taunton',
    'BCSB - REHOBOTH BRANCH': 'Attleboro/Taunton',
    'BCSB - MUNI REHOBOTH BRANCH': 'Attleboro/Taunton',
    'BCSB - MUNI NO ATTLEBORO BRANCH': 'Attleboro/Taunton',
    'BCSB - MUNI RAYNHAM CENTER BRANCH': 'Attleboro/Taunton',
    'BCSB - COUNTY STREET BRANCH': 'Attleboro/Taunton',
    'BCSB - NORTH RAYNHAM BRANCH': 'Attleboro/Taunton',
    'BCSB - RAYNHAM CENTER BRANCH': 'Attleboro/Taunton',
    "BCSB - COMM'L LENDING - FRANKLIN": 'Attleboro/Taunton',
    'BCSB - FRANKLIN BRANCH': 'Attleboro/Taunton',
    'BCSB - CONS INST LENDING- TAUNTON': 'Attleboro/Taunton',
    'BCSB - RESIDENTIAL MTG - ATTLEBORO': 'Attleboro/Taunton',
    'BCSB - RESIDENTIAL MTG- TAUNTON': 'Attleboro/Taunton',
    'BCSB - RESIDENTIAL MTG - FRANKLIN': 'Attleboro/Taunton',
    'BCSB - CONS INST LENDING - ATTLEBORO': 'Attleboro/Taunton',
    'BCSB - SMALL BUSINESS LOAN CENTER': 'Attleboro/Taunton',
    'BCSB - CONTACT CENTER': 'Attleboro/Taunton',
    'BCSB - TAUNTON HIGH SCHOOL': 'Attleboro/Taunton',
    'BCSB - MUNI ATTLEBORO HIGH SCHOOL': 'Attleboro/Taunton',
    'BCSB - ATTLEBORO HIGH SCHOOL': 'Attleboro/Taunton',
    'BCSB - INDIRECT LENDING': 'Attleboro/Taunton'

    # ——— South Coast ———
    'BCSB - MUNI FALL RIVER BRANCH': 'South Coast',
    "BCSB - COMM'L LENDING - FALL RIVER": 'South Coast',
    "BCSB - COMM'L LENDING - CANDLEWORKS": 'South Coast',
    "BCSB - COMM'L LENDING - DARTMOUTH": 'South Coast',
    'BCSB - MUNI DARTMOUTH BRANCH': 'South Coast',
    'BCSB - MUNI NB ASHLEY BLVD BRANCH': 'South Coast',
    'BCSB - NB ASHLEY BLVD BRANCH': 'South Coast',
    'BCSB - MUNI CANDLEWORKS BRANCH': 'South Coast',
    'BCSB - MUNI EAST FREETOWN BRANCH': 'South Coast',
    'BCSB - DARTMOUTH BRANCH': 'South Coast',
    'BCSB - EAST FREETOWN BRANCH': 'South Coast',
    'BCSB - FALL RIVER BRANCH': 'South Coast',
    'BCSB - CANDLEWORKS BRANCH': 'South Coast',
    'BCSB - RESIDENTIAL MTG - DARTMOUTH': 'South Coast',
    'BCSB - RESIDENTIAL MTG - FALL RIVER': 'South Coast',
    'BCSB - RESI LENDING - NEW BEDFORD': 'South Coast',

    # ——— Rhode Island ———
    "BCSB - COMM'L LENDING - WARWICK": 'Rhode Island',
    "BCSB - COMM'L LENDING - PROVIDENCE": 'Rhode Island',
    "BCSB - COMM'L LENDING - PAWTUCKET": 'Rhode Island',
    'BCSB - CUMBERLAND': 'Rhode Island',
    'BCSB - PAWTUCKET BRANCH': 'Rhode Island',
    "BCSB - CMM'L LENDING - FNB-RI": 'Rhode Island',
    'BCSB - MUNI PAWTUCKET BRANCH': 'Rhode Island',
    'BCSB - RESIDENTIAL MTG - PAWTUCKET': 'Rhode Island',
    'BCSB - MUNI GREENVILLE': 'Rhode Island',
    'BCSB - GREENVILLE': 'Rhode Island',
    'BCSB - RESI LENDING - WARWICK': 'Rhode Island',
    'BCSB - CONS INST LENDING - PAWTUCKET': 'Rhode Island',
    'BCSB - CONS INST LENDING - FNB-RI': 'Rhode Island',
    'BCSB - MUNI CUMBERLAND': 'Rhode Island',
    'BCSB - RESIDENTIAL MTG - FNB-RI': 'Rhode Island',

    # ——— Other ———
    'BCSB - RESIDENTIAL MTG - CAPE COD': 'Other',
    # Operational catch-alls (if any are left unmapped in future, they'll fall to 'Other' via the fillna below)
}

# Create the Region column from the mapping
import numpy as np
df['Region'] = df['branchname'].map(region_map).fillna(
    np.where(df['branchname'].str.contains(r'Warwick|Providence|Pawtucket|Cumberland|Greenville|FNB-RI', case=False), 'Rhode Island',
    np.where(df['branchname'].str.contains(r'Fall River|Dartmouth|East Freetown|New Bedford|Candleworks|Ashley Blvd', case=False), 'South Coast',
    np.where(df['branchname'].str.contains(r'Attleboro|Franklin|Raynham|Taunton|Rehoboth|County Street|Main Office', case=False), 'Attleboro/Taunton', 'Other'))))


# ——— Attleboro/Taunton ———
- 'BCSB - MUNI MAIN OFFICE': 'Attleboro/Taunton',
- 'BCSB - MAIN OFFICE': 'Attleboro/Taunton',
- "BCSB - COMM'L LENDING- TAUNTON": 'Attleboro/Taunton',
- 'BCSB - MUNI ATTLEBORO BRANCH': 'Attleboro/Taunton',
- 'BCSB - DEPOSIT OPERATIONS': 'Attleboro/Taunton',
- 'BCSB - NO ATTLEBORO BRANCH': 'Attleboro/Taunton',
- 'BRISTOL COUNTY SAVINGS BANK': 'Attleboro/Taunton',
- "BCSB - COMM'L LENDING - ATTLEBORO": 'Attleboro/Taunton',
- 'BCSB - BEACON SECURITY CORP': 'Attleboro/Taunton',
- 'BCSB - ATTLEBORO BRANCH': 'Attleboro/Taunton',
- 'BCSB - MUNI COUNTY STREET BRANCH': 'Attleboro/Taunton',
- 'BCSB - REHOBOTH BRANCH': 'Attleboro/Taunton',
- 'BCSB - MUNI REHOBOTH BRANCH': 'Attleboro/Taunton',
- 'BCSB - MUNI NO ATTLEBORO BRANCH': 'Attleboro/Taunton',
- 'BCSB - MUNI RAYNHAM CENTER BRANCH': 'Attleboro/Taunton',
- 'BCSB - COUNTY STREET BRANCH': 'Attleboro/Taunton',
- 'BCSB - NORTH RAYNHAM BRANCH': 'Attleboro/Taunton',
- 'BCSB - RAYNHAM CENTER BRANCH': 'Attleboro/Taunton',
- "BCSB - COMM'L LENDING - FRANKLIN": 'Attleboro/Taunton',
- 'BCSB - FRANKLIN BRANCH': 'Attleboro/Taunton',
- 'BCSB - CONS INST LENDING- TAUNTON': 'Attleboro/Taunton',
- 'BCSB - RESIDENTIAL MTG - ATTLEBORO': 'Attleboro/Taunton',
- 'BCSB - RESIDENTIAL MTG- TAUNTON': 'Attleboro/Taunton',
- 'BCSB - RESIDENTIAL MTG - FRANKLIN': 'Attleboro/Taunton',
- 'BCSB - CONS INST LENDING - ATTLEBORO': 'Attleboro/Taunton',
- 'BCSB - SMALL BUSINESS LOAN CENTER': 'Attleboro/Taunton',
- 'BCSB - CONTACT CENTER': 'Attleboro/Taunton',
- 'BCSB - TAUNTON HIGH SCHOOL': 'Attleboro/Taunton',
- 'BCSB - MUNI ATTLEBORO HIGH SCHOOL': 'Attleboro/Taunton',
- 'BCSB - ATTLEBORO HIGH SCHOOL': 'Attleboro/Taunton',
- 'BCSB - INDIRECT LENDING': 'Attleboro/Taunton'

# ——— South Coast ———
- 'BCSB - MUNI FALL RIVER BRANCH': 'South Coast',
- "BCSB - COMM'L LENDING - FALL RIVER": 'South Coast',
- "BCSB - COMM'L LENDING - CANDLEWORKS": 'South Coast',
- "BCSB - COMM'L LENDING - DARTMOUTH": 'South Coast',
- 'BCSB - MUNI DARTMOUTH BRANCH': 'South Coast',
- 'BCSB - MUNI NB ASHLEY BLVD BRANCH': 'South Coast',
- 'BCSB - NB ASHLEY BLVD BRANCH': 'South Coast',
- 'BCSB - MUNI CANDLEWORKS BRANCH': 'South Coast',
- 'BCSB - MUNI EAST FREETOWN BRANCH': 'South Coast',
- 'BCSB - DARTMOUTH BRANCH': 'South Coast',
- 'BCSB - EAST FREETOWN BRANCH': 'South Coast',
- 'BCSB - FALL RIVER BRANCH': 'South Coast',
- 'BCSB - CANDLEWORKS BRANCH': 'South Coast',
- 'BCSB - RESIDENTIAL MTG - DARTMOUTH': 'South Coast',
- 'BCSB - RESIDENTIAL MTG - FALL RIVER': 'South Coast',
- 'BCSB - RESI LENDING - NEW BEDFORD': 'South Coast',

# ——— Rhode Island ———
- "BCSB - COMM'L LENDING - WARWICK": 'Rhode Island',
- "BCSB - COMM'L LENDING - PROVIDENCE": 'Rhode Island',
- "BCSB - COMM'L LENDING - PAWTUCKET": 'Rhode Island',
- 'BCSB - CUMBERLAND': 'Rhode Island',
- 'BCSB - PAWTUCKET BRANCH': 'Rhode Island',
- "BCSB - CMM'L LENDING - FNB-RI": 'Rhode Island',
- 'BCSB - MUNI PAWTUCKET BRANCH': 'Rhode Island',
- 'BCSB - RESIDENTIAL MTG - PAWTUCKET': 'Rhode Island',
- 'BCSB - MUNI GREENVILLE': 'Rhode Island',
- 'BCSB - GREENVILLE': 'Rhode Island',
- 'BCSB - RESI LENDING - WARWICK': 'Rhode Island',
- 'BCSB - CONS INST LENDING - PAWTUCKET': 'Rhode Island',
- 'BCSB - CONS INST LENDING - FNB-RI': 'Rhode Island',
- 'BCSB - MUNI CUMBERLAND': 'Rhode Island',
- 'BCSB - RESIDENTIAL MTG - FNB-RI': 'Rhode Island',

# ——— Other ———
- 'BCSB - RESIDENTIAL MTG - CAPE COD': 'Other',
df['Region'] = df['Branch'].map(region_map).fillna(
    np.where(df['Branch'].str.contains(r'Warwick|Providence|Pawtucket|Cumberland|Greenville|FNB-RI', case=False), 'Rhode Island',
    np.where(df['Branch'].str.contains(r'Fall River|Dartmouth|East Freetown|New Bedford|Candleworks|Ashley Blvd', case=False), 'South Coast',
    np.where(df['Branch'].str.contains(r'Attleboro|Franklin|Raynham|Taunton|Rehoboth|County Street|Main Office', case=False), 'Attleboro/Taunton', 'Other'))))


--- fix typeerror
import pandas as pd
import numpy as np

# Assume you already have: region_map (dict) and df['Branch'] exists
s = df['Branch']

# 1) Exact-name mapping first
region = s.map(region_map)

# 2) Regex-based geographic fallback as a Series
ri = s.str.contains(r'Warwick|Providence|Pawtucket|Cumberland|Greenville|FNB-RI', case=False, na=False)
sc = s.str.contains(r'Fall River|Dartmouth|East Freetown|New Bedford|Candleworks|Ashley Blvd', case=False, na=False)
at = s.str.contains(r'Attleboro|Franklin|Raynham|Taunton|Rehoboth|County Street|Main Office', case=False, na=False)

fallback = pd.Series(
    np.select([ri, sc, at], ['Rhode Island', 'South Coast', 'Attleboro/Taunton'], default='Other'),
    index=df.index
)

# 3) Fill unmapped with the Series (allowed), not an ndarray
df['Region'] = region.fillna(fallback)


----
Grant
,2020,2021,2022,2023,2024,,5 Year Totals,
Attleboro/Taunton," $881,398.00 "," $815,706.67 "," $868,427.68 "," $776,439.66 "," $909,814.80 ",," $4,251,786.81 ",
SouthCoast," $933,728.84 "," $791,106.23 "," $1,162,538.61 "," $975,260.36 "," $1,183,795.00 ",," $5,046,429.04 ",
Rhode Island," $261,250.00 "," $244,000.00 "," $314,615.00 "," $356,715.00 "," $636,957.00 ",," $1,813,537.00 ",
Other," $115,500.00 "," $98,171.76 "," $77,000.00 "," $40,800.00 "," $128,550.00 ",," $460,021.76 ",




2020:
Region Account Type  NetBalance_sum
0  Attleboro/Taunton      Deposit    1.688611e+09
1  Attleboro/Taunton         Loan    1.412844e+09
2              Other         Loan    1.337390e+07
3       Rhode Island      Deposit    2.248410e+08
4       Rhode Island         Loan    4.709164e+08
5        South Coast      Deposit    6.555967e+08
6        South Coast         Loan    6.455994e+08

2021:
Region Account Type  NetBalance_sum
0  Attleboro/Taunton      Deposit    1.688611e+09
1  Attleboro/Taunton         Loan    1.412844e+09
2              Other         Loan    1.337390e+07
3       Rhode Island      Deposit    2.248410e+08
4       Rhode Island         Loan    4.709164e+08
5        South Coast      Deposit    6.555967e+08
6        South Coast         Loan    6.455994e+08

2022:
Same as above

2023:
Same as above

2024:
Same as above



----

array(['BCSB - Muni Main Office', "BCSB - Comm'l Lending- Taunton",
       'BCSB - No Attleboro Branch',
       "BCSB - Comm'l Lending - Candleworks", 'BCSB - Main Office',
       'BCSB - Muni North Raynham Branch', 'BCSB - Muni Attleboro Branch',
       "BCSB - Comm'l Lending - Fall River",
       "BCSB - Comm'l Lending - Dartmouth",
       'BCSB - Muni No Attleboro Branch', 'BCSB - Dartmouth Branch',
       "BCSB - Comm'l Lending - Pawtucket",
       "BCSB - Comm'l Lending - Attleboro",
       'BCSB - Muni Dartmouth Branch', "BCSB - Comm'l Lending - Warwick",
       'BCSB - Muni Candleworks Branch', 'BCSB - Beacon Security Corp',
       'BCSB - Muni Fall River Branch', 'BCSB - North Raynham Branch',
       'BCSB - Raynham Center Branch', 'BCSB - NB Ashley Blvd Branch',
       'BCSB - Pawtucket Branch', 'BCSB - Fall River Branch',
       'BCSB - Attleboro Branch', 'BCSB - Muni Pawtucket Branch',
       'BCSB - Muni NB Ashley Blvd Branch', 'BCSB - Muni Franklin Branch',
       'BCSB - Muni County Street Branch',
       "BCSB - Comm'l Lending - Providence", 'BCSB - Candleworks Branch',
       'BCSB - NB Rockdale Ave Branch',
       "BCSB - Comm'l Lending - Franklin",
       'BCSB - Muni Raynham Center Branch', 'BCSB - Franklin Branch',
       "BCSB - Cmm'l Lending - FNB-RI", 'BCSB - Contact Center',
       'BCSB - Rehoboth Branch', 'BCSB - Muni Rehoboth Branch',
       'BCSB - Residential Mtg - Dartmouth', 'BCSB - Greenville',
       'BCSB - County Street Branch',
       'BCSB - Residential Mtg - Attleboro', 'BCSB - Muni Greenville',
       'Bristol County Savings Bank',
       'BCSB - Residential Mtg - Pawtucket', 'BCSB - Cumberland',
       'BCSB - Residential Mtg- Taunton',
       'BCSB - Cons Inst Lending- Taunton',
       'BCSB - Residential Mtg - Franklin',
       'BCSB - Resi Lending - Warwick', 'BCSB - East Freetown Branch',
       'BCSB - Residential Mtg - Fall River',
       'BCSB - Cons Inst Lending - Dartmouth',
       'BCSB - Residential Mtg - Cape Cod', 'BCSB - Walmart Branch',
       'BCSB - Cons Inst Lending - Pawtucket',
       'BCSB - Cons Inst Lending - Attleboro',
       'BCSB - Cons Inst Lending - FNB-RI',
       'BCSB - Residential Mtg - FNB-RI',
       'BCSB - Cons Inst Lending - Fall River',
       'BCSB - Muni East Freetown Branch', 'BCSB - Taunton High School',
       'BCSB - Cons Inst Lending - Franklin',
       'BCSB - Resi Lending - New Bedford', 'BCSB - Muni Cumberland',
       'BCSB - Indirect Lending', 'BCSB - Muni Attleboro High School',
       'BCSB - Deposit Operations', 'BCSB - Attleboro High School',
       'BCSB - Muni Taunton High School'], dtype=object)


# %%
import os
import sys
from pathlib import Path

# Navigate to project root (equivalent to cd ..)
project_dir = Path(__file__).parent.parent if '__file__' in globals() else Path.cwd().parent
os.chdir(project_dir)

# Add src directory to Python path for imports
src_dir = project_dir / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# Set environment for dev testing
os.environ['REPORT_ENV'] = 'dev'

# %%
import src.config

# %%
import pandas as pd
from deltalake import DeltaTable
from pathlib import Path

# %%
df = DeltaTable(src.config.SILVER / "account").to_pandas()

# %%
import cdutils.acct_file_creation.core
from datetime import datetime

# # Specific date
specified_date = datetime(2020, 12, 31)
df = cdutils.acct_file_creation.core.query_df_on_date(specified_date)

# %%
df

# %%
df['mjaccttypcd'].unique()

# %%
df = df[df['mjaccttypcd'].isin(['CML','MLN','CNS','MTG','CK','SAV','TD'])].copy()

# %%
# Create Account Type mapping - Easier to understand, based on our major field
def map_account_type(acct_code:str):
    """
    Map mjaccttypcd to friendly Account Type
    """
    mapping = {
        'CML':'Loan',
        'MLN':'Loan',
        'CNS':'Loan',
        'MTG':'Loan',
        'CK':'Deposit',
        'SAV':'Deposit',
        'TD':'Deposit'
    }
    return mapping.get(str(acct_code).upper(), 'Other')

df['Account Type'] = df['mjaccttypcd'].apply(map_account_type)

# %%
df['branchname'].unique()

# %%
df

# %%
region_map = {
    # ——— Attleboro/Taunton ———
    'BCSB - MUNI MAIN OFFICE': 'Attleboro/Taunton',
    'BCSB - MAIN OFFICE': 'Attleboro/Taunton',
    "BCSB - COMM'L LENDING- TAUNTON": 'Attleboro/Taunton',
    'BCSB - MUNI ATTLEBORO BRANCH': 'Attleboro/Taunton',
    'BCSB - DEPOSIT OPERATIONS': 'Attleboro/Taunton',
    'BCSB - NO ATTLEBORO BRANCH': 'Attleboro/Taunton',
    'BRISTOL COUNTY SAVINGS BANK': 'Attleboro/Taunton',
    "BCSB - COMM'L LENDING - ATTLEBORO": 'Attleboro/Taunton',
    'BCSB - BEACON SECURITY CORP': 'Attleboro/Taunton',
    'BCSB - ATTLEBORO BRANCH': 'Attleboro/Taunton',
    'BCSB - MUNI COUNTY STREET BRANCH': 'Attleboro/Taunton',
    'BCSB - REHOBOTH BRANCH': 'Attleboro/Taunton',
    'BCSB - MUNI REHOBOTH BRANCH': 'Attleboro/Taunton',
    'BCSB - MUNI NO ATTLEBORO BRANCH': 'Attleboro/Taunton',
    'BCSB - MUNI RAYNHAM CENTER BRANCH': 'Attleboro/Taunton',
    'BCSB - COUNTY STREET BRANCH': 'Attleboro/Taunton',
    'BCSB - NORTH RAYNHAM BRANCH': 'Attleboro/Taunton',
    'BCSB - RAYNHAM CENTER BRANCH': 'Attleboro/Taunton',
    "BCSB - COMM'L LENDING - FRANKLIN": 'Attleboro/Taunton',
    'BCSB - FRANKLIN BRANCH': 'Attleboro/Taunton',
    'BCSB - CONS INST LENDING- TAUNTON': 'Attleboro/Taunton',
    'BCSB - RESIDENTIAL MTG - ATTLEBORO': 'Attleboro/Taunton',
    'BCSB - RESIDENTIAL MTG- TAUNTON': 'Attleboro/Taunton',
    'BCSB - RESIDENTIAL MTG - FRANKLIN': 'Attleboro/Taunton',
    'BCSB - CONS INST LENDING - ATTLEBORO': 'Attleboro/Taunton',
    'BCSB - SMALL BUSINESS LOAN CENTER': 'Attleboro/Taunton',
    'BCSB - CONTACT CENTER': 'Attleboro/Taunton',
    'BCSB - TAUNTON HIGH SCHOOL': 'Attleboro/Taunton',
    'BCSB - MUNI ATTLEBORO HIGH SCHOOL': 'Attleboro/Taunton',
    'BCSB - ATTLEBORO HIGH SCHOOL': 'Attleboro/Taunton',
    'BCSB - INDIRECT LENDING': 'Attleboro/Taunton',

    # ——— South Coast ———
    'BCSB - MUNI FALL RIVER BRANCH': 'South Coast',
    "BCSB - COMM'L LENDING - FALL RIVER": 'South Coast',
    "BCSB - COMM'L LENDING - CANDLEWORKS": 'South Coast',
    "BCSB - COMM'L LENDING - DARTMOUTH": 'South Coast',
    'BCSB - MUNI DARTMOUTH BRANCH': 'South Coast',
    'BCSB - MUNI NB ASHLEY BLVD BRANCH': 'South Coast',
    'BCSB - NB ASHLEY BLVD BRANCH': 'South Coast',
    'BCSB - MUNI CANDLEWORKS BRANCH': 'South Coast',
    'BCSB - MUNI EAST FREETOWN BRANCH': 'South Coast',
    'BCSB - DARTMOUTH BRANCH': 'South Coast',
    'BCSB - EAST FREETOWN BRANCH': 'South Coast',
    'BCSB - FALL RIVER BRANCH': 'South Coast',
    'BCSB - CANDLEWORKS BRANCH': 'South Coast',
    'BCSB - RESIDENTIAL MTG - DARTMOUTH': 'South Coast',
    'BCSB - RESIDENTIAL MTG - FALL RIVER': 'South Coast',
    'BCSB - RESI LENDING - NEW BEDFORD': 'South Coast',

    # ——— Rhode Island ———
    "BCSB - COMM'L LENDING - WARWICK": 'Rhode Island',
    "BCSB - COMM'L LENDING - PROVIDENCE": 'Rhode Island',
    "BCSB - COMM'L LENDING - PAWTUCKET": 'Rhode Island',
    'BCSB - CUMBERLAND': 'Rhode Island',
    'BCSB - PAWTUCKET BRANCH': 'Rhode Island',
    "BCSB - CMM'L LENDING - FNB-RI": 'Rhode Island',
    'BCSB - MUNI PAWTUCKET BRANCH': 'Rhode Island',
    'BCSB - RESIDENTIAL MTG - PAWTUCKET': 'Rhode Island',
    'BCSB - MUNI GREENVILLE': 'Rhode Island',
    'BCSB - GREENVILLE': 'Rhode Island',
    'BCSB - RESI LENDING - WARWICK': 'Rhode Island',
    'BCSB - CONS INST LENDING - PAWTUCKET': 'Rhode Island',
    'BCSB - CONS INST LENDING - FNB-RI': 'Rhode Island',
    'BCSB - MUNI CUMBERLAND': 'Rhode Island',
    'BCSB - RESIDENTIAL MTG - FNB-RI': 'Rhode Island',

    # ——— Other ———
    'BCSB - RESIDENTIAL MTG - CAPE COD': 'Other',
    # Operational catch-alls (if any are left unmapped in future, they'll fall to 'Other' via the fillna below)
}


# %%
import pandas as pd
import numpy as np

# Assume you already have: region_map (dict) and df['Branch'] exists
s = df['branchname']

# 1) Exact-name mapping first
region = s.map(region_map)

# 2) Regex-based geographic fallback as a Series
ri = s.str.contains(r'Warwick|Providence|Pawtucket|Cumberland|Greenville|FNB-RI', case=False, na=False)
sc = s.str.contains(r'Fall River|Dartmouth|East Freetown|New Bedford|Candleworks|Ashley Blvd', case=False, na=False)
at = s.str.contains(r'Attleboro|Franklin|Raynham|Taunton|Rehoboth|County Street|Main Office', case=False, na=False)

fallback = pd.Series(
    np.select([ri, sc, at], ['Rhode Island', 'South Coast', 'Attleboro/Taunton'], default='Other'),
    index=df.index
)

# 3) Fill unmapped with the Series (allowed), not an ndarray
df['Region'] = region.fillna(fallback)


# %%
df

# %%
# Performed 1 aggregation grouped on columns: 'Region', 'Account Type'
grouped_df = df.groupby(['Region', 'Account Type']).agg(NetBalance_sum=('Net Balance', 'sum')).reset_index()

# %%
grouped_df


----


# --- Normalize, Map Regions, and Emit "Other" Review --------------------------
import re
import pandas as pd

# 1) Normalize BRANCH names in a new column (keep original for reference)
def normalize_branch(series: pd.Series) -> pd.Series:
    s = series.fillna("").astype(str).str.upper()

    # Unify quotes/apostrophes and whitespace/hyphens
    s = s.str.replace(r"[‘’ʼ´`]", "'", regex=True)           # curly -> straight
    s = s.str.replace(r"\s*-\s*", " - ", regex=True)         # spaces around hyphen
    s = s.str.replace(r"\s+", " ", regex=True).str.strip()   # collapse spaces

    # Fix a couple of known variants/typos seen historically
    s = s.str.replace("CMM'L", "COMM'L", regex=False)
    s = s.str.replace("COMM’L", "COMM'L", regex=False)

    return s

df["branch_std"] = normalize_branch(df["branchname"])

# 2) Ensure the region map uses UPPERCASE keys (safe even if yours already are)
region_map_upper = {str(k).upper(): v for k, v in region_map.items()}

# 3) Exact match mapping first
df["Region"] = df["branch_std"].map(region_map_upper)

# 4) Regex fallback by geography (safety net; exact map above is the source of truth)
_fallback_patterns = [
    (r"\b(WARWICK|PROVIDENCE|PAWTUCKET|CUMBERLAND|GREENVILLE|FNB-RI)\b", "Rhode Island"),
    (r"\b(FALL RIVER|DARTMOUTH|EAST FREETOWN|NEW BEDFORD|CANDLEWORKS|ASHLEY BLVD)\b", "South Coast"),
    (r"\b(ATTLEBORO|FRANKLIN|RAYNHAM|TAUNTON|REHOBOTH|COUNTY STREET|MAIN OFFICE)\b", "Attleboro/Taunton"),
]

def fallback_region(name: str) -> str | None:
    for pat, region in _fallback_patterns:
        if re.search(pat, name):
            return region
    return None

df["Region"] = df["Region"].fillna(df["branch_std"].apply(lambda x: fallback_region(x) or "Other"))

# 5) Optional: fix Region order so it’s stable across runs
REGION_ORDER = ["Attleboro/Taunton", "South Coast", "Rhode Island", "Other"]
df["Region"] = pd.Categorical(df["Region"], categories=REGION_ORDER, ordered=True)

# 6) Your aggregation (unchanged)
grouped_df = (
    df.groupby(["Region", "Account Type"], observed=True)
      .agg(NetBalance_sum=("Net Balance", "sum"))
      .reset_index()
)

# 7) Always emit a review table for unmapped/“Other”
other_base = df[df["Region"] == "Other"].copy()

# One row per normalized branch, with examples of original values and totals
examples = (
    other_base.groupby("branch_std")["branchname"]
    .apply(lambda x: sorted(set(x))[:3])  # up to 3 example raw names
    .reset_index(name="examples")
)

other_df = (
    other_base.groupby("branch_std", as_index=False)
    .agg(
        n_accounts=("branch_std", "size"),
        NetBalance_sum=("Net Balance", "sum"),
    )
    .merge(examples, on="branch_std", how="left")
    .sort_values(["n_accounts", "NetBalance_sum"], ascending=[False, False])
)

# 8) (Nice to have) quick coverage stats for your log
mapped_rate = (df["Region"] != "Other").mean()
print(f"Region mapping coverage: {mapped_rate:.1%} of rows; {other_df.shape[0]} unmapped branch_std values.")
# -----------------------------------------------------------------------------



Actual data:
Grant
,2020,2021,2022,2023,2024,,5 Year Totals,
Attleboro/Taunton," $881,398.00 "," $815,706.67 "," $868,427.68 "," $776,439.66 "," $909,814.80 ",," $4,251,786.81 ",
SouthCoast," $933,728.84 "," $791,106.23 "," $1,162,538.61 "," $975,260.36 "," $1,183,795.00 ",," $5,046,429.04 ",
Rhode Island," $261,250.00 "," $244,000.00 "," $314,615.00 "," $356,715.00 "," $636,957.00 ",," $1,813,537.00 ",
Other," $115,500.00 "," $98,171.76 "," $77,000.00 "," $40,800.00 "," $128,550.00 ",," $460,021.76 ",




2020:
Region,Account Type,NetBalance_sum
Attleboro/Taunton,Deposit,1608615918.92
Attleboro/Taunton,Loan,1106631023.65
South Coast,Deposit,439192149.71999997
South Coast,Loan,581232890.97
Rhode Island,Deposit,235707727.13
Rhode Island,Loan,441419753.47
Other,Deposit,0.0
Other,Loan,22018220.13



2021:
Region,Account Type,NetBalance_sum
Attleboro/Taunton,Deposit,1750593658.56
Attleboro/Taunton,Loan,1076544087.11
South Coast,Deposit,486256425.48
South Coast,Loan,588273517.84
Rhode Island,Deposit,258077676.75
Rhode Island,Loan,411824181.72
Other,Deposit,0.0
Other,Loan,13998442.81



2022:
Region,Account Type,NetBalance_sum
Attleboro/Taunton,Deposit,1594936398.93
Attleboro/Taunton,Loan,1253226462.19
South Coast,Deposit,552267175.18
South Coast,Loan,623830340.89
Rhode Island,Deposit,252917537.29
Rhode Island,Loan,444093307.37
Other,Deposit,0.0
Other,Loan,11570979.59



2023:
Attleboro/Taunton,Deposit,1691537612.21
Attleboro/Taunton,Loan,1284501915.5
South Coast,Deposit,534343926.29
South Coast,Loan,640067641.46
Rhode Island,Deposit,225298440.06
Rhode Island,Loan,420613579.39
Other,Deposit,0.0
Other,Loan,15358963.25


2024:
Region,Account Type,NetBalance_sum
Attleboro/Taunton,Deposit,1686588531.68
Attleboro/Taunton,Loan,1362871747.8799999
South Coast,Deposit,590446754.03
South Coast,Loan,659063602.77
Rhode Island,Deposit,232130668.73
Rhode Island,Loan,418885502.08
Other,Deposit,0.0
Other,Loan,14168398.56

Other fixes:
- Instead of 4 subplots, we should create each of these as their own PNG.
- The y-axis for the grants (needs to be adjusted to look at the range of the possible values for that individual region over the time period, plus some buffer on either side). For example, if grants go from 600k to 950k for Attleboro/Taunton region, we'd want to show this range somewhere between like 500k and 1200k. Some basic formula to determine this scale to capture the whole range.


----

John wants address
- collateral address to be the trump card
- if not, it can be the borrower address

Can be done. Becomes a bit more tricky because now you have to take property table (cleaned) - which I'm not sure if I have working with collateral, I have to check.
- From there, I can take zip codes and convert to region. Other comes into play there.

Single largest piece of collateral


This took like all day to do.
- Looks good though I think
- Integrate with PBI, as this is all matplotlib right now directly in python.


# 2025-09-15
Notebook based, have to try to get the collateral address
- challenging because I don't know if we have prop data going back that far.
- time travel with property data might be challenging, let's see.



