

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


---

You've nailed the analysis again. Your exploration in the notebook reveals the exact relationships, and your proposed strategy is perfectly aligned with the Medallion Architecture principles we've been using.

The key insight is your last `assert`: the combination of `acctnbr` + `propnbr` + `intrpolicynbr` is the unique composite key for the `acctpropins` table. This confirms `acctpropins` is a **three-way linking table** that connects accounts, properties, and insurance policies.

Your strategy is spot-on:

1.  **Join:** Combine `acctpropins` with `wh_inspolicy` to get all available data in one place.
2.  **Separate:** Split the combined data into two clean Silver tables: a conformed `insurance_policy` dimension table and a linking table.
3.  **Deduplicate:** Ensure the final `insurance_policy` table has `intrpolicynbr` as its unique primary key.

Let's build this out.

---

### Step-by-Step Implementation

We'll create two new Silver tables:

*   `insurance_policy`: A conformed dimension table where `intrpolicynbr` is the unique primary key, containing all descriptive details of a policy.
*   `account_property_insurance_link`: A link table containing only the keys (`acctnbr`, `propnbr`, `intrpolicynbr`) to represent the relationships.

```python
# %% [markdown]
# ### 1. Setup and Load Bronze Data
# Assuming setup is done. We'll load the two Bronze tables related to insurance.

# %%
import pandas as pd
from deltalake import DeltaTable, write_deltalake
import src.config
import os

# Load the source tables
acctpropins_path = src.config.BRONZE / "acctpropins"
acctpropins = DeltaTable(acctpropins_path).to_pandas()
print(f"Loaded {len(acctpropins)} records from acctpropins.")

inspolicy_path = src.config.BRONZE / "wh_inspolicy"
wh_inspolicy = DeltaTable(inspolicy_path).to_pandas()
print(f"Loaded {len(wh_inspolicy)} records from wh_inspolicy.")


# %% [markdown]
# ### 2. Join Insurance Data
# We'll perform a left join from `acctpropins` (the linking table) to `wh_inspolicy` (the details table).
# This enriches each link with the details of the corresponding policy.

# %%
# A left join is perfect here. We want to keep every link from `acctpropins`
# and attach the policy details from `wh_inspolicy`.
full_insurance_data = pd.merge(
    acctpropins,
    wh_inspolicy,
    on='intrpolicynbr',
    how='left',
    suffixes=('_link', '_policy') # Add suffixes in case of any other overlapping column names
)

print("Joined `acctpropins` and `wh_inspolicy`.")
print(f"Resulting table has {len(full_insurance_data)} rows.")
full_insurance_data.info()


# %% [markdown]
# ### 3. Create the Silver Layer Tables
# Now we'll split the joined data into our two target tables: the conformed dimension and the linking table.

# %%
# Step 3.1: Create the conformed `insurance_policy` table.
# This table should only contain information about the policy itself.
# We start with the full data, then deduplicate to ensure one row per policy.

# Select all columns that are policy-specific. This includes all columns from the original
# `wh_inspolicy` table plus any that were in `acctpropins` but are attributes of the policy.
# For this example, let's assume all columns from 'wh_inspolicy' are the master details.
policy_cols = wh_inspolicy.columns.tolist()
silver_insurance_policy = full_insurance_data[policy_cols].copy()

# Critical step: Drop duplicates to ensure `intrpolicynbr` is a unique primary key.
silver_insurance_policy = silver_insurance_policy.drop_duplicates(subset=['intrpolicynbr']).reset_index(drop=True)

print(f"Created `insurance_policy` table with {len(silver_insurance_policy)} unique policies.")
assert silver_insurance_policy['intrpolicynbr'].is_unique, "Policy Number is not unique!"
print("Assertion Passed: `intrpolicynbr` is a unique key for the insurance_policy table.")


# %%
# Step 3.2: Create the `account_property_insurance_link` table.
# This table's only job is to connect the three entities.

link_cols = ['acctnbr', 'propnbr', 'intrpolicynbr']
account_property_insurance_link = full_insurance_data[link_cols].copy()

# The composite key should already be unique, but it's best practice to confirm.
account_property_insurance_link = account_property_insurance_link.drop_duplicates().reset_index(drop=True)

print(f"Created `account_property_insurance_link` table with {len(account_property_insurance_link)} unique links.")


# %% [markdown]
# ### 4. Write Both Tables to the Silver Layer

# %%
# Define paths
SILVER_INSURANCE_PATH = src.config.SILVER / "insurance_policy"
SILVER_INSURANCE_LINK_PATH = src.config.SILVER / "account_property_insurance_link"
os.makedirs(SILVER_INSURANCE_PATH, exist_ok=True)
os.makedirs(SILVER_INSURANCE_LINK_PATH, exist_ok=True)

# Write the conformed policy dimension table
print(f"Writing {len(silver_insurance_policy)} records to silver table: {SILVER_INSURANCE_PATH}")
write_deltalake(SILVER_INSURANCE_PATH, silver_insurance_policy, mode='overwrite', overwrite_schema=True)

# Write the new three-way linking table
print(f"Writing {len(account_property_insurance_link)} records to silver table: {SILVER_INSURANCE_LINK_PATH}")
write_deltalake(SILVER_INSURANCE_LINK_PATH, account_property_insurance_link, mode='overwrite', overwrite_schema=True)

print("\nSuccessfully created and wrote both insurance-related silver tables.")

```

