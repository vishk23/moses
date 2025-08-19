"""
Personal Guarantor section. Will be used in conjunction with the Xactus Credit score component.

Usage:
    src.personal_guarantor
"""
from pathlib import Path

import pandas as pd # type: ignore

import cdutils.input_cleansing # type: ignore

def append_tax_id_to_pers(pers: pd.DataFrame, viewperstaxid: pd.DataFrame) -> pd.DataFrame:
    """
    Creating a pers table with SSN. This will later be added to with credit score
    """
    assert pers['persnbr'].is_unique, "Duplicates exist"
    assert viewperstaxid['persnbr'].is_unique, "Duplicates exist"

    df = pd.merge(pers, viewperstaxid, on='persnbr', how='left')

    return df

def append_credit_score(pers_data: pd.DataFrame) -> pd.DataFrame:
    """
    Inner join on taxid for the pers data
    Note: nested input file for xactus

    Args:
        pers_data (pd.DataFrame)
        
    Returns:
        df (pd.DataFrame)
    """
    INPUT_DIR = Path('./assets/xactus/xactus_output.csv')

    xactus_file = pd.read_csv(INPUT_DIR)
    xactus_file = xactus_file[['SSN','Score_1']].copy()

    # Input validation
    xactus_file_schema = {
        'SSN': float,
        'Score_1': float
    }
    
    xactus_file = cdutils.input_cleansing.enforce_schema(xactus_file, xactus_file_schema)

    assert xactus_file['SSN'].is_unique, "Duplicates exist"

    df = pd.merge(pers_data, xactus_file, left_on='taxid', right_on='SSN', how='inner')
    assert df['persnbr'].is_unique, "Duplicates exist"

    df = df.drop(columns=['SSN']).copy()
    
    return df

def allroles_with_credit_score(allroles: pd.DataFrame, pers_data: pd.DataFrame) -> pd.DataFrame:
    """
    Left joining allroles and personal guarantor data
    """
    df = pd.merge(allroles, pers_data, on='persnbr', how='left')
    df = df.dropna(subset='Score_1')

    # Create calculated field for prior credit score
    # This is the same because we just started getting scores
    df['Prior Credit Score'] = df['Score_1']
    return df



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

