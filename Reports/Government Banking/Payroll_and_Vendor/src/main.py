"""
Payroll and Vendor Report - Main Entry Point

BUSINESS LOGIC EXTRACTED:

Data Sources & Relationships:
- COCCDM.WH_RTXN table for transaction data
- Two accounts: 150523994.00 (vendor) and 150524009.00 (payroll)
- 30-day lookback period for both reports

Business Rules:
- Filters transactions with non-null check numbers only
- Payroll output: Fixed-width text format with specific field positions
- Vendor output: CSV format with 6 columns (including 2 blank columns)
- Transaction amounts converted to positive values in output
- Check numbers padded to 10 digits with leading zeros

Data Processing Flow:
1. Query last 30 days of transactions from both accounts
2. Format payroll data as fixed-width text file
3. Format vendor data as CSV with specific column structure
4. Output both files to local output directory

Key Calculations:
- Date range: Current date minus 30 days
- Amount formatting: Remove decimal points, pad to 10 digits
- Check number formatting: Pad to 10 digits with leading zeros
- Date formatting: MMDDYY for payroll, MM/DD/YYYY for vendor

Business Intelligence Value:
- Government banking transaction monitoring and reconciliation
- Payroll and vendor payment tracking for audit purposes
- Formatted outputs for downstream processing systems
"""

import cdutils.database.connect # type: ignore
from sqlalchemy import text # type: ignore
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

import src.config
import src._version

# Query parameters
PAYROLL_VENDOR_ACCOUNT = 150523994.00
PAYROLL_ACCOUNT = 150524009.00
ANALYSIS_DAYS = 30

def main():
    print(f"Running {src._version.__version__}")

    def fetch_data():
        """
        Main data query
        """
        end_date = datetime.today()
        start_date = end_date - timedelta(days=ANALYSIS_DAYS)
    
        end_date = datetime.today().strftime('%Y-%m-%d')+' 00:00:00'
        start_date = start_date.strftime('%Y-%m-%d')+' 00:00:00'
        
        # Engine 2
        vendor_query = text(f"""
            select COCCDM.WH_RTXN.ACCTNBR,
                COCCDM.WH_RTXN.POSTDATE,
                COCCDM.WH_RTXN.CHECKNBR,
                COCCDM.WH_RTXN.TRANAMT 
            from COCCDM.WH_RTXN 
            where COCCDM.WH_RTXN.ACCTNBR = {PAYROLL_VENDOR_ACCOUNT} 
                and COCCDM.WH_RTXN.POSTDATE >= TO_DATE('{start_date}', 'yyyy-mm-dd hh24:mi:ss') 
                and COCCDM.WH_RTXN.POSTDATE <= TO_DATE('{end_date}', 'yyyy-mm-dd hh24:mi:ss')
            and COCCDM.WH_RTXN.CHECKNBR is not NULL
        """)
        
        payroll_query = text(f"""
            select COCCDM.WH_RTXN.ACCTNBR,
                COCCDM.WH_RTXN.POSTDATE,
                COCCDM.WH_RTXN.CHECKNBR,
                COCCDM.WH_RTXN.TRANAMT 
            from COCCDM.WH_RTXN 
            where COCCDM.WH_RTXN.ACCTNBR = {PAYROLL_ACCOUNT} 
                and COCCDM.WH_RTXN.POSTDATE >= TO_DATE('{start_date}', 'yyyy-mm-dd hh24:mi:ss') 
                and COCCDM.WH_RTXN.POSTDATE <= TO_DATE('{end_date}', 'yyyy-mm-dd hh24:mi:ss')
            and COCCDM.WH_RTXN.CHECKNBR is not NULL    
            """)

        queries = [
            {'key':'vendor_query', 'sql':vendor_query, 'engine':2},
            {'key':'payroll_query', 'sql':payroll_query, 'engine':2}
        ]


        data = cdutils.database.connect.retrieve_data(queries)
        return data

    data = fetch_data()

    vendor_query = data['vendor_query'].copy()
    payroll_query = data['payroll_query'].copy()


    def format_payroll_row(row):
        acct_prefix = "  R150524009 "
        checknbr = str(row['checknbr']).zfill(10)
        postdate = row['postdate'].strftime('%m%d%y')
        tranamt_abs = abs(float(row['tranamt']))  # Ensure it's positive
        tranamt_str = f"{tranamt_abs:.2f}".replace('.', '')  # Remove decimal point
        tranamt_padded = tranamt_str.zfill(10)
        return f"{acct_prefix}{checknbr}{postdate}{tranamt_padded}"

    # Format each row
    formatted_lines = payroll_query.apply(format_payroll_row, axis=1).tolist()

    # Payroll output path
    PAYROLL_OUTPUT_PATH = src.config.OUTPUT_DIR / 'payroll_report.txt' 

    # Write to a .txt file
    with open(PAYROLL_OUTPUT_PATH, "w") as f:
        for line in formatted_lines:
            f.write(line + "\n")
            
    # Format vendor data to match the required output
    vendor_formatted = vendor_query.copy()

    # Make transaction amount positive
    vendor_formatted['tranamt'] = vendor_formatted['tranamt'].abs()

    # Format postdate to MM/DD/YYYY
    vendor_formatted['postdate'] = vendor_formatted['postdate'].dt.strftime('%m/%d/%Y')

    # Create output DataFrame with 6 columns
    vendor_output = vendor_formatted[['acctnbr', 'checknbr', 'tranamt', 'postdate']].copy()

    # Insert empty columns in the correct positions
    vendor_output.insert(3, '', '')  # Blank column after tranamt

    vendor_output = vendor_output[['acctnbr', 'checknbr', 'tranamt', '', '', 'postdate']]

    # Write to CSV without header and index
    VENDOR_OUTPUT_PATH = src.config.OUTPUT_DIR / 'vendor_report.csv' 

    vendor_output.to_csv(VENDOR_OUTPUT_PATH, index=False, header=False)


if __name__ == "__main__":
    print(f"Starting Payroll and Vendor Report")
    main()
    print("Complete!")