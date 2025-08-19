import pandas as pd # type: ignore

def credit_score_flag_creation(df: pd.DataFrame, score_floor: int, score_decrease: float) -> pd.DataFrame:
    """
    Create a dataframe with acctnbr and pass/fail flag
    There is a nested helper function utilized
    """
    def calculate_score_flag(group: pd.DataFrame) -> int:
        """ 
        Calculate the score flag for a group of rows
        """
        valid = group.dropna(subset=['Score_1', 'Prior Credit Score'])

        if valid.empty:
            return 0

        condition1 = valid['Score_1'] < score_floor
        condition2 = (valid['Prior Credit Score'] != 0) & ((valid['Score_1'] / valid['Prior Credit Score']) - 1 <= score_decrease)

        return 1 if (condition1 | condition2).any() else 0
    
    result = df.groupby('acctnbr').apply(calculate_score_flag, include_groups=False).reset_index(name='score_flag')
    
    return result
    
