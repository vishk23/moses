"""
Main Entry Point
"""
from pathlib import Path
from typing import List
from datetime import datetime

import pandas as pd # type: ignore

import src.fetch_data # type: ignore
import src.core_transform # type: ignore
import cdutils.pkey_sqlite # type: ignore
import cdutils.hhnbr # type: ignore
import cdutils.distribution # type: ignore
import src.output_to_excel # type: ignore
import cdutils.loans.calculations # type: ignore
# import cdutils.selo # type: ignore
from src._version import __version__
from src.config import OUTPUT_DIR, EMAIL_TO, EMAIL_CC

def main():
    
    data = src.fetch_data.fetch_data()

   # # # Core transformation pipeline
    raw_data = src.core_transform.main_pipeline(data)

    # Raw data with pkey appended
    raw_data = cdutils.pkey_sqlite.add_pkey(raw_data)
    raw_data = cdutils.pkey_sqlite.add_ownership_key(raw_data)
    raw_data = cdutils.pkey_sqlite.add_address_key(raw_data)

    # Household number
    househldacct = data['househldacct'].copy() 
    raw_data = cdutils.hhnbr.add_hh_nbr(raw_data, househldacct)

    # Categorize loans (if it's a deposit or other type of account, it will just return null)
    loan_category_df = cdutils.loans.calculations.categorize_loans(raw_data)
    loan_category_df = loan_category_df[['acctnbr','Category']].copy()
    
    df = pd.merge(raw_data, loan_category_df, on='acctnbr', how='left')

    # getting other relevant data
    persuserfields = data['WH_PERSUSERFIELDS'].copy()
    allroles = data['WH_ALLROLES'].copy()
    names = data['WH_PERS'].copy()
    
    df['acctnbr'] = df['acctnbr'].astype(str)
    allroles['acctnbr'] = allroles['acctnbr'].astype(str)
    allroles = allroles.sort_values(['acctnbr'])

    
    df_merged = pd.merge(persuserfields, allroles, on='persnbr', how='left')
    df_merged = pd.merge(df_merged, names, on='persnbr', how='left')

    df_merged = df_merged.drop_duplicates(subset=['acctnbr', 'persnbr'])
    df_merged_merged = pd.merge(df_merged, df, on='acctnbr', how='left')

    # keeping relevant columns and renaming them
    df_merged_merged = df_merged_merged[['acctnbr', 'persuserfieldvaluedesc', 'persname', 'ownersortname', 'product', 'Net Balance', 'creditlimitamt', 'Total Exposure', 'Category']]
    df_merged_merged.columns = ['Account Number', 'Associated Party', 'Principals', 'Loan Customer Name', 'Type', 'Net Balance', 'Available Credit', 'Potential Outstanding', 'Category']

    # if ownersortname is null remove row
    df_merged_merged = df_merged_merged[df_merged_merged['Loan Customer Name'].notna()]
    df_merged_merged = df_merged_merged.sort_values(['Associated Party', 'Principals', 'Potential Outstanding'])

    # creating separate dataframes for deposits and loans sheets
    deposits = df_merged_merged[df_merged_merged['Category'].isna()]
    deposits = deposits[['Account Number', 'Associated Party', 'Principals', 'Loan Customer Name', 'Type', 'Net Balance', 'Available Credit', 'Potential Outstanding']]
    loans = df_merged_merged[~df_merged_merged['Category'].isna()]
    loans = loans[['Account Number', 'Associated Party', 'Principals', 'Loan Customer Name', 'Type', 'Net Balance', 'Available Credit', 'Potential Outstanding']]

    deposits = deposits.rename(columns={
        'Potential Outstanding': 'Balance',
        })

    # grabbing date for filename
    today = datetime.today()
    date = f"{today.strftime('%B')} {today.day} {today.year}"
    output_string = 'Acct_Attorney_Consultant ' + date + '.xlsx'
    
    # Output to excel (raw data)
    output_file_path = OUTPUT_DIR / Path(output_string)

    # mapping dataframes to sheets in final product
    sheets = [
        ('Deposits', deposits),
        ('Loans', loans)
    ]

    # date_columns = ['Date Opened', 'Next Rate Change Date', 'LOC Inactive Date', 'Maturity Date'] 
    monetary_columns = ['Net Balance', 'Available Credit', 'Potential Outstanding', 'Balance']
    # percent_columns = ['Interest Rate']
    
    def currency_string_length(series):
        return series.map(lambda x: f"${x:,.2f}" if pd.notnull(x) else '').map(len).max()

    with pd.ExcelWriter(output_file_path, engine='xlsxwriter', datetime_format='mm/dd/yyyy') as writer:
        for sheet_name, df in sheets:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            worksheet = writer.sheets[sheet_name]
            workbook = writer.book

            currency_format = workbook.add_format({'num_format': '$#,##0.00'})
            # date_format = workbook.add_format({'num_format': 'mm/dd/yyyy'})
            # percent_format = workbook.add_format({'num_format': '0.00%'})
            
            # Freeze the top row
            worksheet.freeze_panes(1, 0)

            # auto-fit each column
            for i, col in enumerate(df.columns):
                if col in monetary_columns:
                    max_len = max(currency_string_length(df[col]), len(col)) + 2
                    worksheet.set_column(i, i, max_len, currency_format)
                # elif col in date_columns:
                #     max_len = max([col].astype(str).map(len).max(), len(col)) + 2
                #     worksheet.set_column(i, i, max(20, max_len), date_format)
                # elif col in percent_columns:
                #     worksheet.set_column(i, i, 17, percent_format)
                else:
                    max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
                    worksheet.set_column(i, i, max_len)


    # Format excel
    # src.output_to_excel.format_excel_file(OUTPUT_PATH)

    # Distribution
    subject = f"Monthly Attorney-Consultant-Engineer Report" 
    body = "Hi, \n\nAttached is the Attorney-Consultant-Engineer Report. If you have any questions, please reach out to BusinessIntelligence@bcsbmail.com \n\nThanks!"
    attachment_paths = [output_file_path]
    cdutils.distribution.email_out(EMAIL_TO, EMAIL_CC, subject, body, attachment_paths)


if __name__ == '__main__':
    print(f"Starting [{__version__}]")
    main()
    print("Complete!")