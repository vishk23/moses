"""
Filtering down to the target products. Note if this system is going to be expanded to include a broader subset of the loan portfolio,
this module is where you would change it.

Usage:
    src.transformation.filtering
"""

def filter_to_target_products(df):
    """ 
    Filtering data down to products within Alerts criteria
    
    Args:
        df: loan_data
    
    Returns:
        df: loan_data after filters are applied to set the scope of Alerts system
        
    Operations:
        - currmiaccttypcd (minor) is in:
            - "CM06","CM11","CM30","CM52","CM57","CM62","CM71","CM76"
        - creditlimitamt <= $500,000
        - total household exposure <= $1,000,000
    """
    # Lines of Credit
    df = df[df['currmiaccttypcd'].isin(["CM06","CM11","CM30","CM52","CM57","CM62","CM71","CM76"])]
    # Credit Limit Amount <= $500M & Household Exposure <= $1MM
    df = df[(df['creditlimitamt'] <= 500000) & (df['Total Exposure_hhgroup'] <= 1000000)]
    return df

