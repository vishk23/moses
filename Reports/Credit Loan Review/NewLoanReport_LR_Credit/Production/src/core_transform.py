"""
Core Transformations
"""
from typing import Dict
from pathlib import Path
import os
from datetime import datetime


import pandas as pd # type: ignore
import numpy as np # type: ignore
import src.cdutils.pkey_sqlite



def filter_acctcommon(df):
    """
    Filter acctcommon table

    Args:
        df: acctcommon table from COCC

    Returns:
        result_df: dataframe after filters are applied
    
    Operations:
    [MJACCTTYPCD] IN ("CML", "CNS", "MTG", "MLN") 
    AND 
    [CURRMIACCTTYPCD] != "CI07"
    If [MJACCTTYPCD] IN "CNS", [CURRMIACCTTYPCD] IN ("IL02", "IL11", "IL12", "IL13", "IL14") 
    AND 
    !IsNull([TAXRPTFORORGNBR])
    - Concatenate address fields into one primary_address field
    """
    df = df[df['mjaccttypcd'].isin(['CML', 'MTG', 'MLN'])]
    df = df[df['currmiaccttypcd'] != 'CI07']
    df['primary_address'] = df[['nameaddr1','nameaddr2','nameaddr3']].apply(lambda x: ''.join(filter(None, x)), axis=1)
    df = df.drop(columns=['nameaddr1','nameaddr2','nameaddr3'])
    return df

# %%
def filter_wh_loans(df):
    """
    Filter wh_loans

    Args:
        df: WH_LOANS_TEMP from COCCDM db table
    
    Returns:
        result_df: filtered dataframe of wh_loans

    Operations:
    - Create a day difference between 
    """
    df['day diff'] = (df['rundate'] - df['origdate']).dt.days + 1
    result_df = df[df['day diff'] <= 45]
    return result_df
    
def drop_household_duplicates(househldacct):
    househldacct = househldacct.sort_values(by='datelastmaint', ascending=False).drop_duplicates(subset='acctnbr', keep='first').copy()
    return househldacct

def drop_org_duplicates(wh_org):
    wh_org = wh_org.drop_duplicates(subset='orgnbr', keep='first').copy()
    return wh_org



# %%
def consolidate_prop_data(wh_prop, wh_prop2):
    """
    Consolidate property data between the two property tables in COCC

    Args:
        wh_prop
        wh_prop2

    Returns:
        consolidated_prop_data

    Operations:
    - merge the tables
    - rename columns
    - keep only the property with the highest appraised value
    - fill null values in aprsvalueamt field

    """
    consolidated_prop_data = pd.merge(wh_prop, wh_prop2, how='inner', on='propnbr')
    consolidated_prop_data['acctnbr'] = consolidated_prop_data['acctnbr_x'].combine_first(consolidated_prop_data['acctnbr_y'])
    consolidated_prop_data = consolidated_prop_data.drop(columns=['acctnbr_x','acctnbr_y'])
    consolidated_prop_data['aprsvalueamt'] = consolidated_prop_data['aprsvalueamt'].fillna(0)
    consolidated_prop_data = (consolidated_prop_data.sort_values('aprsvalueamt', ascending=False).groupby('acctnbr', as_index=False).first())
    consolidated_prop_data = consolidated_prop_data.reset_index(drop=True)
    return consolidated_prop_data