### Putting It All Together: A Powerful Gold Table

The beauty of this model is its flexibility. If you wanted to create a Gold-level table showing accounts with their properties and all associated insurance policies, you can now do so with a series of clean joins:

```python
# This is a conceptual example of how you'd use the new tables

# Load all the necessary Silver tables
account = DeltaTable(src.config.SILVER / "account").to_pandas()
prop = DeltaTable(src.config.SILVER / "property").to_pandas()
account_prop_link = DeltaTable(src.config.SILVER / "account_property_link").to_pandas()
insurance_policy = DeltaTable(src.config.SILVER / "insurance_policy").to_pandas()
insurance_link = DeltaTable(src.config.SILVER / "account_property_insurance_link").to_pandas()

# Join accounts to their properties
gold_table = account.merge(account_prop_link, on='acctnbr', how='left') \
                    .merge(prop, on='propnbr', how='left')

# Now, join that result with the insurance information
gold_table = gold_table.merge(insurance_link, on=['acctnbr', 'propnbr'], how='left') \
                       .merge(insurance_policy, on='intrpolicynbr', how='left')

# The `gold_table` is now a fully denormalized view ready for analysis.
# Its grain is (acctnbr, propnbr, intrpolicynbr).
```


----

Excellent question. You've hit on a fundamental best practice for building reliable data warehouses and data lakehouses.

Adding a load timestamp to every record you write to the Silver and Gold layers is crucial for auditing, debugging, and versioning. Let's create a robust function for this, paying special attention to your requirement of handling pre-existing `effdate` columns.

### The Problem: Business Date vs. Load Date

You correctly identified that an `effdate` from a source system is different from the timestamp when you write to your tables. This is a critical distinction:

*   **Business Effective Date (`source_effdate`):** The date/time when a fact became true in the real world (e.g., when a policy started, when an address was updated). This comes *from the source data*.
*   **Load Timestamp:** The date/time when your ETL/ELT pipeline processed the record and loaded it into the target table (e.g., your Silver `property` table). This is *metadata you add*.

Overwriting or confusing these two can lead to a loss of valuable information. The best practice is to **name the new column unambiguously** to avoid this conflict. A name like `load_timestamp_utc` is ideal because it's explicit about what it is and its timezone.

### Recommended Function: `add_load_timestamp`

This function adds a new column with a clear name, `load_timestamp_utc`, and preserves any existing `effdate` column. This is the safest and most robust approach.

```python
import pandas as pd
from typing import Optional

def add_load_timestamp(
    df: pd.DataFrame, 
    col_name: str = "load_timestamp_utc"
) -> pd.DataFrame:
    """
    Adds a column with the current UTC timestamp to a DataFrame.

    This function is idempotent and safe to run on any DataFrame. If the
    specified column name already exists, it will be overwritten with the
    new timestamp. It does not affect any other columns.

    Args:
        df: The pandas DataFrame to modify.
        col_name: The name for the new timestamp column. 
                  Defaults to 'load_timestamp_utc'.

    Returns:
        A new DataFrame with the added timestamp column.
    """
    df_copy = df.copy()
    df_copy[col_name] = pd.Timestamp.now(tz='UTC')
    return df_copy
```

---

### How to Use It in Your Workflow

Integrating this into your pipeline is now clean and simple. You would call it right before writing any DataFrame to the Silver or Gold layer.

#### Example 1: DataFrame **without** an existing `effdate`

