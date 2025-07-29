# View Table Merge Example

This notebook demonstrates the new functionality to merge vieworgtaxid and viewperstaxid tables with the main org/pers tables early in the ETL process.

## Setup

```python
import os, sys
from pathlib import Path
import pandas as pd

# Change to project root and add to Python path
project_root = Path.cwd().parent
os.chdir(project_root)
sys.path.insert(0, str(project_root))

from src.data_quality.core import merge_org_with_view_taxid, merge_pers_with_view_taxid
```

## Example: Organization Tax ID Updates

```python
# Sample WH_ORG data
wh_org = pd.DataFrame({
    'orgnbr': [1001, 1002, 1003],
    'orgname': ['Acme Corp', 'Beta Inc', 'Gamma LLC'],
    'taxid': ['11-1111111', '22-2222222', '33-3333333'],
    'taxidtypcd': ['FEIN', 'FEIN', 'FEIN'],
    'orgtypcddesc': ['Corporation', 'Corporation', 'LLC']
})

print("Original WH_ORG:")
print(wh_org)
```

```python
# Sample VIEWORGTAXID data with updates
vieworgtaxid = pd.DataFrame({
    'orgnbr': [1001, 1002],  # Only updating first two orgs
    'taxidtypcd': ['BOON', 'SPEC'],  # Updated tax type codes
    'taxid': ['99-9999999', '88-8888888']  # Updated tax IDs
})

print("\\nVIEWORGTAXID updates:")
print(vieworgtaxid)
```

```python
# Perform the merge
wh_org_updated = merge_org_with_view_taxid(wh_org, vieworgtaxid)

print("\\nUpdated WH_ORG (after merge):")
print(wh_org_updated)

print("\\nChanges made:")
print("- Organization 1001: taxid changed to '99-9999999', taxidtypcd changed to 'BOON'")
print("- Organization 1002: taxid changed to '88-8888888', taxidtypcd changed to 'SPEC'") 
print("- Organization 1003: No changes (not in view table)")
```

## Example: Person Tax ID Updates

```python
# Sample WH_PERS data
wh_pers = pd.DataFrame({
    'persnbr': [501, 502, 503],
    'persname': ['John Doe', 'Jane Smith', 'Bob Johnson'],
    'taxid': ['111-11-1111', '222-22-2222', '333-33-3333'],
    'employeeyn': ['N', 'N', 'N']
})

print("Original WH_PERS:")
print(wh_pers)
```

```python
# Sample VIEWPERSTAXID data with updates
viewperstaxid = pd.DataFrame({
    'persnbr': [501, 503],  # Only updating persons 501 and 503
    'taxid': ['999-99-9999', '777-77-7777']  # Updated tax IDs
})

print("\\nVIEWPERSTAXID updates:")
print(viewperstaxid)
```

```python
# Perform the merge
wh_pers_updated = merge_pers_with_view_taxid(wh_pers, viewperstaxid)

print("\\nUpdated WH_PERS (after merge):")
print(wh_pers_updated)

print("\\nChanges made:")
print("- Person 501: taxid changed to '999-99-9999'")
print("- Person 502: No changes (not in view table)")
print("- Person 503: taxid changed to '777-77-7777'")
```

## Integration with Main Pipeline

The merge functions are automatically called in the main pipeline when the view tables are available:

```python
# In your production environment, the load_database_tables() function should 
# include the view tables in the returned data dictionary:

# data = {
#     'wh_org': wh_org_df,
#     'wh_pers': wh_pers_df,
#     'vieworgtaxid': vieworgtaxid_df,    # <- Include these view tables
#     'viewperstaxid': viewperstaxid_df,  # <- Include these view tables
#     'orgaddruse': orgaddruse_df,
#     'persaddruse': persaddruse_df,
#     'wh_addr': wh_addr_df,
#     'wh_allroles': wh_allroles_df
# }

# The create_org_final() and create_pers_final() functions will automatically
# check for these view tables and apply the updates before proceeding with
# address merging and filtering to active accounts.
```

## Key Features

1. **Left Join**: Only updates records where matches exist in the view tables
2. **Null Safety**: Null values in view tables don't overwrite existing data
3. **Duplicate Prevention**: Validates that view tables have no duplicate keys
4. **Dtype Handling**: Automatically handles dtype mismatches for join keys
5. **Column Overlap**: Only updates columns that exist in both tables
6. **Graceful Fallback**: If view tables aren't available, processing continues normally

## Validation

The functions include comprehensive validation:
- Check for None inputs
- Verify required columns exist
- Detect and prevent duplicate keys in view tables
- Handle dtype conversion for reliable joins
- Preserve all original data structure and non-overlapping columns
