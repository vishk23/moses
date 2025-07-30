""" 
Non Accrual Report

This is an item for the Resolution Committee Package. This increases
operational efficiency by automating a task done by the Loan Review team.

This report tracks all non-performing loans &amp; reconciles month over month
changes.
"""

from pathlib import Path

import pandas as pd # type: ignore
import numpy as np

import src.fetch_data # type: ignore
import src.fetch_subsequent_data # type: ignore
import src.export_and_format # type: ignore
import src.main_pipeline
import cdutils.loans.calculations # type: ignore
import src.get_total_past_due #type: ignore
# import cdutils.selo # type: ignore
from src._version import __version__
from src.config import BASE_PATH


def main():
    global pd

    # grabbing the 2 most recent effdates
    data = src.fetch_data.fetch_data()
    wh_acctcommon = data['wh_acctcommon']
    effdate1 = wh_acctcommon['effdate'].iloc[-1]
    effdate2 = wh_acctcommon['effdate'].iloc[-2]
    days_diff = (effdate1 - effdate2).days

    # grabbing other relevant data using the 2 effdates as filters
    data2 = src.fetch_subsequent_data.fetch_subsequent_data(effdate1, effdate2)
    curr_acctcommon, prior_acctcommon = data2['wh_acctcommon'], data2['wh_acctcommon2']
    curr_acctloan, prior_acctloan = data2['wh_acctloan'], data2['wh_acctloan2']

    # generating reports for most current month and previous month
    current_report, current_report_raw, df_for_other_pipeline = src.main_pipeline.main_pipeline(effdate1, curr_acctcommon, curr_acctloan)
    prior_month_report, x, y = src.main_pipeline.main_pipeline(effdate2, prior_acctcommon, prior_acctloan)

    # calculating sum of net balance and distinct accounts for previous month
    net_balance_sum = prior_month_report['Net Balance'].sum() / 2 # have to divide by 2 because the sum is including total rows
    count_distinct_accounts = prior_month_report['Account Number'].dropna().nunique()
    summary_df = pd.DataFrame({
        'Net Balance': [net_balance_sum],
        'Count': [count_distinct_accounts]
    })
    old_sum = summary_df

    # prep for calculating repo
    prior_month_right = pd.merge(current_report_raw, prior_month_report, on='Account Number', how='right', suffixes=(None, '_right'))
    df_for_other_pipeline = df_for_other_pipeline.rename(columns={
        'acctnbr': 'Account Number',
        })
    df_for_other_pipeline['Account Number'] = df_for_other_pipeline['Account Number'].astype(str)
    prior_month_right['Account Number'] = prior_month_right['Account Number'].astype(str)

    df3 = pd.merge(df_for_other_pipeline, prior_month_right, on='Account Number', how='inner')
    df3 = df3[df3['product'] == "Repossessed Collateral"]

    # Performing reconciliation (new_additions, removed, and repo collateral)
    # right side only
    new_additions = current_report[~current_report['Account Number'].isin(prior_month_report['Account Number'])] # Reconciliation section for new Non-Accrual loans
    new_additions = new_additions.drop(columns=['Current Balance', 'Charged Off'])
    new_additions.insert(6, 'Total Change', new_additions['Net Balance'])
    new_additions.insert(7, 'COUNT', 1)

    title_row = pd.DataFrame([{
            'Customer Name': 'ADDITIONS',
            'TagType': 'Title'
        }])
    new_additions = pd.concat([title_row, new_additions], ignore_index=True)
    new_additions = new_additions[["Product Name", "Account Number", "Customer Name", "Responsibility Officer", "Days Past Due", "Net Balance", "Total Change", "COUNT", "Risk", "Non Accrual", "Total Amount Due", "Next Payment Due Date", "TagType"]]
    # the rest
    left_only = prior_month_report[~prior_month_report['Account Number'].isin(current_report['Account Number'])]
    left_only = left_only.drop(columns=['Current Balance', 'Charged Off'])
    left_only.insert(6, 'Total Change', left_only['Net Balance'] * -1)
    left_only.insert(7, 'COUNT', -1)
    # closed
    removed = left_only[~left_only['Account Number'].isin(df3['Account Number'])] # Reconciliation section for removed from NPFM
    title_row = pd.DataFrame([{
            'Customer Name': 'REMOVED',
            'TagType': 'Title'
        }])
    removed = pd.concat([title_row, removed], ignore_index=True)
    removed = removed[["Product Name", "Account Number", "Customer Name", "Responsibility Officer", "Days Past Due", "Net Balance", "Total Change", "COUNT", "Risk", "Non Accrual", "Total Amount Due", "Next Payment Due Date", "TagType"]]
    # reposessed collateral

    totalpayments = src.get_total_past_due.isolate_total_past_due(data['totalpaymentsdue'])

    repo = left_only[left_only['Account Number'].isin(df3['Account Number'])].copy() # Previously on NonAccrual and now has Repo Collateral as property type
    repo['Account Number'] = repo['Account Number'].astype(str)
    totalpayments['Account Number'] = totalpayments['Account Number'].astype(str)
    repo = pd.merge(repo, totalpayments, on='Account Number', how='left')
    repo.drop('Total Amount Due', axis=1, inplace=True)
    repo = repo.rename(columns={
        'totaldue': 'Total Amount Due',
        })

    repo.loc[:, 'Product Name'] = 'Repossessed Collateral'
    title_row = pd.DataFrame([{
            'Customer Name': 'INTO OTHER REPO COLLATERAL',
            'TagType': 'Title'
        }])
    repo = pd.concat([title_row, repo], ignore_index=True)
    repo['Total Amount Due'] = repo['Total Amount Due'].astype(float)
    repo = repo[["Product Name", "Account Number", "Customer Name", "Responsibility Officer", "Days Past Due", "Net Balance", "Total Change", "COUNT", "Risk", "Non Accrual", "Total Amount Due", "Next Payment Due Date", "TagType"]]
    repo['Days Past Due'] = repo['Days Past Due'] + days_diff

    src.export_and_format.export_and_format(current_report, current_report_raw, new_additions, removed, repo, old_sum)

   
    # # grabbing date for filename
    # today = datetime.today()
    # date = f"{today.strftime('%B')} {today.day} {today.year}"
    # output_string = './output/Acct_Attorney_Consultant ' + date + '.xlsx'
    
    # # Output to excel (raw data)
    # OUTPUT_PATH = BASE_PATH / Path(output_string)

    # # mapping dataframes to sheets in final product
    # sheets = [
    #     ('Acct_Attorney_Consultant_Report', df_merged_merged)
    # ]

    # # date_columns = ['Date Opened', 'Next Rate Change Date', 'LOC Inactive Date', 'Maturity Date'] 
    # monetary_columns = ['Net Balance', 'Available Credit', 'Potential Outstanding']
    # # percent_columns = ['Interest Rate']
    
    # def currency_string_length(series):
    #     return series.map(lambda x: f"${x:,.2f}" if pd.notnull(x) else '').map(len).max()

    # with pd.ExcelWriter(OUTPUT_PATH, engine='xlsxwriter', datetime_format='mm/dd/yyyy') as writer:
    #     for sheet_name, df in sheets:
    #         df.to_excel(writer, sheet_name=sheet_name, index=False)
    #         worksheet = writer.sheets[sheet_name]
    #         workbook = writer.book

    #         currency_format = workbook.add_format({'num_format': '$#,##0.00'})
    #         # date_format = workbook.add_format({'num_format': 'mm/dd/yyyy'})
    #         # percent_format = workbook.add_format({'num_format': '0.00%'})
            
    #         # Freeze the top row
    #         worksheet.freeze_panes(1, 0)

    #         # auto-fit each column
    #         for i, col in enumerate(df.columns):
    #             if col in monetary_columns:
    #                 max_len = max(currency_string_length(df[col]), len(col)) + 2
    #                 worksheet.set_column(i, i, max_len, currency_format)
    #             # elif col in date_columns:
    #             #     max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
    #             #     worksheet.set_column(i, i, max(20, max_len), date_format)
    #             # elif col in percent_columns:
    #             #     worksheet.set_column(i, i, 17, percent_format)
    #             else:
    #                 max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
    #                 worksheet.set_column(i, i, max_len)


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