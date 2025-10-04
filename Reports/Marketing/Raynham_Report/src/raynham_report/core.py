import pandas as pd
import src.config
from deltalake import DeltaTable
import cdutils.customer_dim # type: ignore
import src.raynham_report.fetch_data
import cdutils.input_cleansing # type: ignore

def filter_distinct_customers_assigned_to_n_raynham(df):
    """
    Unique customers that are assigned to branch in question
    """
    filtered_df = df[df['branchname'] == 'BCSB - NORTH RAYNHAM BRANCH'].copy()
    distinct_customers = filtered_df[['customer_id']].drop_duplicates()
    distinct_customers['eligibility'] = 'Assigned to N Raynham'
    return distinct_customers

def filter_distinct_customers_transacted_at_n_raynham(accts):
    """
    Unique accounts that have transacted at branch in question
    """
    data = src.raynham_report.fetch_data.fetch_rtxn_data()
    transacted = data['transacted'].copy()
    transacted_schema = {
        'acctnbr':'str'
    }
    transacted = cdutils.input_cleansing.cast_columns(transacted, transacted_schema)
    transacted = transacted.merge(accts, how='inner', on='acctnbr')
    distinct_customers = transacted[['customer_id']].drop_duplicates()
    distinct_customers['eligibility'] = 'Transacted at N Raynham within 90 days'

    return distinct_customers 

def filter_distinct_customer_near_branches(accts):
    """
    Unique Customers located near raynham or taunton

    Requested was within 5 mi of branch, but for simplicity, we match on primary zip codes
    """
    zip_codes = ["02767","02780"]
    filtered_df = accts[accts['primaryownerzipcd'].isin(zip_codes)]
    distinct_customers = filtered_df[['customer_id']].drop_duplicates()
    distinct_customers['eligibility'] = 'Zip Code in Raynham (02767) or Taunton (02780)'
    return distinct_customers
    

def generate_raynham_report():
    """
    Objective:

    To create a person mailing list to North raynham Branch Construction customers

    Params:

    Assigned to N Raynham
    Transacted at N Raynham within 90 days
    Address within a 5 mile radius of N. Raynham, Raynham Center, Main Office
    Owns Safe Deposit Box @ N. Raynham
    Exclusions (do we have standard exclusions for all mailings? Including common ones below)
    Customers under 18 years of age
    Deceased customers
    Charged off accounts


    Data fields:

    First name
    Last name
    Address
    City
    State
    Zip
    """

    # Pull in Base Customer Layer
    base_customer_dim = DeltaTable(src.config.SILVER / "base_customer_dim").to_pandas()

    # Pull in Active Accounts (create a clean customer_id for joining)
    accts = DeltaTable(src.config.SILVER / "account").to_pandas()

    # Assigned to Branch from Accts
    assigned = filter_distinct_customers_assigned_to_n_raynham(accts)

    # Transacted at Branch in last 90 days
    transacted = filter_distinct_customers_transacted_at_n_raynham(accts)

    # Address near Branch (zip codes)
    nearby = filter_distinct_customer_near_branches(accts)

    # Union/concat eligible criteria on cust_id
    concat_df = pd.concat([assigned, transacted, nearby], ignore_index=True)
    concat_df = concat_df.drop_duplicates(subset=['customer_id'], keep='first')

    # Inner join with base customer dim
    base_customer_dim = base_customer_dim[[
        'customer_id',
        'customer_type',
        'customer_name',
        'Active Account Owner',
        'loan_net_balance',
        'deposit_balance'
    ]].copy()
    base_customer_dim = base_customer_dim[base_customer_dim['Active Account Owner'] == "Y"].copy()
    customer_df = base_customer_dim.merge(concat_df, how='inner', on='customer_id')

    # Append primary address
    customer_address_link = DeltaTable(src.config.SILVER / "customer_address_link").to_pandas()
    customer_address_link = customer_address_link[customer_address_link['addrusecd'] == 'PRI'].copy()
    customer_address_link = customer_address_link[[
        'customer_id',
        'addrnbr'
    ]].copy()
    customer_address_link_schema = {
        'addrnbr':'str'
    }
    customer_address_link = cdutils.input_cleansing.cast_columns(customer_address_link, customer_address_link_schema)

    address = DeltaTable(src.config.SILVER / "address").to_pandas()
    address_schema = {
        'addrnbr':'str'
    }
    address = cdutils.input_cleansing.cast_columns(address, address_schema)
    address = address.drop(columns='load_timestamp_utc').copy()
    address = customer_address_link.merge(address, how='inner', on='addrnbr')

    customer_df = customer_df.merge(address, on='customer_id', how='left')

    # Need to do exclusions
    pers_dim = DeltaTable(src.config.SILVER / "pers_dim").to_pandas()
    pers_dim = pers_dim[[
        'customer_id',
        'age'
    ]].copy()
    customer_df = customer_df.merge(pers_dim, on='customer_id', how='left')
    
    # Filter out records where age < 18 and customer type = 'Person'
    customer_df = customer_df[~((customer_df['customer_type'] == 'Person') & (customer_df['age'] < 18))]

    # Append pkey
    pkey_slice = accts[['customer_id','portfolio_key']].copy()
    # Assert a customer id is not associated with multiple portfolio keys
    # There is a Many:1 relationship between customers and portfolio key.
    
    customer_df = customer_df.merge(pkey_slice, on='customer_id', how='left')


    # Append pkey
    pkey_slice = accts[['customer_id', 'portfolio_key']].copy()

    # Assert no customers are associated with multiple portfolio keys
    portfolio_key_uniques = pkey_slice.groupby('customer_id')['portfolio_key'].nunique()
    assert (portfolio_key_uniques == 1).all(), "Assertion failed: One or more customers are associated with multiple portfolio keys"

    # Deduplicate pkey_slice to handle potential multiplicity (assuming Many:1 relationship)
    pkey_slice = pkey_slice.drop_duplicates(subset='customer_id')
    customer_df = customer_df.merge(pkey_slice, on='customer_id', how='left')

    # Sort in descending order of deposit balance then loan balance, and drop duplicates on portfolio_key
    customer_df_portfolio = customer_df.sort_values(['deposit_balance', 'loan_net_balance'], ascending=[False, False]).drop_duplicates(subset=['portfolio_key'])

    # Just inspect output
    # Set column order
    # Write out
    # Done

