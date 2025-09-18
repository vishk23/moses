# Core logic specific to project/report

import src.config
import pandas as pd
from deltalake import DeltaTable
from pathlib import Path
import cdutils.deduplication

def main_pipeline():
    # Main loan data, silver table
    TABLE_PATH = src.config.SILVER / "account"
    accts = DeltaTable(TABLE_PATH).to_pandas()

    accts = accts[[
        'acctnbr',
        'ownersortname',
        'mjaccttypcd',
        'currmiaccttypcd',
        'product',
        'curracctstatcd',
        'noteintrate',
        'notebal',
        'bookbalance',
        'branchname',
        'loanofficer',
        'contractdate',
        'datemat',
        'creditlimitamt',
        'loanlimityn',
    ]].copy()

    # Get investor data
    invr = src.loan_trial.fetch_data.fetch_invr()
    wh_invr = invr['wh_invr'].copy()
    wh_invr = wh_invr.sort_values(by='pctowned', ascending=False).copy()
    dedupe_list = [
        {'df':wh_invr, 'field':'acctnbr'}
    ]
    wh_invr = cdutils.deduplication.dedupe(dedupe_list)
    
    acctgrpinvr = invr['acctgrpinvr'].copy()
    
    wh_org = DeltaTable(src.config.BRONZE / "wh_org").to_pandas()
    wh_org = wh_org[[
        'orgnbr',
        'orgname'
    ]]
    dedupe_list = [
        {'df':wh_org, 'field':'orgnbr'}
    ]
    wh_org = cdutils.deduplication.dedupe(dedupe_list)
    wh_org['orgnbr'] = wh_org['orgnbr'].astype(str)
    wh_invr['acctgrpnbr'] = wh_invr['acctgrpnbr'].astype(str)
    acctgrpinvr['acctgrpnbr'] = wh_invr['acctgrpnbr'].astype(str)
    acctgrpinvr['invrorgnbr'] = acctgrpinvr['invrorgnbr'].astype(str)

    merged_investor = wh_invr.merge(acctgrpinvr, on='acctgrpinvr', how='left').merge(wh_org, left_on='invrorgnbr', right_on='orgnbr')
    merged_investor = merged_investor.drop(columns=['orgnbr','invrorgnbr','pctowned','acctgrpnbr']).copy()
    merged_investor['acctnbr'] = merged_investor['acctnbr'].astype(str)
    assert merged_investor['acctnbr'].is_unique, "Duplicates exist. Pre-merge of investor data to full df"
    
    merged_investor = merged_investor.rename{
        'orgname':'Investor Name'
        'originvrrate':'Orig Investor Rate'
        'currinvrrate':'Current Investor Rate'
    }

    df = df.merge(merged_investor, on='acctnbr', how='left')

    # notenextratechange (WH_ACCTCOMMON)
    # noteratechangecalpercd (WH_ACCTCOMMON)
    # rcf
    #H
