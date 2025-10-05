Usage:
cd to Production folder in monorepo
python -m src.main

Automatic distribution


# 2025-08-20

Meeting with Tim

Update balance tracker items


HEAT loans
- change based on rate


# 2025-09-30
Updated wsj prime rate because decrease, affects matrix

    # Adjustment for the Consumer loans: WSJ Prime + 1
    df['modified_noteintrate'] = np.where(
        (df['currmiaccttypcd'] == 'IL33') & (df['contractdate'] >= pd.Timestamp(2025,1,1)), .07,
        np.where((df['currmiaccttypcd'].isin(['IL21','IL31','IL33'])) & (df['contractdate'] >= pd.Timestamp(2025,9,18)), .0825,
        np.where((df['currmiaccttypcd'].isin(['IL21','IL31','IL33'])) & (df['contractdate'] >= pd.Timestamp(2024,12,19)), .085,
        np.where((df['currmiaccttypcd'].isin(['IL21','IL31','IL33'])) & (df['contractdate'] >= pd.Timestamp(2024,11,8)), .0875,


That's a snippet of it. Should be good, but should confirm with Tom K