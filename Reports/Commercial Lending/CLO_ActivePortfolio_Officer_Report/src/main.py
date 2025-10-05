"""
Main Entry Point
"""
from pathlib import Path
from typing import List
from datetime import datetime
from calendar import month_name
import pandas as pd # type: ignore
from deltalake import DeltaTable

import src.fetch_data # type: ignore
import src.core_transform # type: ignore
import cdutils.pkey_sqlite # type: ignore
import cdutils.hhnbr # type: ignore
import src.output_to_excel
import cdutils.loans.calculations # type: ignore
import cdutils.inactive_date # type: ignore
import cdutils.append_pm.core # type: ignore
import cdutils.input_cleansing # type: ignore
# import cdutils.selo # type: ignore
from src._version import __version__
from src.config import BASE_PATH

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
    df = cdutils.inactive_date.append_inactive_date(df)

    # Bring in another column to show SBA Guarantee Expiration Date
    wh_acctuserfields = data['wh_acctuserfields'].copy()
    wh_acctuserfields['acctnbr'] = wh_acctuserfields['acctnbr'].astype(int)
    df['acctnbr'] = df['acctnbr'].astype(int)
    df = pd.merge(df, wh_acctuserfields, on='acctnbr', how='left')

    # dtype casting
    df_schema = {
        'acctnbr':'str'
    }
    df = cdutils.input_cleansing.cast_columns(df, df_schema)

    # Append portfolio manager
    pm = cdutils.append_pm.core.append_pm()
    df = df.merge(pm, how='left', on='acctnbr') 

    # Renaming for readability
    names = {
        'loanofficer': 'Responsibility Officer',
        'persname': 'Portfolio Manager',
        'product': 'Product Name',
        'ownersortname': 'Customer Name',
        'acctnbr': 'Account Number',
        'curracctstatcd': 'Account Status',
        'origdate': 'Date Opened',
        'orig_ttl_loan_amt': 'Original Balance',
        'notebal': 'Current Balance',
        'availbalamt': 'Available Credit',
        'noteintrate': 'Interest Rate',
        'notenextratechangedate': 'Next Rate Change Date',
        'inactivedate': 'LOC Inactive Date',
        'datemat': 'Maturity Date',
        'riskratingcd': 'Risk',
        'acctuserfieldvalue': 'SBA Expiration Date',
        'Net Available': 'Net Available Credit',
        'fdiccatcd': 'FDICCATCD'
    }
    df = df.rename(columns=names)

    # Grabbing relevant columns
    df = df[['Responsibility Officer', 'Portfolio Manager', 'Product Name', 'Customer Name', 'Account Number', 'Account Status', 'Date Opened', 'Original Balance', 'Current Balance', 'Net Balance', 'Available Credit', 'Interest Rate', 'Next Rate Change Date', 'LOC Inactive Date', 'Maturity Date', 'Risk', 'SBA Expiration Date', 'Net Available Credit', 'FDICCATCD']]

    # Set datetime column for SBA exp date
    # df['SBA Expiration Date'] = pd.to_datetime(df['SBA Expiration Date'])

    # Organizing by Responibility Officer and then inside that group organizing by Customer Name
    df = df.sort_values(['Responsibility Officer', 'Customer Name'])
    df = df.reset_index(drop=True)

    # building totals by officer rows
    result_rows = []
    officer_groups = {name: group for name, group in df.groupby('Responsibility Officer')}
    for officer_name, group in officer_groups.items():
        officer = group['Responsibility Officer'].iloc[0]
        n = len(group)
        result_rows.append(group)
        if not group.empty:
            result_rows.append(pd.DataFrame({
                'Responsibility Officer': f'Subtotal: {officer}', 
                'Portfolio Manager': n,
                'Original Balance': group['Original Balance'].sum(),
                'Current Balance': group['Current Balance'].sum(),
                'Net Balance': group['Net Balance'].sum(),
                'Available Credit': group['Available Credit'].sum(),
                # Using weighted average instead of simple average
                'Interest Rate': (group['Interest Rate'] * group['Net Balance']).sum() / group['Net Balance'].sum(), #group['Interest Rate'].mean(),
                'LOC Inactive Date': group['LOC Inactive Date'].max(),
                'Net Available Credit': group['Net Available Credit'].sum(),
                'Temp-Row': [1] # needed to avoid errors
            }))
    
    df = pd.concat(result_rows, ignore_index=True).drop('Temp-Row', axis=1)

    # grabbing date for filename
    today = datetime.today()
    current_first_day = today.replace(day=1)
    prev_year = current_first_day.year - 1 if current_first_day == 1 else current_first_day.year
    prev_month = 12 if current_first_day.month == 1 else current_first_day.month - 1
    prev_month_name = month_name[prev_month] + " " + str(prev_year)
    filename_string = 'CLO Active Portfolio_' + prev_month_name + '.xlsx'
    
    # Output to excel (raw data)
    OUTPUT_DIR = BASE_PATH / "output"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH = OUTPUT_DIR / filename_string
    # df.to_excel(OUTPUT_PATH, sheet_name='Sheet1', index=False)

    # mapping dataframes to sheets in final product
    sheets = [
        ('CLO Active Portfolio', df)
    ]

    df['Account Number'] = df['Account Number'].apply(lambda x: str(int(x)) if pd.notnull(x) else '') # so that numbers dont get shortened to scientific notation

    date_columns = ['Date Opened', 'Next Rate Change Date', 'LOC Inactive Date', 'Maturity Date'] 
    monetary_columns = ['Original Balance', 'Current Balance', 'Net Balance', 'Available Credit', 'Net Available Credit']
    percent_columns = ['Interest Rate']
    
    def currency_string_length(series):
        return series.map(lambda x: f"${x:,.2f}" if pd.notnull(x) else '').map(len).max()

    with pd.ExcelWriter(OUTPUT_PATH, engine='xlsxwriter', datetime_format='mm/dd/yyyy') as writer:
        for sheet_name, df in sheets:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            worksheet = writer.sheets[sheet_name]
            workbook = writer.book

            # format for monetary columns
            currency_format = workbook.add_format({'num_format': '$#,##0.00'})
            # format for datetime columns
            date_format = workbook.add_format({'num_format': 'mm/dd/yyyy'})

            percent_format = workbook.add_format({'num_format': '0.00%'})
            # percent_col_idx = df.columns.get_loc('Interest Rate')
            
            # worksheet.set_column(percent_col_idx, percent_col_idx, 17, percent_format)

            # Freeze the top row
            worksheet.freeze_panes(1, 0)

            # auto-fit each column
            for i, col in enumerate(df.columns):
                if col in monetary_columns:
                    max_len = max(currency_string_length(df[col]), len(col)) + 2
                    worksheet.set_column(i, i, max_len, currency_format)
                elif col in date_columns:
                    max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
                    worksheet.set_column(i, i, max(20, max_len), date_format)
                elif col in percent_columns:
                    worksheet.set_column(i, i, 17, percent_format)
                else:
                    max_len = max(df[col].astype(str).map(len).max(), len(col)) + 4
                    worksheet.set_column(i, i, max_len)


    # Format excel
    # src.output_to_excel.format_excel_file(OUTPUT_PATH)

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
    main()
    print("Complete!")