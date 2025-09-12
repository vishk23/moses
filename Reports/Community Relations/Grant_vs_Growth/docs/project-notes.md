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
