"""
CLO Active Portfolio Officer Report - Main Entry Point

BUSINESS LOGIC EXTRACTED:

Data Sources & Relationships:
- fetch_data(): Pulls active commercial loan portfolio from database
- Multiple table joins: loan data, household accounts, user fields
- Portfolio key relationships via cdutils.pkey_sqlite (ownership, address keys)
- Loan categorization via cdutils.loans.calculations

Business Rules:
- Active commercial loan portfolio organized by Responsibility Officer
- Includes loans with current balances and various statuses
- Subtotals calculated per officer with weighted average interest rates
- SBA guarantee expiration dates tracked in user fields
- Risk rating and FDIC category classification included

Data Processing Flow:
1. Fetch core loan data from database
2. Add portfolio keys (pkey, ownership_key, address_key)  
3. Add household numbers for relationship grouping
4. Categorize loans by type (commercial, consumer, etc.)
5. Append inactive dates and SBA expiration data
6. Rename columns for readability
7. Sort by Responsibility Officer, then Customer Name
8. Generate officer subtotals with aggregated metrics
9. Output to Excel with advanced formatting
10. Email distribution to commercial lending team

Key Calculations:
- Weighted average interest rates by net balance for officer subtotals
- Net Available Credit = Available Credit - some adjustment logic
- Officer-level aggregations: sum balances, count loans, max inactive dates
- Excel formatting: currency, date, and percentage column formatting

Business Intelligence Value:
- Commercial lending portfolio management and monitoring
- Officer workload and portfolio balance tracking
- Risk assessment via credit ratings and loan categorization
- Relationship-based reporting for customer management
"""
from pathlib import Path
from typing import List
from datetime import datetime

import pandas as pd # type: ignore

import src.config
import src.fetch_data # type: ignore
import src.core_transform # type: ignore
import cdutils.pkey_sqlite # type: ignore
import cdutils.hhnbr # type: ignore
import src.output_to_excel
import cdutils.loans.calculations # type: ignore
import cdutils.inactive_date # type: ignore
# import cdutils.selo # type: ignore


def main():
    """Main report execution function"""
    
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

    # Renaming for readability
    names = {
        'loanofficer': 'Responsibility Officer',
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
    df = df[['Responsibility Officer', 'Product Name', 'Customer Name', 'Account Number', 'Account Status', 'Date Opened', 'Original Balance', 'Current Balance', 'Net Balance', 'Available Credit', 'Interest Rate', 'Next Rate Change Date', 'LOC Inactive Date', 'Maturity Date', 'Risk', 'SBA Expiration Date', 'Net Available Credit', 'FDICCATCD']]

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
                'Product Name': n,
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

    # Output to excel - generate filename with current date
    def get_output_filename():
        today = datetime.today()
        date = f"{today.strftime('%B')} {today.day} {today.year}"
        return f'CLO Active Portfolio {date}.xlsx'
    
    output_filename = get_output_filename()
    OUTPUT_PATH = src.config.OUTPUT_DIR / output_filename
    # df.to_excel(OUTPUT_PATH, sheet_name='Sheet1', index=False)

    # mapping dataframes to sheets in final product
    sheets = [
        ('CLO Active Portfolio', df)
    ]

    df['Account Number'] = df['Account Number'].apply(lambda x: str(int(x)) if pd.notnull(x) else '') # so that numbers dont get shortened to scientific notation

    # Excel formatting configuration
    MONETARY_COLUMNS = ['Original Balance', 'Current Balance', 'Net Balance', 'Available Credit', 'Net Available Credit']
    DATE_COLUMNS = ['Date Opened', 'Next Rate Change Date', 'LOC Inactive Date', 'Maturity Date', 'SBA Guarantee Expiration Date']
    PERCENT_COLUMNS = ['Interest Rate']

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
                if col in MONETARY_COLUMNS:
                    max_len = max(currency_string_length(df[col]), len(col)) + 2
                    worksheet.set_column(i, i, max_len, currency_format)
                elif col in DATE_COLUMNS:
                    max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
                    worksheet.set_column(i, i, max(20, max_len), date_format)
                elif col in PERCENT_COLUMNS:
                    worksheet.set_column(i, i, 17, percent_format)
                else:
                    max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
                    worksheet.set_column(i, i, max_len)


    # Distribution (currently disabled - enable when recipients are determined)
    if src.config.EMAIL_TO:  # Only send emails if recipients are configured
        import cdutils.distribution # type: ignore
        
        # Generate email subject with current date
        today = datetime.today()
        date = f"{today.strftime('%B')} {today.day} {today.year}"
        email_subject = f"CLO Active Portfolio Report - {date}"
        
        email_body = """Hi,

Attached is the CLO Active Portfolio Officer Report. If you have any questions, please reach out to BusinessIntelligence@bcsbmail.com

Thanks!"""
        
        cdutils.distribution.email_out(
            recipients=src.config.EMAIL_TO, 
            bcc_recipients=src.config.EMAIL_CC, 
            subject=email_subject, 
            body=email_body, 
            attachment_paths=[OUTPUT_PATH]
        )
        print(f"Email sent to {len(src.config.EMAIL_TO)} recipients with {len(src.config.EMAIL_CC)} CC")
    else:
        print(f"Development mode or no recipients configured - email not sent. Output file: {OUTPUT_PATH}")


if __name__ == '__main__':
    print("Starting CLO Active Portfolio Officer Report")
    main()
    print("Complete!")