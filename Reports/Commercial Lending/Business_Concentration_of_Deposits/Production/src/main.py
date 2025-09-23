
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
        'SV06', # Business Select High Yield
        'CK13',
        'CK15',
        'CK41'
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

    xaa_data = pd.read_csv(file)

    # %%
    # xaa_data.info()

    #

    # %%




    # # %%
    # xaa_data['Analyzed Charges (Pre-ECR)'] = xaa_data['Analyzed Charges (Pre-ECR)'].str.replace('[\$,]','',regex=True)
    # xaa_data['Combined Result for Settlement Period (Post-ECR + Fee-Based Total)'] = xaa_data['Combined Result for Settlement Period (Post-ECR + Fee-Based Total)'].str.replace('[\$,]','',regex=True)

    # Rename to match schema from earlier
    xaa_data = xaa_data.rename(columns={
        'Analyzed Charges (Pre-ECR)':'Analyzed Charges',
        'Combined Result for Settlement Period (Post-ECR)':'Combined Result for Settlement Period'
    })
    # fix csv formatting of float fields
    cols_to_adjust = ['Analyzed Charges','Combined Result for Settlement Period']

    for col in cols_to_adjust:
        xaa_data[col] = xaa_data[col].str.replace(r'[$,]','', regex=True).astype(float)

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


    def create_account_summary_alternative(xaa_data, date_col='cycle_date', target_previous_month=none):
        xaa_data = xaa_data.copy()
        xaa_data[date_col] = pd.to_datetime(xaa_data[date_col])

        # pick target month (previous month in the data unless explicitly provided)
        if target_previous_month is none:
            periods = sorted(xaa_data[date_col].dt.to_period('m').unique(), reverse=true)
            if len(periods) < 2:
                raise valueerror("not enough periods to determine previous month.")
            target_period = periods[1]
        else:
            target_period = (pd.period(target_previous_month, freq='m')
                            if isinstance(target_previous_month, str)
                            else target_previous_month)

        is_target_month = (
            (xaa_data[date_col].dt.year == target_period.year) &
            (xaa_data[date_col].dt.month == target_period.month)
        )

        # trailing-12-months window inclusive of the target month
        target_end = target_period.to_timestamp(how='end')
        cutoff_date = target_end - relativedelta(months=12) + relativedelta(days=1)
        is_trailing_12m = xaa_data[date_col] >= cutoff_date

        # helpers that align masks to the group index
        def sum_where(mask):
            return lambda s: s.where(mask.loc[s.index]).sum()

        def mean_where(mask):
            return lambda s: s.where(mask.loc[s.index]).mean()

        summary = (
            xaa_data
            .groupby('debit account number')
            .agg({
                'analyzed charges': [
                    sum_where(is_target_month),
                    sum_where(is_trailing_12m),
                ],
                'combined result for settlement period': [
                    sum_where(is_target_month),
                    sum_where(is_trailing_12m),
                ],
                'earnings credit rate': [
                    mean_where(is_target_month),
                    mean_where(is_trailing_12m),
                ],
                'primary officer name': 'first',
                'secondary officer name': 'first',
                'treasury officer name': 'first',
            })
            .reset_index()
        )

        # flatten columns to your expected names
        summary.columns = [
            'debit account number',
            'latest_month_analyzed_charges',
            'trailing_12m_analyzed_charges',
            'latest_month_combined_result',
            'trailing_12m_combined_result',
            'latest_month_ecr',
            'trailing_12m_avg_ecr',
            'primary_officer_name_xaa',
            'secondary_officer_name_xaa',
            'treasury_officer_name_xaa',
        ]

        column_order = [
            'debit account number',
            'latest_month_analyzed_charges',
            'latest_month_combined_result',
            'trailing_12m_analyzed_charges',
            'trailing_12m_combined_result',
            'latest_month_ecr',
            'trailing_12m_avg_ecr',
            'primary_officer_name_xaa',
            'secondary_officer_name_xaa',
            'treasury_officer_name_xaa',
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

    # cdutils.distribution.email_out(
    #     recipients = recipients, 
    #     bcc_recipients = bcc_recipients, 
    #     subject = subject, 
    #     body = body, 
    #     attachment_paths = attachment_paths
    #     )

if __name__ == '__main__':
    print(f"Starting [{__version__}]")
    # main(production_flag=True)
    main()
    print("Complete!")



# %%



