from cdutils.database import models  # db.WHAcctLoan, etc.
from cdutils.database.models import *  # Optional autocomplete

from pathlib import Path
from io import StringIO
import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import asyncio
import pandas as pd

# === Load encrypted credentials ===
env_admin_path = Path(__file__).parent / "env_admin"
os.environ['TNS_ADMIN'] = str(env_admin_path / "tns_admin")

key = (env_admin_path / "key.key").read_bytes()
cipher = Fernet(key)
decrypted_env = cipher.decrypt((env_admin_path / ".env.enc").read_bytes()).decode()
load_dotenv(stream=StringIO(decrypted_env))

# === Direct IP or TNS-based DSNs ===
username1 = os.getenv("main_username")
password1 = os.getenv("main_password")
dsn1 = os.getenv("main_dsn")

username2 = os.getenv("datamart_username")
password2 = os.getenv("datamart_password")
dsn2 = os.getenv("datamart_dsn")

connection_string1 = f'oracle+oracledb://{username1}:{password1}@{dsn1}'
connection_string2 = f'oracle+oracledb://{username2}:{password2}@10.1.102.53:24625/?service_name=r1625dm'

engine1 = create_async_engine(connection_string1, future=True)
engine2 = create_async_engine(connection_string2, future=True)

# === Core query helper ===
async def query(sql, engine=1):
    engine_obj = engine1 if engine == 1 else engine2
    async with engine_obj.connect() as conn:
        result = await conn.execute(sql)
        rows = result.fetchall()
        return pd.DataFrame(rows, columns=result.keys())

# === New: Raw SQL support ===
def run_raw_queries(queries: list[dict]) -> dict[str, pd.DataFrame]:
    """
    Usage:
        queries = [
            {
                "key": "wh_acctloan",
                "sql": text("SELECT * FROM COCCDM.WH_ACCTLOAN WHERE EFFDATE = TO_DATE('2023-12-31', 'YYYY-MM-DD')"),
                "engine": 2
            }
        ]
        result = run_raw_queries(queries)
    """
    async def run_all():
        tasks = [asyncio.create_task(query(q['sql'], q['engine'])) for q in queries]
        results = await asyncio.gather(*tasks)
        return {q['key']: df for q, df in zip(queries, results)}

    loop = asyncio.get_event_loop()
    if loop.is_running():
        return loop.run_until_complete(run_all())
    else:
        return asyncio.run(run_all())

# === SQLAlchemy Core-style query interface ===
def retrieve_data(queries, engine=1):
    """
    Accepts:
        - List of SQLAlchemy Core `select(...)` objects
        - Or: list of dicts with {'key', 'sql', 'engine'}

    Returns:
        Dict[str, pd.DataFrame]
    """
    async def run_all():
        tasks = []
        keys = []
        for q in queries:
            if isinstance(q, dict):
                keys.append(q['key'])
                tasks.append(asyncio.create_task(query(q['sql'], q['engine'])))
            else:
                try:
                    model = list(q.columns_clause_froms)[0]
                    keys.append(model.name)
                except:
                    raise ValueError("Could not infer table name from query.")
                tasks.append(asyncio.create_task(query(q, engine)))
        results = await asyncio.gather(*tasks)
        return dict(zip(keys, results))

    loop = asyncio.get_event_loop()
    if loop.is_running():
        return loop.run_until_complete(run_all())
    else:
        return asyncio.run(run_all())



#USAGE 

from sqlalchemy import select, join, and_
from cdutils.database import connect_faster as db
from datetime import date

month_end = date(2023, 12, 31)

# Create a join between two models
j = join(
    db.WHAcctLoan,
    db.WHAcctCommon,
    db.WHAcctLoan.acctnbr == db.WHAcctCommon.acctnbr
)

# Build the SQLAlchemy Core query
query = (
    select(
        db.WHAcctLoan.acctnbr,
        db.WHAcctLoan.cobal,
        db.WHAcctCommon.ownername,
        db.WHAcctCommon.curracctstatcd
    )
    .select_from(j)
    .where(
        and_(
            db.WHAcctLoan.effdate == month_end,
            db.WHAcctCommon.effdate == month_end
        )
    )
)

# Fetch as DataFrame
results = db.retrieve_data([query], engine=2)
df = results['WHAcctLoan']  # Based on left-most model

from sqlalchemy import text
from cdutils.database import connect_faster as db

month_end = '2023-12-31'

queries = [
    {
        "key": "wh_acctloan",
        "sql": text(f"""
            SELECT ACCTNBR, CURRDUEDATE, RISKRATINGCD AS Risk, COBAL
            FROM COCCDM.WH_ACCTLOAN
            WHERE EFFDATE = TO_DATE('{month_end}', 'YYYY-MM-DD')
        """),
        "engine": 2
    }
]

results = db.run_raw_queries(queries)
df = results["wh_acctloan"]
