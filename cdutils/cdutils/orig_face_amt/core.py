import pandas as pd
from deltalake import DeltaTable
from pathlib import Path
import cdutils.input_cleansing # type: ignore
import cdutils.orig_face_amt.fetch_data

def query_orig_face_amt():
    """
    To get original face amount, we query the historical database to get earliest effdate in COCC
    """
    # Fetch data
    data = cdutils.orig_face_amt.fetch_data.fetch_data()
    df = data['query'].copy()

    assert df['acctnbr'].is_unique, "Duplicates on acctnbr"

    # Cast datatypes
    df_schema = {
        'acctnbr':'str'
    }
    df = cdutils.input_cleansing.cast_columns(df, df_schema)

    df = df[[
        'acctnbr',
        'facevalue'
    ]].copy()

    return df

    