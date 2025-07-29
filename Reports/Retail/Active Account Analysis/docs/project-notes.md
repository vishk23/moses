# 2025-07-28 (Chad Doorley)

Dave Medieros & Stephanie N have requested a dataset for the retail interns to start looking at cross sell analysis.
These would be active accounts + open agreements. 

---------------------------------------------------------------------------
ModuleNotFoundError                       Traceback (most recent call last)
Cell In[2], line 1
----> 1 import cdutils.acct_lookup_any_date.lookup_loop

File ~\Documents\gh\bcsb-prod\cdutils\cdutils\acct_lookup_any_date\lookup_loop.py:16
     12 from datetime import datetime
     14 import pandas as pd # type: ignore
---> 16 import cdutils.acct_lookup_any_date.lookup_loop.src.fetch_data # type: ignore
     17 import src.core_transform # type: ignore
     18 import cdutils.pkey_sqlite # type: ignore

ModuleNotFoundError: No module named 'cdutils.acct_lookup_any_date.lookup_loop.src'; 'cdutils.acct_lookup_any_date.lookup_loop' is not a package


Muni minors:

['CK36',
 'CK42',
 'CK18',
 'CK27',
 'CD30',
 'CD15',
 'CK21',
 'CD06',
 'CD39',
 'CK26',
 'CD49']