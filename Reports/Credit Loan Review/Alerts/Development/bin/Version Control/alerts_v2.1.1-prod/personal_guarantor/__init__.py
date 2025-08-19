"""
Personal Guarantor section. Will be used in conjunction with the Xactus Credit score component.

Usage:
    src.personal_guarantor
"""

import pandas as pd # type: ignore

# Personal Guarantors extracted
def personal_guarantors(allroles, persaddruse, wh_addr, pers):
    """
    Personal Guarantor information is pulled from COCC and several tables are merged.
    
    Args:
        allroles: ALLROLES table (COCC)
        persaddruse: PERSADDRUSE table (COCC)
        wh_addr: WH_ADDR table (COCC)
        pers: WH_PERS table (COCC)
        
    Returns:
        df: Dataframe of personal guarantors
        
    Operations:
        - allroles table where 'acctrolecd' = 'GUAR' (guarantor role)
        - allroles where 'persnbr' is not null (this excludes organizations)
        - persaddruse where 'addrusecd' == 'PRI' (only primary address is considered)
        - left merge of allroles & persaddruse tables on 'persnbr'
        - left merge of df (merged df from earlier step) & wh_addr on 'addrnbr'
        - left merge of df & pers on 'persnbr'
        - filtered out unnecessary fields
            - keeping only ['acctnbr','persnbr','firstname','lastname','text1',
                            'cityname','statecd','zipcd']
    """
    allroles = allroles[allroles['acctrolecd'] == 'GUAR']
    allroles = allroles[allroles['persnbr'].notnull()]
    persaddruse = persaddruse[persaddruse['addrusecd'] == "PRI"]
    # Merge
    df = pd.merge(allroles, persaddruse, on='persnbr',how='left', suffixes=('_allroles','_persaddruse'))
    df = pd.merge(df, wh_addr, on='addrnbr',how='left', suffixes=('_df','_addr'))
    df = pd.merge(df, pers, on='persnbr', how='left', suffixes=('_df','_pers'))
    df = df[['acctnbr','persnbr','firstname','lastname','text1','cityname','statecd','zipcd']]
    return df

