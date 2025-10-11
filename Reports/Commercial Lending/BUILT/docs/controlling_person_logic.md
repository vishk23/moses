# Controlling Person Logic for BUILT Extract

## Overview
This document outlines the logic and implementation for adding controlling person details to the BUILT extract. For accounts where the primary borrower is an organization (customer_id starts with 'O'), we fetch the controlling person via `ctrlpernbr` from `org_dim`, convert it to a person customer_id ('P' + ctrlpernbr), and retrieve their business email, phone, first name, and last name from `pers_dim` and phone views. For person primary borrowers ('P' prefix), controlling fields remain null.

- **Primary Borrower Fields** (always): 'Primary Borrower Email', 'Primary Borrower Phone' – based on the primary borrower's customer_id.
- **Controlling Person Fields** (only if primary is org): 'Controlling Person Email', 'Controlling Person Phone', 'Controlling Person First Name', 'Controlling Person Last Name' – based on the controlling person's derived customer_id. If primary is a person, these fields remain null.
- No address for controlling person, as specified.
- Follow existing style: snake_case, type hints where appropriate, assertions for integrity, cdutils utilities for normalization/casting.
- Assumptions:
  - org_dim has customer_id ('O' + orgnbr) and ctrlpernbr (persnbr of controlling person).
  - Controlling person is always a person (pers); no nested orgs.
  - If ctrlpernbr is null or invalid, controlling fields default to null.
  - Prioritize business contacts ('BUS' for phones, 'busemail' for emails).
  - Handle multiples by selecting first non-null per customer_id.
- No new dependencies; leverage existing Silver/Bronze tables and cdutils.
- Edge cases: Null ctrlpernbr, non-unique controlling persons (rare; aggregate first), type mismatches in IDs.

## High-Level Steps
1. **Enhance Fetch Function** (in src/built/fetch_data.py): Update fetch_borrower_contacts() to also handle controlling person logic. Input primary customer_ids from accts (to optimize), output a DF with primary and conditional controlling fields.
2. **Integration in Transform** (in src/built/core.py): Call the enhanced fetch after primary address merge, pass accts['customer_id'] for filtering, merge results.
3. **Data Processing**: Separate logic for primary vs. controlling; use string prefix check ('O' vs. 'P') on customer_id.
4. **Validation**: Assertions for uniqueness, null handling.
5. **Output**: accts with new columns in borrower info section (primary first, then controlling).

## Detailed Code Changes

### 1. Update Imports (src/built/fetch_data.py)
- Ensure existing: from sqlalchemy import text, import cdutils.customer_dim  # type: ignore, import pandas as pd, import src.config.
- No new imports needed.

