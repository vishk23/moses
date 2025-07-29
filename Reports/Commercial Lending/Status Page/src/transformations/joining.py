import pandas as pd # type: ignore

def join_loan_tables(wh_acctcommon_me, wh_acctloan_me, wh_loans_me):
    """
    Merging core loan tables on acctnbr

    Args:
        wh_acctcommon_me (pd.DataFrame): (month end) from COCCDM
        wh_acctloan_me (pd.DataFrame): (month end) from COCCDM
        wh_loans_me (pd.DataFrame): (month end) from COCCDM
    
    Returns:
        df (pd.DataFrame): Combined loan tables into a df
    """
    # Pre-merge validation
    assert wh_acctcommon_me['acctnbr'].is_unique, "Duplicates exist"
    assert wh_acctloan_me['acctnbr'].is_unique, "Duplicates exist"
    assert wh_loans_me['acctnbr'].is_unique, "Duplicates exist"

    # Merging
    df = pd.merge(wh_acctcommon_me, wh_acctloan_me, on='acctnbr', how='left')
    df = pd.merge(df, wh_loans_me, on='acctnbr', how='left')

    # df = df[~(df['fdiccatcd'].isnull())].copy()

    return df

def join_prop_tables(wh_prop, wh_prop2):
    """
    Joining property tables together in a left-join on wh_prop.

    Args:
        wh_prop (pd.DataFrame): OSIBANK.WH_PROP
        wh_prop2 (pd.DataFrame): OSIBANK.WH_PROP2
    
    Returns:
        df (pd.DataFrame): Joined property tables as a df
    """
    wh_prop2 = wh_prop2.drop_duplicates(subset='propnbr', keep='first')

    # Tests
    assert wh_prop2['propnbr'].is_unique, "Duplicates exist"

    wh_prop2 = wh_prop2.drop(columns=['acctnbr']).copy()

    # Merge
    df = pd.merge(wh_prop, wh_prop2, on='propnbr', how='left')

    return df

def consolidation_with_one_prop(main_loan_data, property_data):
    """
    This is the main_loan_data joined with property_data, filtered to only one property per acctnbr.
    This is filtered on max(appraisal value)

    Args:
        main_loan_data (pd.DataFrame)
        property_data (pd.DataFrame)

    Returns:
        df (pd.DataFrame): df with one property per acctnbr
    """
    # Deduplicate the property data based on max appraisal_value_amt
    property_data_sorted = property_data.sort_values(by=['acctnbr','aprsvalueamt'], ascending=[True, False])
    property_dedup = property_data_sorted.drop_duplicates(subset='acctnbr', keep='first')

    # Pre-merge validation
    assert main_loan_data['acctnbr'].is_unique, "Duplicates exist"
    assert property_dedup['acctnbr'].is_unique, "Duplicates exist"

    # Merge
    df = pd.merge(main_loan_data, property_dedup, on='acctnbr', how='left')
    return df

def consolidation_with_multiple_props(main_loan_data, property_data):
    """
    This is the main_loan_data joined with property_data, including multiple properties per acctnbr.
    Keep in mind acctnbr field is not unique here.

    Args:
        main_loan_data (pd.DataFrame)
        property_data (pd.DataFrame)

    Returns:
        df (pd.DataFrame): df with multiple properties per acctnbr
    """
    # Pre-merge validation
    assert main_loan_data['acctnbr'].is_unique, "Duplicates exist"

    # Merge
    df = pd.merge(main_loan_data, property_data, on='acctnbr', how='left')
    return df