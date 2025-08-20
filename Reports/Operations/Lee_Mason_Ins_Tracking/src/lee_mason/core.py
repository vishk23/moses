# Core logic specific to project/report
import pandas as pd
import cdutils.acct_file_creation.core

def main():
    acct_data = cdutils.acct_file_creation.core.query_df_on_date()

    return acct_data



