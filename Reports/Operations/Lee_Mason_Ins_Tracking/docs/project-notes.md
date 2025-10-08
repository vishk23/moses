# 2025-08-20

Picking this back up.

Real estate loans for ins tracking is the goal.

Resi, commercial, HE loans in a flood zone

---

I need Kelly to walk through filters and a few examples to get me to exactly where I need to get to on this.

---


Thank you. It also needs to only home equity loans that are in a flood zone. We will have a blanket policy for HE and will not need to track them unless they are in a flood zone.


# 2025-08-22

I was supposed to meet with Kelly, but I think things got busy on her end.

I'll work on this next week to bring to natural conclusion.
- there are assumptions and filters that I need her to check on. Sometimes, I don't know where things are in our uncataloged database.


# 2025-08-22

Most of the data is from account
- some accounts will have collateral
- some collateral will have insurance attached.
    - I think this is the link, but not sure


Account:
- acctnbr
- ownersortname
- Borrower_name_2 ?
    - NonTax Signator
- primary address (cleaned from BKM)
- primary city
- primary state
- primary zip
- notebal 
    - or bookbal
- creditlimitamt
- total exposure?
Collateral:
- Cleaned PropType
- proptypdesc
- Collateral type:
    - Real Esate/Auto/Misc?
- Prop street
- prop city
- prop state
- prop zip
Insurance:
- insurable value
- replacement cost
- flood zone
- coverage type
    - Hazard, flood, BPP, Auto
- premium escrowed
    - Yes/No
- loan type
    - Resi/Commercial
    - major or some form of product mapping
- building type?
    - residential/commercial/condo/mobile home/land
    - isn't this collateral type
        - proptypdesc



----
# 2025-08-28

Questions for Kelly

On account table, do we only want accounts where there is an active insurance policy?

Commercial (CML/MLN)
Resi (MTG)
- HE only in flood zone?
    - These are a subset of MTG


Chad Business
- 123
    

L&M track every property end goal

4 types of home equity

Doesn't need PMI

If there is no property, don't include loan

coverageamt is the same for insurable value + replacement cost


----
# 2025-08-29

HELOCs

MG52
MG55
MG48
MG71

Finished up v2 of this. It's all in notebook

Did pretty deep analysis of this and put together a lot in the data lakehouse for reusable tables in the process.

# 2025-10-07

Need to get this revision done by EOD

```text
I finally had a chance to review this draft file. Yes, please remove collateral for UCC’s and Assignments.  I made notes on the top of the file for you. The red font columns can be deleted.

 

We need to include an HELOC or Home Equity loans that are in a flood zone or escrowed.
```

Above is message from Kelly

I think HE loans are in there.


Collateral_Type	Loan_Number_nunique
1 Family Residential - Own Occ	2865
All Business Assets	494
UCC - ABA	442
Vehicle - Used	419
1-4 Fam Res - Non Own Occ	361
Condominium	316
Vehicle - New	314
Real Estate - Business	304
Assignment of Leases/Rents	172
UCC Filing / Assignment	157
Multi Family	137
2 Family Residential - Own Occ	128
Real Estate - Bus&Bus Assets	79
Unsecured	73
Vehicle - Business	67
Land - Unimproved	66
Office- General	63
Mixed Use (Retail/Residential)	48
3 Family Residential - Own Occ	47
Equipment	44
Industrial	43
Commercial - Other	42
UCC- of Future Income	42
General Retail	40
Restaurant	35
Warehouse	32
Strip Plaza	23
UCC of Fee Income	21
UCC- Equipment	21
Apartment Building	17
Bus Assets w/Accts Receivable	17
Manufacturing	16
Hotel/Motel	16
Mixed Use (Retail/Office)	15
Land - Improved	15
Bus Assets w/Accts Rcvb & Inv	15
Business Assets w/Equipment	14
Boat	13
Office - Medical	13
Office - Professional	12
Assignment Licenses/Permits	12
Passbook/Savings Secured	11
Gas Station and Convenience St	10
Certificate of Deposit	10
Cash Surrender Value Life Ins	10
Self Storage	9
Autobody/Gas Station	8
Parking Lot	8
Shopping Plaza	8
4 Family Residential - Own Occ	7
Day Care	6
Auto-Truck Repair	6
Retail - Big Box Store	5
Real Estate - Personal & Bus	5
Marketable Securities	5
UCC- Receivables	5
Church	4
Golf Course	4
Solar Farm	4
Outdoor Dealers	4
Real Estate - Pers&Bus Assets	4
Mortgage - Other	4
Other	4
Indoor Recreational	3
Hospitality/Event Space	3
Marina	3
Assign of Developers Rights	3
Assisted Living	3
Campground	3
Seafood Processing Plant	3
SBA Loan	3
Funeral Home	3
Mixed Use (Office/Residential)	3
Dealership	3
Accounts Receivable	2
Assign of Fishing Lic & Permit	2
Car Wash	2
General Contractor	2
Educational Facilities	2
Outdoor Recreation	2
Savings - Partially Secured	2
Classic Auto	1
Assignment of Tax Credits	1
Inventory	1
Dry Cleaner/Laundromat	1
Mobile Home - New	1
Lease Hold Mortgage	1
Margin Related Collateral	1
Key Person LIfe Insurance	1
Security Agreement	1
Stock	1
UCC - Heat Loan	1
Vessel	1

