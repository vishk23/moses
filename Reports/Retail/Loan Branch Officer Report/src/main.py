"""
Loan Branch Officer Report - Main Entry Point

BUSINESS LOGIC EXTRACTED:

Data Sources & Relationships:
- OSIBANK.WH_ACCTCOMMON: Core account information including balances, rates, officers, branches
- OSIBANK.WH_LOANS: Loan-specific details like origination, terms, availability
- OSIBANK.WH_ACCTLOAN: Additional loan fields including credit limits and percentages sold
- OSIEXTN.HOUSEHLDACCT: Household account relationships for customer grouping

Business Rules:
- Only include active accounts (status: ACT, NPFM, DORM)
- Calculate net balance by subtracting charged-off amounts from book balance
- Handle Tax Exempt bonds (CM45) by using notebal instead of bookbalance
- Apply loan categorization based on product codes and characteristics
- Include primary and secondary loan officers for complete officer assignment

Data Processing Flow:
1. Fetch loan data from multiple database tables
2. Apply data type enforcement and schema validation
3. Join loan tables on account number
4. Calculate total exposure fields and clean data
5. Add primary keys and household numbers
6. Append secondary loan officers
7. Categorize loans by product type
8. Filter to required columns and rename for output
9. Generate Excel output with formatted data

Key Calculations:
- Net Balance = Book Balance - Charged Off Balance (COBAL)
- Total Exposure = Net Balance + Net Available + Net Collateral Reserve
- Tax Exempt bond handling: Use NOTEBAL for CM45 products instead of BOOKBALANCE

Business Intelligence Value:
- Provides comprehensive view of loan portfolio by branch and officer
- Enables loan officer performance tracking and portfolio analysis
- Supports business line reporting and management oversight
- Facilitates customer relationship management through household linking
"""

import pandas as pd
from datetime import datetime, timedelta
import calendar
import src.config
import src.loan_branch_officer.fetch_data
import src.loan_branch_officer.core
import src.loan_branch_officer.output_to_excel
import cdutils.pkey_sqlite 
import cdutils.hhnbr
import cdutils.selo
import cdutils.loans.calculations

def main():
    """Main report execution."""
    try:
        print(f"Starting {src.config.REPORT_NAME}")
        print(f"Environment: {src.config.ENV}")
        
        # Fetch data from database
        print("Fetching data from database...")
        data = src.loan_branch_officer.fetch_data.fetch_data()

        # Core transformation pipeline
        print("Processing core transformations...")
        raw_data = src.loan_branch_officer.core.main_pipeline(data)

        # Raw data with pkey appended
        print("Adding primary keys...")
        raw_data = cdutils.pkey_sqlite.add_pkey(raw_data)

        # Attach HH number
        print("Adding household numbers...")
        househldacct = data['househldacct'].copy()
        raw_data = cdutils.hhnbr.add_hh_nbr(raw_data, househldacct)

        # Attach secondary officer
        print("Adding secondary loan officers...")
        df = cdutils.selo.append_selo(raw_data)

        # Categorize loans
        print("Categorizing loans...")
        df = cdutils.loans.calculations.categorize_loans(df)

        # Add owner_id column for joining with agreements
        print("Adding owner_id...")
        df['owner_id'] = df.apply(
            lambda row: f"O{int(float(row['taxrptfororgnbr']))}" if pd.notna(row['taxrptfororgnbr']) and str(row['taxrptfororgnbr']).strip() != ''
            else f"P{int(float(row['taxrptforpersnbr']))}" if pd.notna(row['taxrptforpersnbr']) and str(row['taxrptforpersnbr']).strip() != ''
            else 'Unknown', axis=1
        )

        # Filter down fields
        print("Filtering and formatting output...")
        df = df[[
            'acctnbr',
            'ownersortname',
            'product',
            'mjaccttypcd',
            'currmiaccttypcd',
            'curracctstatcd',
            'loanofficer',
            'branchname',
            'Secondary Lending Officer',
            'contractdate',
            'Net Balance',
            'creditlimitamt',
            'noteopenamt',
            'Category',
            'portfolio_key',
            'owner_id'
        ]].copy()

        # Rename columns for final output
        df = df.rename(columns={
            'loanofficer': 'Primary Officer',
            'branchname': 'Branch Name',
            'mjaccttypcd': 'Major',
            'currmiaccttypcd': 'Minor'
        }).copy()

        # Generate output with report date (previous month)
        # Calculate previous month and year
        today = datetime.now()
        first_day_current_month = today.replace(day=1)
        last_day_previous_month = first_day_current_month - timedelta(days=1)
        report_month = calendar.month_name[last_day_previous_month.month]
        report_year = last_day_previous_month.year
        
        output_filename = f"loan_report_branch_officer_{report_month}_{report_year}.xlsx"
        output_file = src.config.OUTPUT_DIR / output_filename
        print(f"Writing output to: {output_file}")
        print(f"Report period: {report_month} {report_year}")
        
        # Write and format Excel file
        src.loan_branch_officer.output_to_excel.write_and_format_excel(df, output_file)

        # Email distribution
        if src.config.EMAIL_TO:
            import cdutils.distribution
            
            subject = f"{src.config.REPORT_NAME} - {report_month} {report_year}"
            body = f"""Hi,

Attached is the {src.config.REPORT_NAME} for {report_month} {report_year}. This report provides loan portfolio information organized by branch and loan officer.

If you have any questions, please reach out to BusinessIntelligence@bcsbmail.com

Thanks!"""
            
            cdutils.distribution.email_out(
                recipients=src.config.EMAIL_TO,
                cc_recipients=src.config.EMAIL_CC,
                subject=subject,
                body=body,
                attachment_paths=[output_file]
            )
            print(f"Email sent to {len(src.config.EMAIL_TO)} recipients")
        else:
            print("Development mode - email not sent")

        print(f"Completed {src.config.REPORT_NAME}")
        print(f"Records processed: {len(df):,}")
        
        return True
        
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return False
    except Exception as e:
        print(f"Error in {src.config.REPORT_NAME}: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        exit(1)