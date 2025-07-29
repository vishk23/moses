"""
Core Transformations
"""
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import pandas as pd # type: ignore
import numpy as np # type: ignore
from pandas.api.types import is_numeric_dtype

import cdutils.input_cleansing # type: ignore
import cdutils.deduplication # type: ignore
import cdutils.loans.calculations # type: ignore
import cdutils.joining # type: ignore
import cdutils.input_cleansing # type: ignore
import cdutils.loans.inactive_date # type:ignore
import cdutils.timezone # type: ignore 
import cdutils.daily_deposit_staging # type: ignore
import cdutils.summary_row # type: ignore

def main_pipeline(data: Dict) -> pd.DataFrame:
    """
    Main data pipeline for the balance tracker. This ties back to the Call Report as a check.
    """

    # # Cache data for development
    # src.cdutils.caching.cache_data(r'C:\Users\w322800\Documents\cre_caching', data)
    
    # # Unpack data into dataframes
    wh_acctcommon = data['wh_acctcommon'].copy()
    wh_loans = data['wh_loans'].copy()
    wh_acctloan = data['wh_acctloan'].copy()
    # need to pull out some more necessary fields from the data fetch process here

    # Datatype manipulation
    acctcommon_schema = {'acctnbr':'str'}
    wh_acctcommon = cdutils.input_cleansing.enforce_schema(wh_acctcommon, acctcommon_schema)
    loans_schema = {'acctnbr':'str'}
    wh_loans = cdutils.input_cleansing.enforce_schema(wh_loans, loans_schema)
    acctloan_schema = {'acctnbr':'str'}
    wh_acctloan = cdutils.input_cleansing.enforce_schema(wh_acctloan, acctloan_schema)

    # Transforming the data
    main_loan_data = cdutils.joining.join_loan_tables(wh_acctcommon, wh_acctloan, wh_loans)
    # property_data = src.transformations.joining.join_prop_tables(wh_prop, wh_prop2)

    # # Calculated fields & data cleaning
    main_loan_data = cdutils.loans.calculations.append_total_exposure_field(main_loan_data)
    main_loan_data = cdutils.loans.calculations.cleaning_loan_data(main_loan_data)

    # Consolidate loan data & property data
    # single_prop_data = src.transformations.joining.consolidation_with_one_prop(main_loan_data, property_data)
    # multiple_prop_data = src.transformations.joining.consolidation_with_multiple_props(main_loan_data, property_data)

    # Sort data
    df = main_loan_data.sort_values(by=['Total Exposure','acctnbr'], ascending=[False, True])
    # multiple_prop_data = multiple_prop_data.sort_values(by=['Total Exposure','acctnbr'], ascending=[False, True])

    return df

def filtering_on_pkey(df: pd.DataFrame, key: int) -> pd.DataFrame:
    """
    Filter down the large dataset to only the accounts for the portfolio key that was specified
    """
    assert df['acctnbr'].is_unique, "Duplicates exist"
    assert df is not None
    # Should this be a try/except and throw this on a separate path rather than end the report. If there's no pkey to match up here, we can't really do anything.
    assert (df['portfolio_key'] == key).any(), "Portfolio key does not map to any active products"

    df = df[df['portfolio_key'] == key].copy()
    return df

