# # Specific date
# specified_date = datetime(2020, 12, 31)
from typing import Optional
from datetime import datetime

import pandas as pd # type: ignore
from datetime import datetime, timedelta
from pandas.tseries.holiday import USFederalHolidayCalendar

import src.account_data_adhoc.additional_fields # type: ignore
import src.account_data_adhoc.fetch_data # type: ignore
import src.account_data_adhoc.core_transform # type: ignore
import cdutils.pkey_sqlite # type: ignore
import cdutils.hhnbr # type: ignore
import cdutils.loans.calculations # type: ignore
import cdutils.inactive_date # type: ignore
import cdutils.input_cleansing # type: ignore


def get_last_business_day(from_date: Optional[datetime] = None):
    """Get the last business day (excluding weekends and US federal holidays)"""
    if from_date is None:
        candidate_date = datetime.now().date() - timedelta(days=1)
    else:
        candidate_date = from_date.date()
    
    cal = USFederalHolidayCalendar()
    while True:
        # Check if it's a weekend (Saturday=5, Sunday=6)
        if candidate_date.weekday() >= 5:
            candidate_date -= timedelta(days=1)
            continue
            
        # Check if it's a US federal holiday
        holidays = cal.holidays(start=candidate_date, end=candidate_date)
        if len(holidays) > 0:
            candidate_date -= timedelta(days=1)
            continue
            
        # Found a business day
        break
    
    return candidate_date.strftime('%Y-%m-%d %H:%M:%S')



def query_df_on_date(specified_date: Optional[datetime] = None):

    if specified_date is None:
        specified_date = get_last_business_day()
    else:
        assert isinstance(specified_date, datetime), "Specified date must be a datetime object"
        specified_date = get_last_business_day(specified_date)

    data = src.account_data_adhoc.fetch_data.fetch_data(specified_date)

    # # # Core transformation pipeline
    raw_data = src.account_data_adhoc.core_transform.main_pipeline(data)

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

    additional_fields = src.account_data_adhoc.additional_fields.fetch_data(specified_date)

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