```python
# Assume 'silver_property' is your DataFrame ready for writing
# It does NOT have an 'effdate' column
print("--- Before adding timestamp ---")
print(silver_property.head(2))

# Add the load timestamp
silver_property_final = add_load_timestamp(silver_property)

print("\n--- After adding timestamp ---")
print(silver_property_final.head(2))
# You'll see a new 'load_timestamp_utc' column has been added.

# Now write the final DataFrame to Delta Lake
# write_deltalake(SILVER_PROPERTY_PATH, silver_property_final, ...)
```

#### Example 2: DataFrame **with** an existing `effdate`

```python
# Let's create a dummy DataFrame that has a source 'effdate'
data = {'policy_id': [1, 2], 'effdate': ['2022-01-01', '2023-05-10']}
some_policy_df = pd.DataFrame(data)
some_policy_df['effdate'] = pd.to_datetime(some_policy_df['effdate'])

print("--- Before adding timestamp ---")
print(some_policy_df.head())

# Add the load timestamp
policy_df_final = add_load_timestamp(some_policy_df)

print("\n--- After adding timestamp ---")
print(policy_df_final.head())
# Notice 'effdate' is preserved, and 'load_timestamp_utc' is added.
```

### Alternative Function: Renaming the Source Column

If you absolutely must name your new load timestamp column `effdate`, you first need to rename the existing one. This function handles that logic.

**Use this approach with caution**, as renaming columns can sometimes break downstream dependencies if they expect the original column name.

```python
def add_effdate_and_rename_source(
    df: pd.DataFrame, 
    source_col_name: str = "effdate",
    new_load_col_name: str = "effdate",
    renamed_source_prefix: str = "source_"
) -> pd.DataFrame:
    """
    Adds a load timestamp, renaming any existing column with the same name.

    Args:
        df: The DataFrame to modify.
        source_col_name: The name of the column to check for (e.g., 'effdate').
        new_load_col_name: The name for the new load timestamp column.
        renamed_source_prefix: The prefix to add to the renamed source column.

    Returns:
        A new DataFrame with the added timestamp and potentially renamed column.
    """
    df_copy = df.copy()
    
    # Check if the source column exists
    if source_col_name in df_copy.columns:
        renamed_col = f"{renamed_source_prefix}{source_col_name}"
        print(f"'{source_col_name}' found. Renaming to '{renamed_col}'.")
        df_copy.rename(columns={source_col_name: renamed_col}, inplace=True)
        
    # Add the new load timestamp column
    df_copy[new_load_col_name] = pd.Timestamp.now(tz='UTC')
    return df_copy

# --- Example Usage ---
# policy_df_final = add_effdate_and_rename_source(some_policy_df)
# print(policy_df_final)
# Output would have columns: [policy_id, source_effdate, effdate]
```

----