def merge_data(filtered_acctcommon, filtered_wh_loans, wh_acctloan, consolidated_prop_data, wh_org, househldacct):
    """
    Merging dataframes together
    
    Args:
        dfs: all dataframes
    
    Returns:
        merged_df: merged data
    """

    # QA tests
    assert filtered_acctcommon['acctnbr'].is_unique, "Duplicates found"
    assert househldacct['acctnbr'].is_unique, "Duplicates found"
    assert wh_acctloan['acctnbr'].is_unique, "Duplicates found"
    assert consolidated_prop_data['acctnbr'].is_unique, "Duplicates found"
    assert wh_org['orgnbr'].is_unique, "Duplicates found"

    merged_df = pd.merge(filtered_acctcommon, filtered_wh_loans, on='acctnbr', how='inner')
    merged_df = pd.merge(merged_df, wh_acctloan, on='acctnbr', how='left')
    merged_df = pd.merge(merged_df, consolidated_prop_data, on='acctnbr', how='left')
    merged_df = merged_df.drop(columns=['propnbr_y'])
    merged_df = merged_df.rename(columns={'propnbr_x':'propnbr'})
    merged_df = pd.merge(merged_df, wh_org, left_on='taxrptfororgnbr', right_on='orgnbr', how='left').sort_values(by='origdate', ascending=False)
    merged_df = pd.merge(merged_df, househldacct, how='left', on='acctnbr')
    return merged_df





# %%
# Potential Outstanding
def filter_and_merge_loan_tables(acctcommon, acctloan, loans):
    """
    This filters on CML Loans & merges tables to consolidate loan data.
    Data cleansing on numeric fields is performed.
    
    Args:
        acctcommon: WH_ACCTCOMMON
        acctloan: WH_ACCTLOAN
        loans: WH_LOANS
        
    Returns:
        df: Consolidated loan data as a dataframe
        
    Operations:
        - mjaccttypcd (Major) == 'CML'
        - left merge of df (acctcommon) & acctloan on 'acctnbr'
        - left merge of df & loans on 'acctnbr'
        - drop all fields that are completely null/empty
        - Replace null/na values with 0 for numeric fields:
            - total pct sold
            - avail bal amt
            - credit limit collateral reserve amt
        - loans with risk rating 4 or 5 are excluded
    """
    # CML loans
    df = acctcommon[acctcommon['mjaccttypcd'].isin(['CML'])]
    df = df[df['curracctstatcd'].isin(['ACT','NPFM'])]

    # Merging and dropping blank fields
    df = pd.merge(df, acctloan, on='acctnbr', how='left', suffixes=('_df', '_acctloan'))
    df = pd.merge(df, loans, on='acctnbr', how='left', suffixes=('_df', '_loans'))
    df = df.dropna(axis=1, how='all')
    
    # Data Cleansing
    df['totalpctsold'] = df['totalpctsold'].fillna(0)
    df['availbalamt'] = df['availbalamt'].fillna(0)
    df['credlimitclatresamt'] = df['credlimitclatresamt'].fillna(0)
    
    return df



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
    list_of_numeric = ['bookbalance','notebal','availbalamt','totalpctsold','noteopenamt','noteintrate','cobal','credlimitclatresamt']
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



# %%
def get_most_recent_file(folder_path):
    today_str = datetime.now().strftime('%Y%m%d')
    today_date = datetime.strptime(today_str, '%Y%m%d')

    files = os.listdir(folder_path)

    csv_files = [f for f in files if f.startswith("r360_") and f.endswith(".csv")]

    valid_files = {}
    for file in csv_files:
        try:
            date_str = file.split("_")[1].split(".csv")[0]
            file_date = datetime.strptime(date_str, '%Y%m%d')
            if file_date <= today_date:
                valid_files[file_date] = file
        except (IndexError, ValueError):
            continue

    if not valid_files:
        print("No history")
        return None
    else:
        most_recent_date = max(valid_files.keys())
        most_recent_file = valid_files[most_recent_date]

        return os.path.join(folder_path, most_recent_file)
    
def append_grouping_keys(loan_data, househldacct, pkey):
    assert househldacct['acctnbr'].is_unique, "Duplicates found"
    assert pkey['acctnbr'].is_unique, "Duplicates found"

    loan_data = pd.merge(loan_data, househldacct, on='acctnbr', how='left')
    loan_data = pd.merge(loan_data, pkey, on='acctnbr', how='left')
    return loan_data

