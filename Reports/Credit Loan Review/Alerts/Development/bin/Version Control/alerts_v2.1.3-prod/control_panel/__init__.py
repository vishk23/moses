"""
Control Panel Module. Here we can adjust the parameters for the system.

Usage:
```
import src.control_panel
```
"""
import pandas as pd # type: ignore
import numpy as np # type: ignore

import src.flags.credit_score

def criteria_flags(
        loan_data: pd.DataFrame,
        credit_score_data: pd.DataFrame,
        score_floor: int,
        score_decrease: float,
        ttm_pd_amt: int = 3,
        ttm_pd30_amt: int = 1,
        ttm_overdrafts: int = 5,
        deposit_change_pct: float = -.3,
        min_deposits: float = 250000,
        utilization_limit: float = .6,
        ) -> pd.DataFrame:
    """
    Criteria flags are assigned on to each line item for
    identification of fails.
    
    Args:
        loan_data
        
        # Parameters
        ttm_pd_amt = 3
        ttm_pd30_amt = 1
        ttm_overdrafts = 5
        deposit_change_pct = -.3
        min_deposits = 250000
        utilization_limit = .6
        
    Returns:
        df: loan_data with new identifier flag columns
            ['past_due_flag']
            ['ttm_overdrafts_flag']
            ['deposit_change_flag']
            ['ttm_utilization_flag']
            - 'cleanup_provision' already exists as a boolean column
    
    Operations:
        - parameters are set
        - if ttm_pd > parameter or ttm_pd30 >= parameter, then past_due_flag = 1, else 0
        - if ttm_overdrafts >= parameter, then ttm_overdrafts_flag = 1, else 0
        - if deposit_change_pct >= parameter, then deposit_change_flag = 1, else 0
        - if ttm_line_utilization >= parameter, then ttm_utilization_flag = 1, else 0
        - flag created for passing all tests (1: passed all, 0: failed at least 1)
    """
    
    credit_score_data = src.flags.credit_score.credit_score_flag_creation(credit_score_data, score_floor, score_decrease)
    assert credit_score_data['acctnbr'].is_unique, "Duplicates exist"

    loan_data = pd.merge(loan_data, credit_score_data, on='acctnbr', how='left')
    loan_data['score_flag'] = loan_data['score_flag'].fillna(0)
    # loan_data['TTM Days Overdrawn'] = loan_data['TTM Days Overdrawn'].fillna(0)
        
    # Flag Column Creation
    loan_data['past_due_flag'] = np.where((loan_data['ttm_pd'] >= ttm_pd_amt) | (loan_data['ttm_pd30'] >= ttm_pd30_amt), 1, 0) 
    loan_data['ttm_overdrafts_flag'] = np.where((loan_data['TTM Days Overdrawn'] >= ttm_overdrafts), 1, 0)
    loan_data['deposit_change_flag'] = np.where((loan_data['Deposit Change Pct'] <= deposit_change_pct) & (loan_data['TTM_AvgBal'] >= min_deposits), 1, 0)
    loan_data['ttm_utilization_flag'] = np.where((loan_data['ttm line utilization'] >= utilization_limit), 1, 0)
    loan_data['passed_all_flag'] = np.where((loan_data['past_due_flag'] == 0) & (loan_data['ttm_overdrafts_flag'] == 0) & (loan_data['deposit_change_flag'] == 0) & (loan_data['ttm_utilization_flag'] == 0) & (loan_data['cleanup_provision'] == 0) & (loan_data['score_flag'] == 0), 1, 0)
    
    return loan_data

