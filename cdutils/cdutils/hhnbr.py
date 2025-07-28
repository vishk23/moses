import pandas as pd
import cdutils.input_cleansing
import cdutils.deduplication


def add_hh_nbr(df: pd.DataFrame, househldacct: pd.DataFrame) -> pd.DataFrame:
    """
    After dropping duplicates from household acct (sorting in reverse chronological order), add householdnbr to any df
    """
    assert df is not None, "df cannot be None"
    assert not df.empty, "df cannot be empty"

    househldacct_sorted = househldacct.sort_values(by='datelastmaint', ascending=False)

    dedupe_list = [{'df':househldacct_sorted, 'field':'acctnbr'}]
    household_new = cdutils.deduplication.dedupe(dedupe_list)

    # Enforce schema
    schema_df = {
        'acctnbr': str,
    }

    df = cdutils.input_cleansing.enforce_schema(df, schema_df)

    schema_household = {
        'acctnbr': str,
    }

    household_new = cdutils.input_cleansing.enforce_schema(household_new, schema_household)

    merged_df = pd.merge(df, household_new, on='acctnbr', how='left')

    return merged_df