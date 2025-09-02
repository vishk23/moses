# %%
"""
Main Entry Point
"""
from pathlib import Path
import pandas as pd # type: ignore
import shutil
import src.swap_pnc.fetch_data # type: ignore
import src.swap_pnc.core # type: ignore
import cdutils.pkey_sqlite # type: ignore
import cdutils.hhnbr # type: ignore
import cdutils.loans.calculations # type: ignore
import cdutils.inactive_date # type: ignore
import src.swap_pnc.output_to_excel
import cdutils.database.connect # type: ignore
from sqlalchemy import text # type: ignore
import cdutils.input_cleansing # type: ignore
import cdutils.distribution # type: ignore
import src.config as config
import src._version

def process_assets_excel():
    assets_folder = config.ASSETS_FOLDER
    archive_folder = config.ARCHIVE_FOLDER
    staged_data_path = config.STAGED_DATA_PATH
    assets_folder.mkdir(exist_ok=True)
    archive_folder.mkdir(exist_ok=True)
    xlsx_files = list(assets_folder.glob("*.xlsx"))
    assert len(xlsx_files) <= 1, f"Found {len(xlsx_files)} .xlsx files in assets folder. Expected 0 or 1."
    if len(xlsx_files) == 0:
        print("No .xlsx files found in assets folder. Moving on.")
        return
    xlsx_file = xlsx_files[0]
    print(f"Processing file: {xlsx_file.name}")
    try:
        df1 = pd.read_excel(xlsx_file, sheet_name='DIRECT')
        df2 = pd.read_excel(xlsx_file, sheet_name='INDIRECT and RPA')
        common_cols = df1.columns.intersection(df2.columns)
        df1 = df1[common_cols]
        df2 = df2[common_cols]
        df = pd.concat([df1,df2], ignore_index=True)
        print(f"Successfully loaded {xlsx_file.name} with {len(df)} rows and {len(df.columns)} columns")
        df.to_csv(staged_data_path, index=False)
        print(f"Data written to {staged_data_path}")
        archive_file_path = archive_folder / xlsx_file.name
        if archive_file_path.exists():
            archive_file_path.unlink()
            print(f"Replaced existing file in archive: {archive_file_path.name}")
        shutil.move(str(xlsx_file), str(archive_file_path))
        print(f"Moved {xlsx_file.name} to archive folder")
    except Exception as e:
        print(f"Error processing {xlsx_file.name}: {str(e)}")
        raise

