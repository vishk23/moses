"""
Upstream dependencies: Needs to run after silver account table (because that gets fed into create calculated columns). Portfolio key also needs
to run before this (that is an upstream of the silver account table).

Stucture for Customer Dimensional Modeling

Base Customer Dim is the first one created.

Feeds to Child tables: Pers + Org tables with specific data that can explicitly join to enrich data where needed. This is seamless for end user
in PowerBI or other method of data being served.

This is the building block to create a centralized view of the customer.
"""

import src.silver.customer_dim.fetch_data # type: ignore
import cdutils.add_effdate # type: ignore
import cdutils.deduplication # type: ignore
import cdutils.customer_dim # type: ignore
import cdutils.input_cleansing # type: ignore
import pandas as pd
import src.config
from deltalake import DeltaTable
import datetime

def sort_dedupe_raw(df, dedupe_list):
    if 'adddate' in df.columns:
        df_sorted = df.sort_values(by='adddate', ascending=False)
    else:
        pass

    result = cdutils.deduplication.dedupe(dedupe_list)
    return result

def calculate_age(row):
    dob = pd.to_datetime(row['datebirth'], errors='coerce')
    dod = pd.to_datetime(row['datebirth'], errors='coerce')

    if pd.isna(dob):
        return None

    if not pd.isna(dod):
        return -1

    effdate = pd.to_datetime(row['effdate'], errors='coerce')
    if pd.isna('effdate') or effdate <= dob:
        return None

    age_days = (effdate - dob).days
    age_years = age_days // 365.25

    # Cap at 125, assume deceased and we never updated database
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

    # Join with account data to get counts and balances
    
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

    return wh_org