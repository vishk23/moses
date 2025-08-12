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