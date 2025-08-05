
"""
I-CRE Production & Balance Growth Loader Files
"""

from pathlib import Path
from typing import Dict

import pandas as pd # type: ignore

import src.cdutils.database
import src.cdutils.caching
import src.transformations.joining
import src.transformations.calculations # type: ignore

def core_pipeline(data: Dict, start_date: str) -> pd.DataFrame:
    """
    Core Pipeline for ETL for I-CRE production Graph
    """
    
    # # Unpack data into dataframes
    wh_acctcommon = data['wh_acctcommon'].copy()
    wh_loans = data['wh_loans'].copy()
    wh_acctloan = data['wh_acctloan'].copy()
    wh_acct = data['wh_acct'].copy()
    wh_prop = data['wh_prop'].copy()
    wh_prop2 = data['wh_prop2'].copy()

    # Transforming the data
    main_loan_data = src.transformations.joining.join_loan_tables(wh_acctcommon, wh_acctloan, wh_loans, wh_acct)
    property_data = src.transformations.joining.join_prop_tables(wh_prop, wh_prop2)

    # # Calculated fields & data cleaning
    main_loan_data = src.transformations.calculations.append_total_exposure_field(main_loan_data)
    main_loan_data = src.transformations.calculations.cleaning_loan_data(main_loan_data)

    # Consolidate loan data & property data
    single_prop_data = src.transformations.joining.consolidation_with_one_prop(main_loan_data, property_data)
    # multiple_prop_data = src.transformations.joining.consolidation_with_multiple_props(main_loan_data, property_data)

    # Sort data
    single_prop_data = single_prop_data.sort_values(by=['Total Exposure','acctnbr'], ascending=[False, True])
    # multiple_prop_data = multiple_prop_data.sort_values(by=['Total Exposure','acctnbr'], ascending=[False, True])

    # Sort to I-CRE
    single_prop_data = single_prop_data[single_prop_data['fdiccatcd'].isin(['REMU','RENO'])].copy()

    # Filter to only this year
    start_date = pd.to_datetime(start_date)
    orig_this_year = single_prop_data[single_prop_data['origdate'] >= start_date].copy()
    return single_prop_data, orig_this_year

def sum_production(df: pd.DataFrame) -> float:
    sum_production_amt = df['noteopenamt'].sum()
    return sum_production_amt

def main():
    data_2024 = src.cdutils.database.fetch_data() 
    data_2023 = src.cdutils.database.fetch_data_2023() 
    data_2022 = src.cdutils.database.fetch_data_2022() 

    data_2024, orig_2024 = core_pipeline(data_2024, '2024-01-01 00:00:00')
    data_2023, orig_2023 = core_pipeline(data_2023, '2023-01-01 00:00:00')
    data_2022, orig_2022 = core_pipeline(data_2022, '2022-01-01 00:00:00')

    datasets = [orig_2024, orig_2023, orig_2022]    
    years = [2024, 2023, 2022]

    production_results = []
    for year, df in zip(years, datasets):
        total = df['noteopenamt'].sum()
        production_results.append({'Year': year, 'Production Total': total})

    production_summary = pd.DataFrame(production_results)

    OUTPUT_PATH = Path('./output/icre_production.xlsx')
    production_summary.to_excel(OUTPUT_PATH, index=False)

    datasets = [data_2024, data_2023, data_2022]    
    years = [2024, 2023, 2022]

    balance_results = []
    for year, df in zip(years, datasets):
        total = df['Net Balance'].sum()
        balance_results.append({'Year': year, 'Balance Total': total})

    balance_summary = pd.DataFrame(balance_results)

    OUTPUT_PATH = Path('./output/icre_balances.xlsx')
    balance_summary.to_excel(OUTPUT_PATH, index=False)
 


if __name__ == '__main__':
    main()