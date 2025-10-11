import src.config
from deltalake import DeltaTable
import pandas as pd
import cdutils.input_cleansing # type: ignore
import src.built.fetch_data
import cdutils.customer_dim # type: ignore

def add_asset_class(df, mapping_dict):
    """
    Appends a new field 'asset_class' to df based on highest appraised values by property type
    """
    # Coerce aprsvalueamt to numeric for safety
    df['aprsvalueamt'] = pd.to_numeric(df['aprsvalueamt'], errors='coerce')
    
    def get_asset_class(group):
        # Strip whitespace from proptypdesc for matching
        group = group.copy()
        group['proptypdesc'] = group['proptypdesc'].str.strip()
        
        grouped_sum = group.groupby('proptypdesc')['aprsvalueamt'].sum()
        if grouped_sum.empty or grouped_sum.isna().all():
            return None

        asset_type = grouped_sum.idxmax()
        return asset_type
    
    raw_asset_classes = df.groupby('acctnbr').apply(get_asset_class, include_groups=False).to_dict()
    
    # Create reverse mapping: proptypdesc -> category
    reverse_mapping = {}
    for category, subtypes in mapping_dict.items():
        for subtype in subtypes:
            # Strip whitespace here too for consistency
            reverse_mapping[subtype.strip()] = category
    
    # Map acctnbr to proptypdesc, then to category (with fallback 'Other' for unmapped subtypes)
    df['asset_class'] = (
        df['acctnbr']
        .map(raw_asset_classes)
        .map(lambda x: reverse_mapping.get(x.strip() if pd.notna(x) else None, 'Other') if pd.notna(x) else 'No Data')
    )
    return df

def fetch_cml():
    """
    CML piece of BUILT extract
    """
    acctnbrs = [
        "151038843",
        "151193118",
        "151208305",
        "151167189",
        "151207620",
        "151095041",
        "151068098",
        "151068684",
        "151158766",
        "150443887",
        "150969031",
        "151173897",
    ].copy()

    accts = DeltaTable(src.config.SILVER / "account").to_pandas()

    # Filter to hasan defined acctnbrs for now
    accts = accts[accts['acctnbr'].isin(acctnbrs)].copy()
    accts['MACRO TYPE'] = 'Commercial'
    return accts 

def fetch_resi():
    """
    Resi piece of BUILT extract
    """
    accts = DeltaTable(src.config.SILVER / "account").to_pandas()

    # Filter to Resi Construction loans
    # TODO: Add in the holdback logic 
    resi_definite = ["MG01","MG64"]
    accts = accts[accts['currmiaccttypcd'].isin(resi_definite)]

    accts['MACRO TYPE'] = 'Residential'
    return accts

def generate_participation_sold_detail():
    """
    Generates the participation sold detail DataFrame.
    """
    # Get investor data
    invr = src.built.fetch_data.fetch_invr()
    wh_invr = invr['wh_invr'].copy()
    acctgrpinvr = invr['acctgrpinvr'].copy()

    # Load and process base_customer_dim
    base_customer_dim = DeltaTable(src.config.SILVER / "base_customer_dim").to_pandas()
    base_customer_dim = base_customer_dim[['customer_id', 'customer_name']].copy()

    # Type conversions
    wh_invr['acctgrpnbr'] = wh_invr['acctgrpnbr'].astype(str)
    acctgrpinvr['acctgrpnbr'] = acctgrpinvr['acctgrpnbr'].astype(str)

    # Apply orgify
    acctgrpinvr = cdutils.customer_dim.orgify(acctgrpinvr, 'invrorgnbr')

    # Assertions (removed in function for production, but can be added if needed)
    # assert acctgrpinvr['acctgrpnbr'].is_unique, "Dupes"

    # Merges
    merged_investor = wh_invr.merge(acctgrpinvr, on='acctgrpnbr', how='left').merge(
        base_customer_dim, on='customer_id', how='left'
    )

    # Filter for sold status
    merged_investor = merged_investor[merged_investor['invrstatcd'] == 'SOLD'].copy()

    # Drop column
    merged_investor = merged_investor.drop(columns=['datelastmaint']).copy()

    # Rename column
    merged_investor = merged_investor.rename(columns={
        'customer_name': 'Participant Name'
    }).copy()

    # Cast columns
    merged_investor_schema = {
        'acctnbr': 'str'
    }
    merged_investor = cdutils.input_cleansing.cast_columns(merged_investor, merged_investor_schema)

    # Filter to required columns
    merged_investor = merged_investor[[
        'acctnbr',
        'pctowned',
        'Participant Name'
    ]].copy()

    # Convert pctowned to numeric
    merged_investor['pctowned'] = pd.to_numeric(merged_investor['pctowned'])

    return merged_investor

