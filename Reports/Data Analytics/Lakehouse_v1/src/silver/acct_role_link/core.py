import pandas as pd
import src.config
from deltalake import DeltaTable
import cdutils.customer_dim # type: ignore
import cdutils.input_cleansing # type: ignore
import cdutils.add_effdate # type: ignore

def generate_acct_role_link():
    """
    Genereate silver linking able for accounts & roles 
    """
    wh_allroles = DeltaTable(src.config.BRONZE / "wh_allroles").to_pandas()
    wh_allroles = cdutils.customer_dim.orgify(wh_allroles, 'orgnbr')
    wh_allroles = wh_allroles.rename(columns={'customer_id':'org_id'}).copy()
    wh_allroles = cdutils.customer_dim.persify(wh_allroles, 'persnbr')
    wh_allroles['customer_id'] = wh_allroles['customer_id'].fillna(wh_allroles['org_id'])
    wh_allroles = wh_allroles.drop(columns=['org_id'])

    # Enforce acctnbr type
    wh_allroles_schema = {
        'acctnbr':'str'
    }

    wh_allroles = cdutils.input_cleansing.cast_columns(wh_allroles, wh_allroles_schema)
    
    # Add effdate
    df = wh_allroles[[
        'acctnbr',
        'customer_id',
        'acctrolecd',
        'acctroledesc'
    ]].copy()
    df = cdutils.add_effdate.add_effdate(df)

    return df 