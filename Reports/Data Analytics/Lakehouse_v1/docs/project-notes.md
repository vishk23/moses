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


----

You are absolutely right. My apologies for jumping ahead to the deduplication step. Merging the tables first is a much better approach to unify the schemas.

Using an **outer join on the composite key (`acctnbr`, `propnbr`)** is the correct way to combine all available information from both `wh_prop` and `wh_prop2`. This ensures that you create a single, wide record for each unique account-property link, pulling in all columns from both tables.

Let's walk through that superior approach.

### The Challenge of the Merge

When you merge `wh_prop` and `wh_prop2`, you'll notice they share column names beyond the keys (e.g., if both tables had a `last_updated` column). `pandas.merge` handles this by adding suffixes (like `_x` and `_y`) to the duplicate column names. We will then need to *coalesce* these columns—that is, take the value from the `_x` column, and if it's null, take the value from the `_y` column.

This process gives us a complete, flattened table representing every account-property link with all available data.

### Revised Strategy

1.  **Full Outer Join:** Merge `wh_prop` and `wh_prop2` using a `full outer` join. This type of join keeps all records from both tables [builtin.com](https://builtin.com/articles/sql-merge-two-tables). We'll join on the composite key `['acctnbr', 'propnbr']`.
2.  **Coalesce Columns:** For any columns that were present in both tables and now have `_x` and `_y` suffixes, create a single new column by taking the non-null value from either one. We can prioritize one source (e.g., `wh_prop2`) if both have data.
3.  **Build Two Silver Tables:** This merged table is incredibly valuable, but as you noted, `propnbr` is still not unique. This leads us to a best-practice Medallion architecture solution: create **two** distinct tables in the Silver layer.
    *   `property`: A conformed dimension table where `propnbr` **is the unique primary key**. This is the table you originally wanted. We create it by deduplicating the merged data on `propnbr`.
    *   `account_property_link`: A **linking table** that preserves the many-to-many relationship, containing just `acctnbr` and `propnbr`.

This approach gives you both a clean, unique list of properties *and* a clean way to represent their relationships to accounts.

---

### Step-by-Step Implementation (Revised)

```python
# %% [markdown]
# ### 1. Setup and Load Data (Same as before)
# ... (Assuming setup and data loading code is here) ...
import pandas as pd
from deltalake import DeltaTable, write_deltalake
import os
import src.config
# ... (load prop and prop2 into pandas DataFrames) ...

# For demonstration, let's ensure we have the data loaded.
prop_path = src.config.BRONZE / "wh_prop"
prop = DeltaTable(prop_path).to_pandas()
prop2_path = src.config.BRONZE / "wh_prop2"
prop2 = DeltaTable(prop2_path).to_pandas()

# %% [markdown]
# ### 2. Full Outer Join on Composite Key
# Merge `wh_prop` and `wh_prop2` to create a single, wide DataFrame.
# This combines all columns for each unique `(acctnbr, propnbr)` pair.

# %%
# Using a full outer join on the composite key
# 'how="outer"' ensures we keep all records from both tables.
# The suffixes will be added to any columns that exist in both DataFrames (excluding the join keys).
merged_props = pd.merge(
    prop,
    prop2,
    how='outer',
    on=['acctnbr', 'propnbr'],
    suffixes=('_prop', '_prop2') # Use clear suffixes
)

print(f"Merged table has {len(merged_props)} records and {len(merged_props.columns)} columns.")
merged_props.info()


# %% [markdown]
# ### 3. Coalesce Duplicate Columns
# After the merge, we might have columns like `some_col_prop` and `some_col_prop2`.
# We need to combine them into a single `some_col`.

# %%
# This is a generic function to perform the coalesce operation.
def coalesce_columns(df, suffix1, suffix2):
    """
    Identifies columns with suffixes, creates a new coalesced column,
    and drops the old ones. It prioritizes the column with suffix2.
    """
    df_copy = df.copy()
    # Find all columns that have the first suffix
    cols1 = [c for c in df_copy.columns if c.endswith(suffix1)]
    
    for col1 in cols1:
        # Get the base column name and the corresponding column with the second suffix
        base_name = col1.removesuffix(suffix1)
        col2 = f"{base_name}{suffix2}"
        
        if col2 in df_copy.columns:
            # Create the new coalesced column.
            # It takes the value from col2 first, and if that is null, it takes the value from col1.
            df_copy[base_name] = df_copy[col2].fillna(df_copy[col1])
            
            # Drop the old suffixed columns
            df_copy = df_copy.drop(columns=[col1, col2])
            print(f"Coalesced '{base_name}' from '{col1}' and '{col2}'.")
            
    return df_copy

# Apply the function to our merged data
coalesced_data = coalesce_columns(merged_props, suffix1='_prop', suffix2='_prop2')
print("\nData after coalescing columns:")
coalesced_data.info()


# %% [markdown]
# ### 4. Create the Silver Layer Tables
# From our clean, coalesced data, we now create our two target tables.

# %%
# Step 4.1: Create the linking table (trivial)
# This table just preserves the many-to-many relationship keys.
account_property_link = coalesced_data[['acctnbr', 'propnbr']].copy()
account_property_link = account_property_link.drop_duplicates().reset_index(drop=True)

print(f"Created `account_property_link` table with {len(account_property_link)} unique links.")

# Step 4.2: Create the conformed `property` dimension table
# To do this, we must deduplicate based on `propnbr`.
# We need a business rule. Let's assume a property record linked to a higher `acctnbr`
# is more recent or important. This is an arbitrary choice for demonstration.
# In a real scenario, you would use a modification date or source system priority.
master_property = coalesced_data.sort_values(by='acctnbr', ascending=False)
master_property = master_property.drop_duplicates(subset=['propnbr'], keep='first')

# The property table should not contain the account number, as that link is now separate.
master_property = master_property.drop(columns=['acctnbr'])
master_property = master_property.reset_index(drop=True)

print(f"Created master `property` table with {len(master_property)} unique properties.")
assert master_property['propnbr'].is_unique, "propnbr is not unique in the master property table!"
print("Assertion Passed: `propnbr` is a unique key for the property table.")


# %% [markdown]
# ### 5. Write Both Tables to the Silver Layer

# %%
# Define paths
SILVER_PROPERTY_PATH = src.config.SILVER / "property"
SILVER_LINK_PATH = src.config.SILVER / "account_property_link"
os.makedirs(SILVER_PROPERTY_PATH, exist_ok=True)
os.makedirs(SILVER_LINK_PATH, exist_ok=True)

# Write the conformed property table
print(f"Writing {len(master_property)} records to silver table: {SILVER_PROPERTY_PATH}")
write_deltalake(SILVER_PROPERTY_PATH, master_property, mode='overwrite', overwrite_schema=True)

# Write the linking table
print(f"Writing {len(account_property_link)} records to silver table: {SILVER_LINK_PATH}")
write_deltalake(SILVER_LINK_PATH, account_property_link, mode='overwrite', overwrite_schema=True)

print("\nSuccessfully created and wrote both `property` and `account_property_link` tables.")
```


---

Building silver table for properties

there is proptypecd and proptypcd
- proptypecd is incomplete so we'll use the latter as the golden record


----

Need to create silver table for insurance data too


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
assert acctpropins['intrpolicynbr'].is_unique, "Dupes"

# %%
acctpropins['CompositeKey'] = acctpropins['propnbr'].astype(str) + acctpropins['intrpolicynbr'].astype(str)

# %%
assert acctpropins['CompositeKey'].is_unique, "Dupes"

# %%
acctpropins['CompositeKey'] = acctpropins['propnbr'].astype(str) + acctpropins['intrpolicynbr'].astype(str) + acctpropins['acctnbr'].astype(str)

# %%
assert acctpropins['CompositeKey'].is_unique, "Dupes"

# %%
TABLE_PATH = src.config.BRONZE / "wh_inspolicy"
wh_inspolicy = DeltaTable(TABLE_PATH).to_pandas()


# %%
wh_inspolicy

# %%
assert wh_inspolicy['intrpolicynbr'].is_unique, "Dupes"

# %%
# Passes
