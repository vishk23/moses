import src.silver.customer_dim.fetch_data
import pandas as pd

def generate_customer_dim_table():
    """
    Create Customer Dim table with P+persnbr or O+orgnbr as primary key
    """
    data = src.silver.customer_dim.fetch_data.fetch_data()
    wh_pers = data['wh_pers'].copy()
    wh_org =data['wh_org'].copy()

    