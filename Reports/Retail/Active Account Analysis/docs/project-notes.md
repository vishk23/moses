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

wh_org
<class 'pandas.core.frame.DataFrame'>
Index: 16911 entries, 0 to 17131
Data columns (total 23 columns):
 #   Column         Non-Null Count  Dtype         
---  ------         --------------  -----         
 0   orgnbr         16911 non-null  object        
 1   orgname        16911 non-null  object        
 2   orgtypcd       16737 non-null  object        
 3   orgtypcddesc   16737 non-null  object        
 4   taxid          13163 non-null  object        
 5   taxidtypcd     13315 non-null  object        
 6   rpt1099intyn   16911 non-null  object        
 7   privacyyn      16911 non-null  object        
 8   taxexemptyn    16911 non-null  object        
 9   cipratingcd    67 non-null     object        
 10  creditscore    1424 non-null   float64       
 11  siccd          331 non-null    object        
 12  siccddesc      331 non-null    object        
 13  sicsubcd       310 non-null    object        
 14  sicsubcddesc   307 non-null    object        
 15  naicscd        11217 non-null  object        
 16  naicscddesc    11217 non-null  object        
 17  adddate        16911 non-null  datetime64[ns]
 18  datelastmaint  16911 non-null  datetime64[ns]
 19  rundate        16911 non-null  datetime64[ns]
 20  allowpromoyn   16911 non-null  object        
 21  homeemail      2369 non-null   object        
 22  busemail       5016 non-null   object        
dtypes: datetime64[ns](3), float64(1), object(19)
memory usage: 3.1+ MB

wh_pers
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 167591 entries, 0 to 167590
Data columns (total 28 columns):
 #   Column              Non-Null Count   Dtype         
---  ------              --------------   -----         
 0   persnbr             167591 non-null  object        
 1   persname            167591 non-null  object        
 2   perssortname        167591 non-null  object        
 3   taxid               161923 non-null  object        
 4   adddate             167591 non-null  datetime64[ns]
 5   datebirth           164060 non-null  datetime64[ns]
 6   datedeath           3368 non-null    datetime64[ns]
 7   age                 164060 non-null  float64       
 8   employeeyn          167591 non-null  object        
 9   privacyyn           167591 non-null  object        
 10  cipratingcd         8 non-null       object        
 11  naicscd             191 non-null     object        
 12  naicsdesc           191 non-null     object        
 13  siccd               41 non-null      object        
 14  sicdesc             41 non-null      object        
 15  sicsubcd            20 non-null      object        
 16  sicsubdesc          20 non-null      object        
 17  creditscore         42653 non-null   object        
 18  spousepersnbr       496 non-null     float64       
 19  spousepersname      496 non-null     object        
 20  spouseperssortname  496 non-null     object        
 21  datelastmaint       167591 non-null  datetime64[ns]
 22  rundate             167591 non-null  datetime64[ns]
 23  allowpromoyn        167591 non-null  object        
 24  homeemail           86373 non-null   object        
 25  busemail            12334 non-null   object        
 26  firstname           167591 non-null  object        
 27  lastname            167591 non-null  object        
dtypes: datetime64[ns](5), float64(2), object(21)
memory usage: 35.8+ MB