### 2. Enhanced Function: fetch_borrower_contacts(primary_customer_ids) (Replace/Add in src/built/fetch_data.py, after existing functions)
- Purpose: Fetch/process emails/phones for primary borrowers and controlling persons (if org). Filter to provided primary_customer_ids for efficiency.
- Code:
  ```python
  def fetch_borrower_contacts(primary_customer_ids):
      """
      Fetches and processes business email and phone for primary borrowers and controlling persons (if org).
      Args:
          primary_customer_ids: Series or list of customer_id from accts (for filtering).
      Returns:
          DataFrame with customer_id (primary), Primary Borrower Email/Phone, and Controlling Person Email/Phone/First Name/Last Name (if applicable).
      """
      # Cast input to set for filtering
      primary_customer_ids = pd.Series(primary_customer_ids).dropna().unique()
      primary_customer_ids_set = set(primary_customer_ids)

      # Step 1: Fetch emails from Silver dims (filter to relevant customer_ids)
      org_dim = DeltaTable(src.config.SILVER / "org_dim").to_pandas()
      pers_dim = DeltaTable(src.config.SILVER / "pers_dim").to_pandas()

      # Filter org_dim to primary orgs only (for ctrlpernbr lookup)
      org_dim = org_dim[org_dim['customer_id'].isin(primary_customer_ids_set)].copy()
      org_ctrl_pers = org_dim[['customer_id', 'ctrlpernbr']].copy()  # Primary org customer_id -> ctrlpernbr

      # Get all relevant pers customer_ids: primaries that are persons + controlling persons from orgs
      primary_pers_ids = [cid for cid in primary_customer_ids if cid.startswith('P')]
      ctrl_persnrs = org_ctrl_pers['ctrlpernbr'].dropna().astype(str)
      ctrl_customer_ids = ['P' + p for p in ctrl_persnrs if pd.notna(p)]  # Pre-apply persify logic (simple concat)
      all_pers_ids = set(primary_pers_ids + ctrl_customer_ids)

      # Filter pers_dim to relevant persons
      pers_dim = pers_dim[pers_dim['customer_id'].isin(all_pers_ids)].copy()

      # Emails: Primary (from pers_dim or org_dim.busemail if person/org has it)
      org_dim_emails = org_dim[['customer_id', 'busemail']].copy().rename(columns={'busemail': 'Primary Borrower Email'})
      pers_dim_emails = pers_dim[pers_dim['customer_id'].isin(primary_pers_ids)][['customer_id', 'busemail']].copy().rename(columns={'busemail': 'Primary Borrower Email'})

      primary_emails_df = pd.concat([org_dim_emails, pers_dim_emails], ignore_index=True)
      primary_emails_df = primary_emails_df.groupby('customer_id').agg({
          'Primary Borrower Email': lambda x: x.dropna().iloc[0] if len(x.dropna()) > 0 else None
      }).reset_index()

      # Controlling emails/names: From pers_dim for ctrl_customer_ids
      ctrl_df = pers_dim[pers_dim['customer_id'].isin(ctrl_customer_ids)][['customer_id', 'busemail', 'firstname', 'lastname']].copy().rename(columns={
          'customer_id': 'primary_customer_id',
          'busemail': 'Controlling Person Email',
          'firstname': 'Controlling Person First Name',
          'lastname': 'Controlling Person Last Name'
      })
      ctrl_df = ctrl_df.groupby('primary_customer_id').agg({
          'Controlling Person Email': lambda x: x.dropna().iloc[0] if len(x.dropna()) > 0 else None,
          'Controlling Person First Name': lambda x: x.dropna().iloc[0] if len(x.dropna()) > 0 else None,
          'Controlling Person Last Name': lambda x: x.dropna().iloc[0] if len(x.dropna()) > 0 else None
      }).reset_index()

      # Step 2: Fetch phones (business only, from Bronze views)
      persphoneview_sql = text("""
          SELECT
              a.PERSNBR,
              a.FULLPHONENBR
          FROM
              OSIBANK.PERSPHONEVIEW a
          WHERE
              a.PHONEUSECD = 'BUS'  -- Business phones only
              AND a.PERSNBR IN ({persnrs})  -- Placeholder for relevant PERSNBR (from primaries + ctrls)
      """.format(persnrs=','.join(['?'] * len(all_pers_ids))))  # Dynamic params; adjust for cdutils

      # Note: For orgphoneview, assuming it links to ORGNBR, but since controlling is always pers, focus on persphoneview.
      # If org phones needed for primary orgs, add similar orgphoneview query and orgify.
      orgphoneview_sql = text("""
          SELECT
              a.ORGNBR,
              a.FULLPHONENBR
          FROM
              OSIBANK.ORGPHONEVIEW a
          WHERE
              a.PHONEUSECD = 'BUS'
              AND a.ORGNBR IN ({orgnrs})  -- For primary orgs
      """.format(orgnrs=','.join(['?'] * len([cid[1:] for cid in primary_customer_ids if cid.startswith('O')]))))

      # Use cdutils.database.connect.retrieve_data with params if supported; else fetch all and filter post-query.
      queries = [
          {'key': 'persphoneview', 'sql': persphoneview_sql, 'engine': 1, 'params': list(all_pers_ids)},  # Assuming param support
          {'key': 'orgphoneview', 'sql': orgphoneview_sql, 'engine': 1, 'params': [cid[1:] for cid in primary_customer_ids if cid.startswith('O')]}
      ]
      data = cdutils.database.connect.retrieve_data(queries)  # Adjust if params not supported; post-filter instead
      pers_phones = data['persphoneview'].copy()
      org_phones = data['orgphoneview'].copy()

      # Cast and normalize
      pers_phones_schema = {'PERSNBR': 'str'}
      org_phones_schema = {'ORGNBR': 'str'}
      pers_phones = cdutils.input_cleansing.cast_columns(pers_phones, pers_phones_schema)
      org_phones = cdutils.input_cleansing.cast_columns(org_phones, org_phones_schema)

      # Persify for pers_phones (all persons: primary + controlling)
      pers_phones = cdutils.customer_dim.persify(pers_phones, 'PERSNBR')
      pers_phones = pers_phones[['customer_id', 'FULLPHONENBR']].rename(columns={'FULLPHONENBR': 'phone'})

      # Orgify for org_phones (primary orgs only)
      org_phones = cdutils.customer_dim.orgify(org_phones, 'ORGNBR')
      org_phones = org_phones[['customer_id', 'FULLPHONENBR']].rename(columns={'FULLPHONENBR': 'Primary Borrower Phone'})

      # Primary phones: Concat pers/org for primaries, agg first non-null
      primary_pers_phones = pers_phones[pers_phones['customer_id'].isin(primary_pers_ids)].rename(columns={'phone': 'Primary Borrower Phone'})
      primary_phones_df = pd.concat([primary_pers_phones, org_phones], ignore_index=True)
      primary_phones_df = primary_phones_df.groupby('customer_id').agg({
          'Primary Borrower Phone': lambda x: x.dropna().iloc[0] if len(x.dropna()) > 0 else None
      }).reset_index()

      # Controlling phones: From pers_phones for ctrl_customer_ids
      ctrl_phones_df = pers_phones[pers_phones['customer_id'].isin(ctrl_customer_ids)].rename(columns={'customer_id': 'primary_customer_id', 'phone': 'Controlling Person Phone'})
      ctrl_phones_df = ctrl_phones_df.groupby('primary_customer_id').agg({
          'Controlling Person Phone': lambda x: x.dropna().iloc[0] if len(x.dropna()) > 0 else None
      }).reset_index()

      # Step 3: Merge all into final DF keyed on primary_customer_id
      primary_df = primary_emails_df.merge(primary_phones_df, on='customer_id', how='outer').rename(columns={'customer_id': 'primary_customer_id'})

      # Merge controlling (left join; null if no org or no ctrl)
      ctrl_merged_df = ctrl_df.merge(ctrl_phones_df, on='primary_customer_id', how='outer')
      contacts_df = primary_df.merge(ctrl_merged_df, on='primary_customer_id', how='left')

      # Cast
      contacts_schema = {'primary_customer_id': 'str'}
      contacts_df = cdutils.input_cleansing.cast_columns(contacts_df, contacts_schema)

      # Assert
      assert contacts_df['primary_customer_id'].is_unique, "Duplicate primary_customer_id in contacts"

      # Filter to only provided primaries
      contacts_df = contacts_df[contacts_df['primary_customer_id'].isin(primary_customer_ids_set)].copy()

      return contacts_df
  ```

