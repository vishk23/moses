import pandas as pd # type: ignore


def creating_monthly_delta(data_prior_summary: pd.DataFrame, data_current_summary: pd.DataFrame) -> pd.DataFrame:
    """
    Combining the two summary tables to find the monthly delta for each category
    """
    df = pd.merge(data_prior_summary, data_current_summary, how='inner', on='Category', suffixes=('_prior','_current'))

    # Create delta
    df['Delta'] = ((df['Net Balance_current'] - df['Net Balance_prior']) / 1000)
    
    # Ordering
    custom_order = ['CRE','C&I','HOA','Residential','Consumer','Indirect']
    df['Category'] = pd.Categorical(df['Category'], categories=custom_order, ordered=True)
    df = df.sort_values('Category')
    df = df[['Category','Delta']].copy()
    return df