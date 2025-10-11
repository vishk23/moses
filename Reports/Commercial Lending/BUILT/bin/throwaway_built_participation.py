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
from deltalake import DeltaTable
import pandas as pd
import cdutils.input_cleansing # type: ignore

# %%
accts = DeltaTable(src.config.SILVER / "account").to_pandas()

# %%
accts

# %%
acctuserfields = DeltaTable(src.config.BRONZE / "wh_acctuserfields").to_pandas()

# %%
acctuserfields

# %%
fpts = acctuserfields[acctuserfields['acctuserfieldcd'] == 'FPTS'].copy()

# %%
fpts

# %%
assert fpts['acctnbr'].is_unique, "Dupes"

# %%
fpts = fpts[[
    'acctnbr',
    'acctuserfieldvalue'
]].copy()

import cdutils.input_cleansing
fpts_schema = {
    'acctnbr':'str'
}

fpts = cdutils.input_cleansing.cast_columns(fpts, fpts_schema)

accts = accts.merge(fpts, how='left', on='acctnbr')

# %%
accts

# %%
mismatch_fpts = (
    ((accts['totalpctsold'] > 0) & (accts['acctuserfieldvalue'] != 'Y')) |
    ((accts['acctuserfieldvalue'] == 'Y') & (accts['totalpctsold'] <= 0))
)

mismatched_records = accts[mismatch_fpts]

print(f"Total mismatch: {len(mismatched_records)}")

# %%
mismatched_records

# %%
import cdutils.database.connect # type: ignore
from sqlalchemy import text # type: ignore
from datetime import datetime
from typing import Optional

# Define fetch data here using cdutils.database.connect
# There are often fetch_data.py files already in project if migrating

def fetch_invr():
    """
    Main data query
    """
    
    wh_invr = text(f"""
    SELECT
        a.ACCTNBR,
        a.ACCTGRPNBR,
        a.INVRSTATCD,
        a.PCTOWNED,
        a.ORIGINVRRATE,
        a.CURRINVRRATE,
        a.DATELASTMAINT
    FROM
        OSIBANK.WH_INVR a
    """)
    
    acctgrpinvr = text(f"""
    SELECT
        a.ACCTGRPNBR,
        a.INVRORGNBR
    FROM
        OSIBANK.ACCTGRPINVR a
    """)

    queries = [
        {'key':'wh_invr', 'sql':wh_invr, 'engine':1},
        {'key':'acctgrpinvr', 'sql':acctgrpinvr, 'engine':1},
    ]

    data = cdutils.database.connect.retrieve_data(queries)
    return data



# %%
# Get investor data
invr = fetch_invr()
wh_invr = invr['wh_invr'].copy()


acctgrpinvr = invr['acctgrpinvr'].copy()

# %%

base_customer_dim = DeltaTable(src.config.SILVER / "base_customer_dim").to_pandas()
base_customer_dim = base_customer_dim[[
    'customer_id',
    'customer_name'
]].copy()

# %%

wh_invr['acctgrpnbr'] = wh_invr['acctgrpnbr'].astype(str)


acctgrpinvr['acctgrpnbr'] = acctgrpinvr['acctgrpnbr'].astype(str)

import cdutils.customer_dim
acctgrpinvr = cdutils.customer_dim.orgify(acctgrpinvr, 'invrorgnbr')



# %%
acctgrpinvr

# %%
assert acctgrpinvr['acctgrpnbr'].is_unique, "Dupes"
# assert acctgrpinvr['customer_id'].is_unique, "Dupes"

# %%
merged_investor = wh_invr.merge(acctgrpinvr, on='acctgrpnbr', how='left').merge(base_customer_dim, on='customer_id', how='left')


# %%
merged_investor

# %%
merged_investor = merged_investor[merged_investor['invrstatcd'] == 'SOLD'].copy()

# %%
merged_investor = merged_investor.drop(columns=['datelastmaint']).copy()

# %%
merged_investor = merged_investor.rename(columns={
    'customer_name':'Participant Name'
}).copy()

# %%
merged_investor.info()

# %%
merged_investor_schema = {
    'acctnbr':'str'
}
merged_investor = cdutils.input_cleansing.cast_columns(merged_investor, merged_investor_schema)

# %%
merged_investor.describe()

# %%
merged_investor

# %%
# Filter down to minimal things that they would need to see
merged_investor = merged_investor[[
    'acctnbr',
    'pctowned',
    'Participant Name'
]].copy()

# %%
merged_investor

# %%
merged_investor['pctowned'] = pd.to_numeric(merged_investor['pctowned'])

# %%
merged_investor

# %%
# At this point, you could group by acctnbr and sum up pct owned. You could create a number of participants


