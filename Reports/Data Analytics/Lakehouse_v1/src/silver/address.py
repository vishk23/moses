import pandas as pd
import numpy as np
from pathlib import Path
from deltalake import write_deltalake, DeltaTable
import src.config

# %%
def create_full_street_address(df):
    """
    Processes a list of raw address records and returns a cleaned list.
    """

    STREET_TYPES = {
        'street', 'apartment number','building number', 'suite number', 'room number'
    }
    POBOX_TYPE = 'post office box number'

    # Step A: Extract both street parts AND po box parts into temporary columns
    for i in [1, 2, 3]:
        text_col = f'text{i}'
        type_col = f'addrlinetypdesc{i}'
        
        # Condition for street parts
        is_street_part = df[type_col].str.lower().isin(STREET_TYPES).fillna(False)
        df[f'street_part{i}'] = df[text_col].where(is_street_part)
        
        # Condition for PO Box parts
        is_pobox_part = (df[type_col].str.lower() == POBOX_TYPE).fillna(False)
        df[f'pobox_part{i}'] = df[text_col].where(is_pobox_part)


    # Step B: Combine the parts into two separate, complete address strings
    street_parts = ['street_part1', 'street_part2', 'street_part3']
    pobox_parts = ['pobox_part1', 'pobox_part2', 'pobox_part3']

    df['combined_street'] = df[street_parts].apply(
        lambda row: ' '.join(row.dropna().astype(str)), axis=1
    )
    df['combined_pobox'] = df[pobox_parts].apply(
        lambda row: ' '.join(row.dropna().astype(str)), axis=1
    )

    # Step C: Apply the final rule: Use Street, but if it's empty, use PO Box.
    # First, replace empty strings '' in the street column with NaN so .fillna() works
    df['combined_street'] = df['combined_street'].replace('', np.nan)

    # Now, use .fillna() to populate empty street addresses with the po box value
    df['Full_Street_Address'] = df['combined_street'].fillna(df['combined_pobox'])


    # --- 3. Finalizing the Extract ---

    # Create the final, clean DataFrame with user-friendly column names
    df_clean = df[[
        'addrnbr',
        'Full_Street_Address',
        'cityname',
        'statecd',
        'zipcd'
    ]].copy()

    return df_clean 

def generate_address():
    WH_ADDR = src.config.BRONZE / "wh_addr"
    df = DeltaTable(WH_ADDR).to_pandas()
    df_transformed = create_full_street_address(df)
    return df_transformed
