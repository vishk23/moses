# %%
import cdutils.database.connect # type: ignore
from sqlalchemy import text # type: ignore
import cdutils.deduplication # type: ignore
import cdutils.input_cleansing # type: ignore
import numpy as np
import pandas as pd
import re


def fetch_data():
    """
    Main data query
    """
    wh_acctcommon = text(f"""
    SELECT
        a.OWNERSORTNAME,
        a.LOANOFFICER,
        a.ACCTOFFICER,
        a.ACCTNBR
    FROM
        OSIBANK.WH_ACCTCOMMON a
    WHERE
        (a.CURRACCTSTATCD IN ('ACT','NPFM','DORM'))
        AND (a.MJACCTTYPCD IN ('CML','MLN','CK','SAV','TD'))
        AND (a.CURRMIACCTTYPCD != 'CI07')
    """)

    wh_allroles = text(f"""
    SELECT
        *
    FROM
        OSIBANK.WH_ALLROLES a
    WHERE
        a.ACCTROLECD in ('OWN', 'GUAR', 'LNCO', 'Tax Owner','Tax Signator','SIGN')
    """)

    wh_org = text(f"""
    SELECT
        *
    FROM
        OSIBANK.WH_ORG a
    """)

    wh_pers = text(f"""
    SELECT
        *
    FROM
        OSIBANK.WH_PERS a
    """)

    queries = [
        {'key':'wh_acctcommon', 'sql':wh_acctcommon, 'engine':1},
        {'key':'wh_allroles', 'sql':wh_allroles, 'engine':1},
        {'key':'wh_org', 'sql':wh_org, 'engine':1},
        {'key':'wh_pers', 'sql':wh_pers, 'engine':1},
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data

def create_officer_df():
    # %%
    data = fetch_data()

    # %%
    wh_acctcommon = data['wh_acctcommon'].copy()
    wh_allroles = data['wh_allroles'].copy()
    wh_org = data['wh_org'].copy()
    wh_pers = data['wh_pers'].copy()

    # %%
    # We no longer have to do this because we filter on DB level
    # wh_allroles = wh_allroles[wh_allroles['acctrolecd'].isin(['OWN', 'GUAR', 'LNCO', 'Tax Owner'])].copy()

    # %%
    wh_allroles

    # %%
    wh_allroles_schema = {
        'acctnbr':'str'
    }

    wh_acctcommon_schema = {
        'acctnbr':'str'
    }

    wh_allroles = cdutils.input_cleansing.enforce_schema(wh_allroles, wh_allroles_schema)
    wh_acctcommon = cdutils.input_cleansing.enforce_schema(wh_acctcommon, wh_acctcommon_schema)


    # %%

    # %%
    merged_df = pd.merge(wh_allroles, wh_acctcommon, on='acctnbr', how='left')

    # %%
    merged_df

    # %%

    # %%
    dedupe_list = [
        {'df':wh_org, 'field':'orgnbr'},
        {'df':wh_pers, 'field':'persnbr'}
    ]

    # %%
    wh_org_clean, wh_pers_clean = cdutils.deduplication.dedupe(dedupe_list)

    # %%
    wh_org_clean

    # %%
    wh_pers_clean

    # %%
    assert wh_org_clean['orgnbr'].is_unique, "Fail"
    assert wh_pers_clean['persnbr'].is_unique, "Fail"


    # %%
    wh_org_clean = wh_org_clean[[
        'orgnbr',
        'orgname'
    ]].copy()

    wh_pers_clean = wh_pers_clean[[
        'persnbr',
        'persname'
    ]].copy()

    # %%
    merged_df = pd.merge(merged_df, wh_org_clean, on='orgnbr', how='left')

    # %%
    merged_df = pd.merge(merged_df, wh_pers_clean, on='persnbr', how='left')

    # %%
    merged_df

    # %%


    # %%
    merged_df['customer_name'] = np.where(merged_df['persname'].isnull(), merged_df['orgname'], merged_df['persname'])

    merged_df = merged_df.dropna(subset='loanofficer')


    def clean_customer_name(name):
        """
        Clean a customer name by removing middle initials and suffixes to enable better joining.
        
        Examples:
            "Stephen P. Blaze" -> "Stephen Blaze"
            "John Q. Public" -> "John Public"
            "Mary Jane Smith JR" -> "Mary Jane Smith"
            "Robert A. Johnson JR." -> "Robert Johnson"
            "J.P. Morgan" -> "J.P. Morgan" (multiple initials, leave as is)
        
        Args:
            name (str): The customer name to clean
            
        Returns:
            str: The cleaned customer name with middle initials and suffixes removed
        """
        if not isinstance(name, str) or not name.strip():
            return name
        
        # Remove extra whitespace and normalize
        name = ' '.join(name.split())
        
        # Common suffixes to remove (case-insensitive matching)
        suffixes = ['JR', 'JR.', 'SR', 'SR.', 'II', 'III', 'IV', 'V']
        
        # Remove suffixes from the end
        for suffix in suffixes:
            # Check for suffix at the end (case-insensitive)
            if name.upper().endswith(' ' + suffix):
                name = name[:-len(' ' + suffix)].strip()
                break
        
        # Only process names that look like people (not businesses)
        # Skip if it contains business indicators
        business_indicators = ['LLC', 'LLP', 'INC', 'CORP', 'CORPORATION', 'LTD', 'LIMITED',
                            'CO', 'COMPANY', 'TRUST', 'ESTATE', 'FOUNDATION', 'FUND',
                            'REALTY', 'CONSTRUCTION', 'SERVICES', 'GROUP', 'ASSOCIATES',
                            'ENTERPRISES', 'SOLUTIONS', 'SYSTEMS', 'TECHNOLOGIES',
                            'HOLDINGS', 'PROPERTIES', 'MANAGEMENT', 'CONSULTING',
                            'PARTNERSHIP', 'PARTNERS', 'INVESTMENTS', 'CAPITAL',
                            'VENTURES', 'DEVELOPMENT', 'BUILDERS', 'CONTRACTORS',
                            'MORTGAGE', 'FINANCIAL', 'INSURANCE', 'AGENCY', 'FIRM']
        
        name_upper = name.upper()
        if any(indicator in name_upper for indicator in business_indicators):
            return name  # Don't modify business names
        
        # Pattern to match person names: First name + Middle Initial + Last name
        # Only matches if it looks like: "FirstName MiddleInitial LastName" (3 parts total)
        # This avoids matching business names like "N B Vision Realty"
        parts = name.split()
        
        if len(parts) == 3:
            first_name, middle_part, last_name = parts
            
            # Only remove middle initial if:
            # 1. Middle part is a single letter with optional period
            # 2. First and last names look like typical person names (start with capital, reasonable length)
            if (len(middle_part.replace('.', '')) == 1 and 
                middle_part[0].isupper() and
                len(first_name) > 1 and first_name[0].isupper() and
                len(last_name) > 1 and last_name[0].isupper()):
                return f"{first_name} {last_name}"
        
        # If no middle initial pattern found, return the name (already suffix-cleaned)
        return name
    def normalize_customer_names(df, customer_column='customer_name'):
        """
        Normalize customer names in a DataFrame by removing middle initials.
        
        Args:
            df (pd.DataFrame): The DataFrame containing customer names
            customer_column (str): The name of the column containing customer names
            
        Returns:
            pd.DataFrame: DataFrame with normalized customer names
        """
        if df is None or df.empty:
            return df
        
        if customer_column not in df.columns:
            raise ValueError(f"Column '{customer_column}' not found in DataFrame")
        
        # Create a copy to avoid modifying the original
        df_normalized = df.copy()
        
        # Apply the cleaning function to the customer name column
        df_normalized[customer_column] = df_normalized[customer_column].apply(clean_customer_name)
        
        return df_normalized
    merged_df = normalize_customer_names(merged_df)

    # %%
    # merged_df.info()

    # %%
    # Function to get mode, handling cases where there might be multiple modes
    def get_mode(series):
        series_clean = series.dropna()
        if len(series_clean) == 0:
            return None
        
        # Get unique values first
        unique_values = pd.Series(series_clean.unique())
        mode_result = unique_values.mode()
        
        # Return first mode if multiple modes exist
        return mode_result.iloc[0] if len(mode_result) > 0 else None
    # Group and calculate mode
    rel_entity_data_grouped = merged_df.groupby('customer_name').agg({
        'loanofficer': get_mode,
    }).reset_index()

    rel_entity_data_grouped = rel_entity_data_grouped.rename(columns={
        'loanofficer':'Loan Officer_related',
    }).copy()

    # %%
    rel_entity_data_grouped = rel_entity_data_grouped.dropna(subset='Loan Officer_related').copy()

    # %%
    return rel_entity_data_grouped

    # %%



