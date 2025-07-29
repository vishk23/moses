import src.getAllData as getAllData
import src.pkey as pkey
import src.format_excel_file as format_excel_file
from src._version import __version__
from src.config import OUTPUT_DIR

import pandas as pd
from datetime import datetime
from pathlib import Path

def main() -> None:
    # getting all data we need
    persuserfield, portfoliokey = getAllData.fetch_data_persuserfield(), pkey.pkey()
    roles = getAllData.fetch_data_allroles()
    allroles, wh_pers = roles['WH_ALLROLES'].copy(), roles['WH_PERS'].copy()

    # filtering out employees
    wh_pers = wh_pers[['persnbr', 'employeeyn']]
    wh_pers = wh_pers[wh_pers['employeeyn'] == 'N']
    allroles = pd.merge(allroles, wh_pers, on='persnbr')

    # getting only persnbrs where they have a Y for either pttm or pttr or prtd
    persuserfield = persuserfield.iloc[:, :3]
    persuserfield = persuserfield.sort_values(by='persnbr', ascending=True)
    pivoted = persuserfield.pivot(index='persnbr', columns='userfieldcd', values='value')
    pivoted = pivoted.fillna('N')
    only_ppl_with_y = pivoted[(pivoted['PTTM'] == 'Y') | (pivoted['PTTR'] == 'Y') | (pivoted['PRTD'] == 'Y')]

    # removing rows with no persnbr and merging data, and employee rows
    # allroles = allroles[allroles['emplroleyn'] == 'N']
    df_cleaned = allroles.dropna(subset=['persnbr'])
    merged_df = pd.merge(only_ppl_with_y, df_cleaned, on='persnbr')
    merged_df = merged_df.sort_values(by='persnbr', ascending=True)

    # only keeping rows in pkey where account status is ACT or NPFD 
    portfoliokey['acctnbr'] = portfoliokey['acctnbr'].astype(int)
    portfoliokey = portfoliokey[(portfoliokey['curracctstatcd'] == 'ACT') | (portfoliokey['curracctstatcd'] == 'NPFM')]
    
    merged_df2 = pd.merge(merged_df, portfoliokey[['acctnbr', 'ownersortname', 'Net Balance', 'Total Exposure', 'Category']], on='acctnbr')

    # keeping only relevant data
    valid_roles = ['Tax Owner', 'NonTax Owner']
    bad_categories = ['CRE', 'C&I', 'HOA']
    merged_df2 = merged_df2[merged_df2['acctroledesc'].isin(valid_roles)]
    merged_df2 = merged_df2[~merged_df2['Category'].isin(bad_categories)]
    
    # for each persnbr there shouldn't be any duplicate account numbers associated with it
    df_unique = merged_df2.drop_duplicates(subset=['persnbr', 'acctnbr'], keep='first')

    # no category means its a deposit, category exists means its a loan
    deposits = df_unique[df_unique['Category'].isna()].groupby('persnbr')['Net Balance'].sum()
    loans = df_unique[df_unique['Category'].notna()].groupby('persnbr')['Total Exposure'].sum()

    summary = pd.concat([deposits, loans], axis=1).fillna(0)

    # grabbing other columns
    otherdata = df_unique.drop_duplicates('persnbr')[['persnbr', 'PTTM', 'PTTR', 'PRTD','ownersortname']].set_index('persnbr')
    final_df = summary.merge(otherdata, left_index=True, right_index=True).reset_index()
    
    final_df = final_df[['ownersortname', 'persnbr', 'PTTM', 'PTTR', 'PRTD','Net Balance', 'Total Exposure']]
    

    names = {
        'ownersortname': 'Customer Name',
        'persnbr': 'Customer Number',
        'PTTM': 'PTTM',
        'PTTR': 'PTTR',
        'PRTD': 'PRTD',
        'Net Balance': 'Deposit Total Owner Balance',
        'Total Exposure': 'Loans Total Owner Balance'
    }

    final_df = final_df.rename(columns=names)

    # grabbing date for filename
    today = datetime.today()
    date = f"{today.strftime('%B')} {today.day} {today.year}"
    
    output_file_path = OUTPUT_DIR / Path("Prime Time Travel Customers " + date + ".xlsx")

    final_df.to_excel(output_file_path, index=False)
    format_excel_file.format_excel_file(output_file_path)


if __name__ == '__main__':
    print(f"Starting [{__version__}]")
    main()
    print("Complete!")