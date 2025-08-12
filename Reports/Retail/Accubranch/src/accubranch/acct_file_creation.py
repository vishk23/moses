# # Specific date
# specified_date = datetime(2020, 12, 31)

import pandas as pd # type: ignore

import src.accubranch.additional_fields
import src.accubranch.fetch_data # type: ignore
import src.accubranch.core_transform # type: ignore
import cdutils.pkey_sqlite # type: ignore
import cdutils.hhnbr # type: ignore
import cdutils.loans.calculations # type: ignore
import cdutils.inactive_date # type: ignore
import cdutils.input_cleansing # type: ignore

def query_df_on_date(specified_date):

    data = src.accubranch.fetch_data.fetch_data(specified_date)

    # # # Core transformation pipeline
    raw_data = src.accubranch.core_transform.main_pipeline(data)

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

    # %%
    loan_category_df = cdutils.loans.calculations.categorize_loans(raw_data)

    # %%
    loan_category_df = loan_category_df[['acctnbr','Category']].copy()

    # %%
    df = pd.merge(raw_data, loan_category_df, on='acctnbr', how='left')

    # %%
    df

    # %%

    df = cdutils.inactive_date.append_inactive_date(df)

    # %%
    df

    # %%
    pers = data['wh_pers'].copy()

    # %%
    # df.info()

    # %%

    additional_fields = src.additional_fields.fetch_data(specified_date)

    # %%
    additional_fields_to_append = additional_fields['wh_acctcommon'].copy()

    # %%

    additional_fields_to_append_schema = {
        'acctnbr':'str'
    }

    additional_fields_to_append = cdutils.input_cleansing.enforce_schema(additional_fields_to_append, additional_fields_to_append_schema)

    # %%
    df = pd.merge(df, additional_fields_to_append, how='left', on='acctnbr')

    # %%
    return df

