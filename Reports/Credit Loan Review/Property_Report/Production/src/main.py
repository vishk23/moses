# %%
"""
Main Entry Point
"""
from pathlib import Path
from typing import List
from datetime import datetime

import pandas as pd # type: ignore

import src.fetch_data # type: ignore
import src.core_transform # type: ignore
import cdutils.pkey_sqlite # type: ignore
import cdutils.hhnbr # type: ignore
import src.output_to_excel
import cdutils.loans.calculations # type: ignore
import cdutils.inactive_date # type: ignore
import cdutils.distribution # type: ignore
from src._version import __version__






def main(production_flag: bool=False):
    if production_flag:
        BASE_PATH = Path(r'\\00-DA1\Home\Share\Line of Business_Shared Services')
        assert "prod" in __version__, (f"Cannot run in production mode without 'prod' in the __version__")
    else:
        BASE_PATH = Path('.')

    data = src.fetch_data.fetch_data()

    # # # Core transformation pipeline
    raw_data = src.core_transform.main_pipeline(data)

    # Raw data with pkey appended
    raw_data = cdutils.pkey_sqlite.add_pkey(raw_data)
    raw_data = cdutils.pkey_sqlite.add_ownership_key(raw_data)
    raw_data = cdutils.pkey_sqlite.add_address_key(raw_data)

    # Append household number
    househldacct = data['househldacct'].copy()
    raw_data = cdutils.hhnbr.add_hh_nbr(raw_data, househldacct)

    # Categorize loans (if it's a deposit or other type of account, it will just return null)
    loan_category_df = cdutils.loans.calculations.categorize_loans(raw_data)
    loan_category_df = loan_category_df[['acctnbr','Category']].copy()
    df = pd.merge(raw_data, loan_category_df, on='acctnbr', how='left')


    df = cdutils.inactive_date.append_inactive_date(df)

    # %%
    df = df[df['Category'].isin(['CRE','C&I','HOA'])].copy()

    # %%

    # %%
    prop_data = src.fetch_data.prop_data()

    # %%
    prop = prop_data['wh_prop'].copy()
    prop2 = prop_data['wh_prop2'].copy()

    # %%
    # assert prop['propnbr'].is_unique, "Duplicates"

    # %%
    # assert prop2['propnbr'].is_unique, "Duplicates"

    # %%
    prop_schema = {
        "propnbr":"str",
        "acctnbr":"str"
    }

    prop2_schema = {
        "propnbr":"str",
        "acctnbr":"str"
    }

    prop = cdutils.input_cleansing.enforce_schema(prop, prop_schema)
    prop2 = cdutils.input_cleansing.enforce_schema(prop2, prop2_schema)


    # %%
    props = pd.merge(
        prop, 
        prop2, 
        on=['acctnbr','propnbr'],
        how='outer',
        suffixes=('_prop','_prop2'),
        indicator=True
    )

    # %%
    props['_merge'].value_counts(dropna=False)



    # %%
    df_merged = pd.merge(df, props, on='acctnbr',how='left', suffixes=('_acct','_prop'), indicator=False)


    # %%
    prop_groups = {
        'Autobody/Gas Station': ['Autobody/Gas Station','Gas Station and Convenience St','Auto-Truck Repair'],
        'Other': ['Other','Commercial - Other'],
        'Retail': ['Retail - Big Box Store','Shopping Plaza','Strip Plaza','Dry Cleaner/Laundromat','General Retail'],
        'Hospitality': ['Hotel/Motel','Hospitality/Event Space'],
        'Recreation': ['Outdoor Recreation','Indoor Recreational'],
        'Industrial': ['Manufacturing','Warehouse'],
        'Land': ['Land - Unimproved','Land - Improved'],
        'Mixed Use': ['Mixed Use (Retail/Office)','Mixed Use (Retail/Residential)','Mixed Use (Office/Residential)'],
        'Multi Family': ['Apartment Building'],
        'General Office': ['Office - Professional','Office- General'],
        'Medical Office': ['Office - Medical'],
        'Restaurant': ['Restaurant']
    }
    proptype_mapping = {code: group for group, codes in prop_groups.items() for code in codes}
    df_merged['Cleaned PropType'] = df_merged['proptypdesc'].map(proptype_mapping).fillna(df_merged['proptypdesc'])

    # %%

    # %%
    type_totals = (
        df_merged.groupby(['acctnbr','Cleaned PropType'], as_index=False, dropna=False).agg(tot_appraisal=('aprsvalueamt','sum'))
    )
    idx = type_totals.groupby('acctnbr')['tot_appraisal'].idxmax()
    top_type = type_totals.loc[idx]


    # %%
    result = pd.merge(df, top_type, on='acctnbr', how='left')

    # %%

    # %%
    type_totals = (
        df_merged.groupby(['acctnbr','proptypdesc'], as_index=False, dropna=False).agg(tot_appraisal=('aprsvalueamt','sum'))
    )
    idx = type_totals.groupby('acctnbr')['tot_appraisal'].idxmax()
    top_type = type_totals.loc[idx]

    # %%
    top_type

    # %%
    result = pd.merge(result, top_type, on='acctnbr', how='left')

    # %%
    result['Cleaned PropType'].value_counts(dropna=False)


    # %%
    result = result[[
        'acctnbr',
        'product',
        'riskratingcd',
        'ownersortname',
        'loanofficer',
        'noteintrate',
        'origdate',
        'datemat',
        'inactivedate',
        'notebal',
        'creditlimitamt',
        'Net Balance',
        'Net Available',
        'Net Collateral Reserve',
        'Total Exposure',
        'orig_ttl_loan_amt',
        'fdiccatdesc',
        'Category',
        'Cleaned PropType',
        'tot_appraisal_x',
        'proptypdesc',
        'tot_appraisal_y'
    ]].copy()

    # %%
    result

    # %%
    result = result.rename(columns={
        'tot_appraisal_x':'tot_appraisal_cleaned',
        'tot_appraisal_y':'tot_appraisal_proptypdesc'
    }).copy()

    result['tot_appraisal_cleaned'] = pd.to_numeric(result['tot_appraisal_cleaned'])
    result['tot_appraisal_proptypdesc'] = pd.to_numeric(result['tot_appraisal_cleaned'])

    # %%
    result
    # %%
    # Output to excel (raw data)
    OUTPUT_PATH = BASE_PATH / Path('./output/cml_property_report.xlsx')
    result.to_excel(OUTPUT_PATH, sheet_name='Sheet1', index=False)

    # Format excel
    src.output_to_excel.format_excel_file(OUTPUT_PATH)

    # Distribution
    recipients = [
        # "Sean.Cartwright@bcsbmail.com",
        # "Linda.Sternfelt@bcsbmail.com",
        # "Paul.Kocak@bcsbmail.com"
        "chad.doorley@bcsbmail.com"
    ]
    bcc_recipients = [
        "chad.doorley@bcsbmail.com",
        "businessintelligence@bcsbmail.com"
    ]
    subject = f"CML Property Report" 
    body = "Hi, \n\nAttached is the Monthly CML Property Report. If you have any questions, please reach out to BusinessIntelligence@bcsbmail.com \n\nThanks!"
    attachment_paths = [OUTPUT_PATH]
    cdutils.distribution.email_out(recipients, bcc_recipients, subject, body, attachment_paths)


if __name__ == '__main__':
    print(f"Starting [{__version__}]")
    # main(production_flag=True)
    main()
    print("Complete!")