2025-08-28 16:17:35 | INFO | === REPORT RUNNER SESSION START [PROD MODE] ===
2025-08-28 16:17:35 | INFO | DISCOVERY COMPLETE | Found 36 reports | Environment: PROD
2025-08-28 16:17:35 | INFO | BATCH START | 1 reports | Filter: name = Lakehouse_v1 | Environment: PROD
2025-08-28 16:17:35 | INFO | START | Lakehouse Transformation | Business Line: Data Analytics | Environment: PROD
2025-08-28 16:17:35 | INFO | DEBUG | Python executable: C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Scripts\python.exe
2025-08-28 16:17:35 | INFO | DEBUG | Working directory: Reports\Data Analytics\Lakehouse_v1
2025-08-28 16:17:35 | INFO | DEBUG | Command: C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Scripts\python.exe -m src.main
2025-08-28 16:32:40 | ERROR | FAILED | Lakehouse Transformation | Runtime: 15.08 minutes
2025-08-28 16:32:40 | ERROR | Python executable: C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Scripts\python.exe
2025-08-28 16:32:40 | ERROR | Working directory: Reports\Data Analytics\Lakehouse_v1
2025-08-28 16:32:40 | ERROR | Return code: 1
2025-08-28 16:32:40 | ERROR | STDERR:
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Data Analytics\Lakehouse_v1\src\main.py", line 36, in <module>
    main()
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Data Analytics\Lakehouse_v1\src\main.py", line 31, in main
    src.silver.core.generate_silver_tables()
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Data Analytics\Lakehouse_v1\src\silver\core.py", line 63, in generate_silver_tables
    insurance, acct_prop_ins_link = src.silver.insurance.generate_insurance_table()
                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Data Analytics\Lakehouse_v1\src\silver\insurance.py", line 24, in generate_insurance_table
    insurance_policy = insurance_policy.drop(columns=['acctnbr','propnbr']).copy()
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\frame.py", line 5588, in drop
    return super().drop(
           ^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\generic.py", line 4807, in drop
    obj = obj._drop_axis(labels, axis, level=level, errors=errors)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\generic.py", line 4849, in _drop_axis
    new_axis = axis.drop(labels, errors=errors)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\indexes\base.py", line 7136, in drop
    raise KeyError(f"{labels[mask].tolist()} not found in axis")
KeyError: "['acctnbr', 'propnbr'] not found in axis"
2025-08-28 16:32:40 | ERROR | STDOUT:
Running v1.0.0-prod
Running Lakehouse Transformation for Data Team
Schedule: Daily
Owner: Chad Doorley
Environment: prod
Start bronze table generation
No all-null columns found. Returning original dataframe
Start account
Successfully wrote account data
Starting address ...
Successfully wrote address data
Starting property ...
Coalesced 'rundate' from 'rundate_prop' and 'rundate_prop2'.
Coalesced 'nbrofunits' from 'nbrofunits_prop' and 'nbrofunits_prop2'.
Coalesced 'datelastmaint' from 'datelastmaint_prop' and 'datelastmaint_prop2'.
Coalesced 'load_timestamp_utc' from 'load_timestamp_utc_prop' and 'load_timestamp_utc_prop2'.

Data after coalescing columns:
Created `account_property_link` table with 85845 unique links.
Created master `property` table with 85672 unique properties.
Assertion Passed: `propnbr` is a unique key for the property table.
No all-null columns found. Returning original dataframe
Successfully wrote property data
Starting property ...
2025-08-28 16:32:40 | INFO | BATCH COMPLETE | Total: 1 | Successful: 0 | Failed: 1 | Batch Runtime: 15.08 minutes
2025-08-28 16:32:40 | INFO | === REPORT RUNNER SESSION END ===


# 2025-09-07
Noticed that fields are being weird when converted directly from oracle DB to parquet. An example is my bronze table. I noticed looking at my noteintrate field on wh_acctcommon

TODO:
- [ ] Fix datatypes in DeltaTables
    - noteintrate and certain other fields come out weird without running through a numeric test or something. I think they are objects by default
    - vishnu might already have solution to this

Or we can just handle. Might be better pattern to read in as is, no manipulations. From there, when building silver and gold tables, we transform and get them ready for use. Data cleaning stage.



# 2025-09-09

We shouldn't be reading anything from bronze for reporting. I can as one off, but I'll have to go back and fix. I think it makes more sense to really build all the things you'd need from silver tables and then create gold tables from there too.
- this will be the overarching structure that will eat the old repository structure slowly.

Somethings will be lightweight and sit outside of that. Or maybe not. Maybe it all goes in there.

# 2025-09-23
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Data Analytics\Lakehouse_v1\src\main.py", line 36, in <module>
    main()
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Data Analytics\Lakehouse_v1\src\main.py", line 27, in main
    src.bronze.core.generate_bronze_tables()
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Data Analytics\Lakehouse_v1\src\bronze\core.py", line 98, in generate_bronze_tables
    write_deltalake(WH_PROP2_PATH, wh_prop2, mode='overwrite', schema_mode='merge')
  File "C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\deltalake\writer\writer.py", line 125, in write_deltalake 
    table._table.write(
_internal.SchemaMismatchError: Schema error: Cannot merge field marginpct from Decimal128(7, 6) to Decimal128(5, 4)
Schema error: Cannot merge field marginpct from Decimal128(7, 6) to Decimal128(5, 4)

Failure this morning with updating lakehouse
- fixing by overwriting existing schema. Need to handle data types more explicitly. Upstream change can't break my system


# 2025-09-24
CustomerDim

Objective:
- provide a clear way 

Fields:
customer_id: O+orgnbr or P+persnbr
customer_name: ownersortname
first_name: only for person
last_name: only for person
is_active: boolean
customer_since: date of first acct opened
unique_loan_accts: # of loan accts
unique_deposit_accts: # of deposit accts
loan_balance: $ net balance for loans
loan_exposure: $ total loan exposure
deposit_balance: $ net balance for deposits
taxid: taxid
dob: date of birth
dod: date of death
age: calculated field, current day - dob
deceased: boolean, if age >= 110, set to True
loan_officer: mode of loan officers, else null
acct_officer: mode of deposit officers, else null

---

AccountDim

Objective:
- Provide a clear 

product