# Function for adds/deletes
def apply_adds_deletes(raw_data: pd.DataFrame, filtered_data: pd.DataFrame, additions: Optional[List] = None, deletes: Optional[List] = None):
    """
    Apply additions and deletions to the filtered data, gracefully handling all edge cases.
    
    Parameters:
    - raw_data (pd.DataFrame): The raw data containing all account information.
    - filtered_data (pd.DataFrame): The filtered data based on the portfolio key.
    - additions (Optional[List]): List of account numbers to add. Only valid account numbers 
                                  (existing in raw_data and not in filtered_data) are added; others are ignored.
    - deletes (Optional[List]): List of account numbers to delete. Only account numbers 
                                existing in filtered_data are deleted; others are ignored.
    
    Returns:
    - pd.DataFrame: The updated filtered data after applying valid additions and deletions.
    """
    # Enforce data type to string
    if additions is not None:
        additions = [str(item) for item in additions] 
    if deletes is not None:
        deletes = [str(item) for item in deletes] 

    # Convert inputs to sets, handling None and empty cases gracefully
    additions_set = set(additions) if additions is not None and len(additions) > 0 else set()
    deletes_set = set(deletes) if deletes is not None and len(deletes) > 0 else set()
    
    # Extract account numbers as sets from DataFrames, assuming 'acctnbr' exists
    raw_acctnbr_set = set(raw_data['acctnbr']) if not raw_data.empty else set()
    filtered_acctnbr_set = set(filtered_data['acctnbr']) if not filtered_data.empty else set()
    
    # Compute valid additions: must be in raw_data and not already in filtered_data
    to_add = additions_set.intersection(raw_acctnbr_set).difference(filtered_acctnbr_set)
    additions_df = raw_data[raw_data['acctnbr'].isin(to_add)] if to_add else pd.DataFrame(columns=raw_data.columns)
    
    # Combine filtered_data with valid additions
    updated_data = pd.concat([filtered_data, additions_df], ignore_index=True) if not additions_df.empty else filtered_data.copy()
    
    # Compute valid deletions: must be in the original filtered_data
    to_delete = deletes_set.intersection(filtered_acctnbr_set)
    
    # Remove only valid deletions
    updated_data = updated_data[~updated_data['acctnbr'].isin(to_delete)] if to_delete else updated_data
    
    return updated_data 
   


