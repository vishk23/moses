""" 
Alerts: Main entry point
Developed by CD
[v2.1.1-prod] 2025-02-08


Usage:
    python -m src.main
"""

from io import StringIO
import time
import os
from datetime import datetime, timedelta, date
from typing import List
from collections import defaultdict, Counter

from io import StringIO
from pathlib import Path
import asyncio
import sys

import pandas as pd # type: ignore
import numpy as np # type: ignore

import src.cdutils.caching
import src.cdutils.database
import src.control_panel
import src.flags
import src.flags.deposits
import src.transformation.joining
import src.transformation.total_exposure
import src.transformation.cleaning
import src.transformation.filtering
import src.household
import src.personal_guarantor
import src.flags.past_due
import src.flags.line_utilization


def main():

    # Database Connection Configuration
    data = src.cdutils.database.fetch_data()

    # Unpack
    acctcommon = data['acctcommon'].copy()
    acctloan = data['acctloan'].copy()
    loans = data['loans'].copy()
    househldacct = data['househldacct'].copy()
    acctstatistichist = data['acctstatistichist'].copy()
    acctloanlimithist = data['acctloanlimithist'].copy()

    # # Data for Xactus
    # allroles = data['allroles'].copy()
    # persaddruse = data['persaddruse'].copy()
    # wh_addr = data['wh_addr'].copy()
    # pers = data['pers'].copy()

    # Caching
    # src.cdutils.caching.cache_data(Path(r'Z:\Chad Projects\Alerts\Production\assets\caching'), data)
    
    # Unpack cached data
    # acctcommon = pd.read_csv(Path(r'Z:\Chad Projects\Alerts\Production\assets\caching\acctcommon.csv'))
    # acctloan = pd.read_csv(Path(r'Z:\Chad Projects\Alerts\Production\assets\caching\acctloan.csv'))
    # loans = pd.read_csv(Path(r'Z:\Chad Projects\Alerts\Production\assets\caching\loans.csv'))
    # househldacct = pd.read_csv(Path(r'Z:\Chad Projects\Alerts\Production\assets\caching\househldacct.csv'))
    # acctstatistichist = pd.read_csv(Path(r'Z:\Chad Projects\Alerts\Production\assets\caching\acctstatistichist.csv'))
    # acctloanlimithist = pd.read_csv(Path(r'Z:\Chad Projects\Alerts\Production\assets\caching\acctloanlimithist.csv'))
   
    
    # Core ETL
    loan_data = src.transformation.joining.filter_and_merge_loan_tables(acctcommon, acctloan, loans)
    loan_data = src.transformation.total_exposure.append_total_exposure_field(loan_data)
    househldacct = src.transformation.cleaning.drop_hh_duplicates(househldacct)
    loan_data = src.transformation.joining.append_household_number(loan_data, househldacct)
    household_grouping_df = src.household.household_total_exposure(loan_data)
    loan_data = src.household.append_household_exposure(loan_data, household_grouping_df)
    loan_data = src.transformation.filtering.filter_to_target_products(loan_data)
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
    
    # Control Panel for Parameters
    loan_data = src.control_panel.criteria_flags(
        loan_data,
        ttm_pd_amt = 3,
        ttm_pd30_amt = 1,
        ttm_overdrafts = 5,
        deposit_change_pct = -.3,
        min_deposits = 250000,
        utilization_limit = .7
    )

    # Consolidation of the columns necessary
    final_df = loan_data[['acctnbr','effdate','ownername','product','loanofficer','inactivedate','Net Balance','Net Available','Net Collateral Reserve','cobal','creditlimitamt','Total Exposure_hhgroup','ttm_pd','ttm_pd30','TTM Overdrafts','NOTEBAL','Year Ago Balance','Deposit Change Pct','ttm line utilization','cleanup_provision','riskratingcd','past_due_flag','ttm_overdrafts_flag','deposit_change_flag','ttm_utilization_flag','passed_all_flag']]

    # Writing output
    file_path = r'\\10.161.85.66\Home\Share\Data & Analytics Initiatives\Project Management\Chad Projects\Alerts\Production\Output\alerts.xlsx'
    final_df.to_excel(file_path, index=False, engine='openpyxl')
        
    print('Execution Complete!')
    
if __name__ == "__main__":
    main()

    




