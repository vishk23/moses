"""
Upstream dependencies: Needs to run after silver account table (because that gets fed into create calculated columns). Portfolio key also needs
to run before this (that is an upstream of the silver account table).

Stucture for Customer Dimensional Modeling

Base Customer Dim is the first one created.

Feeds to Child tables: Pers + Org tables with specific data that can explicitly join to enrich data where needed. This is seamless for end user
in PowerBI or other method of data being served.

This is the building block to create a centralized view of the customer.
"""

from dateutil.relativedelta import relativedelta  # For more precise age calc (optional)
import src.silver.customer_dim.fetch_data # type: ignore
import cdutils.add_effdate # type: ignore
import cdutils.deduplication # type: ignore
import cdutils.customer_dim # type: ignore
import cdutils.input_cleansing # type: ignore
import pandas as pd
import src.config
from deltalake import DeltaTable
import datetime
import numpy as np

def sort_dedupe_raw(df, dedupe_list):
    if 'adddate' in df.columns:
        df_sorted = df.sort_values(by='adddate', ascending=False)
    else:
        pass

    result = cdutils.deduplication.dedupe(dedupe_list)
    return result


def calculate_age(row):
    dob = pd.to_datetime(row['datebirth'], errors='coerce')
    dod = pd.to_datetime(row['datedeath'], errors='coerce')  

    if pd.isna(dob):
        return None  # No birth date: can't compute age

    if not pd.isna(dod):  # Valid death date: mark as deceased
        return -1

    effdate = pd.to_datetime(row['effdate'], errors='coerce')
    if pd.isna(effdate) or effdate <= dob:  
        return None  # Invalid/missing effdate or effdate before birth: age unknown

    # More precise age calc (optional: replace approx below)
    delta = relativedelta(effdate, dob)
    age_years = delta.years

    # Cap at 125 (arbitrary but as-per spec; consider logging for data review)
    if age_years >= 125:
        return -1
    else:
        return int(age_years)

def generate_base_customer_dim_table():
    """
    Create Base Customer Dim table with P+persnbr or O+orgnbr as primary key
    """
    # data = src.silver.customer_dim.fetch_data.fetch_data()
    # wh_pers = data['wh_pers'].copy()
    # wh_org =data['wh_org'].copy()

    wh_pers = DeltaTable(src.config.BRONZE / "wh_pers").to_pandas()
    wh_org = DeltaTable(src.config.BRONZE / "wh_org").to_pandas()

    # Sort descending and dedupe primary keys 
    dedupe_list = [
            {'df':wh_org, 'field':'orgnbr'}
        ]
    wh_org = sort_dedupe_raw(wh_org, dedupe_list)

    dedupe_list = [
            {'df':wh_pers, 'field':'persnbr'}
        ]
    wh_pers = sort_dedupe_raw(wh_pers, dedupe_list)

    # Org + Persify
    wh_org = cdutils.customer_dim.orgify(wh_org, 'orgnbr')
    wh_pers = cdutils.customer_dim.persify(wh_pers, 'persnbr')

    # Add Customer type field
    wh_org['customer_type'] = 'Organization'
    wh_pers['customer_type'] = 'Person'

    # Concat fields
    customer_dim = pd.concat([wh_org, wh_pers], ignore_index=True)
    
    # Coalesce customer name + filter down
    customer_dim['customer_name'] = customer_dim['orgname'].fillna(customer_dim['persname'])
    customer_dim = customer_dim[[
        'customer_id',
        'customer_type',
        'customer_name',
        'adddate'
    ]].copy()

    # Add taxid
    data = src.silver.customer_dim.fetch_data.fetch_taxid_data()
    vieworgtaxid = data['vieworgtaxid'].copy()
    viewperstaxid = data['viewperstaxid'].copy()
    
    vieworgtaxid = cdutils.customer_dim.orgify(vieworgtaxid, 'orgnbr')
    viewperstaxid = cdutils.customer_dim.persify(viewperstaxid, 'persnbr')

    # Concat taxid
    taxid_concat = pd.concat([vieworgtaxid, viewperstaxid], ignore_index=True)
    assert taxid_concat['customer_id'].is_unique, "Duplicates on concat taxid"

    # Merge
    customer_dim = customer_dim.merge(taxid_concat, on='customer_id', how='left')



    # Append loans/deposit statistics as a calculated dimension
    accts = DeltaTable(src.config.SILVER / "account").to_pandas()

    # Filter and group by customer_id for loans
    loans_df = accts[accts['Macro Account Type'] == 'Loan']
    grouped_loans = loans_df.groupby('customer_id', dropna=False).agg(
        distinct_loans=('acctnbr', 'nunique'),
        loan_net_balance=('Net Balance', 'sum')
    ).reset_index()

    # Filter and group by customer_id for deposits
    deposits_df = accts[accts['Macro Account Type'] == 'Deposit']
    grouped_deposits = deposits_df.groupby('customer_id', dropna=False).agg(
        distinct_deposits=('acctnbr', 'nunique'),
        deposit_balance=('Net Balance', 'sum')
    ).reset_index()

    # Filter and group by customer_id for other products
    others_df = accts[accts['Macro Account Type'] == 'Other']
    grouped_others = others_df.groupby('customer_id', dropna=False).agg(
        distinct_other_products=('acctnbr', 'nunique'),
        other_balance=('Net Balance', 'sum')
    ).reset_index()

    # Merge all grouped DataFrames on customer_id, using outer join to include all customers
    grouped_df = grouped_loans.merge(grouped_deposits, on='customer_id', how='outer') \
                            .merge(grouped_others, on='customer_id', how='outer') \
                            .fillna(0)

    customer_dim = customer_dim.merge(grouped_df, how='left', on='customer_id')

    # Add Active Account Owner flag (Y/N)
    # If sum of Distinct Loans, Distinct Deposits, Distinct Other = 0, then 'N', else 'Y'
    customer_dim['Active Account Owner'] = np.where(
        (customer_dim['distinct_loans'] + customer_dim['distinct_deposits'] + customer_dim['distinct_other_products']) > 0,
        'Y',
        'N'
    )   

    # Linked to Active Account Flag can be added in later using allroles table

    # Add effdate
    customer_dim = cdutils.add_effdate.add_effdate(customer_dim)

    return customer_dim