def loan_section(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Filter down to only loans
    """
    assert df['acctnbr'].is_unique, "acctnbr field is not unique"

    if df is None:
        return None

    # Limit scope to loans
    df = df[df['mjaccttypcd'].isin(['CML','MLN','MTG','CNS'])].copy()

    # Saving ACH manager products in memory in case needed
    ach_manager = df.loc[df['currmiaccttypcd'] == 'CI07'].copy()

    # Exclude ACH manager products
    df = df.loc[df['currmiaccttypcd'] != 'CI07'].copy()

    # # Original recon
    # original_recon_amt = df['Net Balance'].sum()

    # Stratify the portfolio
    def cleaning_call_codes(df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleaning Stage for fdiccatcd
        - CML indirect get reclassified to AUTO
        - HOA gets its own category HOA
        - Tax Exempt Bonds become OTAL (other)
        - MTG loans are given their own code 'MTG', just for grouping purposes
        - Indirect Consumer loans originated by bank are put in Consumer/Other (CNOT)
        - Other/CML is the catch all for loans that don't have an FDIC code
        """
        df['fdiccatcd'] = np.where(df['currmiaccttypcd'].isin(['CM15','CM16']), 'AUTO', df['fdiccatcd'])
        df['fdiccatcd'] = np.where(df['currmiaccttypcd'].isin(['CM46','CM47']), 'HOA', df['fdiccatcd'])
        df['fdiccatcd'] = np.where(df['currmiaccttypcd'].isin(['CM45']), 'OTAL', df['fdiccatcd'])
        df['fdiccatcd'] = np.where(df['mjaccttypcd'].isin(['MTG']), 'MTG', df['fdiccatcd'])
        df['fdiccatcd'] = np.where(df['currmiaccttypcd'].isin(['IL09','IL10']), 'CNOT', df['fdiccatcd'])
        df['fdiccatcd'] = np.where(df['fdiccatcd'].isnull(), 'OTAL', df['fdiccatcd'])
        return df

    df = cleaning_call_codes(df) 

    fdic_groups = {
    # Note call codes have been adjusted in an earlier stage to stratify the portfolio
    'CRE': ['CNFM','OTCN','LAND','LNDV','RECN','REFI','REOE','REJU','REOW','RENO','REMU','OTAL','AGPR','REFM'],
    'C&I': ['CIUS'],
    'HOA': ['HOA'],
    'Residential': ['MTG'],
    'Consumer': ['CNOT','CNCR'],
    'Indirect': ['AUTO']
    }
    call_code_mapping = {code: group for group, codes in fdic_groups.items() for code in codes}
    df['Category'] = df['fdiccatcd'].map(call_code_mapping)
    # adjusted_loan_data = df.copy()

    # Attach inactive date
    df = cdutils.loans.inactive_date.append_inactive_date(df)

    cml = df[df['Category'].isin(['CRE','C&I','HOA'])].copy()
    personal = df[~(df['Category'].isin(['CRE','C&I','HOA']))]
    
    return cml, personal, ach_manager

def deposit_section(df: pd.DataFrame) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
    """
    Filter down the deposit section
    """
    assert df['acctnbr'].is_unique, "acctnbr field is not unique"

    if df is None:
        return (None, None)

    # Limit scope to deposits
    deposits = df[df['mjaccttypcd'].isin(['CK','SAV','TD'])].copy()
    other = df[~(df['mjaccttypcd'].isin(['CK','SAV','TD','CML','MTG','CNS','MLN']))].copy()
    
    # Attach data from daily deposit update
    deposits = cdutils.daily_deposit_staging.attach_daily_deposit_fields(deposits)

    
    return deposits, other


def household_title_logic(cml, personal, deposits):
    """
    Generate the household title based on the accounts in the relationship

    The business logic is:
    - Group by entity (customer name) on loan exposure. The entity with largest loan exposure becomes the head of the relationship

    Args:
        cml (df): loans that are commercial
        personal (df): loans that are not commercial
        deposits (df): all deposit accounts in relationship

    Returns:
        household_title (str): This is the head of household/relationship based on the logic gates we set up
    """

    def title_helper(df, sum_column):
        # Make sure we have relevant columns
        required_cols = ['ownersortname', sum_column]
        for col in required_cols:
            assert col in df.columns, "Missing required column"

        # Make sure column being summed is numeric
        assert pd.api.types.is_numeric_dtype(df[sum_column]), "Sum Column needs to be numeric"

        grouped = df.groupby('ownersortname')[sum_column].sum().sort_values(ascending=False)
        if not grouped.empty:
            return str(grouped.index[0])
        return None

    # Check for largest cml customer
    if cml is not None:
        head = title_helper(cml, 'Total Exposure')
        if head is not None:
            return head
    
    # Check for largest personal customer
    if personal is not None:
        head = title_helper(personal, 'Total Exposure')
        if head is not None:
            return head
        
    # Check for largest deposit customer
    if deposits is not None:
        head = title_helper(deposits, 'bookbalance')
        if head is not None:
            return head
    
    # Otherwise, there are no active accounts in relationship and we return None
    return None
    
def related_entities(data: Dict, df_list: List[pd.DataFrame]) -> pd.DataFrame:
    """
    Related entities section. It takes in a list of dataframes (df_list) and based on the acctnbrs in those dataframes, it appends all related entities from the acctrole table. Finally, it appends the taxid from pers or org taxid.
    
    Args:
        data (dict): This is a data package that has the dataframes within that can be unpacked
            - wh_allroles: From COCC database (r1625.world)
            - viewperstaxid: From COCC database (r1625.world)
            - vieworgtaxid: From COCC database (r1625.world)
            - wh_pers: From COCC database (r1625.world)
            - wh_org: From COCC database (r1625.world)
        df_list: List of dfs to extract the acctnbrs from

    Returns:
        df (pd.DataFrame): Two columns (Entity Name & Tax ID)
    """
    # Tests/Asserts
    assert data is not None, "Data dict cannot be None, we need the data tables"
    assert df_list is not None, "List of dataframes cannot be None here"
    
    # Unpack the data
    wh_allroles = data['wh_allroles'].copy()
    viewperstaxid = data['viewperstaxid'].copy()
    vieworgtaxid = data['vieworgtaxid'].copy()
    wh_pers = data['wh_pers'].copy()
    wh_org = data['wh_org'].copy()

    # Input Cleansing (data type check)
    schema_wh_allroles = {
        'acctnbr': str,
        'persnbr': str,
        'orgnbr': str
    }
    wh_allroles = cdutils.input_cleansing.enforce_schema(wh_allroles, schema_wh_allroles)

    schema_viewperstaxid = {
        'persnbr': str,
        'taxid': str
    }

    viewperstaxid = cdutils.input_cleansing.enforce_schema(viewperstaxid, schema_viewperstaxid)

    schema_vieworgtaxid = {
        'orgnbr': str,
        'taxid': str
    }

    vieworgtaxid = cdutils.input_cleansing.enforce_schema(vieworgtaxid, schema_vieworgtaxid)

    schema_wh_pers = {
        'persnbr': str,
        'persname': str
    }

    wh_pers = cdutils.input_cleansing.enforce_schema(wh_pers, schema_wh_pers)

    schema_wh_org = {
        'orgnbr': str,
        'orgname': str
    }

    wh_org = cdutils.input_cleansing.enforce_schema(wh_org, schema_wh_org)

    # Gather acctnbrs from every df in df_list
    acctnbr_series = []
    for df in df_list:
        if "acctnbr" not in df.columns:
            raise KeyError("Each DataFrame needs acctnbr")
        acctnbr_series.append(df['acctnbr'])

    acctnbrs = pd.concat(acctnbr_series, ignore_index=True).drop_duplicates()

    # Related entities (filter down wh_allroles to what we need)
    roles_to_include = ['Tax Owner', 'GUAR', 'OWN', 'LNCO']
    filtered_roles = wh_allroles[wh_allroles['acctrolecd'].isin(roles_to_include)].copy()
    related_entities = filtered_roles[filtered_roles['acctnbr'].isin(acctnbrs)]

    # Merging to get taxid
    merged_df = pd.merge(related_entities, viewperstaxid, on='persnbr', how='left')
    merged_df = pd.merge(merged_df, vieworgtaxid, on='orgnbr', how='left', suffixes=('_pers','_org'))

    # Dedupe Pers/org tables
    dedupe_list = [
        {'df':wh_pers, 'field':'persnbr'},
        {'df':wh_org, 'field':'orgnbr'}
    ]
    wh_pers, wh_org = cdutils.deduplication.dedupe(dedupe_list)

    assert wh_pers['persnbr'].is_unique, "Failure"
    assert wh_org['orgnbr'].is_unique, "Failure"

    # Merge to get pers/orgnames
    merged_df = pd.merge(merged_df, wh_pers, on='persnbr', how='left')
    merged_df = pd.merge(merged_df, wh_org, on='orgnbr', how='left')

    # Calculated fields
    merged_df['taxid'] = np.where(merged_df['taxid_pers'].isnull(), merged_df['taxid_org'], merged_df['taxid_pers'])
    merged_df['entity_name'] = np.where(merged_df['persname'].isnull(), merged_df['orgname'], merged_df['persname'])
    
    # Reduce df to only necessary fields
    result_df = merged_df[['entity_name','taxid']].copy()

    # Deduplicate final related entities table to ensure they only show up once
    dedupe_list = [
        {'df':result_df, 'field':'entity_name'}
    ]

    result_df = cdutils.deduplication.dedupe(dedupe_list).copy()

    result_df['Placeholder'] = None

    result_df = result_df[['entity_name','Placeholder','taxid']].copy()

    return result_df


def summary_section(df_pkg: Dict) -> pd.DataFrame:
    """
    This function is for getting the data necessary to fill in the summary section at the top. This includes things like YTD/TTM average deposit balance, total relationship exposure, etc...

    Args:
        df_pkg (dict): Pass in a list of dfs that are going to be critical to creating the relationship summary section at the top

    Returns:
        output_list
    Usage:
    df_list = [cml, deposits]
        summary_section = summary_section(df_list)
    """
    
    # Need a switch function to toggle YTD/TTM for deposit total
    # Based on it being in between 1/1 - 3/31 (YTD) or later (TTM)

    # Unpack the df list, if cml not None:
        # Assert total exposure column is numeric
        # Take the average of the cml['total_exposure'] column and save that as 'total_commitments'
        # Else return 0

    cml = df_pkg['cml'].copy()
    deposits = df_pkg['deposits'].copy()

    # if cml is not None:
    #     try:
    #         # assert cml['Total Exposure'] is numeric (pd_numeric)
    #         assert is_numeric_dtype(cml['Total Exposure']), "Total Exposure is not numeric"
    #         total_commitments = cml['Total Exposure'].sum()
    #     except:
    #         pass
        
    #     try:
    #         # assert cml['Net Balance'] is numeric (pd_numeric)
    #         assert is_numeric_dtype(cml['Net Balance']), "Net Balance is not numeric"
    #         total_outstanding = cml['Net Balance'].sum()
    #     except:
    #         pass

    #     try:
    #         # Find the total SWAP Exposure
    #         swaps = cml[cml['product'] == 'SWAP Exposure Loans'].copy()
    #         total_swap_exposure = swaps['Total Exposure'].sum()
    #     except:
    #         pass

    # else:
    #     total_commitments = 0
    #     total_outstanding = 0
    #     total_swap_exposure = 0


    # Initialize defaults
    total_commitments   = 0
    total_outstanding   = 0
    total_swap_exposure = 0

    # Only proceed if cml is a non‑empty DataFrame
    if isinstance(cml, pd.DataFrame) and not cml.empty:
        # Ensure required columns exist and are numeric
        for col in ("Total Exposure", "Net Balance"):
            if col not in cml.columns:
                raise KeyError(f"Missing required CML column: {col!r}")
            assert is_numeric_dtype(cml[col]), f"{col!r} must be numeric"
        
        total_commitments = cml["Total Exposure"].sum()
        total_outstanding = cml["Net Balance"].sum()
        # SWAP Exposure: same pattern, sum up only the matching rows
        swap_mask = cml["product"] == "SWAP Exposure Loans"
        if swap_mask.any():
            # we've already asserted "Total Exposure" is numeric
            total_swap_exposure = cml.loc[swap_mask, "Total Exposure"].sum()

    if deposits is not None and not deposits.empty:
        deposit_timeframe = None
        assert pd.api.types.is_datetime64_any_dtype(deposits['effdate']), "effdate is not datetime"

        first_effdate = deposits['effdate'].iloc[0]

        if first_effdate.quarter == 1:
            deposit_balance = deposits['TTM_AvgBal'].sum()
            deposit_timeframe = 'TTM Average Balance'
        else:
            deposit_balance = deposits['ytdavgbal'].sum()
            deposit_timeframe = 'YTD Average Balance'
    else:
        deposit_balance = 0
        deposit_timeframe = 'TTM Average Balance'


    # first_effdate = first_effdate.strftime('%m/%d/%Y')

    summary_output = {
        'total_commitments': total_commitments,
        'total_outstanding': total_outstanding,
        'total_swap_exposure': total_swap_exposure,
        'deposit_balance': deposit_balance,
        'deposit_timeframe': deposit_timeframe,
    }

    return summary_output

def final_cml(cml):
    """
    Filter down the cml raw data to specifically how it needs to appear on the output
    """
    # Update maturity date based on line of credit or not
    # Other implementation uses loanlimityn
    cml['Terms'] = np.where(cml['loanlimityn'] == 'Y', cml['inactivedate'], cml['datemat'])

    # Face calcuation (creditlimitamt else noteopenamt)
    cml['Face'] = np.where(cml['loanlimityn'] == 'Y', cml['creditlimitamt'], cml['noteopenamt'])

    # Drop unneccessary columns
    cml = cml[['contractdate','acctnbr','product','Face','Net Balance','noteintrate','Terms','ownersortname']].copy()
    cml = cdutils.timezone.convert_datetime_to_str(cml)

    # Add subtotal row
    cml = cdutils.summary_row.append_summary_row(
        df=cml,
        sum_cols = ['Face','Net Balance'],
        avg_cols = ['noteintrate'],
        label_col = 'product',
        label = 'Total'
    )

    return cml


def final_personal(personal):
    """
    Filter down the personal raw data to specifically how it needs to appear on the output
    """
    # If its a line of credit type product (HELOC, etc...), use inactive date, otherwise maturity date
    personal['Terms'] = np.where(personal['loanlimityn'] == 'Y', personal['inactivedate'], personal['datemat'])

    # Face calcuation (creditlimitamt else noteopenamt)
    personal['Face'] = np.where(personal['loanlimityn'] == 'Y', personal['creditlimitamt'], personal['noteopenamt'])

    # Drop unneccessary columns
    personal = personal[['contractdate','acctnbr','product','Face','Net Balance','noteintrate','datemat','ownersortname']].copy()
    personal = cdutils.timezone.convert_datetime_to_str(personal)

    # Add subtotal row
    personal = cdutils.summary_row.append_summary_row(
        df=personal,
        sum_cols = ['Face','Net Balance'],
        avg_cols = ['noteintrate'],
        label_col = 'product',
        label = 'Total'
    )
    return personal

 
def final_deposits(deposits):
    """
    Filter down the deposit raw date to specifically how it needs to eappear on the output
    """
    # Rename columns and drop unnecessary columns
    deposits = deposits[['contractdate','acctnbr','product','TTM_AvgBal','ytdavgbal','TTM_DAYS_OVERDRAWN','ownersortname']].copy() 
    deposits = cdutils.timezone.convert_datetime_to_str(deposits) 
    # Add subtotal row
    deposits = cdutils.summary_row.append_summary_row(
        df=deposits,
        sum_cols = ['TTM_AvgBal','ytdavgbal'],
        label_col = 'product',
        label = 'Total'
    )
    return deposits

    


    



    
    
