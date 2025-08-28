# 2025-08-25

building off previous system of golden parquet file, just use the delta lake architecture to be the standard layer to store data. Much better with obj storage with ACID transaction support and time travel.

This is the way forward


Currently pausing this. Issue with delta-rs and windows path
- monitor


# 2025-08-27
Added several new tables here

Couple issues on dtypes


# 2025-08-28
Prop cleaning

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
os.environ['REPORT_ENV'] = 'prod'

# %%
import src.config
from deltalake import DeltaTable
from pathlib import Path
import pandas as pd


# %%
# TABLE_PATH = src.config.BRONZE / "metadata_lookup_engine1"
TABLE_PATH = src.config.SILVER / "account"


# %%
account = DeltaTable(TABLE_PATH).to_pandas()

# %%
account

# %%
TABLE_PATH = src.config.BRONZE / "acctpropins"
acctpropins = DeltaTable(TABLE_PATH).to_pandas()

# %%
acctpropins

# %%
TABLE_PATH = src.config.BRONZE / "wh_inspolicy"
wh_inspolicy = DeltaTable(TABLE_PATH).to_pandas()


# %%
wh_inspolicy['instypdesc'].unique()

# %%
wh_inspolicy

# %%
TABLE_PATH = src.config.BRONZE / "wh_prop"
prop = DeltaTable(TABLE_PATH).to_pandas()
prop

# %%
prop['CompositeKey'] = prop['acctnbr'].astype(str) + prop['propnbr'].astype(str)
assert prop['CompositeKey'].is_unique, "Duplicate records"

# %%
TABLE_PATH = src.config.BRONZE / "wh_prop2"
prop2 = DeltaTable(TABLE_PATH).to_pandas()
prop2

# %%
prop2['CompositeKey'] = prop2['acctnbr'].astype(str) + prop2['propnbr'].astype(str)
assert prop2['CompositeKey'].is_unique, "Duplicate records"


