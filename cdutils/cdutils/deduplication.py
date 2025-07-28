# Goal is to create a nice function that can take a list of df 
from typing import List, Dict, Union
import pandas as pd

# Define argument type checking
Instruction = Dict[str, Union[pd.DataFrame, str, List[str]]]
def dedupe(df_list: List[Instruction] ) -> List[pd.DataFrame]:
    """
    Accept a list of dfs that need to be deduplicated on a specific field and return the list of dfs after cleaning has been performed
    
    Usage:
        dedupe_list = [
            {'df':result_df, 'field':'entity_name'}
        ]

        result_df = cdutils.deduplication.dedupe(dedupe_list)
        # This is automatically doing result_df[0] if there is only 1 df passed in, otherwise you can do df1, df2 and it'll define correctly
        # This allows you to extract a list of dfs cleanly
    """
    # Asserts
    results = []

    for idx, item in enumerate(df_list):
        assert 'df' in item, "Invalid argument passed in, missing df as key"
        df = item['df']
        assert isinstance(df, pd.DataFrame), f"df is not a dataframe from argument"

        if 'field' not in item and 'fields' not in item:
            raise ValueError("No field or fields passed in as argument")
        
        if 'field' in item:
            dedupe_val = item['field']
            
            assert isinstance(dedupe_val, str), "Field name is not a string passed in"
            dedupe_cols = [dedupe_val]
        else:
            dedupe_val = item['fields']
            assert isinstance(dedupe_val, list), "Fields must be a list passed in"
            dedupe_cols = dedupe_val
            for col in dedupe_cols:
                assert isinstance(col, str), "Field names need to be strings (within fields argument)"
        
        for col in dedupe_cols:
            assert col in df.columns, f"Column '{col}' not found in df"

        df_deduped = df.drop_duplicates(subset=dedupe_cols, keep='first')
        results.append(df_deduped)
    
    return results[0] if len(results) == 1 else results