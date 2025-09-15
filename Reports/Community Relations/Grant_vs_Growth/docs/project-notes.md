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

I guess if the property ever existed, it probably isn't being cached. There is an account to property link.

Might be in good shape, assuming we never get rid of properties.

For each snapshot, we have account data.
- we can look at current prop table and prop link and create this.
- firt consolidate acct_prop linking to group by acctnbr and get the property with the highest appraisal value amt
- then we can append to the current daily snapshot, should be fine to use from there 

Ok, let's see how this looks after I build it


Zip code matching

# Normalize ZIPs to 5 digits (handles ints and ZIP+4)
z = (
    df['zipcd']
      .astype(str)
      .str.extract(r'(\d{5})', expand=False)
      .str.zfill(5)
)

# --- Rhode Island: ALL ZIPs from unitedstateszipcodes.org/ri/ ---
ri_zips = {
    '02801','02802','02804','02806','02807','02808','02809','02812','02813','02814',
    '02815','02816','02817','02818','02822','02823','02824','02825','02826','02827',
    '02828','02829','02830','02831','02832','02833','02835','02836','02837','02838',
    '02839','02840','02841','02842','02852','02854','02857','02858','02859','02860',
    '02861','02862','02863','02864','02865','02871','02872','02873','02874','02875',
    '02876','02877','02878','02879','02880','02881','02882','02883','02885','02886',
    '02887','02888','02889','02891','02892','02893','02894','02895','02896','02898',
    '02901','02902','02903','02904','02905','02906','02907','02908','02909','02910',
    '02911','02912','02914','02915','02916','02917','02918','02919','02920','02921','02940',
}

# --- ALL Bristol County, MA ZIPs (from unitedstateszipcodes.org/ma/) ---
# Includes Standard, PO Box, and Unique.
bristol_all = {
    '02031','02048','02334'
    '02356','02357','02375',
    '02702','02703','02712','02714','02715','02717','02718','02719',
    '02720','02721','02722','02723','02724',
    '02725','02726',
    '02740','02741','02742','02743','02744','02745','02746','02747','02748',
    '02760','02761','02763','02764','02766','02767','02768','02769',
    '02771','02777','02779','02780','02783','02790','02791',
}

# --- South Coast subset of Bristol County ---
# Defined as East Freetown & Assonet and everything south of them: Fall River,
# New Bedford, Dartmouth, Fairhaven, Acushnet, Somerset, Swansea, Westport (+ PO Box/Unique).
bristol_south_coast = {
    # Freetown
    '02702','02717',
    # Fall River (incl. PO Box)
    '02720','02721','02722','02723','02724',
    # Somerset
    '02725','02726',
    # Swansea
    '02777',
    # New Bedford (incl. PO Boxes)
    '02740','02741','02742','02744','02745','02746',
    # Dartmouth (incl. North/South + PO Box)
    '02747','02748','02714',
    # Fairhaven
    '02719',
    # Acushnet (and overlap ZIP that also covers NB)
    '02743',
    # Westport (incl. Westport Point PO Box)
    '02790','02791',
}

# --- Attleboro/Taunton subset = remaining Bristol County ZIPs ---
bristol_attleboro_taunton = bristol_all - bristol_south_coast

# --- Build the mapping dict in priority order ---
zip_region_map = {
    **{z: 'Rhode Island'      for z in ri_zips},
    **{z: 'South Coast'       for z in bristol_south_coast},
    **{z: 'Attleboro/Taunton' for z in bristol_attleboro_taunton},
}

# Map; anything not in RI or Bristol County buckets → 'Other'
df['Region'] = z.map(zip_region_map).fillna('Other')
```


----

New totals:

2020:
Region,Account Type,NetBalance_sum
Attleboro/Taunton,Deposit,1283329351.36
Attleboro/Taunton,Loan,561706669.78
Other,Deposit,335807280.83
Other,Loan,671630745.35
Rhode Island,Deposit,274046931.2
Rhode Island,Loan,531009913.66
South Coast,Deposit,390332232.38
South Coast,Loan,386954559.43

2021:
Region,Account Type,NetBalance_sum
Attleboro/Taunton,Deposit,1354851013.02
Attleboro/Taunton,Loan,508184138.72
Other,Deposit,412378122.03
Other,Loan,659102856.73
Rhode Island,Deposit,297490407.67
Rhode Island,Loan,537998738.38
South Coast,Deposit,430208218.07
South Coast,Loan,385354495.65

2022:
Region,Account Type,NetBalance_sum
Attleboro/Taunton,Deposit,1234648743.59
Attleboro/Taunton,Loan,527476376.64
Other,Deposit,385868985.44
Other,Loan,742140118.51
Rhode Island,Deposit,272669870.47
Rhode Island,Loan,629057054.01
South Coast,Deposit,506933511.9
South Coast,Loan,434047540.88


2023:
Region,Account Type,NetBalance_sum
Attleboro/Taunton,Deposit,1344039693.32
Attleboro/Taunton,Loan,508956474.41
Other,Deposit,372391911.03
Other,Loan,805851622.23
Rhode Island,Deposit,249830466.05
Rhode Island,Loan,604175380.77
South Coast,Deposit,484917908.16
South Coast,Loan,441558622.19


2024:
Region,Account Type,NetBalance_sum
Attleboro/Taunton,Deposit,1293358041.54
Attleboro/Taunton,Loan,500647400.35
Other,Deposit,428429855.78
Other,Loan,851957994.24
Rhode Island,Deposit,268775299.16
Rhode Island,Loan,623901471.37
South Coast,Deposit,518602757.96
South Coast,Loan,478482385.33