def retrieve_historical_keys(history_path):
    if history_path is None:
        return None
    else:
        history = pd.read_csv(history_path)
        return history
    
# def append_historical_keys(data, history=None):
#     if history is None:
#         return data
#     else:
#         history_subset = history[['acctnbr','portfolio_key']]
#         assert history_subset['acctnbr'].is_unique, "Duplicates found"
#         data = pd.merge(data, history_subset, on='acctnbr', how='left')
#         data = data.set_index('acctnbr')
#         data = data.to_dict(orient='index').copy()
#         return data
    


# %%
def calculate_total_exposure(df):
    hh_exposure = df.groupby('householdnbr', as_index=False)['Total Exposure'].sum()
    hh_exposure = hh_exposure.rename(columns={'Total Exposure':'total_exposure_hh'}).copy()
    pkey_exposure = df.groupby('portfolio_key', as_index=False)['Total Exposure'].sum()
    pkey_exposure = pkey_exposure.rename(columns={'Total Exposure':'total_exposure_pkey'}).copy()
    hh_exposure = pd.DataFrame(hh_exposure)
    pkey_exposure = pd.DataFrame(pkey_exposure)

    df = pd.merge(df, hh_exposure, on='householdnbr', how='left')
    df = pd.merge(df, pkey_exposure, on='portfolio_key', how='left')
    return df

# %%
def append_exposure(df, keys_df):
    # QA test
    list_of_numeric = ['bookbalance','notebal','availbalamt','totalpctsold','noteopenamt','noteintrate','cobal','credlimitclatresamt']
    for col in list_of_numeric:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    def convert_to_float(value):
        try:
            return float(value)
        except:
            return None
        
    for col in list_of_numeric:
        df[col] = df[col].apply(convert_to_float)

    assert df['acctnbr'].is_unique, "Duplicates found"
    assert keys_df['acctnbr'].is_unique, "Duplicates found"

    df = pd.merge(df, keys_df, how='left', on='acctnbr')
    return df

# %%
# NEW LOAN section
def split_data(df):
    """
    Goal is to split the data between CML & MTG for this section, add subtitles, and necessary blank fields
    """
    df['Notes'] = None
    df['Next Rev Date'] = None
    df['Appr in CT File'] = None
    df['Exceptions on List'] = None

    cml = df.loc[df['mjaccttypcd'] == 'CML', [
        'Notes',
        'Next Rev Date',
        'Appr in CT File',
        'Exceptions on List',
        'householdnbr',
        'origdate',
        'contractdate',
        'product',
        'loanofficer',
        'ownersortname',
        'acctnbr',
        'origbal',
        'notebal',
        'availbalamt',
        'total_exposure_hh',
        'total_exposure_pkey',
        'riskratingcd',
        'fdiccatcd',
        'fdiccatdesc',
        'naicscd',
        'naicscddesc',
        'proptypecd',
        'proptypdesc',
        'noteintrate',
        'propnbr',
        'propdesc',
        'noteopenamt'
    ]].copy()

    cml = cml.sort_values(by='contractdate', ascending=False)

    mtg = df.loc[df['mjaccttypcd'] == 'MTG', [
        'Notes',
        'Next Rev Date',
        'Appr in CT File',
        'Exceptions on List',
        'householdnbr',
        'origdate',
        'contractdate',
        'product',
        'loanofficer',
        'ownersortname',
        'acctnbr',
        'origbal',
        'notebal',
        'availbalamt',
        'total_exposure_hh',
        'total_exposure_pkey',
        'riskratingcd',
        'fdiccatcd',
        'fdiccatdesc',
        'naicscd',
        'naicscddesc',
        'proptypecd',
        'proptypdesc',
        'noteintrate',
        'propnbr',
        'propdesc',
        'noteopenamt'
    ]].copy()

    mtg = mtg.sort_values(by='contractdate', ascending=False)

    def create_subtitle_row(df, subtitle):
        """
        Create a new row with a subtitle to break sections apart

        Args:
            df: either cml or mtg
            subtitle (str): section title
        
        Returns:
            df with additional row for subtitle
        """
        new_row = pd.DataFrame(columns=df.columns)
        new_row.loc[1, 'product'] = subtitle
        new_row = new_row.fillna('')
        df = pd.concat([new_row, df]).copy()
        return df
    
    cml = create_subtitle_row(cml, 'Commercial Loans')
    mtg = create_subtitle_row(mtg, 'Residential Loans')

    blank_row = pd.DataFrame(columns=cml.columns)
    blank_row = blank_row.fillna('')
    
    df = pd.concat([cml, blank_row])
    df = pd.concat([df, mtg])

    return df