def generate_pers_dim():
    """
    Generate silver layer person dimension table
    This table is a child of the base customer dim

    Primary key is customer_id and will be used to enrich customer dimensional queries with info
    that applies specifically to People, not organizations
    """
    wh_pers = DeltaTable(src.config.BRONZE / "wh_pers").to_pandas()

    # Sort descending and dedupe primary keys 
    dedupe_list = [
            {'df':wh_pers, 'field':'persnbr'}
        ]
    wh_pers = sort_dedupe_raw(wh_pers, dedupe_list)

    # Persify
    wh_pers = cdutils.customer_dim.persify(wh_pers, 'persnbr')

    wh_pers = wh_pers[[
        'customer_id',
        'perssortname',
        'datebirth',
        'datedeath',
        'employeeyn',
        'privacyyn',
        'homeemail',
        'busemail'
    ]].copy()

    wh_pers = cdutils.add_effdate.add_effdate(wh_pers)

    wh_pers['age'] = wh_pers.apply(calculate_age, axis=1)

    # Append first name and last name
    data = src.silver.customer_dim.fetch_data.fetch_pers_data()
    pers = data['pers'].copy()

    # Sort descending and dedupe primary keys 
    dedupe_list = [
            {'df':pers, 'field':'persnbr'}
        ]
    pers = sort_dedupe_raw(pers, dedupe_list)

    # Persify
    pers = cdutils.customer_dim.persify(pers, 'persnbr')

    pers = pers.rename(columns={
        'firstnameupper':'firstname',
        'lastnameupper':'lastname'
    }).copy()

    wh_pers = wh_pers.merge(pers, on='customer_id', how='left')

    # Add userfields for Unsubscribe/OptOut
    wh_persuserfields = DeltaTable(src.config.BRONZE / "wh_persuserfields").to_pandas()

    wh_persuserfields = cdutils.customer_dim.persify(wh_persuserfields, 'persnbr')

    # Step 1: Filter to only the relevant persuserfieldcd values
    df_filtered = wh_persuserfields[wh_persuserfields['persuserfieldcd'].isin(['OPTF', 'OPTB', 'MEMA', 'MSMS'])]

    # Step 2: Pivot the data - index on customer_id, columns on persuserfieldcd, values from persuserfieldvalue
    # This creates one row per customer_id, with columns for each cd, filled with values or NaN/None where missing
    df_pivot = df_filtered.pivot(
        index='customer_id',
        columns='persuserfieldcd',
        values='persuserfieldvalue'
    ).reset_index()  # Reset to make customer_id a regular column again

    # Step 3: Rename the columns to your desired names
    df_pivot = df_pivot.rename(columns={
        'MSMS': 'Unsubscribe_SMS_Date',  # Preserves the original value (e.g., a date or string)
        'MEMA': 'Unsubscribe_Email_Date',  
        'OPTF': 'Opt_Out_Affiliates',
        'OPTB': 'OPT_Out_BCSB'  # Preserves the original value (e.g., Y/N)
    })

    # Optional: If you want to explicitly convert NaN to None (Python None)
    df_pivot = df_pivot.where(pd.notnull(df_pivot), None)
    
    wh_pers = wh_pers.merge(df_pivot, on='customer_id', how='left')

    # Add phone numbers
    persphoneview = DeltaTable(src.config.BRONZE / "persphoneview").to_pandas()

    # Pivot to get PER and BUS as columns
    df_pivot_phones = persphoneview.pivot(index='persnbr', columns='phoneusecd', values='fullphonenbr').reset_index()
    df_pivot_phones = df_pivot_phones.rename(columns={'PER': 'persphonenbr', 'BUS': 'workphonenbr'})

    # Persify
    df_pivot_phones = cdutils.customer_dim.persify(df_pivot_phones, 'persnbr')

    # Merge
    wh_pers = wh_pers.merge(df_pivot_phones[['customer_id', 'persphonenbr', 'workphonenbr']], on='customer_id', how='left')

    return wh_pers

