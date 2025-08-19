"""
Weighted Average Rate & Unadvanced Funds
"""
import cdutils.dealer_split # type: ignore

import pandas as pd # type: ignore
import numpy as np # type: ignore


def weighted_avg_rate(df: pd.DataFrame, title: str='Weighted Avg Rate', weight_col: str = 'Net Balance', value_col: str = 'modified_noteintrate') -> pd.DataFrame:
    """
    Create weighted average rate
    """
    df = df.copy()
    df['WeightedRate'] = df[weight_col] * df[value_col]
    grouped_df = df.groupby('Category').apply(
        lambda x: x['WeightedRate'].sum() / x[weight_col].sum(), include_groups=False
    ).reset_index(name=title).copy()
    return grouped_df

def yield_and_unadvanced_creation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes the full data current (from the main pipeline) and creates a total loan yield, new loan yield, and unadvanced funds for every category

    Args:
        df (pd.Dataframe): This is the full_data_current from the current output of the pipeline function

    Returns:
        df (pd.DataFrame): Simple table that will be added to the right most columns of the balance tracker in a separate excel update function
    """
    # Manual Rate Adjustments for Heat Loans (CNS) WSJ + 100 bp
    df = df.copy()
    
    # Adjustment for the Consumer loans: WSJ Prime + 1
    df['modified_noteintrate'] = np.where(
        (df['currmiaccttypcd'] == 'IL33') & (df['contractdate'] >= pd.Timestamp(2025,1,1)), .07,
        np.where((df['currmiaccttypcd'].isin(['IL21','IL31','IL33'])) & (df['contractdate'] >= pd.Timestamp(2024,12,19)), .085,
        np.where((df['currmiaccttypcd'].isin(['IL21','IL31','IL33'])) & (df['contractdate'] >= pd.Timestamp(2024,12,19)), .085,
        np.where((df['currmiaccttypcd'].isin(['IL21','IL31','IL33'])) & (df['contractdate'] >= pd.Timestamp(2024,11,8)), .0875,
        np.where((df['currmiaccttypcd'].isin(['IL21','IL31','IL33'])) & (df['contractdate'] >= pd.Timestamp(2024,9,19)), .09,
        np.where((df['currmiaccttypcd'].isin(['IL21','IL31','IL33'])) & (df['contractdate'] >= pd.Timestamp(2023,7,27)), .095,
        np.where((df['currmiaccttypcd'].isin(['IL21','IL31','IL33'])) & (df['contractdate'] >= pd.Timestamp(2023,5,4)), .0925,
        np.where((df['currmiaccttypcd'].isin(['IL21','IL31','IL33'])) & (df['contractdate'] >= pd.Timestamp(2023,3,23)), .09,
        np.where((df['currmiaccttypcd'].isin(['IL21','IL31','IL33'])) & (df['contractdate'] >= pd.Timestamp(2023,2,2)), .0875,
        np.where((df['currmiaccttypcd'].isin(['IL21','IL31','IL33'])) & (df['contractdate'] >= pd.Timestamp(2022,12,16)), .085,
        np.where((df['currmiaccttypcd'].isin(['IL21','IL31','IL33'])) & (df['contractdate'] >= pd.Timestamp(2022,11,3)), .08,
        np.where((df['currmiaccttypcd'].isin(['IL21','IL31','IL33'])) & (df['contractdate'] >= pd.Timestamp(2022,9,22)), .0725,
        np.where((df['currmiaccttypcd'].isin(['IL21','IL31','IL33'])) & (df['contractdate'] >= pd.Timestamp(2022,7,28)), .065,
        np.where((df['currmiaccttypcd'].isin(['IL21','IL31','IL33'])) & (df['contractdate'] >= pd.Timestamp(2022,6,16)), .0575,
        np.where((df['currmiaccttypcd'].isin(['IL21','IL31','IL33'])), .05,
        df['noteintrate']))))))))))))))
    )

    # Attach dealer split rate and subtract this from noteint rate
    df = cdutils.dealer_split.append_dealersplit(df)
    df['modified_noteintrate'] = np.where(df['Category'] == 'Indirect', df['modified_noteintrate'] - df['SPLT'], df['modified_noteintrate'])



    # Create total yield
    total_yield = weighted_avg_rate(df, title='Total Loan Yield')

    # Create new loan yield
    datetime_cols = ['effdate','origdate']
    for col in datetime_cols:
        df[col] = pd.to_datetime(df[col])

    new_loan_df = df[
        (df['origdate'].dt.month == df['effdate'].dt.month) & (df['origdate'].dt.year == df['effdate'].dt.year)
    ].copy()

    # # Attach transaction amt

    # # Create advances column
    # resi_minor_
    # new_loan_df['Advances'] = np.where(
    #     ()
    # )

    new_yield = weighted_avg_rate(new_loan_df, title='New Loan Yield')

    df['Unadvanced'] = (df['availbalamt']) / 1000

    # Unadvanced
    unadvanced = df.groupby('Category')['Unadvanced'].sum().reset_index()
    unadvanced = unadvanced.rename(columns={'Unadvanced':'Unadvanced Funds'})

    # Merge
    merged_df = pd.merge(new_yield, total_yield, how='inner', on='Category')
    merged_df = pd.merge(merged_df, unadvanced, how='inner', on='Category')

    return merged_df


