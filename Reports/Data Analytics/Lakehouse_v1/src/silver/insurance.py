import src.config
from deltalake import DeltaTable
from pathlib import Path
import pandas as pd
from src.utils.parquet_io import cast_all_null_columns_to_string

def generate_insurance_table():
    # Get data from bronze tables
    TABLE_PATH = src.config.BRONZE / "acctpropins"
    acctpropins = DeltaTable(TABLE_PATH).to_pandas()
    TABLE_PATH = src.config.BRONZE / "wh_inspolicy"
    wh_inspolicy = DeltaTable(TABLE_PATH).to_pandas()

    # Left join
    full_insurance_data = pd.merge(
        acctpropins,
        wh_inspolicy,
        on='intrpolicynbr',
        how='left',
        suffixes=('_link', '_policy') # Add suffixes in case of any other overlapping column names
    )

    insurance_policy = full_insurance_data.drop_duplicates(subset=['intrpolicynbr']).reset_index(drop=True)

    link_cols = ['acctnbr', 'propnbr', 'intrpolicynbr']
    acct_prop_insurance_link = full_insurance_data[link_cols].copy()

    insurance_policy = cast_all_null_columns_to_string(insurance_policy)
    acct_prop_insurance_link = cast_all_null_columns_to_string(acct_prop_insurance_link)

    return insurance_policy, acct_prop_insurance_link
