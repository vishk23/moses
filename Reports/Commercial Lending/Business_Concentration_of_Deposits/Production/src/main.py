
"""
Main Entry Point
"""
from pathlib import Path

import pandas as pd # type: ignore

import cdutils.pkey_sqlite # type: ignore
import cdutils.filtering # type: ignore
import cdutils.input_cleansing # type: ignore
import cdutils.cmo_append # type: ignore
import src.add_fields
import src.core_transform
import src.output_to_excel
from src._version import __version__
import src.output_to_excel_multiple_sheets
import cdutils.distribution # type: ignore
from datetime import datetime
from dateutil.relativedelta import relativedelta

def main(production_flag: bool=False):
    if production_flag:
        BASE_PATH = Path(r'\\00-DA1\Home\Share\Line of Business_Shared Services')
        assert "prod" in __version__, (f"Cannot run in production mode without 'prod' in the __version__")
    else:
        BASE_PATH = Path('.')



    # %%
    # Get staging data from the daily deposit update. View dev section of documentation for more detail
    INPUT_PATH = Path(r"\\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Data_Analytics\Daily_Deposit_Update\Production\output\DailyDeposit_staging.xlsx")
    data = pd.read_excel(INPUT_PATH)

    # Add portfolio key
    data = cdutils.pkey_sqlite.add_pkey(data)

    # Add int rate
    data = src.add_fields.add_noteintrate(data)


    # Custom list of minors (Business Deposits)
    minors = [
        'CK24', # 1st Business Checking
        'CK12', # Business Checking
        'CK25', # Simple Business Checking
        'CK30', # Business Elite Money Market
        'CK19', # Business Money Market
        'CK22', # Business Premium Plus MoneyMkt
        'CK23', # Premium Business Checking
        'CK40', # Community Assoc Reserve
        'CD67', # Commercial Negotiated Rate
        'CD01', # 1 Month Business CD
        'CD07', # 3 Month Business CD
        'CD17', # 6 Month Business CD
        'CD31', # 1 Year Business CD
        'CD35', # 1 Year Business CD
        'CD37', # 18 Month Business CD
        'CD38', # 2 Year Business CD
        'CD50', # 3 Year Business CD
        'CD53', # 4 Year Business CD
        'CD59', # 5 Year Business CD
        'CD76', # 9 Month Business CD
        'CD84', # 15 Month Business CD
        'CD95', # Business <12 Month Simple CD
        'CD96', # Business >12 Month Simple CD
        'CK28', # Investment Business Checking
        'CK33', # Specialty Business Checking
        'CK34', # ICS Shadow - Business - Demand
        'SV06' # Business Select High Yield
    ]

    # Filter to only business deposit accounts
    data = cdutils.filtering.filter_to_business_deposits(data, minors)


    # Add CMO
    data = cdutils.cmo_append.append_cmo(data)


    data_schema = {
        'noteintrate': float
    }

    data = cdutils.input_cleansing.enforce_schema(data, data_schema).copy()




    # %%
    # Exclude BCSB internal accounts
    data = data[~data['ownersortname'].str.contains('BRISTOL COUNTY SAVINGS', case=False, na=False)].copy()

    # %%
    data

    # %%







    # %%
    # %%
    ASSETS_PATH = Path('./assets')

    files = [f for f in ASSETS_PATH.iterdir() if f.is_file()]

    assert len(files) == 1, f"Expected exactly 1 file in {ASSETS_PATH}, found {len(files)}."

    file = files[0]
    assert file.suffix == '.csv', f"Expected an excel file"

    xaa_data = pd.read_csv(file, header=3)

    # %%
    # xaa_data.info()

    #

    # %%




    # # %%
    # xaa_data['Analyzed Charges (Pre-ECR)'] = xaa_data['Analyzed Charges (Pre-ECR)'].str.replace('[\$,]','',regex=True)
    # xaa_data['Combined Result for Settlement Period (Post-ECR + Fee-Based Total)'] = xaa_data['Combined Result for Settlement Period (Post-ECR + Fee-Based Total)'].str.replace('[\$,]','',regex=True)

    # %%
    xaa_schema = {
        'Analyzed Charges':'float',
        'Combined Result for Settlement Period':'float',
        'Earnings Credit Rate':'float',
        'Debit Account Number':'str'
    }
    xaa_data = cdutils.input_cleansing.enforce_schema(xaa_data, xaa_schema)



    # %%

    from datetime import datetime, timedelta

    def create_account_summary_alternative(xaa_data, date_col='cycle_date'):
        # Ensure date column is datetime
        xaa_data = xaa_data.copy()
        xaa_data[date_col] = pd.to_datetime(xaa_data[date_col])
        # Calculate cutoff date for 12 months
        max_date = xaa_data[date_col].max()
        cutoff_date = max_date - timedelta(days=365)
        # Add ranking column to identify latest month per account
        xaa_data['date_rank'] = (xaa_data
                                .groupby('Debit Account Number')[date_col]
                                .rank(method='dense', ascending=False))
        # Create flags for latest month and trailing 12 months
        xaa_data['is_latest_month'] = xaa_data['date_rank'] == 1
        xaa_data['is_trailing_12m'] = xaa_data[date_col] >= cutoff_date
        # Aggregate using conditional sums
        summary = (xaa_data
                .groupby('Debit Account Number')
                .agg({
                    # Latest month aggregations
                    'Analyzed Charges': [
                        lambda x: x[xaa_data.loc[x.index, 'is_latest_month']].sum(),
                        lambda x: x[xaa_data.loc[x.index, 'is_trailing_12m']].sum(),
                    ],
                    'Combined Result for Settlement Period': [
                        lambda x: x[xaa_data.loc[x.index, 'is_latest_month']].sum(),
                        lambda x: x[xaa_data.loc[x.index, 'is_trailing_12m']].sum()
                    ],
                    'Earnings Credit Rate': [
                        lambda x: x[xaa_data.loc[x.index, 'is_latest_month']].mean(),
                        lambda x: x[xaa_data.loc[x.index, 'is_trailing_12m']].mean()
                    ],
                    'Primary Officer Name': 'first',
                    'Secondary Officer Name': 'first',
                    'Treasury Officer Name': 'first'
                })
                .reset_index())
        # Flatten column names
        summary.columns = [
            'Debit Account Number',
            'Latest_Month_Analyzed_Charges',
            'Trailing_12M_Analyzed_Charges',
            'Latest_Month_Combined_Result',
            'Trailing_12M_Combined_Result',
            'Latest_Month_ECR',
            'Trailing_12M_Avg_ECR',
            'Primary_Officer_Name_XAA',
            'Secondary_Officer_Name_XAA',
            'Treasury_Officer_Name_XAA'
        ]
        # Reorder columns
        column_order = [
            'Debit Account Number',
            'Latest_Month_Analyzed_Charges',
            'Latest_Month_Combined_Result',
            'Trailing_12M_Analyzed_Charges',
            'Trailing_12M_Combined_Result',
            'Latest_Month_ECR',
            'Trailing_12M_Avg_ECR',
            'Primary_Officer_Name_XAA',
            'Secondary_Officer_Name_XAA',        
            'Treasury_Officer_Name_XAA'
        ]
        return summary[column_order]


    # %%
    summarized_xaa = create_account_summary_alternative(xaa_data, date_col='Cycle End Date')

    # %%
    summarized_xaa_schema = {
        'Primary_Officer_Name_XAA':'str',
        'Secondary_Officer_Name_XAA':'str',        
        'Treasury_Officer_Name_XAA':'str'
    }
    summarized_xaa = cdutils.input_cleansing.enforce_schema(summarized_xaa, summarized_xaa_schema)

    # %%

    # %%
    summarized_xaa = summarized_xaa.rename(columns={
        'Debit Account Number':'acctnbr',

    }).copy()

    assert summarized_xaa['acctnbr'].is_unique, "Duplicates"




    # %%





    # %%
    # %%
    merged_data = pd.merge(data, summarized_xaa, on='acctnbr', how='left')

    # %%

    fill_na_column_list = [
        'Latest_Month_Analyzed_Charges',
        'Latest_Month_Combined_Result',
        'Trailing_12M_Analyzed_Charges',
        'Trailing_12M_Combined_Result',
        'Latest_Month_ECR',
        'Trailing_12M_Avg_ECR',
    ]
    for item in fill_na_column_list:
        merged_data[item] = merged_data[item].fillna(0)


    # Sort descending order of notebal
    merged_data = merged_data.sort_values(by='notebal', ascending=False)

    # %%
    # merged_data.info()

    # %%
    merged_data



    # %%
    # This part doesn't work. Look at noteinrate, gets weird

    # %%
    formatted_data = src.core_transform.main_pipeline(merged_data)

    # %%
    formatted_data

    # %%
    formatted_data = formatted_data.rename(columns={
        'portfolio_key':'Portfolio Key',
        'product':'Product',
        '3Mo_AvgBal':'3Mo Avg Bal',
        'TTM_AvgBal':'TTM Avg Bal',
        'TTM_DAYS_OVERDRAWN':'TTM Days Overdrawn',
        'TTM_NSF_COUNT':'TTM NSF Count'
    }).copy()


    # %%
    # Create summary sheet

    summary_data = formatted_data[~(formatted_data['Portfolio Key'] == "") & (formatted_data['Acct No.'] == "")].copy()
    summary_data = summary_data[[
        'Portfolio Key',
        'Borrower Name',
        'Account Officer',
        'Cash Management Officer',
        'Current Balance',
        'Interest Rate',
        '3Mo Avg Bal',
        'TTM Avg Bal',
        'Year Ago Balance',
        'TTM Days Overdrawn',
        'TTM NSF Count',
        'Current Mo Analyzed Fees (Pre-ECR)',
        'Current Mo Net Analyzed Fees (Post-ECR)',
        'TTM Analyzed Fees (Pre-ECR)',
        'TTM Net Analyzed Fees (Post-ECR)',
        'Current ECR'
    ]].copy()


    # %%
    # %%
    # Output to excel (raw data)
    # BASE_PATH = Path('.')
    OUTPUT_PATH = BASE_PATH / Path('./output/business_deposits_concentration_with_xaa.xlsx')
    with pd.ExcelWriter(OUTPUT_PATH, engine="openpyxl") as writer:
        formatted_data.to_excel(writer, sheet_name='Relationship Detail', index=False)
        summary_data.to_excel(writer, sheet_name='Relationship Summary', index=False)
        merged_data.to_excel(writer, sheet_name='Unformatted', index=False)


    # Format excel
    src.output_to_excel_multiple_sheets.format_excel_file(OUTPUT_PATH)


    # Usage
    # # Distribution
    recipients = [
        # "chad.doorley@bcsbmail.com"
        "Hasan.Ali@bcsbmail.com",
        "steve.sherman@bcsbmail.com",
        "Michael.Patacao@bcsbmail.com",
        "Jeffrey.Pagliuca@bcsbmail.com",
        "Timothy.Chaves@bcsbmail.com",
        "Isaura.Tavares@bcsbmail.com",
        "Taylor.Tierney@bcsbmail.com",
        "Anderson.Lovos@bcsbmail.com",

    ]
    bcc_recipients = [
        "chad.doorley@bcsbmail.com",
        "businessintelligence@bcsbmail.com"
    ]

    prev_month = datetime.now() - relativedelta(months=1)
    result = prev_month.strftime("%B %Y")

    subject = f"Business Deposits + XAA Concentration Report - {result}" 
    body = "Hi all, \n\nAttached is the Business Deposits + XAA Concentration Report through the most recent month end. If you have any questions, please reach out to BusinessIntelligence@bcsbmail.com\n\n"
    attachment_paths = [OUTPUT_PATH]

    cdutils.distribution.email_out(
        recipients = recipients, 
        bcc_recipients = bcc_recipients, 
        subject = subject, 
        body = body, 
        attachment_paths = attachment_paths
        )

if __name__ == '__main__':
    print(f"Starting [{__version__}]")
    # main(production_flag=True)
    main()
    print("Complete!")



# %%



