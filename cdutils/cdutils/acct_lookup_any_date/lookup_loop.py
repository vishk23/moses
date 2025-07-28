# %%
## Memorializing this as the easy way to lookup accounts


# %%
"""
Main Entry Point
"""
from pathlib import Path
from typing import List
import argparse
from datetime import datetime

import pandas as pd # type: ignore

import src.fetch_data # type: ignore
import src.core_transform # type: ignore
import cdutils.pkey_sqlite # type: ignore
import cdutils.hhnbr # type: ignore

# Current (doesn't really work without)
# data = src.fetch_data.fetch_data()


# Specific date
specified_date = datetime(2020, 12, 31)

def query_df_on_date(specified_date):

    data = src.fetch_data.fetch_data(specified_date)

    # # # Core transformation pipeline
    raw_data = src.core_transform.main_pipeline(data)

    # Raw data with pkey appended
    raw_data = cdutils.pkey_sqlite.add_pkey(raw_data)
    raw_data = cdutils.pkey_sqlite.add_ownership_key(raw_data)
    raw_data = cdutils.pkey_sqlite.add_address_key(raw_data)

    # %%
    househldacct = data['househldacct'].copy()
    raw_data = cdutils.hhnbr.add_hh_nbr(raw_data, househldacct)

    # %%
    raw_data

    # %%
    import cdutils.loans.calculations

    # %%
    loan_category_df = cdutils.loans.calculations.categorize_loans(raw_data)

    # %%
    loan_category_df = loan_category_df[['acctnbr','Category']].copy()

    # %%
    df = pd.merge(raw_data, loan_category_df, on='acctnbr', how='left')

    # %%
    df

    # %%
    import cdutils.inactive_date

    df = cdutils.inactive_date.append_inactive_date(df)

    # %%
    df

    # %%
    pers = data['wh_pers'].copy()

    # %%
    df.info()

    # %%
    import src.additional_fields

    additional_fields = src.additional_fields.fetch_data(specified_date)

    # %%
    additional_fields_to_append = additional_fields['wh_acctcommon'].copy()

    # %%
    import cdutils.input_cleansing

    additional_fields_to_append_schema = {
        'acctnbr':'str'
    }

    additional_fields_to_append = cdutils.input_cleansing.enforce_schema(additional_fields_to_append, additional_fields_to_append_schema)

    # %%
    df = pd.merge(df, additional_fields_to_append, how='left', on='acctnbr')

    # %%
    return df

# %%
# OUTPUT_PATH = Path('acct_table.csv')
# df.to_csv(OUTPUT_PATH, index=False)

# %%
# import hashlib

# %%
# def mask_pii(data, columns_to_mask, length=10):
#     """
#     Create a masking layer

#     Pass in a dataframe to blackbox abstraction and get a dataframe returned with masked PII in specified fields

#     Parameters:
#     - data: raw data
#     - columns_to_mask: list of columns
#     - length: length of hash (10+ is recommended based on size of the data)
#     """
#     df_hashed = data.copy()

#     for col in columns_to_mask:
#         if col in df_hashed.columns:
#             df_hashed[col] = df_hashed[col].astype(str).apply(
#                 lambda x: hashlib.sha256(x.encode('utf-8')).hexdigest()[:length]
#             )
#         else:
#             raise ValueError(f"Column {col} not found in dataframe passed in")
        
#     return df_hashed

# %%
# columns_to_mask = [
#     'acctnbr',
#     'ownersortname',
#     'loanofficer',
#     'acctofficer',
#     'taxrptfororgnbr',
#     'taxrptforpersnbr'
#     ]

# masked_df = mask_pii(df, columns_to_mask)

# %%
# masked_df

# %%
# transposed_df = masked_df.head(3).T.reset_index()

# %%
# transposed_df

# %%
# OUTPUT_PATH = Path('masked_acct_table.csv')
# masked_df.to_csv(OUTPUT_PATH, index=False)

# %%



