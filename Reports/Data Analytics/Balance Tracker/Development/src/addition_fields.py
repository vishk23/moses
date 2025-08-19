"""
Weighted Average Rate & Unadvanced Funds
"""
import cdutils.dealer_split # type: ignore
import src.fetch_data

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
        df['noteintrate'])))))))))))))
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

    # new_loan_df = df[
    #     (df['origdate'].dt.month == df['effdate'].dt.month) & (df['origdate'].dt.year == df['effdate'].dt.year)
    # ].copy()

    # Using the Transaction table
    start_date = new_loan_df['effdate'].iloc[0].strftime('%Y-%m-01 00:00:00')
    end_date = new_loan_df['effdate'].iloc[0].strftime('%Y-%m-%d 00:00:00')

    rtxn_data_pack = src.fetch_data.fetch_rtxn(start_date, end_date)

    acctcommon = rtxn_data_pack['acctcommon'].copy()
    rtxn = rtxn_data_pack['rtxn'].copy() 
    rtxn_schema = {'tranamt': 'float', 'acctnbr':'str'}
    rtxn = cdutils.input_cleansing.enforce_schema(rtxn, rtxn_schema)

    acctcommon_schema = {'acctnbr':'str'}
    acctcommon = cdutils.input_cleansing.enforce_schema(acctcommon, acctcommon_schema)
    rtxn = pd.merge(rtxn, acctcommon, how='left', on='acctnbr')

    # Calculting net advances
    resi_minors = ("MG48", "MG50", "MG52", "MG55", "MG60")
    resi_codes = ("PDSB","CWTH","CKUS","XDSB")
    secondary_codes = ("PDSB", "OPA")
    cml_minors = ("CM06", "CM30", "CM52")
    disb_codes_cml = ("PDSB", "SWPI")
    receipt_codes_cml = ("PRCT", "SWPR")

    def calculate_advances(row):
        if (row['currmiaccttypcd'] in resi_minors) and (row['tranamt'] < 0) and (row['rtxntypcd'] in resi_codes):
            return row['tranamt']
        elif (row['rtxntypcd'] in secondary_codes) and (row['currmiaccttypcd'] not in cml_minors):
            return row['tranamt']
        else:
            return 0

    rtxn['advances'] = rtxn.apply(calculate_advances, axis=1)


    # Need trancd formula built out: NDSB
    # This will be a separate column that we add to advances
    rtxn['new loan disb'] = np.where(rtxn['rtxntypcd'] == 'NDSB', rtxn['tranamt'], 0)

    rtxn['cml_disb'] = np.where((rtxn['rtxntypcd'].isin(disb_codes_cml)) & (rtxn['currmiaccttypcd'].isin(cml_minors)), rtxn['tranamt'], 0)
    rtxn['cml_receipit'] = np.where((rtxn['rtxntypcd'].isin(receipt_codes_cml)) & (rtxn['currmiaccttypcd'].isin(cml_minors)), rtxn['tranamt'], 0)

    acct_grouping = rtxn.groupby('acctnbr').agg({
        'advances':'sum',
        'new loan disb':'sum',
        'cml_disb':'sum',
        'cml_receipt':'sum'
    }).reset_index()
    

    acct_grouping['advances'] = abs(acct_grouping['advances'])
    acct_grouping['net cml advance'] = (acct_grouping['cml_disb'] + acct_grouping['cml_receipt']) * -1
    acct_grouping['net cml advance'] = acct_grouping['net cml advance'].replace(-0.0,0.0)
    acct_grouping['net cml advance'] = np.where(acct_grouping['net cml advance'] < 0, 0, acct_grouping['net cml advance'])
    acct_grouping['advances'] = np.where(acct_grouping['net cml advance'] > 0, acct_grouping['net cml advance'], acct_grouping['advances'])
    acct_grouping_final = acct_grouping[['acctnbr','advances','new loan disb']].copy()

    # Merging
    new_loan_df = pd.merge(new_loan_df, acct_grouping_final, on='acctnbr', how='left')

    new_loan_df['advances'] = new_loan_df['advances'].fillna(0)
    new_loan_df['new loan disb'] = new_loan_df['new loan disb'].fillna(0)
    new_loan_df['new_and_advanced'] = new_loan_df['advances'] + (new_loan_df['new loan disb'] * -1)


    # Apply abs value to net advances

    # Create a separate formula on transaction table for the 3 commercial minors that we need to net disb - reciepts
    # or embed this into the second line of that formula above (couldn't get this correct based on the formula/codes Tom gave me)

    # Then we merge it into new_load_df as an extra field and this is used in the weighted_avg_rate as the weight_col instead of Net Balance


    new_yield = weighted_avg_rate(df, title='New Loan Yield', weight_col='new_and_advanced')

    df['Unadvanced'] = (df['availbalamt']) / 1000

    # Unadvanced
    unadvanced = df.groupby('Category')['Unadvanced'].sum().reset_index()
    unadvanced = unadvanced.rename(columns={'Unadvanced':'Unadvanced Funds'})

    # Merge
    merged_df = pd.merge(new_yield, total_yield, how='inner', on='Category')
    merged_df = pd.merge(merged_df, unadvanced, how='inner', on='Category')

    return merged_df


