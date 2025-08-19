# pkey_sqlite.py
import sqlite3
from datetime import datetime
from pathlib import Path
import os

from sqlalchemy import create_engine, inspect, text # type: ignore
import pandas as pd # type: ignore

def create_sqlite_engine(db_filename: str, use_default_dir: bool = True, base_dir: Path = None):
    """
    Create a SQLAlchemy engine to interface with sqlite db
    """
    if use_default_dir:
        assets_dir = Path('.') / 'assets'
        assets_dir.mkdir(parents=True, exist_ok=True)
        db_path = assets_dir / db_filename
    else:
        if base_dir is None:
            raise ValueError("You must provide a valid Path object when using use_default_dir=False")
        base_dir.mkdir(parents=True, exist_ok=True)
        db_path = base_dir / db_filename

    # build connection string
    connection_str = f"sqlite:///{db_path.resolve()}"
    engine = create_engine(connection_str)
    return engine

def get_most_recent_historical_key(engine, table_name: str='historical_keys') -> pd.DataFrame:
    """
    Retrieves rows from sqlite db for most recent date
    """
    inspector = inspect(engine)
    if table_name not in inspector.get_table_names():
        return None
    
    with engine.connect() as conn:

        # Get max timestamp
        max_timestamp_query = text(f"""
        SELECT
            MAX(timestamp) as timestamp
        FROM
            {table_name}
        """
        )

        result = conn.execute(max_timestamp_query)
        max_timestamp = result.scalar()

        if not max_timestamp:
            return None
        
    query = text(f"""
    SELECT
        *
    FROM
        {table_name}
    WHERE
        timestamp = '{max_timestamp}'
    """
    )
    df = pd.read_sql(query, con=engine)
    df['acctnbr'] = df['acctnbr'].astype(int)

    return df

def query_current_db(engine):
    query = text(f"""
    SELECT
        *
    FROM
        current_keys
    """)
    df = pd.read_sql(query, con=engine)
    df['acctnbr'] = df['acctnbr'].astype(int)
    return df

def write_current_run_to_current_db(df: pd.DataFrame, engine, table_name: str='current_keys'):
    """
    Update current.db
    """
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)

def append_records_to_historical_db(df: pd.DataFrame, engine, table_name: str='historical_keys'):
    """
    Append most recent run to historical db with timestamp
    """
    curr_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df['timestamp'] = curr_timestamp
    df.to_sql(table_name, con=engine, if_exists='append', index=False)


def add_pkey(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add portfolio key from the R360 process to the dataframe that is passed in as an arguement

    Args:
        df (pd.DataFrame): Any dataframe can be passed in as long as it has the "acctnbr" field

    Returns:
        df (pd.DataFrame): Dataframe with pkey appended


    Operations:
    - extract pkey from the current.db (or Data Warehouse in future implementations)
        - this is currently a sqlite.db that is updated on a daily basis to get the current groupings for all relationships
    - append pkey to the dataframe by grouping on acctnbr and doing a left join

    Tests/Asserts:
    - Test that acctnbr exists in df
    - Assert the datatypes of acctnbr are the same in both of the dataframes that are being joined
    - current.db exists (if someone moved it or the drive is offline, this will fail)
    """

    # Assert that df is not None
    assert df is not None, "Dataframe must not be none"

    DB_PATH = Path(r"\\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Data_Analytics\R360\Production\assets")

    # Asserts that the pkey database exists
    assert DB_PATH.exists(), f"Directory that houses pkey not accessible"
    assert (DB_PATH / "current.db").exists(), f"current.db does not exist or is not accesible"

    engine = create_sqlite_engine('current.db', use_default_dir=False, base_dir=DB_PATH)
    pkey_df = pd.read_sql("SELECT * FROM current_keys", con=engine)
    pkey_df['acctnbr'] = pkey_df['acctnbr'].astype(str)
    df['acctnbr'] = pkey_df['acctnbr'].astype(str)

    # Assert 
    assert pd.api.types.is_string_dtype(pkey_df['acctnbr']), "acctnbr is not a string"
    assert pd.api.types.is_string_dtype(df['acctnbr']), "acctnbr is not a string"

    df = pd.merge(df, pkey_df, on='acctnbr', how='left')

    return df

