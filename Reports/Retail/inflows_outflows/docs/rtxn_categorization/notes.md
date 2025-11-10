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


---


wh_rtxn

<class 'pandas.core.frame.DataFrame'>
RangeIndex: 83913 entries, 0 to 83912
Data columns (total 45 columns):
 #   Column              Non-Null Count  Dtype                           
---  ------              --------------  -----                           
 0   acctnbr             83913 non-null  int64                           
 1   rtxnnbr             83913 non-null  int64                           
 2   rtxnstatcd          83913 non-null  object                          
 3   effdate             83913 non-null  datetime64[us]                  
 4   rundate             83913 non-null  datetime64[us]                  
 5   parentrtxnnbr       4463 non-null   float64                         
 6   applnbr             79194 non-null  float64                         
 7   applname            79194 non-null  object                          
 8   rtxntypcd           83913 non-null  object                          
 9   rtxntypdesc         83913 non-null  object                          
 10  holdacctnbr         5925 non-null   float64                         
 11  currrtxnstatcd      83913 non-null  object                          
 12  tranamt             83913 non-null  object                          
 13  origpostdate        83913 non-null  datetime64[us]                  
 14  rtxnreasoncd        0 non-null      object                          
 15  actdatetime         83913 non-null  datetime64[us]                  
 16  origpersnbr         8937 non-null   float64                         
 17  apprpersnbr         333 non-null    float64                         
 18  cashboxnbr          81631 non-null  float64                         
 19  extrtxndesctext     58435 non-null  object                          
 20  origntwknodenbr     40328 non-null  float64                         
 21  orgnbr              40328 non-null  float64                         
 22  allotnbr            155 non-null    float64                         
 23  reversalrtxnnbr     13 non-null     float64                         
 24  rtmttxncatcd        0 non-null      object                          
 25  rtmtyr              22 non-null     float64                         
 26  rtxnsourcecd        83770 non-null  object                          
 27  intrrtxndesctext    6633 non-null   object                          
 28  postdate            83913 non-null  datetime64[us]                  
 29  checknbr            5757 non-null   float64                         
 30  datelastmaint       83913 non-null  datetime64[us]                  
 31  agreenbr            41245 non-null  float64                         
 32  tran_source_key     0 non-null      object                          
 33  membernbr           41245 non-null  float64                         
 34  networkcd           41447 non-null  object                          
 35  cardtxnnbr          41447 non-null  float64                         
 36  otcpersnbr          2577 non-null   float64                         
 37  payto               97 non-null     object                          
 38  parentacctnbr       4463 non-null   float64                         
 39  txnfeeamt           41245 non-null  object                          
 40  sourceid            21169 non-null  object                          
 41  companyentrydesc    15481 non-null  object                          
 42  otcorgnbr           0 non-null      object                          
 43  load_timestamp_utc  83913 non-null  datetime64[us, UTC]             
 44  eastern_time        83913 non-null  datetime64[us, America/New_York]
dtypes: datetime64[us, America/New_York](1), datetime64[us, UTC](1), datetime64[us](6), float64(17), int64(2), object(18)
memory usage: 28.8+ MB