Exclude anything with:
All Business Assets
UCC
Assign
Land
Vehicle
Equipment
Bus Assets w/Acct Receivable
Bus Assets
Boat
Passbook
Certificate of Deposit
Cash Life Insurance
Parking Lot
Marketable Securities
Accounts Receivable
Savings
Classic Auto
Inventory
Mobile Home
Lease Hold Mortgage
Key Person life insurance
security agreement
stock
Vessel



# List of terms to exclude (case insensitive)
exclude_terms = [
    "All Business Assets",
    "UCC",
    "Assign",
    "Land",
    "Vehicle",
    "Equipment",
    "Bus Assets w/Acct Receivable",
    "Bus Assets",
    "Boat",
    "Passbook",
    "Certificate of Deposit",
    "Cash Life Insurance",
    "Parking Lot",
    "Marketable Securities",
    "Accounts Receivable",
    "Savings",
    "Classic Auto",
    "Inventory",
    "Mobile Home",
    "Lease Hold Mortgage",
    "Key Person life insurance",
    "security agreement",
    "stock",
    "Vessel"
]

# Function to check if any exclude term is in the collateral type (case insensitive)
def should_exclude(collateral_type):
    ct_lower = collateral_type.lower()
    return any(term.lower() in ct_lower for term in exclude_terms)

# Apply the filter
filtered_df = df[~df['Collateral_Type'].apply(should_exclude)]


# 2025-10-08

Sent v2 to Kelly yesterday

A couple tweaks to make
- Esrow didn't come through correctly, fix
    - done
- If HE minors, line should be one (for prop) if floodzone = 'X', else we null it out, for other MTG and CML fields
    - 
- participations bought excluded
    - ACCTUSERFIELDS
        - PARP - Purchased/Bought (boolean)
        - PAPU - Purchased %

FPTS is sold?
- Should check this
- separate topic, outside scope here
    - not as reliable as totalpctsold.
    - not as well maintained of a field. Some where totalpctsold and no flag


Logic for final piece:
# Filter out HE records where flood zone = 'X'
heloc_minors = ['MG52','MG55','MG48','MG71']

# if record in cleaned df['currmiaccttypcd'].isin(heloc_minors) and cleaned_df['Flood_Zone'] contains X , or TBD, or B, or C (case insensitive)
# then drop the record

# Afterward: Next operation is to set anything in floodzone that contains contains X , or TBD, or B, or C (case insensitive) to None

```python
import pandas as pd

# Assuming cleaned_df is your DataFrame with columns 'currmiaccttypcd' and 'Flood_Zone'

# Define the list of heloc_minors
heloc_minors = ['MG52', 'MG55', 'MG48', 'MG71']

# Regex pattern to match 'X', 'TBD', 'B', or 'C' case-insensitively as substrings
flood_zone_pattern = r'(?i)(X|TBD|B|C)'

# Step 1: Drop rows where 'currmiaccttypcd' is in heloc_minors 
# AND 'Flood_Zone' contains one of the specified strings
mask_to_drop = (
    cleaned_df['currmiaccttypcd'].isin(heloc_minors) & 
    cleaned_df['Flood_Zone'].str.contains(flood_zone_pattern, na=False)
)
cleaned_df = cleaned_df[~mask_to_drop]

# Step 2: Set 'Flood_Zone' to None where it contains one of the specified strings
cleaned_df.loc[cleaned_df['Flood_Zone'].str.contains(flood_zone_pattern, na=False), 'Flood_Zone'] = None
```

C:\Users\w322800\AppData\Local\Temp\ipykernel_23660\3142456051.py:13: UserWarning: This pattern is interpreted as a regular expression, and has match groups. To actually get the groups, use str.extract.
  cleaned_df['Flood_Zone'].str.contains(flood_zone_pattern, na=False)
C:\Users\w322800\AppData\Local\Temp\ipykernel_23660\3142456051.py:18: UserWarning: This pattern is interpreted as a regular expression, and has match groups. To actually get the groups, use str.extract.
  cleaned_df.loc[cleaned_df['Flood_Zone'].str.contains(flood_zone_pattern, na=False), 'Flood_Zone'] = None