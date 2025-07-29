import src.fetch_data as fetch_data
from src._version import __version__
from src.config import OUTPUT_DIR, EMAIL_TO, EMAIL_CC

import pandas as pd # type: ignore
from datetime import datetime
from pathlib import Path
import os

import cdutils.distribution # type: ignore

def main() -> None:

    # grabbing all relevant data we will need
    data = fetch_data.fetch_data()

    # left joining all data together
    merged_df = pd.merge(data['wh_acctcommon'], data['wh_acctloan'], on='acctnbr', how='left')
    # merged_df = pd.merge(merged_df, data['wh_prop'], on='acctnbr', how='left')
    # merged_df = pd.merge(merged_df, data['wh_prop2'], on='propnbr', how='left')
    merged_df = pd.merge(merged_df, data['wh_loans'], on='acctnbr', how='left')

    persnbr = data['persnbr']
    persnbr = persnbr[persnbr['acctrolecd'] == 'SELO']
    merged_df = pd.merge(merged_df, persnbr, on='acctnbr', how='left')

    # Making columns floats instead of objects for easier use in excel later
    float_cols = ['noteintrate', 'notebal', 'noteopenamt', 
                  'bookbalance', 'noteintcalcschednbr', 'intbase', 
                  'escbal', 'cobal', 'minratechangedown', 
                  'maxratechangedown', 'prepaycharge', 
                #   'aprsvalueamt', 
                #   'propvalue'
                  ]
    for col in float_cols:
        merged_df[col] = pd.to_numeric(merged_df[col])

    merged_df = merged_df[(merged_df['curracctstatcd'] != "CLS") & (merged_df['curracctstatcd'] != "CO")]
    merged_df = merged_df.rename(columns={'persname': 'secondary officer'})

    # filtering data for the three officers
    df1 = merged_df[(merged_df['acctofficer'] == 'NANCY P. CABRAL') | (merged_df['acctofficer'] == 'DAVID FERREIRA') | (merged_df['acctofficer'] == 'GEORGE J. MENDROS')]
    df2 = merged_df[(merged_df['secondary officer'] == 'NANCY P. CABRAL') | (merged_df['secondary officer'] == 'DAVID FERREIRA') | (merged_df['secondary officer'] == 'GEORGE J. MENDROS')]

    # creating deposit and loan summaries for each officer
    df1_summary = (
        df1.groupby('acctofficer')
        .agg({
            'bookbalance': 'sum',
            'acctnbr': pd.Series.nunique
        })
        .reset_index()
    )

    df2_summary = (
        df2.groupby('secondary officer')
        .agg({
            'bookbalance': 'sum',
            'acctnbr': pd.Series.nunique
        })
        .reset_index()
    )

    df1_summary.columns = ['Officer', 'Deposit Balance Total', 'Deposit Count']
    df2_summary.columns = ['Officer', 'Loan Balance Total', 'Loan Count']

    summary_df = pd.merge(df1_summary, df2_summary, on='Officer', how='left')


    deposit_cols_to_keep = ['acctnbr',      # columns we want to keep in final dataframe
    'mjaccttypcd',
    'ownername',
    'curracctstatcd',
    'bookbalance',
    'acctofficer',
    'noteintrate',
    'notenextratechangedate',
    'noteratechangecalpercd',
    'noteopenamt',
    'notebal',
    'noteintcalcschednbr',
    'calcbaltypcd',
    'intmethcd',
    'ratetypcd',
    'intbase',
    'datemat',
    'contractdate']
    
    deposits_nancy = df1[df1['acctofficer'] == 'NANCY P. CABRAL'].sort_values(by='bookbalance', ascending=False)
    deposits_david = df1[df1['acctofficer'] == 'DAVID FERREIRA'].sort_values(by='bookbalance', ascending=False)
    deposits_george = df1[df1['acctofficer'] == 'GEORGE J. MENDROS'].sort_values(by='bookbalance', ascending=False)

    deposits_nancy = deposits_nancy[deposit_cols_to_keep]
    deposits_david = deposits_david[deposit_cols_to_keep]
    deposits_george = deposits_george[deposit_cols_to_keep]


    loan_cols_to_keep = ['acctnbr',     # columns we want to keep in final dataframe
    'mjaccttypcd',
    'ownername',
    'curracctstatcd',
    'bookbalance',
    'noteintrate',
    'loanofficer',
    'secondary officer',
    'acctofficer',
    'notenextratechangedate',
    'noteratechangecalpercd',
    'noteopenamt',
    'notebal',
    'noteintcalcschednbr',
    'calcbaltypcd',
    'intmethcd',
    'ratetypcd',
    'intbase',
    'datemat',
    'contractdate',
    'escbal',
    'purpcd',
    'cobal',
    'fdiccatcd',
    'date1stpmtdue',
    'nextduedate',
    'minratechangedown',
    'maxratechangedown',
    'prepaycharge',
    'lastpaymentdate',
    # 'propnbr',
    # 'aprsvalueamt',
    # 'aprsdate',
    # 'propaddr1',
    # 'propaddr2',
    # 'propaddr3',
    # 'propcity',
    # 'propstate',
    # 'propzip',
    # 'proptypdesc',
    # 'propvalue',
    # 'proptypcd',
    # 'propdesc'
    ]

    loans_nancy = df2[df2['secondary officer'] == 'NANCY P. CABRAL'].sort_values(by='bookbalance', ascending=False)
    loans_david = df2[df2['secondary officer'] == 'DAVID FERREIRA'].sort_values(by='bookbalance', ascending=False)
    loans_george = df2[df2['secondary officer'] == 'GEORGE J. MENDROS'].sort_values(by='bookbalance', ascending=False)

    loans_nancy = loans_nancy[loan_cols_to_keep]
    loans_david = loans_david[loan_cols_to_keep]
    loans_george = loans_george[loan_cols_to_keep]

    # mapping dataframes to sheets in final product
    sheets = [
        ('Summary', summary_df),
        ('Deposits_Dave', deposits_david),
        ('Loans_Dave', loans_david),
        ('Deposits_George', deposits_george),
        ('Loans_George', loans_george),
        ('Deposits_Nancy', deposits_nancy),
        ('Loans_Nancy', loans_nancy)
    ]

    # grabbing date for filename
    today = datetime.today()
    date = f"{today.strftime('%B')} {today.day} {today.year}"

    filename = 'Portfolio_Report ' + date + '.xlsx'

    # will be used with email distribution so production flag doesn't matter
    output_file_path = OUTPUT_DIR / Path(filename)

    def currency_string_length(series):
        return series.map(lambda x: f"${x:,.2f}" if pd.notnull(x) else '').map(len).max()

    date_columns = ['notenextratechangedate', 'contractdate', 'datemat', 'date1stpmtdue', 'nextduedate', 'lastpaymentdate', 'aprsdate'] 
    monetary_columns = ['Deposit Balance Total', 'Loan Balance Total', 'bookbalance', 'noteopenamt', 'notebal', 'escbal', 'cobal', 'prepaycharge', 'propvalue']
    
    with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
        for sheet_name, df in sheets:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            worksheet = writer.sheets[sheet_name]
            workbook = writer.book

            # format for monetary columns
            currency_format = workbook.add_format({'num_format': '$#,##0.00'})
            # format for datetime columns
            datetime_format = workbook.add_format({'num_format': 'yyyy-mm-dd hh:mm:ss'})

            # Freeze the top row
            worksheet.freeze_panes(1, 0)

            # auto-fit each column
            for i, col in enumerate(df.columns):
                if col in monetary_columns:
                    max_len = max(currency_string_length(df[col]), len(col)) + 2
                    worksheet.set_column(i, i, max_len, currency_format)
                elif col in date_columns:
                    max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
                    worksheet.set_column(i, i, max(20, max_len), datetime_format)
                else:
                    max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
                    worksheet.set_column(i, i, max_len)

    # # Distribution
    # subject = f"SBRM Portfolio Report" 
    # body = "Hi, \n\nAttached is the Monthly SBRM Portfolio Report. If you have any questions, please reach out to BusinessIntelligence@bcsbmail.com \n\nThanks!"
    # attachment_paths = [output_file_path]
    # cdutils.distribution.email_out(EMAIL_TO, EMAIL_CC, subject, body, attachment_paths)

if __name__ == '__main__':
    print(f"Starting [{__version__}]")
    main()