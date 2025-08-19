# %%
import os
import sys
from pathlib import Path

# %%
import pandas as pd
import numpy as np

# %%
import cdutils.acct_file_creation.core
from datetime import datetime
import src.smb_campaign.fetch_data
import cdutils.deduplication

def main_pipeline():


    # %%
    df = cdutils.acct_file_creation.core.query_df_on_date()

    # %%
    df

    # %%
    # Fetch wh_org data
    raw_data = src.smb_campaign.fetch_data.fetch_data()

    # %%

    # %%
    # Dedupe org table
    if 'wh_org' in raw_data:
        dedupe_list = [{'df': raw_data['wh_org'], 'field': 'orgnbr'}]
        raw_data['wh_org'] = cdutils.deduplication.dedupe(dedupe_list)

    # %%
    wh_org = raw_data['wh_org'].copy()

    # %%
    assert wh_org['orgnbr'].is_unique, "Not unique"

    # %%
    wh_org

    # %%
    wh_org['orgtypcd'].unique()

    # %%
    filtered_org = wh_org[~(wh_org['orgtypcd'].isin(['BRCH','BANK']))].copy()

    # %%
    filtered_org.info()

    # %%
    filtered_org = filtered_org[[
        'orgnbr',
        'orgname',
        'orgtypcd',
        'orgtypcddesc'
    ]].copy()

    # %%
    # Aggregate stats (total loans/deposits) per orgnbr
    ## orgs only
    acct_orgs = df[df['taxrptforpersnbr'].isna()].copy()

    # %%

    # %%
    ## loans/deposit categorization
    # Account type mappings
    ACCOUNT_TYPE_MAPPING = {
        'CML': 'Commercial Loan',
        'MLN': 'Commercial Loan',
        'CNS': 'Consumer Loan',
        'MTG': 'Residential Loan',
        'CK': 'Checking',
        'SAV': 'Savings',
        'TD': 'CD'
    }

    acct_orgs['Account Type'] = acct_orgs['mjaccttypcd'].map(ACCOUNT_TYPE_MAPPING)

    # %%
    acct_orgs = acct_orgs[~(acct_orgs['Account Type'].isna())].copy()

    # %%
    acct_orgs

    # %%
    MACRO_TYPE_MAPPING = {
        'CML': 'Loan',
        'MLN': 'Loan',
        'CNS': 'Loan',
        'MTG': 'Loan',
        'CK': 'Deposit',
        'SAV': 'Deposit',
        'TD': 'Deposit'
    }

    acct_orgs['Macro Account Type'] = acct_orgs['mjaccttypcd'].map(MACRO_TYPE_MAPPING)

    # %%
    # Get other entity details
    entity_details = acct_orgs.groupby('taxrptfororgnbr').agg(
        primaryownercity=('primaryownercity', 'first'),
        primaryownerstate=('primaryownerstate','first'),
        earliest_opendate=('contractdate','min')
    ).reset_index()

    # %%
    entity_details

    # %%
    entity_details['taxrptfororgnbr'] = entity_details['taxrptfororgnbr'].astype(int).astype(str)

    # %%
    filtered_org['orgnbr'] = filtered_org['orgnbr'].astype(str)

    # %%
    merged_df = pd.merge(filtered_org, entity_details, left_on='orgnbr', right_on='taxrptfororgnbr', how='inner')

    # %%
    merged_df = merged_df.drop(columns=['taxrptfororgnbr']).copy()

    # %%
    merged_df

    # %%
    # Need to get address information
    # ORGADDRUSE
    # WH_ADDR

    # %%
    wh_addr = raw_data['wh_addr'].copy()
    orgaddruse = raw_data['orgaddruse'].copy()

    # %%
    wh_addr['addrlinetypdesc1'].unique()

    # %%
    def create_full_street_address(df):
        """
        Processes a list of raw address records and returns a cleaned list.
        """

        STREET_TYPES = {
            'street', 'apartment number','building number', 'suite number', 'room number'
        }
        POBOX_TYPE = 'post office box number'

        # Step A: Extract both street parts AND po box parts into temporary columns
        for i in [1, 2, 3]:
            text_col = f'text{i}'
            type_col = f'addrlinetypdesc{i}'
            
            # Condition for street parts
            is_street_part = df[type_col].str.lower().isin(STREET_TYPES).fillna(False)
            df[f'street_part{i}'] = df[text_col].where(is_street_part)
            
            # Condition for PO Box parts
            is_pobox_part = (df[type_col].str.lower() == POBOX_TYPE).fillna(False)
            df[f'pobox_part{i}'] = df[text_col].where(is_pobox_part)


        # Step B: Combine the parts into two separate, complete address strings
        street_parts = ['street_part1', 'street_part2', 'street_part3']
        pobox_parts = ['pobox_part1', 'pobox_part2', 'pobox_part3']

        df['combined_street'] = df[street_parts].apply(
            lambda row: ' '.join(row.dropna().astype(str)), axis=1
        )
        df['combined_pobox'] = df[pobox_parts].apply(
            lambda row: ' '.join(row.dropna().astype(str)), axis=1
        )

        # Step C: Apply the final rule: Use Street, but if it's empty, use PO Box.
        # First, replace empty strings '' in the street column with NaN so .fillna() works
        df['combined_street'] = df['combined_street'].replace('', np.nan)

        # Now, use .fillna() to populate empty street addresses with the po box value
        df['Full_Street_Address'] = df['combined_street'].fillna(df['combined_pobox'])


        # --- 3. Finalizing the Extract ---

        # Create the final, clean DataFrame with user-friendly column names
        df_clean = df[[
            'addrnbr',
            'Full_Street_Address',
            'cityname',
            'statecd',
            'zipcd'
        ]].copy()

        return df_clean 

    # %%
    cleaned_addr = create_full_street_address(wh_addr)

    # %%
    cleaned_addr

    # %%
    orgaddruse

    # %%
    orgaddruse = orgaddruse[orgaddruse['addrusecd'].isin(['PRI'])].copy()

    # %%
    orgaddruse['orgnbr'] = orgaddruse['orgnbr'].astype(str)
    orgaddruse['addrnbr'] = orgaddruse['addrnbr'].astype(str)

    cleaned_addr['addrnbr'] = cleaned_addr['addrnbr'].astype(str)

    # %%
    merged_address = pd.merge(orgaddruse, cleaned_addr, on='addrnbr', how='inner')

    # %%
    merged_address

    # %%
    wh_addr

    # %%
    merged_final = pd.merge(merged_df, merged_address, on='orgnbr', how='left')

    # %%
    merged_final = merged_final[[
        'orgname',
        'orgtypcddesc',
        'earliest_opendate',
        'Full_Street_Address',
        'cityname',
        'statecd',
        'zipcd'
    ]].copy()

    # %%
    merged_final = merged_final.rename(columns={
        'orgname':'Organization Name',
        'orgtypcddesc':'Org Type',
        'earliest_opendate':'Earliest Open Date',
        'Full_Street_Address':'Full Street Address',
        'cityname':'City',
        'statecd':'State',
        'zipcd':'Zip'
    }).copy()


    # %%
    return merged_final

# %%
# check = merged_final.copy()

# %%
# import numpy as np

# %%
# check['test'] = np.where(check['primaryownercity'] != check['cityname'], 1, 0)

# %%
# Will turn into formal pipeline after getting feedback from business line