# %%
# CRA section
def cra_section(df):
    """
    CRA Sheet creation
    """
    df['#'] = None
    # df['Committed'] = None
    df['Round'] = None
    df['Gross Sales'] = None
    df['MSA'] = None
    df['State'] = None
    df['County'] = None
    df['Census'] = None
    df['SBP'] = None
    df['Reason'] = None
    df['Comments'] = None

    df = df.loc[~(df['currmiaccttypcd'].isin(['CM15','CM16']))].copy()
    df = df.loc[df['mjaccttypcd'] != 'MTG'].copy()

    df = df.loc[df['mjaccttypcd'] == 'CML', [
        '#',
        'contractdate',
        'ownersortname',
        'acctnbr',
        'noteopenamt',
        'Round',
        'Gross Sales',
        'primary_address',
        'primaryownercity',
        'primaryownerstate',
        'primaryownerzipcd',
        'Comments',
        'fdiccatcd',
        'MSA',
        'State',
        'County',
        'Census',
        'product',
        'SBP',
        'Reason',
        'noteintrate',
        'loanofficer',
        'origdate',
        'proptypdesc',
        'riskratingcd'
    ]].copy()

    df = df.sort_values(by='contractdate', ascending=False)

    return df




def main_pipeline(data: Dict) -> pd.DataFrame:
    """
    Main data pipeline 
    """
    base_dir = Path(r"\\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Data_Analytics\R360\Production\assets")
    current_engine = src.cdutils.pkey_sqlite.create_sqlite_engine('current.db', use_default_dir=False, base_dir=base_dir)

    wh_acctcommon = data['wh_acctcommon'].copy()
    wh_loans = data['wh_loans'].copy()
    wh_acctloan = data['wh_acctloan'].copy()
    wh_org = data['wh_org'].copy()
    wh_prop = data['wh_prop'].copy()
    wh_prop2 = data['wh_prop2'].copy()
    househldacct = data['househldacct'].copy()


    filtered_acctcommon = filter_acctcommon(wh_acctcommon)
    filtered_wh_loans = filter_wh_loans(wh_loans)
    consolidated_prop_data = consolidate_prop_data(wh_prop, wh_prop2)

    househldacct = drop_household_duplicates(househldacct)
    wh_org = drop_org_duplicates(wh_org)
    merged_df = merge_data(filtered_acctcommon, filtered_wh_loans, wh_acctloan, consolidated_prop_data, wh_org, househldacct)

    loan_data = filter_and_merge_loan_tables(wh_acctcommon, wh_acctloan, wh_loans)
    loan_data = append_total_exposure_field(loan_data)

    pkey = src.cdutils.pkey_sqlite.query_current_db(engine=current_engine)
    loan_data = append_grouping_keys(loan_data, househldacct, pkey)

    loan_data = calculate_total_exposure(loan_data)
    loan_data_keys = loan_data.loc[:,['acctnbr','total_exposure_hh','total_exposure_pkey']].copy()


    merged_df = append_exposure(merged_df, loan_data_keys)

    new_loan_page = split_data(merged_df)
    cra_page = cra_section(merged_df)

    return new_loan_page, cra_page

