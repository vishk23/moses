import pandas as pd
import src.config
from deltalake import DeltaTable
import cdutils.customer_dim # type: ignore
import cdutils.input_cleansing # type: ignore
import cdutils.add_effdate # type: ignore

def generate_investor_data():
    """
    Generate a cleaned investor table 
    """
    # TODO
    
    # base_customer_dim = DeltaTable(src.config.BRONZE / "base_customer_dim").to_pandas()
    # base_customer_dim = base_customer_dim[[
    #     'customer_id',
    #     'customer_name'
    # ]].copy()
    

    # wh_invr['acctgrpnbr'] = wh_invr['acctgrpnbr'].astype(str)
    # acctgrpinvr['acctgrpnbr'] = acctgrpinvr['acctgrpnbr'].astype(str)
    # acctgrpinvr['invrorgnbr'] = acctgrpinvr['invrorgnbr'].astype(str)

    # merged_investor = wh_invr.merge(acctgrpinvr, on='acctgrpnbr', how='left').merge(wh_org, left_on='invrorgnbr', right_on='orgnbr') 