def main():
    print(f"Running {src._version.__version__}")
    process_assets_excel()
    data = src.swap_pnc.fetch_data.fetch_data()
    raw_data = src.swap_pnc.core.main_pipeline(data)
    raw_data = cdutils.pkey_sqlite.add_pkey(raw_data)
    raw_data = cdutils.pkey_sqlite.add_ownership_key(raw_data)
    raw_data = cdutils.pkey_sqlite.add_address_key(raw_data)
    househldacct = data['househldacct'].copy()
    raw_data = cdutils.hhnbr.add_hh_nbr(raw_data, househldacct)
    loan_category_df = cdutils.loans.calculations.categorize_loans(raw_data)
    loan_category_df = loan_category_df[['acctnbr','Category']].copy()
    df = pd.merge(raw_data, loan_category_df, on='acctnbr', how='left')
    df = cdutils.inactive_date.append_inactive_date(df)
    def fetch_data():
        wh_acctuserfields = text(f"""
        SELECT
            *
        FROM
            OSIBANK.WH_ACCTUSERFIELDS a
        WHERE
            (a.ACCTUSERFIELDCD = 'PNC')
        """)
        queries = [
            {'key':'wh_acctuserfields', 'sql':wh_acctuserfields, 'engine':1},
        ]
        data = cdutils.database.connect.retrieve_data(queries)
        return data
    data = fetch_data()
    wh_acctuserfields = data['wh_acctuserfields'].copy()
    wh_acctuserfields_schema = {
        'acctuserfieldvalue':'str',
        'acctnbr':'str'
    }
    df_schema = {
        'acctnbr':'str'
    }
    wh_acctuserfields = cdutils.input_cleansing.enforce_schema(wh_acctuserfields, wh_acctuserfields_schema)
    df = cdutils.input_cleansing.enforce_schema(df, df_schema)
    df_combined = wh_acctuserfields.merge(df, on='acctnbr', how='left')
    swap_exposure = df_combined[df_combined['product'] == 'SWAP Exposure Loans'].copy()
    other_loans = df_combined[df_combined['product'] != 'SWAP Exposure Loans'].copy()
    result = swap_exposure.merge(other_loans[['acctnbr','acctuserfieldvalue','orig_ttl_loan_amt','Net Balance']], on='acctuserfieldvalue',how='left',suffixes=('','_other'))
    result_cleaned = result[[
        'acctuserfieldvalue',
        'acctnbr',
        'ownersortname',
        'Net Available',
        'origdate',
        'loanofficer',
        'riskratingcd',
        'datemat',
        'inactivedate',
        'orig_ttl_loan_amt_other',
        'acctnbr_other',
        'Net Balance_other'
    ]].copy()
    PNC_STAGING_FILE = config.STAGED_DATA_PATH
    pnc_data = pd.read_csv(PNC_STAGING_FILE)
    pnc_data = pnc_data[['Deal ID','NPV+AI','Eff. Date']].copy()
    pnc_data_schema = {
        'Deal ID':'str'
    }
    pnc_data = cdutils.input_cleansing.enforce_schema(pnc_data, pnc_data_schema)
    result_cleaned_schema = {
        'acctuserfieldvalue':'str'
    }
    result_cleaned = cdutils.input_cleansing.enforce_schema(result_cleaned, result_cleaned_schema)
    result_cleaned = pd.merge(result_cleaned, pnc_data, left_on='acctuserfieldvalue', right_on='Deal ID', how='left')
    result_cleaned['% PNC Marked to BCSB Swap Exposure'] = result_cleaned['NPV+AI'] / result_cleaned['Net Available']
    result_cleaned = result_cleaned[[
        'acctuserfieldvalue',
        'acctnbr',
        'ownersortname',
        'Eff. Date',
        'Net Available',
        'NPV+AI',
        '% PNC Marked to BCSB Swap Exposure',
        'origdate',
        'loanofficer',
        'riskratingcd',
        'datemat',
        'inactivedate',
        'orig_ttl_loan_amt_other',
        'acctnbr_other',
        'Net Balance_other'
    ]].copy()
    result_cleaned = result_cleaned.rename(columns={
        'acctuserfieldvalue':'Dealer ID',
        'acctnbr':'Swap Exposure Account Number',
        'ownersortname':'Customer Name',
        'Eff. Date':'Effective Date',
        'Net Available':'BCSB Swap Exposure',
        'NPV+AI':'PNC Marked to Market',
        'origdate':'Date Opened',
        'loanofficer':'Responsibility Officer',
        'riskratingcd':'Risk',
        'datemat':'Maturity Date',
        'inactivedate':'Inactive Date',
        'orig_ttl_loan_amt_other':'Original SWAP Mortgage',
        'acctnbr_other':'SWAP Loan Account Number',
        'Net Balance_other':'SWAP Loan Net Balance'
    }).copy()
    result_cleaned = result_cleaned.sort_values(by='Customer Name').copy()
    OUTPUT_PATH = config.OUTPUT_PATH
    result_cleaned.to_excel(OUTPUT_PATH, sheet_name='Sheet1', index=False)
    src.swap_pnc.output_to_excel.format_excel_file(OUTPUT_PATH)
    recipients = config.EMAIL_TO
    bcc_recipients = config.EMAIL_BCC
    subject = f"SWAP Report" 
    body = "Hi, \n\nAttached is the Monthly SWAP Report. If you have any questions, please reach out to BusinessIntelligence@bcsbmail.com \n\nThanks!"
    attachment_paths = [OUTPUT_PATH]
    cdutils.distribution.email_out(recipients=recipients, bcc_recipients=bcc_recipients, subject=subject, body=body, attachment_paths=attachment_paths)

if __name__ == "__main__":
    main()