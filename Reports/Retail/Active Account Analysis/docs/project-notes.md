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


 ---

 # 2025-07-29 (Chad Doorley)

I need agreements tied to active accounts.
WH_AGREEMENTS has OWNERORGNBR and OWNERPERSNBR which can be tied via WH_ALLROLES to active accounts, which are a result of my daily_acct_file df that is already available. I need this script in main.


Context on this project:
Active Account & Agreement Analysis
For Stephanie Nordberg in Retail Department

This will run monthly.

I have 2 data contracts:
- supply them with active accounts monthly basis and active agreements from WH_AGREEMENTS.

Need to filter down my df to only applicable fields (I'll do this manually) and I need to find active agreements

 ---

Looking into this:
Employee has 91 agreements (some active)
----

wh_agreement
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 401864 entries, 0 to 401863
Data columns (total 22 columns):
 #   Column                Non-Null Count   Dtype         
---  ------                --------------   -----         
 0   acctnbr               401864 non-null  int64         
 1   agreenbr              401864 non-null  int64         
 2   persnbr               401864 non-null  int64         
 3   rundate               401864 non-null  datetime64[ns]
 4   effdate               401864 non-null  datetime64[ns]
 5   inactivedate          214233 non-null  datetime64[ns]
 6   cyclewthdllimitamt    336763 non-null  object        
 7   cycledepositlimitamt  336865 non-null  object        
 8   prefix                401864 non-null  int64         
 9   cardnbr               401864 non-null  object        
 10  agreetypcd            401864 non-null  object        
 11  ownerpersnbr          349268 non-null  object        
 12  ownerorgnbr           52596 non-null   object        
 13  nextmembernbr         401864 non-null  int64         
 14  servchgacctnbr        66418 non-null   float64       
 15  nextservchgdate       52014 non-null   datetime64[ns]
 16  servchgwaiveyn        401864 non-null  object        
 17  maintchgwaiveyn       401864 non-null  object        
 18  extcardnbr            401855 non-null  object        
 19  datelastmaint         401864 non-null  datetime64[ns]
 20  agrmntnbr             401864 non-null  object        
 21  agrmntstatcd          401864 non-null  object        
dtypes: datetime64[ns](5), float64(1), int64(5), object(11)
memory usage: 67.5+ MB