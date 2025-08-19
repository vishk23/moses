"""
Usage:
    import src.transformations.filters
"""
import pandas as pd # type: ignore

def filtering_down_to_relevant_fields(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reducing total columns down to ones requested

    Args:
        df (pd.DataFrame)

    Returns
        df (pd.DataFrame): Same dataset, just reduced total columns
    """
    df = df[[
        'acctnbr',
        'ownersortname',
        'text1',
        'text2',
        'cityname',
        'statecd',
        'zipcd',
        'notebal',
        'creditlimitamt',
        'origdate',
        'proptypdesc',
        'propdesc',
        'propaddr1',
        'propaddr2',
        'propcity',
        'propstate',
        'propzip',
        'instypcd',
        'instypdesc',
        'coverageamt',
        'premamt',
        'escrowyn',
        'mjaccttypcd',
        'currmiaccttypcd',
        'fdiccatcd',
        'fdiccatdesc'
        ]].copy()
    
    return df
