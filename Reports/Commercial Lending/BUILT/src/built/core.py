import src.config
from deltalake import DeltaTable
import pandas as pd
import cdutils.input_cleansing # type: ignore

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

def transform(accts):
    accts = accts[[
        'effdate', # Effective date of data
        'acctnbr', # Loan Number
        'MACRO TYPE', # CML/Resi
        'creditlimitamt', # Loan Amount - this will go to 0 if it switches to Perm
        'loanlimityn', # LOC Type (Y/N)
        'notebal', # Draw Funded to Date
        'Net Balance', # BCSB Net Balance
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
    # TODO

    # Inactive date additional fields for # extensions and orig inactivedate
    # TODO

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



