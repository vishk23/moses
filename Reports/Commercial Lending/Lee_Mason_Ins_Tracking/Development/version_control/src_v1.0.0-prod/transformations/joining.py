import pandas as pd # type: ignore
import numpy as np # type: ignore

def join_loan_tables(wh_acctcommon, wh_acctloan, wh_loans):
    """
    Merging core loan tables on acctnbr

    Args:
        wh_acctcommon (pd.DataFrame): (month end) from COCCDM
        wh_acctloan (pd.DataFrame): (month end) from COCCDM
        wh_loans (pd.DataFrame): (month end) from COCCDM
    
    
    Returns:
        df (pd.DataFrame): Combined loan tables into a df
    """
    # Pre-merge validation
    assert wh_acctcommon['acctnbr'].is_unique, "Duplicates exist"
    assert wh_acctloan['acctnbr'].is_unique, "Duplicates exist"
    assert wh_loans['acctnbr'].is_unique, "Duplicates exist"

    # Merging
    df = pd.merge(wh_acctcommon, wh_acctloan, on='acctnbr', how='left')
    df = pd.merge(df, wh_loans, on='acctnbr', how='left')

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

def appending_owner_address(
        df: pd.DataFrame, 
        orgaddruse: pd.DataFrame, 
        persaddruse: pd.DataFrame, 
        wh_addr: pd.DataFrame
        ) -> pd.DataFrame:
    """
    Getting the primary address of the owner of the account and appending it

    Args:
        df (pd.DataFrame): main data
        orgaddruse (pd.DataFrame): OSIBANK.ORGADDRUSE (R1625)
        persaddruse (pd.DataFrame): OSIBANK.ORGADDRUSE (R1625)
        wh_addr (pd.DataFrame): OSIBANK:WH_ADDR (R1625)

    Returns:
        df (pd.DataFrame): main dataset, with primary owner's address
    """
    # Duplicate testing
    assert orgaddruse['orgnbr'].is_unique, "Duplicates"
    assert persaddruse['persnbr'].is_unique, "Duplicates"
    assert wh_addr['addrnbr'].is_unique, "Duplicates"

    # Merging
    df = pd.merge(df, orgaddruse, left_on='taxrptfororgnbr', right_on='orgnbr', how='left')
    df = pd.merge(df, persaddruse, left_on='taxrptforpersnbr', right_on='persnbr', how='left')

    # Cleaning
    df['addrnbr'] = np.where(df['addrnbr_x'].isnull(), df['addrnbr_y'], df['addrnbr_x'])
    df = df.drop(['addrnbr_x','addrnbr_y','orgnbr','persnbr'], axis=1)

    # Merge
    df = pd.merge(df, wh_addr, how='left', on='addrnbr')

    return df


def merging_insurance_tables(acctpropins: pd.DataFrame, wh_inspolicy: pd.DataFrame) -> pd.DataFrame:
    """
    Merging the insurance tables

    Args:
        acctpropins (pd.DataFrame): OSIBANK.ACCTPROPINS (R1625)
        wh_inspolicy (pd.DataFrame): OSIBANK.WH_INSPOLICY (R1625)

    Returns:
        insurance_merged (pd.DataFrame): merged insurance data

    Note:
        check with Kelly if she wants effective date from acctpropins or from wh_inspolicy
            - some other duplicate columns in there too
    """
    # Duplicate check
    assert wh_inspolicy['intrpolicynbr'].is_unique, "Duplicates found"

    # Merging
    insurance_merged = pd.merge(acctpropins, wh_inspolicy, how='left', on='intrpolicynbr')

    # Cleaning
    insurance_merged = insurance_merged.drop(['acctnbr'], axis=1)

    return insurance_merged


# Now we put it all together

def append_insurance_data_to_main(df: pd.DataFrame, insurance_data: pd.DataFrame) -> pd.DataFrame:
    """
    Left merge on main dataset (loans + property data already merged) and insurance data. This ensures loans without policies remain too.

    Args:
        df (pd.Dataframe): Core data
        insurance_data (pd.DataFrame): insurance_merged is fed in

    Returns:
        df (pd.DataFrame): data with insurance policy data. There may be duplicate acctnbr and property numbers due to multiple policies
    """
    df = pd.merge(df, insurance_data, how='left', on='propnbr')
    
    return df