def generate_org_dim():
    """
    Generate silver layer org dimension table
    This table is a child of the base customer dim

    Primary key is customer_id and will be used to enrich customer dimensional queries with info
    that applies specifically to organizations only, not people (pers table)
    """
    wh_org = DeltaTable(src.config.BRONZE / "wh_org").to_pandas()

    # Sort descending and dedupe primary keys 
    dedupe_list = [
            {'df':wh_org, 'field':'orgnbr'}
        ]
    wh_org = sort_dedupe_raw(wh_org, dedupe_list)

    # Orgify 
    wh_org = cdutils.customer_dim.orgify(wh_org, 'orgnbr')

    wh_org = wh_org[[
        'customer_id',
        'orgtypcd',
        'orgtypcddesc',
        'rpt1099intyn',
        'privacyyn',
        'taxexemptyn',
        'naicscd',
        'naicscddesc',
        'homeemail',
        'busemail'
    ]].copy()

    wh_org = cdutils.add_effdate.add_effdate(wh_org)

    data = src.silver.customer_dim.fetch_data.fetch_org_data()
    org = data['org'].copy()

    # Sort descending and dedupe primary keys 
    dedupe_list = [
            {'df':org, 'field':'orgnbr'}
        ]
    org = sort_dedupe_raw(org, dedupe_list)

    # Orgify
    org = cdutils.customer_dim.orgify(org, 'orgnbr')

    wh_org = wh_org.merge(org, on='customer_id', how='left')

    wh_orguserfields = DeltaTable(src.config.BRONZE / "wh_orguserfields").to_pandas()

    wh_orguserfields = cdutils.customer_dim.orgify(wh_orguserfields, 'orgnbr')
    # Assuming your DataFrame is named 'df' with columns: org_id, orguserfieldcd, orguserfieldvalue
    # Step 1: Filter to only the relevant orguserfieldcd values (excluding MSMS)
    df_filtered = wh_orguserfields[wh_orguserfields['orguserfieldcd'].isin(['OPTF', 'OPTB', 'MEMA'])]

    # Step 2: Pivot the data - index on org_id, columns on orguserfieldcd, values from orguserfieldvalue
    # This creates one row per org_id, with columns for each cd, filled with values or NaN/None where missing
    df_pivot = df_filtered.pivot(
        index='customer_id',
        columns='orguserfieldcd',
        values='orguserfieldvalue'
    ).reset_index()  # Reset to make org_id a regular column again

    # Step 3: Rename the columns to your desired names
    df_pivot = df_pivot.rename(columns={
        'MEMA': 'Unsubscribe_Email_Date', 
        'OPTF': 'Opt_Out_Affiliates',
        'OPTB': 'OPT_Out_BCSB'  # Preserves the original value (e.g., Y/N)
    })

    # Optional: If you want to explicitly convert NaN to None (Python None)
    df_pivot = df_pivot.where(pd.notnull(df_pivot), None)

    wh_org = wh_org.merge(df_pivot, on='customer_id', how='left')

    # Add phone numbers
    orgphoneview = DeltaTable(src.config.BRONZE / "orgphoneview").to_pandas()

    # Pivot to get BUS as workphonenbr
    df_pivot_phones = orgphoneview.pivot(index='orgnbr', columns='phoneusecd', values='fullphonenbr').reset_index()
    df_pivot_phones = df_pivot_phones.rename(columns={'BUS': 'workphonenbr'})

    # Orgify
    df_pivot_phones = cdutils.customer_dim.orgify(df_pivot_phones, 'orgnbr')

    # Merge
    wh_org = wh_org.merge(df_pivot_phones[['customer_id', 'workphonenbr']], on='customer_id', how='left')

    return wh_org
