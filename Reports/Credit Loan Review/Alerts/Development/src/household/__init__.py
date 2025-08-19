"""
Module for the household number (total exposure and appending)
"""
import pandas as pd # type: ignore

def household_total_exposure(df):
    """
    Household Total Exposure:
    Grouping on household key, the total exposure is summed
    
    Args:
        df: loan_data
    
    Returns:
        household_grouping_df: A new dataframe with 2 columns:
            - Householdnbr
            - Total Exposure ($)
    
    Operations:
        - Group By: Householdnbr
        - Sum: Total Exposure
    
    """
    household_grouping_df = df.groupby('householdnbr')['Total Exposure'].sum().reset_index()
    household_grouping_df = pd.DataFrame(household_grouping_df)
    return household_grouping_df


def append_household_exposure(df, household_grouping_df):
    """
    Append household exposure back to loan_data
    
    Args:
        df: loan_data
        household_grouping_df: df with household number & total exposure
        
    Returns:
        df: loan data after appending household exposure
        
    Operations:
        - Left merge of df & household_grouping_df on 'householdnbr'
        
    """
    df = pd.merge(df, household_grouping_df, on='householdnbr', how='left', suffixes=('_df','_hhgroup'))
    return df