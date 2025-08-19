"""
Past due criteria testing (for pass/fail flag)

Usage:
    import src.flags.past_due    
"""
import pandas as pd # type: ignore

def count_pd(df):
    """
    This will count past due (15+) flags on the account
    
    Args:
        df: ACCTSTATISTICHIST table (COCC)
        
    Returns:
        merged_df: A dataframe with 3 columns:
            - acctnbr
            - ytd_pd (count)
            - ttm_pd (count)
    
    Operations:
        - ytd_df created where event_date >= year_start date
        - ttm_df created where event_date >= year_ago date
        - statistictypcd (statistic type code) = 'PD'
        - Group by acctnbr, sum statistic count
        - rename columns to ytd_pd & ttm_pd
        - Outer merge ytd_df & ttm_df on acctnbr
        - fill null values with 0
    """
    ytd_df = df[df['event_date'] >= df['year_start']]
    ttm_df = df[df['event_date'] >= df['year_ago_date']]
    
    ytd_df = ytd_df[ytd_df['statistictypcd'].isin(['PD'])]
    ttm_df = ttm_df[ttm_df['statistictypcd'].isin(['PD'])]
    
    # Unit Tests
    assert (ytd_df['event_date'] >= ytd_df['year_start']).all(), "Filtering did not apply correctly"
    assert (ttm_df['event_date'] >= ttm_df['year_ago_date']).all(), "Filtering did not apply correctly"
    
    ytd_df = ytd_df.groupby('acctnbr')['statisticcount'].sum().reset_index()
    ttm_df = ttm_df.groupby('acctnbr')['statisticcount'].sum().reset_index()
    
    ytd_df = ytd_df.rename(columns={'statisticcount':'ytd_pd'})
    ttm_df = ttm_df.rename(columns={'statisticcount':'ttm_pd'})
    
    merged_df = pd.merge(ytd_df, ttm_df, on='acctnbr', how='outer')
    merged_df['ytd_pd'] = merged_df['ytd_pd'].fillna(0)
    merged_df['ttm_pd'] = merged_df['ttm_pd'].fillna(0)
    
    # Unit Tests
    assert merged_df['ytd_pd'].isnull().sum() == 0, "There are null values"
    assert merged_df['ttm_pd'].isnull().sum() == 0, "There are null values"

    
    return merged_df


#################################
def count_pd30(df):
    """
    This will count past due (30+) flags on the account
    
    Args:
        df: ACCTSTATISTICHIST table (COCC)
        
    Returns:
        merged_df: A dataframe with 3 columns:
            - acctnbr
            - ytd_pd30 (count)
            - ttm_pd30 (count)
    
    Operations:
        - ytd_df created where event_date >= year_start date
        - ttm_df created where event_date >= year_ago date
        - statistictypcd (statistic type code) = 'PD30'
        - Group by acctnbr, sum statistic count
        - rename columns to ytd_pd30 & ttm_pd30
        - Outer merge ytd_df & ttm_df on acctnbr
        - fill null values with 0
    """
    ytd_df = df[df['event_date'] >= df['year_start']]
    ttm_df = df[df['event_date'] >= df['year_ago_date']]
    
    ytd_df = ytd_df[ytd_df['statistictypcd'].isin(['PD30'])]
    ttm_df = ttm_df[ttm_df['statistictypcd'].isin(['PD30'])]
    
    # Unit Tests
    assert (ytd_df['event_date'] >= ytd_df['year_start']).all(), "Filtering did not apply correctly"
    assert (ttm_df['event_date'] >= ttm_df['year_ago_date']).all(), "Filtering did not apply correctly"
    
    ytd_df = ytd_df.groupby('acctnbr')['statisticcount'].sum().reset_index()
    ttm_df = ttm_df.groupby('acctnbr')['statisticcount'].sum().reset_index()
    
    ytd_df = ytd_df.rename(columns={'statisticcount':'ytd_pd30'})
    ttm_df = ttm_df.rename(columns={'statisticcount':'ttm_pd30'})
    
    merged_df = pd.merge(ytd_df, ttm_df, on='acctnbr', how='outer')
    merged_df['ytd_pd30'] = merged_df['ytd_pd30'].fillna(0)
    merged_df['ttm_pd30'] = merged_df['ttm_pd30'].fillna(0)
    
    # Unit Tests
    assert merged_df['ytd_pd30'].isnull().sum() == 0, "There are null values"
    assert merged_df['ttm_pd30'].isnull().sum() == 0, "There are null values"

    
    return merged_df


#################################
def append_pd_info(loan_data, pd_df, pd30_df):
    """
    Appending past due and past due 30 counts to loan data
    
    Args:
        loan_data: filtered down loan_data
        pd_df: past due 15 days data
        pd30_df: past due 30 days data
        
    Returns:
        df: loan_data, with appended past due and past due 30 counts
    
    Operations:
    """
    df = pd.merge(loan_data, pd_df, on='acctnbr', how='left')
    df = pd.merge(df, pd30_df, on='acctnbr', how='left')
    
    df['ytd_pd'] = df['ytd_pd'].fillna(0)
    df['ttm_pd'] = df['ttm_pd'].fillna(0)
    df['ytd_pd30'] = df['ytd_pd30'].fillna(0)
    df['ttm_pd30'] = df['ttm_pd30'].fillna(0)
    
    assert df['ytd_pd'].isnull().sum() == 0, "There are null values"
    assert df['ttm_pd'].isnull().sum() == 0, "There are null values"
    assert df['ytd_pd30'].isnull().sum() == 0, "There are null values"
    assert df['ttm_pd30'].isnull().sum() == 0, "There are null values"
    
    return df

