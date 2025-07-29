import pandas as pd

"""
Builds the final E Contract support from the
merged daily funding reports and book to look.
"""
def buildReport(merged_df):

    report = pd.DataFrame({
        'Dealer Name': merged_df['Dealer Name'], 
        'Customer Name': merged_df['Applicant Name'],
        'Funded Date': merged_df['Funding Date'],
        'Amt Financed': merged_df['Amount Financed'],
        '# of Apps Approved': merged_df['Application Approved'],
        '# of Apps Funded': None,
        '# of ECons Funded': merged_df['Contract Type'],
        '% of ECons Funded': None})
    
    report = report.sort_values(by='Dealer Name')
    report = report.reset_index(drop=True)


    # building dealer totals rows

    result_rows = []

    dealer_groups = {name: group for name, group in report.groupby('Dealer Name')}
    for dealer_name, group in dealer_groups.items():
        dealer = group['Dealer Name'].iloc[0]
        num_apps_funded = len(group)
        # removing lines where '# of ECons Funded' == 0
        group = group[group['# of ECons Funded'] != 0]
        result_rows.append(group)
        if not group.empty:
            result_rows.append(pd.DataFrame({
                'Dealer Name': f'{dealer} TOTAL', 
                'Customer Name': None,
                'Funded Date': None,
                'Amt Financed': group['Amt Financed'].sum(),
                '# of Apps Approved': group['# of Apps Approved'].iloc[0],
                '# of Apps Funded': num_apps_funded,
                '# of ECons Funded': f"{dealer} ECONS FUNDED: " + str(group['# of ECons Funded'].sum()),
                '% of ECons Funded': str(group['# of ECons Funded'].sum() / num_apps_funded * 100) + "%",
                'Temp-Row': [1]
            }))
    result_rows

    final_df = pd.concat(result_rows, ignore_index=True).drop('Temp-Row', axis=1)

    # buildling grand total row

    total_amt_financed = final_df[~final_df['Dealer Name'].str.contains('total', case=False, na=False)]['Amt Financed'].sum()
    total_apps_approved = final_df[final_df['Dealer Name'].str.contains('total', case=False, na=False)]['# of Apps Approved'].sum()
    total_apps_funded = final_df[final_df['Dealer Name'].str.contains('total', case=False, na=False)]['# of Apps Funded'].sum()
    total_econs_funded = final_df[~final_df['Dealer Name'].str.contains('total', case=False, na=False)]['# of ECons Funded'].sum()
    econs_to_apps_funded = str(f"{(total_econs_funded / total_apps_funded * 100):,.2f}") + "%"



    totals = ['Grand Total', None, None, total_amt_financed, total_apps_approved, total_apps_funded, total_econs_funded, econs_to_apps_funded]
    final_df.loc[len(final_df)], final_df.loc[len(final_df)+1] = None, totals
    
    # formatting
    final_df['Amt Financed'] = final_df['Amt Financed'].apply(lambda x: f"${x:,.2f}" if pd.notnull(x) else None)

    return final_df