def generate_inactive_df(acctloanlimithist):
    """
    This takes the ACCTLOANLIMITHIST data as a raw source.

    Transforms and produces a df with 1 acctnbr per row with # of extensions (number of unique inactive dates - 1) # TODO
    """


    # First drop records where inactivedate is null
    df = acctloanlimithist.dropna(subset=['inactivedate']).copy()

    df_schema = {
        'acctnbr':'str'
    }
    df = cdutils.input_cleansing.cast_columns(df, df_schema)
    # Make sure inactivedate is datetime
    df['inactivedate'] = pd.to_datetime(df['inactivedate'])

    # Group by acctnbr and create count nunique of inactive dates and also orig_inactive date (which would be the earliest in chronological)
    result = df.groupby('acctnbr').agg(
        num_extensions=('inactivedate', lambda x: x.nunique() - 1),
        orig_inactive_date=('inactivedate', 'min')
    ).reset_index()

    return result
    

def transform(accts):
    accts = accts[[
        'effdate', # Effective date of data
        'acctnbr', # Loan Number
        'MACRO TYPE', # CML/Resi
        'creditlimitamt', # Loan Amount - this will go to 0 if it switches to Perm
        'loanlimityn', # LOC Type (Y/N)
        'notebal', # Draw Funded to Date
        'Net Balance', # BCSB Net Balance
        'availbalamt',
        'Net Available',
        'credlimitclatresamt',
        'Net Collateral Reserve',
        'totalpctsold',
        # 'contractdate', # Date loan closed. Opted to use orig date below, but check with Hasan/Dawn
        'origdate', # Date loan hit core system (Close Date)
        'datemat', # Maturity Date (full loan)
        'inactivedate', # Inactive Date (LOC type product expires) - For BUILT purposes this would be Maturity Date I believe
        # Create calculated field for term (Months) between inactivedate and origdate
        'noteintrate', # Interest Rate (Current)
        'mjaccttypcd', # Major code
        'currmiaccttypcd', # Minor code (1:1 match with product)
        'product', # Product Type
        # Asset class, calculated from proptypdesc mode with appraised values
        # All prop date requested
        # Appraisal info
        # Owner occ
        # Borrower info
        'customer_id',
        'ownersortname'
    ]].copy()

    accts = accts.rename(columns={
        'ownersortname':'Primary Borrower Name'
    }).copy()

    # Append last advance date (lastdisbursdate from wh_loans)
    wh_loans = DeltaTable(src.config.BRONZE / "wh_loans").to_pandas()
    wh_loans = wh_loans[[
        'acctnbr',
        'lastdisbursdate'
    ]].copy()
    wh_loans_schema = {
        'acctnbr':'str',
    }

    wh_loans = cdutils.input_cleansing.cast_columns(wh_loans, wh_loans_schema)

    accts = accts.merge(wh_loans, on='acctnbr', how='left')

    # Participation info
    pct_sold_loans = generate_participation_sold_detail()

    # Group by acctnbr
    grouped_pct_sold_loans = (
        pct_sold_loans
        .groupby('acctnbr')
        .agg(
            Lead_Participant=('Participant Name', 'first'),  # First 'Participant Name' as Lead Participant
            Total_Participants=('Participant Name', 'nunique')  # Number of unique 'Participant Name'
        )
        .reset_index()  # Reset index to keep acctnbr as a column
    )

    # Merge with accts on acctnbr using left join
    accts = accts.merge(grouped_pct_sold_loans, on='acctnbr', how='left')

    # Assert that acctnbr is unique in accts
    assert accts['acctnbr'].is_unique, "acctnbr is not unique in accts"    

    wh_acctuserfields = DeltaTable(src.config.BRONZE / "wh_acctuserfields").to_pandas()
    papu = wh_acctuserfields[wh_acctuserfields['acctuserfieldcd'] == 'PAPU'].copy()
    parp = wh_acctuserfields[wh_acctuserfields['acctuserfieldcd'] == 'PARP'].copy()

    # assert both papu & parp ['acctnbr'].is_unique, "Dupes"

    papu_schema = {
        'acctnbr':'str'
    }
    papu = cdutils.input_cleansing.cast_columns(papu, papu_schema)

    parp_schema = {
        'acctnbr':'str'
    }
    parp = cdutils.input_cleansing.cast_columns(parp, parp_schema)

    # Filter down both to just df[['acctnbr','acctuserfieldvalue']]
    papu = papu[['acctnbr', 'acctuserfieldvalue']].copy()
    parp = parp[['acctnbr', 'acctuserfieldvalue']].copy()

    # Name acctuserfieldvalue accordingly
    papu = papu.rename(columns={'acctuserfieldvalue': 'totalpctbought'})
    parp = parp.rename(columns={'acctuserfieldvalue': 'lead_bank'})

    # Left join papu to accts on acctnbr, adding totalpctbought
    accts = accts.merge(papu, on='acctnbr', how='left')

    # Left join parp to accts on acctnbr, adding lead_bank
    accts = accts.merge(parp, on='acctnbr', how='left')   
    
    # Clean totalpctbought: remove '%' if present, convert to numeric, and divide by 100 if > 1 (assuming >1 means percentage like 44.76 for 44.76%, else leave as 0-1)
    accts['totalpctbought'] = pd.to_numeric(accts['totalpctbought'].str.replace('%', ''), errors='coerce')
    mask_pct = accts['totalpctbought'] > 1
    accts.loc[mask_pct, 'totalpctbought'] = accts.loc[mask_pct, 'totalpctbought'] / 100

    # Assert that the base fields are numeric for the calculation
    fields_to_full = ['creditlimitamt', 'notebal', 'availbalamt', 'credlimitclatresamt']
    for field in fields_to_full:
        assert pd.api.types.is_numeric_dtype(accts[field]), f"'{field}' must be numeric"

    # Create Full_ versions of the fields
    for field in fields_to_full:
        full_field = f'Full_{field}'
        accts[full_field] = accts[field]
        mask_not_null = accts['totalpctbought'].notna()
        accts.loc[mask_not_null, full_field] = accts.loc[mask_not_null, field] / accts.loc[mask_not_null, 'totalpctbought']
    
    # Inactive date additional fields for # extensions and orig inactivedate
    raw_data = src.built.fetch_data.fetch_inactive_date_data()
    acctloanlimithist = raw_data['acctloanlimithist'].copy()

    inactive_df = generate_inactive_df(acctloanlimithist)
    accts = accts.merge(inactive_df, on='acctnbr', how='left')
    
    

    # Controlling person section
    # TODO


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
    address = address.drop(columns=['load_timestamp_utc']).copy()
    address = customer_address_link.merge(address, how='inner', on='addrnbr')
    address = address.drop(columns=['addrnbr']).copy()

    address = address.rename(columns={
        'Full_Street_Address':'Primary Borrower Address',
        'cityname':'Primary Borrower City',
        'statecd':'Primary Borrower State',
        'zipcd':'Primary Borrower Zip',
    }).copy()
    accts = accts.merge(address, how='left', on='customer_id')

    accts_schema = {
        'acctnbr':'str'
    }
    accts = cdutils.input_cleansing.cast_columns(accts, accts_schema)

    acct_prop_link = DeltaTable(src.config.SILVER / "account_property_link").to_pandas()

    acct_prop_link_schema = {
        'acctnbr':'str',
        'propnbr':'str'
    }

    acct_prop_link = cdutils.input_cleansing.cast_columns(acct_prop_link, acct_prop_link_schema)
    acct_prop_link = acct_prop_link[[
        'acctnbr',
        'propnbr'
    ]].copy()

    # Property
    property = DeltaTable(src.config.SILVER / "property").to_pandas()
    prop_schema = {
        'propnbr':'str',
        'addrnbr':'str'
    }

    property = cdutils.input_cleansing.cast_columns(property, prop_schema)

    # Filter down to applicable columns
    property = property[[
        'propnbr',
        'aprsvalueamt',
        'aprsdate',
        'proptypdesc',
        'addrnbr',
        'owneroccupiedcd',
        'owneroccupieddesc',
        'nbrofunits',
    ]].copy()

    # Merge
    accts = accts.merge(acct_prop_link, on='acctnbr', how='left')
    accts = accts.merge(property, on='propnbr', how='left')

    address = DeltaTable(src.config.SILVER / "address").to_pandas()
    address_schema = {
        'addrnbr':'str'
    }
    address = cdutils.input_cleansing.cast_columns(address, address_schema)

    address = address.drop(columns='load_timestamp_utc').copy()
    address = address.rename(columns={
        'Full_Street_Address':'Property Address',
        'cityname':'Property City',
        'statecd':'Property State',
        'zipcd':'Primary Zip',
    }).copy()

    accts = accts.merge(address, on='addrnbr', how='left')

    # Append asset class
    # Property type grouping configuration
    PROPERTY_TYPE_GROUPS = {
        'Autobody/Gas Station': ['Autobody/Gas Station','Gas Station and Convenience St','Auto-Truck Repair','Car Wash'],
        'Retail': ['Retail - Big Box Store','Shopping Plaza','Strip Plaza','General Retail','Dealership'],
        'Hospitality': ['Hotel/Motel','Hospitality/Event Space','Assisted Living'],
        'Recreation': ['Outdoor Recreation','Indoor Recreational','Golf Course','Marina'],
        'Industrial': ['Manufacturing','Warehouse','Industrial','Seafood Processing Plant','Solar Farm'],
        'Land': ['Land - Unimproved','Land - Improved','Parking Lot'],
        'Mixed Use': ['Mixed Use (Retail/Office)','Mixed Use (Retail/Residential)','Mixed Use (Office/Residential)'],
        'Multi Family': ['Apartment Building','Multi Family'],
        'General Office': ['Office - Professional','Office- General'],
        'Medical Office': ['Office - Medical'],
        'Restaurant': ['Restaurant'],
        'Residential': ['1-4 Fam Res - Non Own Occ','1 Family Residential - Own Occ','2 Family Residential - Own Occ','Condominium'],
        'Storage': ['Self Storage'],
        'Educational': ['Educational Facilities','Day Care'],
        'Religious': ['Church'],
        'Vehicles': ['Vehicle - Business','Boat'],
        'Other': ['Commercial - Other','Real Estate - Business','Real Estate - Bus&Bus Assets','Real Estate - Personal & Bus','Real Estate - Pers&Bus Assets','All Business Assets','Bus Assets w/Accts Receivable','UCC - ABA','UCC- Equipment','Assignment of Leases/Rents','General Contractor','Outdoor Dealers','Marketable Securities','SBA Loan','Funeral Home','Savings - Partially Secured','Passbook/Savings Secured']
    }
    accts = add_asset_class(accts, mapping_dict=PROPERTY_TYPE_GROUPS)
    accts = accts[~(accts['addrnbr'].isnull())].copy()

    return accts

    # Participation data can be separate or in there
    # INVR fields maybe, could just leave off for this cycle


def generate_built_extract():
    """
    Full built extract
    """
    cml = fetch_cml()
    resi = fetch_resi()

    cml = transform(cml)
    resi = transform(resi)

    concat_df = pd.concat([cml, resi], ignore_index=True)
    return concat_df



