""" 
Alerts: Main entry point
Developed by CD


Usage:
    python -m src.main
"""

from pathlib import Path

import pandas as pd # type: ignore
import numpy as np # type: ignore

import cdutils.input_cleansing # type: ignore
import src.fetch_data
import src.control_panel
import src.flags
import src.flags.credit_score
import src.flags.deposits
import cdutils.joining # type: ignore
import cdutils.loans.calculations # type: ignore
import src.transformation.cleaning
import src.transformation.filtering
import src.household
import src.personal_guarantor
import src.flags.past_due
import src.flags.line_utilization
from src._version import __version__
import src.transformation.joining
import src.transformation.total_exposure


def main(production_flag: bool=False):
    if production_flag:
        BASE_PATH = Path(r'\\00-DA1\Home\Share\Line of Business_Shared Services\Credit_Loan_Review\Alerts\Production')
        assert "prod" in __version__, (f"Cannot run in production mode without 'prod' in the __version__")
    else:
        BASE_PATH = Path('.')

    # Database Connection Configuration
    data = src.fetch_data.fetch_data()

    # Unpack
    acctcommon = data['acctcommon'].copy()
    acctloan = data['acctloan'].copy()
    loans = data['loans'].copy()
    househldacct = data['househldacct'].copy()
    acctstatistichist = data['acctstatistichist'].copy()
    acctloanlimithist = data['acctloanlimithist'].copy()
    allroles = data['allroles'].copy()
    pers = data['pers'].copy()
    viewperstaxid = data['viewperstaxid'].copy()

    # # Data for Xactus
    # allroles = data['allroles'].copy()
    # persaddruse = data['persaddruse'].copy()
    # wh_addr = data['wh_addr'].copy()
    # pers = data['pers'].copy()

    # Caching
    # src.cdutils.caching.cache_data(Path(r'C:\Users\w322800\Documents\alerts_caching'), data)
    
    # # Unpack cached data
    # acctcommon = pd.read_csv(Path(r'C:\Users\w322800\Documents\alerts_caching\acctcommon.csv'))
    # acctloan = pd.read_csv(Path(r'C:\Users\w322800\Documents\alerts_caching\acctloan.csv'))
    # loans = pd.read_csv(Path(r'C:\Users\w322800\Documents\alerts_caching\loans.csv'))
    # househldacct = pd.read_csv(Path(r'C:\Users\w322800\Documents\alerts_caching\househldacct.csv'))
    # acctstatistichist = pd.read_csv(Path(r'C:\Users\w322800\Documents\alerts_caching\acctstatistichist.csv'))
    # acctloanlimithist = pd.read_csv(Path(r'C:\Users\w322800\Documents\alerts_caching\acctloanlimithist.csv'))
    # allroles = pd.read_csv(Path(r'C:\Users\w322800\Documents\alerts_caching\allroles.csv'))
    # pers = pd.read_csv(Path(r'C:\Users\w322800\Documents\alerts_caching\pers.csv'))
    # viewperstaxid = pd.read_csv(Path(r'C:\Users\w322800\Documents\alerts_caching\viewperstaxid.csv'))

    # Input cleaning
    viewperstaxid_schema = {
    'persnbr': int,
    'taxid': float
    }

    viewperstaxid = cdutils.input_cleansing.enforce_schema(viewperstaxid, viewperstaxid_schema)
    
    # # Core ETL
    loan_data = src.transformation.joining.filter_and_merge_loan_tables(acctcommon, acctloan, loans)
    loan_data = src.transformation.total_exposure.append_total_exposure_field(loan_data)
    househldacct = src.transformation.cleaning.drop_hh_duplicates(househldacct)
    loan_data = src.transformation.joining.append_household_number(loan_data, househldacct)
    household_grouping_df = src.household.household_total_exposure(loan_data)
    loan_data = src.household.append_household_exposure(loan_data, household_grouping_df)

    # Main parameters for loans
    loan_data = src.transformation.filtering.filter_to_target_products(
        loan_data,
        creditlimitamt=500000,
        total_exposure=1000000
    ) # Note that minor list is hard-coded to line of credit minors in the filtering module
    
    # Additional ETL
    acctstatistic_output = src.transformation.cleaning.acctstatistichist_cleaning(acctstatistichist, acctcommon)
    pd_df = src.flags.past_due.count_pd(acctstatistic_output)
    pd30_df = src.flags.past_due.count_pd30(acctstatistic_output)
    loan_data = src.flags.past_due.append_pd_info(loan_data, pd_df, pd30_df)
    deposit_data = src.flags.deposits.deposit_criteria_testing()
    loan_data = src.flags.deposits.append_deposit_data(loan_data, deposit_data)
    utilization_data, cleanup_data = src.flags.line_utilization.line_utilization_fetch(loan_data)
    loan_data = src.flags.line_utilization.append_line_utilization_data(loan_data, utilization_data, cleanup_data)
    inactive_date_df = src.transformation.joining.get_inactive_date(acctloanlimithist)
    loan_data = src.transformation.joining.append_inactive_date(loan_data, inactive_date_df)
    pers_data = src.personal_guarantor.append_tax_id_to_pers(pers, viewperstaxid)
    pers_data = src.personal_guarantor.append_credit_score(pers_data)
    credit_score_data = src.personal_guarantor.allroles_with_credit_score(allroles, pers_data)

    # Control panel for additional parameters
    loan_data = src.control_panel.criteria_flags(
        loan_data,
        credit_score_data,
        score_floor = 680, # Minimum Credit Score for any guarantor related to the loan
        score_decrease = -0.1, # Decrease of credit score since prior period
        ttm_pd_amt = 3, # Times in trailing 12 Months Past Due (15-29)
        ttm_pd30_amt = 1, # Times in trailing 12 Months Past Due (30+)
        ttm_overdrafts = 5, # Number of days with an overdrawn balance in trailing 12 Months
        deposit_change_pct = -.3, # Aggregate deposits in relationship decrease (-30% loss)
        min_deposits = 50000, # Minimum deposits to be eligible to flag deposit decrease
        utilization_limit = .7 # Line Utilization flag for trailing 12 months
    )

    # Consolidation of the columns necessary
    final_df = loan_data[['acctnbr','effdate','ownername','product','loanofficer','inactivedate','Net Balance','Net Available','Net Collateral Reserve','cobal','creditlimitamt','Total Exposure_hhgroup','ttm_pd','ttm_pd30','TTM Days Overdrawn','3Mo_AvgBal','TTM_AvgBal','Deposit Change Pct','ttm line utilization','cleanup_provision','riskratingcd','past_due_flag','ttm_overdrafts_flag','deposit_change_flag','ttm_utilization_flag','score_flag','passed_all_flag']]

    # Writing output
    ALERTS_PATH = BASE_PATH / Path('./Output/alerts.xlsx')
    final_df.to_excel(ALERTS_PATH, index=False, engine='openpyxl', sheet_name='Sheet1')

    CREDSCORE_PATH = BASE_PATH / Path('./Output/credit_score_detail.xlsx')
    credit_score_data.to_excel(CREDSCORE_PATH, index=False, engine='openpyxl', sheet_name='Sheet1')
        
    print('Execution Complete!')
    
if __name__ == "__main__":
    print(f"Starting alerts [{__version__}]")
    # main(production_flag=True)
    main()
    print("Complete!")

    




