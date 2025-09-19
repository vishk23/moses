# Core logic specific to project/report

import src.config
import pandas as pd
from deltalake import DeltaTable
from pathlib import Path
import cdutils.deduplication
import src.loan_trial.fetch_data

def main_pipeline():
    # Main loan data, silver table
    TABLE_PATH = src.config.SILVER / "account"
    accts = DeltaTable(TABLE_PATH).to_pandas()

    MACRO_TYPE_MAPPING = {
            'CML': 'Loan',
            'MLN': 'Loan',
            'CNS': 'Loan',
            'MTG': 'Loan',
            'CK': 'Deposit',
            'SAV': 'Deposit',
            'TD': 'Deposit'
        }

    accts['Macro Account Type'] = accts['mjaccttypcd'].map(MACRO_TYPE_MAPPING)
    accts = accts[accts['Macro Account Type'] == 'Loan'].copy()

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
        'credlimitclatresamt',
        'nextratechg',
        'amortterm',
        'riskratingcd',
        'fdiccatcd',
        'fdiccatdesc',
        'inactivedate',
    ]].copy()

    # Get investor data
    invr = src.loan_trial.fetch_data.fetch_invr()
    wh_invr = invr['wh_invr'].copy()


    acctgrpinvr = invr['acctgrpinvr'].copy()

    wh_org = DeltaTable(src.config.BRONZE / "wh_org").to_pandas()
    wh_org = wh_org[[
        'orgnbr',
        'orgname'
    ]].copy()
    dedupe_list = [
        {'df':wh_org, 'field':'orgnbr'}
    ]
    wh_org = cdutils.deduplication.dedupe(dedupe_list).copy()
    wh_org['orgnbr'] = wh_org['orgnbr'].astype(str)
    wh_invr['acctgrpnbr'] = wh_invr['acctgrpnbr'].astype(str)
    acctgrpinvr['acctgrpnbr'] = wh_invr['acctgrpnbr'].astype(str)
    acctgrpinvr['invrorgnbr'] = acctgrpinvr['invrorgnbr'].astype(str)

    merged_investor = wh_invr.merge(acctgrpinvr, on='acctgrpnbr', how='left').merge(wh_org, left_on='invrorgnbr', right_on='orgnbr')
    merged_investor = merged_investor.sort_values(by='pctowned', ascending=False).copy()
    dedupe_list = [
        {'df':merged_investor, 'field':'acctnbr'}
    ]
    merged_investor = cdutils.deduplication.dedupe(dedupe_list).copy()
    merged_investor = merged_investor.drop(columns=['orgnbr','invrorgnbr','pctowned','acctgrpnbr']).copy()
    merged_investor['acctnbr'] = merged_investor['acctnbr'].astype(str)
    assert merged_investor['acctnbr'].is_unique, "Duplicates exist. Pre-merge of investor data to full df"

    merged_investor = merged_investor.rename(columns={
        'orgname':'Investor Name',
        'originvrrate':'Orig Investor Rate',
        'currinvrrate':'Current Investor Rate'
    }).copy()

    accts = accts.merge(merged_investor, on='acctnbr', how='left')

    # acctloan
    acctloan = DeltaTable(src.config.BRONZE / "wh_acctloan")
    acctloan = acctloan[[
        'acctnbr',
        'currduedate',
        'totalpaymentsdue',
        'totalpidue',
        'minintrate',
        'maxintrate',
        'maxratechangedown',
        'maxratechangeup',
        'ratechangerndmethcd',
        'pmtchangerndmethcd',
        'marginpct',
        'marginfixed',
        'deffeerem',
        'deffeerate',
        'defcostrem',
        'defcostrate',
        'escbal',
        'escrowdue',
        'escintrate',
        'escaccruedint',
        'esccompmth',
        'creditreporttypcd',
        'purpcd'
    ]].copy()

    acctloan['acctnbr'] = acctloan['acctnbr'].astype(str)
    assert acctloan['acctnbr'].is_unique, "Duplicates premerge accts & acctloan"
    
    accts = accts.merge(acctloan, how='left', on='acctnbr')

    # wh_loans 
    wh_loans = DeltaTable(src.config.BRONZE / "wh_loans")
    wh_loans = wh_loans[[
        'acctnbr',
        'rcf',
        'ratechangeleaddays',
        'totalpidue',
        'revolveloanyn'
    ]].copy()

    wh_loans['acctnbr'] = wh_loans['acctnbr'].astype(str)
    assert wh_loans['acctnbr'].is_unique, "Duplicates premerge accts & wh_loans"
    accts = accts.merge(wh_loans, how='left', on='acctnbr')

    # wh_acctcommon 
    wh_acctcommon = DeltaTable(src.config.BRONZE / "wh_acctcommon")
    wh_acctcommon = wh_acctcommon[[
        'acctnbr',
        'intbase',
        'intmethcd',
        'ratetypcd',
        'daysmethcd',
        'notenextratechange',
    ]].copy()

    wh_acctcommon['acctnbr'] = wh_acctcommon['acctnbr'].astype(str)
    assert wh_acctcommon['acctnbr'].is_unique, "Duplicates premerge accts & wh_acctcommon"
    accts = accts.merge(wh_acctcommon, how='left', on='acctnbr')

    acctsubacct = src.fetch_data.fetch_acctsubacct()
    acctsubacct = acctsubacct['acctsubacct'].copy()
    acctsubacct = acctsubacct.sort_values(by='effdate', ascending=False)

    dedupe_list = [
        {'df':acctsubacct, 'field':'acctsubacct'}
    ]
    acctsubacct = cdutils.deduplication.dedupe(dedupe_list).copy()
    acctsubacct = acctsubacct[[
        'acctnbr',
        'escrowcushionamt',
        'alternateescpmtamt'
    ]].copy()
    acctsubacct['acctnbr'] = acctsubacct['acctnbr'].astype(str)
    assert acctsubacct['acctnbr'].is_unique, "Duplicates premerge accts & acctsubacct"
    accts = accts.merge(acctsubacct, how='left', on='acctnbr')

    # Prop data
    property = DeltaTable(src.config.SILVER / "property").to_pandas()
    property = property[[
        'propnbr',
        'aprsvalueamt',
        'proptypcd',
        'proptypdesc',
        'propdesc',
        'propvalue',
        'owneroccupiedcd',
        'owneroccupieddesc',
        'purchaseprice',
        'purchasedate',
        'platbooknbr',
        'platbookpage',
        'floodzone',
        'floodzoneyn'
    ]].copy()

    # Link
    account_property_link = DeltaTable(src.config.SILVER / "account_property_link").to_pandas()
    account_property_link = account_property_link[[
        'acctnbr',
        'propnbr'
    ]].copy()

    property['propnbr'] = property['propnbr'].astype(str)
    assert property['propnbr'].is_unique, "Duplicates on property premerge with linking table"

    merged_prop = account_property_link.merge(property, how='left', on='propnbr')
    merged_prop = merged_prop.sort_values(by='aprsvalueamt', ascending=False)
    dedupe_list = [
        {'df':merged_prop, 'field':'acctnbr'}
    ]
    merged_prop = cdutils.deduplication.dedupe(dedupe_list).copy()
    #
    # # Insurance data for escrow
    # insurance = DeltaTable(src.config.SILVER / "insurance").to_pandas()
    # insurance = insurance[[
    #     'intrpolicynbr',
    #     'escrowyn',
    # ]].copy()
    #
    # insurance = insurance.rename(columns={
    #     'escrowyn':'Escrow Insurance'
    # }).copy()
    #
    # assert insurance['intrpolicynbr'].is_unique, "Duplicates premerge insurance and acct_prop_ins_link"
    # acct_prop_ins_link = DeltaTable(src.config.SILVER / "acct_prop_ins_link").to_pandas()
    # acct_prop_ins_link = acct_prop_ins_link[[
    #     'propnbr',
    #     'intrpolicynbr'
    # ]].copy()
    # acct_prop_ins_link = acct_prop_ins_link.drop_duplicates().reset_index(drop=True)
    #
    # insurance['intrpolicynbr'] = insurance['intrpolicynbr'].astype(str)
    # acct_prop_ins_link['propnbr'] = acct_prop_ins_link['propnbr'].astype(str)
    # acct_prop_ins_link['intrpolicynbr'] = acct_prop_ins_link['intrpolicynbr'].astype(str)
    #
    # acct_prop_ins_link = acct_prop_ins_link.merge(insurance, how='left', on='intrpolicynbr')
    # merged_prop = 

    
    merged_prop['acctnbr'] = merged_prop['acctnbr'].astype(str)
    assert merged_prop['acctnbr'].is_unique, "Duplicates premerge merged_prop and accts"
    accts = accts.merge(merged_prop, how='left', on='acctnbr')

    return accts

    # notenextratechange (WH_ACCTCOMMON)
    # noteratechangecalpercd (WH_ACCTCOMMON)
    # rcf
    #H
