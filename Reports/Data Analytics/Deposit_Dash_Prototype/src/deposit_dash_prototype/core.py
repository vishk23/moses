# Core logic specific to project/report
#

from deltalake import DeltaTable
import pandas as pd
from pathlib import Path
import src.config
import cdutils.acct_file_creation.core
from src.utils.parquet_io import add_load_timestamp

def main_pipeline():
# Main account table
    df = DeltaTable(src.config.SILVER / "account").to_pandas()
# Create loans/deposits distinction
    MACRO_TYPE_MAPPING = {
        'CML':'Loan',
        'MLN':'Loan',
        'CNS':'Loan',
        'MTG':'Loan',
        'CK':'Deposit',
        'SAV':'Deposit',
        'TD':'Deposit'
    }


    df['Macro Account Type'] = df['mjaccttypcd'].map(MACRO_TYPE_MAPPING)
    

# Get MTD/YTD metrics to append to that
# Actually -> ME balance, YTD balance
# Left join

# Absent of proper portfolio silver dimension table
# Separate field for presence of Muni (Y/N)
# We group by portfolio key and come up with a dimension
# Example: portfolio key is primary key and then I have a calculated field (agg, probably lambda function)

    return df


