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


acct_daily_file (active_accounts)
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 89601 entries, 0 to 89600
Data columns (total 50 columns):
 #   Column                  Non-Null Count  Dtype         
---  ------                  --------------  -----         
 0   effdate                 89601 non-null  datetime64[ns]
 1   acctnbr                 89601 non-null  object        
 2   ownersortname           89601 non-null  object        
 3   product                 89601 non-null  object        
 4   noteopenamt             89601 non-null  float64       
 5   ratetypcd               71559 non-null  object        
 6   mjaccttypcd             89601 non-null  object        
 7   currmiaccttypcd         89601 non-null  object        
 8   curracctstatcd          89601 non-null  object        
 9   noteintrate             89601 non-null  float64       
 10  bookbalance             89601 non-null  float64       
 11  notebal                 89601 non-null  float64       
 12  contractdate            89600 non-null  datetime64[ns]
 13  datemat                 32936 non-null  datetime64[ns]
 14  taxrptfororgnbr         12437 non-null  float64       
 15  taxrptforpersnbr        77164 non-null  float64       
 16  loanofficer             23477 non-null  object        
 17  acctofficer             62632 non-null  object        
 18  creditlimitamt          89601 non-null  float64       
 19  origintrate             22765 non-null  object        
 20  marginfixed             23477 non-null  object        
 21  fdiccatcd               22829 non-null  object        
 22  amortterm               23477 non-null  float64       
 23  totalpctsold            89601 non-null  float64       
 24  cobal                   89601 non-null  float64       
 25  credlimitclatresamt     89601 non-null  float64       
 26  riskratingcd            2746 non-null   object        
 27  origdate                23293 non-null  datetime64[ns]
 28  currterm                23477 non-null  float64       
 29  loanidx                 23466 non-null  object        
 30  rcf                     3023 non-null   object        
 31  availbalamt             89601 non-null  float64       
 32  fdiccatdesc             22829 non-null  object        
 33  origbal                 22600 non-null  float64       
 34  loanlimityn             23477 non-null  object        
 35  Net Balance             89601 non-null  float64       
 36  Net Available           89601 non-null  float64       
 37  Net Collateral Reserve  89601 non-null  float64       
 38  Total Exposure          89601 non-null  float64       
 39  orig_ttl_loan_amt       89601 non-null  float64       
 40  portfolio_key           89601 non-null  int64         
 41  ownership_key           87104 non-null  float64       
 42  address_key             87104 non-null  float64       
 43  householdnbr            80059 non-null  float64       
 44  datelastmaint           80059 non-null  datetime64[ns]
 45  Category                23477 non-null  object        
 46  inactivedate            2557 non-null   datetime64[ns]
 47  branchname              89601 non-null  object        
 48  primaryownercity        89578 non-null  object        
 49  primaryownerstate       89554 non-null  object        
dtypes: datetime64[ns](6), float64(22), int64(1), object(21)
memory usage: 34.2+ MB


----

# 2025-10-01
python -m src.main
Starting Active Account & Agreement Analysis
Running v1.0.0-prod
Environment: prod
Output directory: \\00-da1\Home\Share\Line of Business_Shared Services\Retail Banking\Active_Account_Agreement_Analysis\output
Loading active accounts...
Loaded 89601 active accounts
Loading base data...
Loading WH_ORG...
Loaded 17093 unique organizations
Loading WH_PERS...
Loaded 169238 unique persons
Loading WH_AGREEMENTS...
Column 'agrmntnbr' not found. Creating it with default None values.
Column 'agrmntstatcd' not found. Creating it with default None values.
Found 187856 active agreements out of 406179 total
Merging in agreement type descriptions...
Adding owner names...
Building owner-agreement type matrix...
Agreement owner matrix saved to: \\00-da1\Home\Share\Line of Business_Shared Services\Retail Banking\Active_Account_Agreement_Analysis\output\Agreements\Agreement Owner Matrix October 1 2025.xlsx
Filtered active accounts saved to: \\00-da1\Home\Share\Line of Business_Shared Services\Retail Banking\Active_Account_Agreement_Analysis\output\Accounts\Active Accounts October 1 2025.xlsx

Summary:
- Unique Owners: 60791
- Agreement Types: ['Business Debit', 'Business Debit Instant Issue', 'Charge Consumer ATM', 'Charge Consumer Debit', 'Charge Instant Issue Consumer', 'Internet Banking', 'Prime T BAW ATM Card', 'Prime T BAW Consumer Debit', 'Prime T Instant Issue Consumer', 'Telephone Banking']
Complete!