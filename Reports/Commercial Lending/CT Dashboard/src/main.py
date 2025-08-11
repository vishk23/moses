
"""
Main Entry Point
"""
import shutil
import re
from pathlib import Path
from typing import List
from datetime import datetime

from lxml import html
import pandas as pd # type: ignore
import numpy as np

import src.ct_dashboard.fetch_cocc_data 
import src.ct_dashboard.ingest
import src.output_to_excel_multiple_sheets
from src._version import __version__
import src.rel_entity_officer


def main():
    files = src.ct_dashboard.ingest.process_xls_files()

    cocc_data = src.fetch_cocc_data.fetch_data()

    cocc_data = cocc_data['wh_acctcommon'].copy()

    # %%
    # Function to get mode, handling cases where there might be multiple modes
    def get_mode(series):
        series_clean = series.dropna()
        if len(series_clean) == 0:
            return None
        
        # Get unique values first
        unique_values = pd.Series(series_clean.unique())
        mode_result = unique_values.mode()
        
        # Return first mode if multiple modes exist
        return mode_result.iloc[0] if len(mode_result) > 0 else None
    # Group and calculate mode
    cocc_data_grouped = cocc_data.groupby('ownersortname').agg({
        'loanofficer': get_mode,
        'acctofficer': get_mode
    }).reset_index()

    cocc_data_grouped = cocc_data_grouped.rename(columns={
        'ownersortname':'customer_name',
        'loanofficer':'Loan Officer',
        'acctofficer':'Deposit Officer',
    }).copy()
    cocc_data_grouped

    # %%
    # cocc_data_grouped.info()
    rel_entity_grouped = src.rel_entity_officer.create_officer_df()

    # %%
    def merge_with_mode(df_dict, cocc_data_grouped, rel_entity_grouped):
        """
        Take in the dictionary of dataframes and append the mode of the loan officer and acct officer

        Only applies to active/dorm/non-performing accounts
        """
        merged_dict = {}
        for key, df in df_dict.items():
            merged_df = df.merge(cocc_data_grouped, on='customer_name', how='left')
            merged_df = merged_df.merge(rel_entity_grouped, on='customer_name', how='left')
            
            # handling dtypes
            date_fields = ['period_date','due_date','report_date']
            for field in date_fields:
                merged_df[field] = pd.to_datetime(merged_df[field])

            merged_df = merged_df.sort_values(by='period_date', ascending=True)

            merged_df['Loan Officer_new'] = np.where(merged_df['Loan Officer'].isnull(), merged_df['Loan Officer_related'], merged_df['Loan Officer'])

            merged_df = merged_df[[
                'customer_name',
                'Loan Officer_new',
                'Deposit Officer',
                'item_name',
                'required_value',
                'actual_value',
                'period_date',
                'due_date',
                'days_past_due',
                'interval',
                'comments',
                'report_date'
            ]].copy()

            merged_df = merged_df.rename(columns={
                'Loan Officer_new':'Loan Officer'
            }).copy()

            merged_dict[key] = merged_df

        return merged_dict


    # %%
    cleaned_dict = merge_with_mode(files, cocc_data_grouped, rel_entity_grouped)

    # %%
    cleaned_dict.keys()

    # %%
    ticklers_past_due = cleaned_dict['ticklers_past_due'].copy()
    ticklers_past_due

    # # %%
    # ticklers_coming_due_365 = cleaned_dict['ticklers_coming_due_365'].copy()
    # ticklers_coming_due_365

    # %%
    covenants_past_due = cleaned_dict['covenants_past_due'].copy()
    covenants_past_due

    # # %%
    # covenants_coming_due_365 = cleaned_dict['covenants_coming_due_365'].copy()
    # covenants_coming_due_365

    # %%

    covenants_in_default = cleaned_dict['covenants_in_default'].copy()
    covenants_in_default

    # %%


    COVENANT_OUTPUT_PATH = BASE_PATH / Path('./output/CT_Covenant_Tracking.xlsx')
    with pd.ExcelWriter(COVENANT_OUTPUT_PATH, engine="openpyxl") as writer:
        # covenants_coming_due_365.to_excel(writer, sheet_name='Coming Due', index=False)
        covenants_past_due.to_excel(writer, sheet_name='Past Due', index=False)
        covenants_in_default.to_excel(writer, sheet_name='In Default', index=False)

    # Format excel
    src.output_to_excel_multiple_sheets.format_excel_file(COVENANT_OUTPUT_PATH)

    TICKLER_OUTPUT_PATH = BASE_PATH / Path('./output/CT_Tickler_Tracking.xlsx')
    with pd.ExcelWriter(TICKLER_OUTPUT_PATH, engine="openpyxl") as writer:
        # ticklers_coming_due_365.to_excel(writer, sheet_name='Coming Due', index=False)
        ticklers_past_due.to_excel(writer, sheet_name='Past Due', index=False)

    # Format excel
    src.output_to_excel_multiple_sheets.format_excel_file(TICKLER_OUTPUT_PATH)

    # Distribution
    # recipients = [
    #     # "chad.doorley@bcsbmail.com",
    # ]
    # bcc_recipients = [
    #     "chad.doorley@bcsbmail.com",
    #     "businessintelligence@bcsbmail.com"
    # ]
    # subject = f"File Name" 
    # body = "Hi, \n\nAttached is your requested report. If you have any questions, please reach out to BusinessIntelligence@bcsbmail.com \n\nThanks!"
    # attachment_paths = [OUTPUT_PATH]
    # cdutils.distribution.email_out(recipients, bcc_recipients, subject, body, attachment_paths)






if __name__ == '__main__':
    print(f"Starting [{__version__}]")
    # main(production_flag=True)
    main()
    print("Complete!")

