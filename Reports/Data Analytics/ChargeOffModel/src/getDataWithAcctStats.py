import pandas as pd
import numpy as np
from tqdm import tqdm
import src.fetch_acctstat_data as fetch_acctstat_data
import src.pkey as pkey
import src.fetch_data_historical_acctcommon as fetch_data_historical_acctcommon

def getDataWithAcctStats():

    """
    Fetches and preprocess data to get ready for scaling and training.
    """


    print("Querying database...")
    accstat_data = fetch_acctstat_data.fetch_acctstat_data()
    acctstatistichist = accstat_data['acctstatistichist']
    acctstatistichist = pd.pivot_table(acctstatistichist,   # Gets lifetime delinquency from historical data
                            index='acctnbr',
                            columns='statistictypcd',
                            values='statisticcount',
                            aggfunc='sum',
                            fill_value=0
                            ).reset_index()
    
    data = pkey.pkey()
    data = data.dropna(subset=['Category']) # Removing all rows where category is empty, meaning it is not a loan

    data['contractdate'] = pd.to_datetime(data['contractdate'])
    data['datemat'] = pd.to_datetime(data['datemat'])
    data['contract_to_maturity_days'] = (data['datemat'] - data['contractdate']).dt.days # calculating contract_to_maturity_days

    # ensuring acctnbr is same datatype in both tables for merge
    data['acctnbr'] = data['acctnbr'].astype(str)
    acctstatistichist['acctnbr'] = acctstatistichist['acctnbr'].astype(str)

    data_with_acct_stats = pd.merge(data, acctstatistichist, on='acctnbr', how='left') # Merging borrower data with loan data
    data_with_acct_stats.replace('', np.nan, inplace=True)

    # filling empty values
    numeric_cols = data_with_acct_stats.select_dtypes(include=['number']).columns
    data_with_acct_stats[numeric_cols] = data_with_acct_stats[numeric_cols].fillna(0)
    object_cols = data_with_acct_stats.select_dtypes(include=['object']).columns
    data_with_acct_stats[object_cols] = data_with_acct_stats[object_cols].fillna('0')


    # Preventing data leakage by changing all rows labeled 'Repossessed Collateral' to their original product type
    # or removing the row altogether if we don't have enough historical data.
    print("Preprocessing data...")
    for index, row in tqdm(data_with_acct_stats.iterrows()):
        if row['product'] == 'Repossessed Collateral':
            acct = row['acctnbr']
            acct_data = fetch_data_historical_acctcommon.fetch_data_historical_acctcommon(acct)
            acct_df = acct_data['wh_acctcommon']
            new_product = acct_df.iloc[0]['product']
            data_with_acct_stats.at[index, 'product'] = new_product

    data_without_repo = data_with_acct_stats[(data_with_acct_stats['product'] != "Repossessed Collateral")]

    # Extracting relevant features
    X = data_without_repo[[
        'product',
        #'noteopenamt',
        'ratetypcd', 
        'noteintrate', 
        #'contractdate', 
        #'datemat',
        'contract_to_maturity_days',
        'origintrate', 
        'riskratingcd',
        #'availbalamt',
        'DOD', 'EFEE', 'EXT', 'KITE', 'MCHG', 'NSF', 'PD', 'PD12',
        'PD15', 'PD18', 'PD30', 'PD60', 'PD90', 'RGD3', 'RGD6', 'RNEW', 'SKIP',
        'UCF']].copy()

    X['riskratingcd'] = X['riskratingcd'].str.replace(r'\D', '', regex=True) # Removing letters from riskrating
    X.replace('', np.nan, inplace=True)
    X.fillna(0, inplace=True)
    y = data_without_repo['cobal'].copy()

    # converting cobal to binomial distribution
    y = (y > 0).astype(int)


    # One-hot encoding ratetype and product features
    X_encoded = pd.get_dummies(X, columns=['ratetypcd'], prefix='ratetypcd')
    X_encoded['ratetypcd_FIX'], X_encoded['ratetypcd_VAR'] = X_encoded['ratetypcd_FIX'].astype(int), X_encoded['ratetypcd_VAR'].astype(int)
    X_final = pd.get_dummies(X_encoded, columns=['product'], prefix='product')

    return X_final, y, data_without_repo