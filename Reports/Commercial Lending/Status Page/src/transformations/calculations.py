import numpy as np
import pandas as pd

def append_total_exposure_field(df):
    """ 
    Single Obligor Exposure Calculation
    
    Args:
        df: loan_data is loaded in
    
    Returns:
        df: loan_data is returned with new fields appended
        
    Operations:
        bookbalance -> if currmiaccttypcd == 'CM45', use notebal, else bookbalance
            - Tax Exempt bonds always have $0 as book balance so adjustment is made
        net balance == bookbalance - cobal
            - BCSB balance - Charged off amount (COBAL)
        net available == available balance amount * (1 - total pct sold)
        net collateral reserve == collateral reserve * (1 - total pct sold)
        total exposure == net balance + net available + net collateral reserve
    """
    # QA test
    list_of_numeric = ['bookbalance','notebal','availbalamt','totalpctsold','noteopenamt','creditlimitamt','noteintrate','cobal','credlimitclatresamt']
    for col in list_of_numeric:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    def convert_to_float(value):
        try:
            return float(value)
        except:
            return None
        
    for col in list_of_numeric:
        df[col] = df[col].apply(convert_to_float)
    
    # Tax Exempt bonds always have $0 Book Balance so need to take NOTEBAL
    df['bookbalance'] = np.where(df['currmiaccttypcd'].isin(['CM45']), df['notebal'], df['bookbalance'])
    df['Net Balance'] = df['bookbalance'] - df['cobal']
    df['Net Available'] = df['availbalamt'] * (1 - df['totalpctsold'])
    df['Net Collateral Reserve'] = df['credlimitclatresamt'] * (1 - df['totalpctsold'])
    df['Total Exposure'] = df['Net Balance'] + df['Net Available'] + df['Net Collateral Reserve']
    return df

def cleaning_loan_data(main_loan_data):
    """
    Additional cleaning of the main_loan_data dataset, excluding ACH manager products and converting datetime fields to appropriate data type
    
    Args:
        main_loan_data (pd.DataFrame)

    Returns:
        main_loan_data (pd.DataFrame)
    """
    # Exclude ACH Manager products
    # main_loan_data = main_loan_data.loc[main_loan_data['currmiaccttypcd'] != 'CI07'].copy()

    # Convert datetime fields
    date_fields = ['origdate','datemat']
    main_loan_data[date_fields] = main_loan_data[date_fields].apply(pd.to_datetime)

    # Create calculated field for total original loan amount
    main_loan_data['orig_ttl_loan_amt'] = np.where(main_loan_data['noteopenamt'] == 0, main_loan_data['creditlimitamt'], main_loan_data['noteopenamt'])

    return main_loan_data

    