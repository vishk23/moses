import pandas as pd
import src.config
from deltalake import DeltaTable
import cdutils.customer_dim.core # type: ignore

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

    # Assigned to Branch from Accts
    accts = DeltaTable(src.config.SILVER / "accounts").to_pandas()

    # Transacted at Branch in last 90 days

    # Address near Branch (zip codes)

    # Union/concat eligible criteria on cust_id

    # Inner join with base customer dim

    # Append primary address
