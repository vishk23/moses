import pandas as pd
import src.config
from deltalake import DeltaTable
from pathlib import Path

def coalesce_columns(df, suffix1, suffix2):
    """
    Identifies columns with suffixes, creates a new coalesced column,
    and drops the old ones. It prioritizes the column with suffix2.
    """
    df_copy = df.copy()
    # Find all columns that have the first suffix
    cols1 = [c for c in df_copy.columns if c.endswith(suffix1)]
    
    for col1 in cols1:
        # Get the base column name and the corresponding column with the second suffix
        base_name = col1.removesuffix(suffix1)
        col2 = f"{base_name}{suffix2}"
        
        if col2 in df_copy.columns:
            # Create the new coalesced column.
            # It takes the value from col2 first, and if that is null, it takes the value from col1.
            df_copy[base_name] = df_copy[col2].fillna(df_copy[col1])
            
            # Drop the old suffixed columns
            df_copy = df_copy.drop(columns=[col1, col2])
            print(f"Coalesced '{base_name}' from '{col1}' and '{col2}'.")
            
    return df_copy


def create_silver_prop_tables():
    # Read in bronze tables for property from COCC
    TABLE_PATH = src.config.BRONZE / "wh_prop"
    prop = DeltaTable(TABLE_PATH).to_pandas()
    TABLE_PATH = src.config.BRONZE / "wh_prop2"
    prop2 = DeltaTable(TABLE_PATH).to_pandas()

    # Merge
    merged_props = pd.merge(
        prop,
        prop2,
        how='outer',
        on=['acctnbr', 'propnbr'],
        suffixes=('_prop', '_prop2') # Use clear suffixes
    )

    # Apply the function to our merged data
    coalesced_data = coalesce_columns(merged_props, suffix1='_prop', suffix2='_prop2')
    print("\nData after coalescing columns:")

    # This table just preserves the many-to-many relationship keys.
    account_property_link = coalesced_data[['acctnbr', 'propnbr']].copy()
    account_property_link = account_property_link.drop_duplicates().reset_index(drop=True)

    print(f"Created `account_property_link` table with {len(account_property_link)} unique links.")


    master_property = coalesced_data.sort_values(by='acctnbr', ascending=False)
    master_property = master_property.drop_duplicates(subset=['propnbr'], keep='first')

    # The property table should not contain the account number, as that link is now separate.
    master_property = master_property.drop(columns=['acctnbr'])
    master_property = master_property.reset_index(drop=True)

    print(f"Created master `property` table with {len(master_property)} unique properties.")
    assert master_property['propnbr'].is_unique, "propnbr is not unique in the master property table!"
    print("Assertion Passed: `propnbr` is a unique key for the property table.")


    # This field is present in both wh_prop and wh_prop2, but is incomplete in wh_prop
    master_property = master_property.drop(columns=['proptypecd']).copy()

    return account_property_link, master_property



