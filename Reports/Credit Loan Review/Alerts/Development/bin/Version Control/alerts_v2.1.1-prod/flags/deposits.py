"""
Deposit Testing Module (for Pass/Fail flag)

Usage:
    src.flags.deposits
"""
import pandas as pd # type: ignore

def deposit_criteria_testing():
    """
    Consolidates deposits by household and calculates deposit change (%) over trailing 12 months
        
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
    deposit_file_path = r'\\10.161.85.66\Home\Share\Line of Business_Shared Services\Commercial Credit\Deposits\DailyDeposit\DailyDeposit.xlsx'
    deposit_data = pd.read_excel(deposit_file_path, engine='openpyxl')
    
    deposit_data['NOTEBAL'].fillna(0)
    deposit_data['Year Ago Balance'].fillna(0)
    deposit_data['TTM Overdrafts'].fillna(0)

    grouped_df = deposit_data.groupby('HOUSEHOLDNBR').agg({
        'NOTEBAL':'sum',
        'Year Ago Balance':'sum',
        'TTM Overdrafts':'sum'
    }).reset_index()
    
    grouped_df['Deposit Change Pct'] = (grouped_df['NOTEBAL']/grouped_df['Year Ago Balance']) - 1
    grouped_df = grouped_df.rename(columns={'HOUSEHOLDNBR':'householdnbr'})
    
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

