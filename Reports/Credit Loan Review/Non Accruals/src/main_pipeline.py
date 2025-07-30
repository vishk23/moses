import pandas as pd # type: ignore
import numpy as np # type: ignore

def main_pipeline(effdate, acctcommon, acctloan):
        
        # ------------ following alteryx workflow ------------ 
        
        acctcommon = acctcommon[acctcommon['effdate'] == effdate]
        acctcommon.loc[acctcommon['currmiaccttypcd'].isin(['CM15', 'CM16']), 'mjaccttypcd'] = 'CNS'

        df_for_other_pipeline = pd.merge(acctcommon, acctloan, on='acctnbr', how='left')
        
        npfm_rows = acctcommon[acctcommon['curracctstatcd'] == "NPFM"]
        
        merged1 = pd.merge(npfm_rows, acctloan, on='acctnbr', how='left')

        merged1['acctnbr'] = merged1['acctnbr'].astype(str)

        merged1['Days Past Due'] = (merged1['effdate'] - merged1['currduedate']).dt.days
        
        merged1['Days Past Due'] = np.where(merged1['Days Past Due'] < 0, 0, merged1['Days Past Due'])

        merged1 = merged1.rename(columns={
        'acctnbr': 'Account Number',
        'product': 'Product Name',
        'ownersortname': 'Customer Name',
        'loanofficer': 'Responsibility Officer',
        'bookbalance': 'Current Balance',
        'cobal': 'Charged Off',
        'riskratingcd': 'Risk',
        })

        merged1['Non Accrual'] = 'Yes'
        merged1['Net Balance'] = merged1['Current Balance'] - merged1['Charged Off']
        merged1 = merged1[merged1['Product Name'] != "Repossessed Collateral"]

        decimal_cols = ['Current Balance', 'Charged Off', 'Net Balance', 'totalpaymentsdue']
        for col in decimal_cols:
            merged1[col] = merged1[col].astype(float)
        merged1['Risk'] = merged1['Risk'].astype(str)
        merged1['Risk'] = merged1['Risk'].replace(['None', 'nan'], 'Unknown')

        merged11 = merged1[merged1['mjaccttypcd'].isin(['CML', 'MLN'])]
        


        new_row = pd.DataFrame([{
            'Current Balance': merged11['Current Balance'].sum(),
            'Charged Off': merged11['Charged Off'].sum(),
            'Net Balance': merged11['Net Balance'].sum(),
            'Non Accrual': len(merged11['Non Accrual']),
            'TagType': 'Sum'
        }])
        none_row = pd.DataFrame([{
            'TagType': None
        }])
        merged11 = pd.concat([merged11, new_row], ignore_index=True)
        merged11 = pd.concat([merged11, none_row], ignore_index=True)



        merged12 = merged1[merged1['mjaccttypcd'].isin(['CNS'])]

        merged12T = merged12[merged12['Product Name'] == 'Unsecured HEAT Loans'].sort_values(by='Customer Name')
        merged12F = merged12[merged12['Product Name'] != 'Unsecured HEAT Loans']

        new_row = pd.DataFrame([{
            'Current Balance': merged12T['Current Balance'].sum(),
            'Charged Off': merged12T['Charged Off'].sum(),
            'Net Balance': merged12T['Net Balance'].sum(),
            'Non Accrual': len(merged12T['Non Accrual']),
            'TagType': 'Sum'
        }])
        
        merged12 = pd.concat([merged12T, new_row], ignore_index=True)
        merged12 = pd.concat([merged12, none_row], ignore_index=True)

        new_row = pd.DataFrame([{
            'Current Balance': merged12F['Current Balance'].sum(),
            'Charged Off': merged12F['Charged Off'].sum(),
            'Net Balance': merged12F['Net Balance'].sum(),
            'Non Accrual': len(merged12F['Non Accrual']),
            'TagType': 'Sum'
        }])

        merged13 = pd.concat([merged12F.sort_values(by='Customer Name'), new_row], ignore_index=True)
        merged13 = pd.concat([merged13, none_row], ignore_index=True)


        merged14 = merged1[merged1['mjaccttypcd'].isin(['MTG'])]

        new_row = pd.DataFrame([{
            'Current Balance': merged14['Current Balance'].sum(),
            'Charged Off': merged14['Charged Off'].sum(),
            'Net Balance': merged14['Net Balance'].sum(),
            'Non Accrual': len(merged14['Non Accrual']),
            'TagType': 'Sum'
        }])

        merged14 = pd.concat([merged14.sort_values(by='Customer Name'), new_row], ignore_index=True)
        merged14 = pd.concat([merged14, none_row], ignore_index=True)

        if not merged12['Account Number'].isna().all():
            merged_data = pd.concat([merged11, merged12, merged13, merged14], ignore_index=True)
        else:
            merged_data = pd.concat([merged11, merged13, merged14], ignore_index=True)

        merged_data = merged_data[['Product Name', 'Account Number', 'Customer Name', 'Responsibility Officer', 'Days Past Due', 'Current Balance', 'Charged Off', 'Net Balance', 'Risk', 'Non Accrual', 'totalpaymentsdue', 'currduedate', 'TagType']]
        merged_data = merged_data.rename(columns={
        'totalpaymentsdue': 'Total Amount Due',
        'currduedate': 'Next Payment Due Date'
        })


        return merged_data, merged1, df_for_other_pipeline