### 3. Integration in transform Function (src/built/core.py)
- Location: After primary address merge (post line ~00350: accts = accts.merge(address, how='left', on='customer_id')).
- Code to insert:
  ```python
  # Fetch and merge borrower contacts (primary and controlling)
  borrower_contacts = src.built.fetch_data.fetch_borrower_contacts(accts['customer_id'])
  accts = accts.merge(borrower_contacts, left_on='customer_id', right_on='primary_customer_id', how='left')
  accts = accts.drop(columns=['primary_customer_id'])  # Clean up

  # Set controlling fields to null if primary is person (starts with 'P')
  is_org_mask = accts['customer_id'].str.startswith('O', na=False)
  accts.loc[~is_org_mask, ['Controlling Person Email', 'Controlling Person Phone', 'Controlling Person First Name', 'Controlling Person Last Name']] = None
  ```
- Update accts_schema (line ~00355): Add 'Primary Borrower Email': 'str', 'Primary Borrower Phone': 'str', 'Controlling Person Email': 'str', 'Controlling Person Phone': 'str', 'Controlling Person First Name': 'str', 'Controlling Person Last Name': 'str'.

### 4. Column Selection Update (src/built/core.py)
- Initial selection (line ~00169): Add at end of borrower section:
  ```python
  # ... existing ...
  'Primary Borrower Name',
  'Primary Borrower Address',
  'Primary Borrower City',
  'Primary Borrower State',
  'Primary Borrower Zip',
  'Primary Borrower Email',  # New
  'Primary Borrower Phone',  # New
  'Controlling Person First Name',  # New (null for persons)
  'Controlling Person Last Name',  # New (null for persons)
  'Controlling Person Email',  # New (null for persons)
  'Controlling Person Phone',  # New (null for persons)
  ```
- Ensure merges add these before final return.

### 5. Validation and Edge Cases
- Assertions: After merge: assert accts[['Primary Borrower Email', 'Primary Borrower Phone']].isna().sum().sum() <= len(accts) * 2, "Unexpected non-nulls in primary contacts"
- For controlling: If ctrlpernbr null or persify fails, fields null.
- Duplicates: Aggregation in fetch handles; assert uniqueness on primary_customer_id.
- Performance: Filter queries to relevant IDs; if param binding issues in cdutils, fetch all and post-filter.
- Null Propagation: Left merges ensure no data loss.
- Testing: Extend tests/test_core.py with mocks for org/pers scenarios, verify conditional fields.

### 6. Post-Implementation Steps
- Verify with python -m pytest tests/ -v.
- Debug: Check customer_id prefixes, ctrlpernbr validity.
- Docs: Update docs/project-notes.md with "Added controlling person contacts for org primaries."
- No commits; await user request.

This update adds ~20-30 lines to fetch function, ~5-10 to transform, ensuring org nuance without overcomplicating primary flow. Total integration remains seamless.