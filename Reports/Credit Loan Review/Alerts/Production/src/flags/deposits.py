"""
Deposit Testing Module (for Pass/Fail flag)

Usage:
    src.flags.deposits
"""
import pandas as pd # type: ignore
from pathlib import Path

import src.deposit_file

def deposit_criteria_testing() -> pd.DataFrame:
    """
    Consolidates deposits by household and calculates deposit change (%) over trailing 12 months
    
    Args:
        househldacct (pd.DataFrame): Cleaned version of househldacct table from R1625
    Returns:
        grouped_df: deposit dataframe with deposit change over time and count of overdrafts for each household
        
    Operations:
        - Access daily deposit update from Excel file on DA-1 drive
        - Fill null values with 0 for columns:
            - NOTEBAL
            - Year Ago Balance
            - TTM Overdrafts
        - Group by household number and sum NOTEBAL, Year Ago Balance, and TTM Overdrafts
        - Deposit Change Pct = (NOTEBAL/Year Ago Balance) - 1
        - Renamed HOUSEHOLDNBR field to match loan_data householdnbr field
    """
    DAILY_DEPOSIT_STAGING_DATA = Path(r"\\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Data_Analytics\Daily_Deposit_Update\Production\output\DailyDeposit_staging.xlsx")
    deposit_data = pd.read_excel(DAILY_DEPOSIT_STAGING_DATA, sheet_name='Sheet1')
    
    deposit_data = deposit_data.rename(columns={
        'TTM_DAYS_OVERDRAWN':'TTM Days Overdrawn',
        'TTM_NSF_COUNT':'TTM NSF'
    }).copy()

    grouped_df = deposit_data.groupby('householdnbr').agg({
        '3Mo_AvgBal':'sum',
        'TTM_AvgBal':'sum',
        'TTM Days Overdrawn':'sum',
        'TTM NSF':'sum'
    }).reset_index()
    
    grouped_df['Deposit Change Pct'] = (grouped_df['3Mo_AvgBal'].astype(float)/grouped_df['TTM_AvgBal'].astype(float)) - 1
    grouped_df['Deposit Change Pct'] = grouped_df['Deposit Change Pct'].fillna(0)
    
    return grouped_df 


#################################
def append_deposit_data(loan_data, deposit_data):
    """
    Append deposit criteria to the loan data
    
    Args:
        loan_data: loan data
        deposit_data: deposit data aggregated to household
        
    Returns:
        merged_df: loan_data with deposit data appended
        
    Operations:
        - left merge with loan_data & deposit data on householdnbr
    
    """
    merged_df = pd.merge(loan_data, deposit_data, on='householdnbr', how='left')
    return merged_df

