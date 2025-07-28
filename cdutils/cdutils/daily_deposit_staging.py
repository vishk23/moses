from pathlib import Path

import pandas as pd

import cdutils.input_cleansing

def attach_daily_deposit_fields(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add fields from daily_deposit to the dataframe that is passed in as an arguement

    Args:
        df (pd.DataFrame): Any dataframe can be passed in as long as it has the "acctnbr" field

    Returns:
        df (pd.DataFrame): Dataframe with fields from daily deposit update (staging) appended


    Tests/Asserts:
    - Test that acctnbr exists in df
    """

    # Assert that df is not None
    assert df is not None, "Dataframe must not be none"

    DAILY_DEPOSIT_PATH = Path(r"\\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Data_Analytics\Daily_Deposit_Update\Production\output")

    # Asserts that the daily deposit exists
    assert DAILY_DEPOSIT_PATH.exists(), f"Directory that houses daily deposit staging not accessible"
    assert (DAILY_DEPOSIT_PATH / "DailyDeposit_staging.xlsx").exists(), f"Daily Deposit Staging file does not exist or is not accesible"
    DAILY_DEPOSIT_PATH = DAILY_DEPOSIT_PATH / "DailyDeposit_staging.xlsx"

    # Read in daily_deposit_staging
    daily_deposit = pd.read_excel(DAILY_DEPOSIT_PATH)
    daily_deposit_schema = {
        'acctnbr': str
    }
    daily_deposit = cdutils.input_cleansing.enforce_schema(daily_deposit, daily_deposit_schema)
    
    df_schema = {
        'acctnbr': str
    }
    df = cdutils.input_cleansing.enforce_schema(df, df_schema)

    # Assert 
    assert pd.api.types.is_string_dtype(daily_deposit['acctnbr']), "acctnbr is not a string"
    assert pd.api.types.is_string_dtype(df['acctnbr']), "acctnbr is not a string"
    assert daily_deposit['acctnbr'].is_unique, "acctnbr in daily deposit update is not unique"

    daily_deposit = daily_deposit[['acctnbr','ytdavgbal','3Mo_AvgBal','TTM_AvgBal','Year Ago Balance','TTM_DAYS_OVERDRAWN','TTM_NSF_COUNT','YTD_DAYS_OVERDRAWN','YTD_NSF_COUNT']].copy()
    df = pd.merge(df, daily_deposit, on='acctnbr', how='left')

    return df

