# %%
import os
import sys
from pathlib import Path

# Navigate to project root (equivalent to cd ..)
project_dir = Path(__file__).parent.parent if '__file__' in globals() else Path.cwd().parent
os.chdir(project_dir)

# Add src directory to Python path for imports
src_dir = project_dir / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# Set environment for dev testing
os.environ['REPORT_ENV'] = 'prod'

# %%

import cdutils.database.connect # type: ignore
from sqlalchemy import text # type: ignore
from datetime import datetime
from typing import Optional

# Define fetch data here using cdutils.database.connect
# There are often fetch_data.py files already in project if migrating
def fetch_data(start_date, end_date):
    """
    Main data query
    """
    query = text(f"""
    SELECT
        *
    FROM
        COCCDM.WH_RTXN a
    WHERE
        (a.RUNDATE >= TO_DATE('{start_date}', 'YYYY-MM-DD HH24:MI:SS')) AND
        (a.RUNDATE <= TO_DATE('{end_date}', 'YYYY-MM-DD HH24:MI:SS'))
    """)    
    # vieworgtaxid = text(f"""
    # SELECT
    #     *
    # FROM
    #     OSIBANK.VIEWORGTAXID a
    # """)

    queries = [
        {'key':'query', 'sql':query, 'engine':2},
        
        # {'key':'vieworgtaxid', 'sql':vieworgtaxid, 'engine':1},
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data


# %%
start_date = datetime(2025, 9, 1)
end_date = datetime(2025, 9, 30)

# %%
data = fetch_data(start_date=start_date, end_date=end_date)

# %%
df = data['query'].copy()

# %%
df

# %%
df['acctnbr'] = df['acctnbr'].astype(str)
df['rtxnnbr'] = df['rtxnnbr'].astype(str)

# %%
df.info()

# %%
df['composite_key'] = df['acctnbr'] + df['rtxnnbr']

# %%
df = df[df['rtxnstatcd'] == 'C'].copy()

# %%
df


