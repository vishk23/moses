**Overview**: Track implementation of key sections for the BUILT report generation in `src/core.py` and related files. Update status as tasks progress; run tests via `python -m pytest tests/ -v` after changes.

- [x] **Participation Section**: Implement logic for participation data extraction and validation.  
  *Tests*: Passed all unit tests in `tests/test_core.py`.  
  *Notes*: Integrated with `fetch_data.py`; no issues.

- [x] **Inactive Date Section**: Add handling for inactive dates in asset filtering.  
  *Tests*: Passed; verified with sample data in notebooks.  
  *Notes*: Updated config in `src/config.py`.

- [x] **Add Portfolio Manager**: Include portfolio manager fields in output DataFrame.  
  *Tests*: Passed; bundle size unchanged.  
  *Notes*: Minor addition to existing pipeline.

- [x] **Controlling Person Information Section**: Fetch and merge controlling person data from SQL queries.  
  *Tests*: Pending; run after implementation.  
  *Notes*: Reference `docs/controlling_person_logic.md` for business rules.

- [x] Escrow Holdback for Resi Loans

- [ ] Fix inactive date # of Extensions to only count where creditlimitamt != 0.

Links:
https://clientexperience.getbuilt.com/project-updates

# 2025-09-04

Kickoff meeting with everyone


From hasan
```
FYI, just so we are on the same page – Tim and I discussed not having all construction loans roll into BUILT.  We will set thresholds for loan that exceed a certain dollar figure.  It could be $1MM or $2MM – I need to review the construction loan portfolio.  We don’t want smaller less complex loans in Built and eat up our CUCV (amount we can put into Built for free).  When the time comes to provide the loan data, I just want to make sure we don’t give them all construction loans.
```


# 2025-09-18

Resi:
2 residential minors
- 

we sell - disbursement of repairs
- set up schedules for disbursements


Savngs 

Escrow Reserve Holdback
- field

Chris to send me logic on resi side.


Met with Hasan/kelly a/Deva to review cml side and process
- sent through


# 2025-10-04
Need to have extract done by Mon Oct 6

Will get done. Mapped out a bunch of this in my head already, just need to build.

CML
- hard code 12 acctnbrs
    - later userfield to specify built
MTG
- chris gave me specific instructions on logic

Package into a single file
loan_type: commercial/resi

Separate pipelines but same schema (mostly), concat together

# 2025-10-05

Action plan:
1. new core.py
2. cml first
    - hard code acctnbrs
    - acct user field to specify later on
3. get all fields to match extract from silver layer (bronze if needed or source)
4. mtg data
    - look at chris logic he sent me
    - create separately with same schema
5. concat together
6. schedule send first thing in morning
    - explain I'm on PTO but will be back EOD to send to them via mimecast.
    - please send me thoughts/revisions/questions if necessary


Question for Hasan:
- once these are no longer construction and switch to PERM, they no longer are managed in BUILT correct?
    - They would just come off the extract in view

Please correct me if I'm wrong.

Need clarification on closedate whether that's contractdate or origdate
- making executive decision that it's orgidate

# 2025-10-06

FIELDS:
Loan Number

Line Of Credit Account Number
Project Reference ID
Project Type
Loan Amount

Draw Funded to Date
Close Date
Maturity Date
Interest Rate
Cost Center
Account/ GL Number 
Is Builder
Additional Reference ID

Line Of Credit Account Number
Loan Amount
Term (Months)
Revolving
Loan Maturity Date
Line of Credit Type

Product Type (Residential)

Asset Class

Renovation Product
Purpose
Retainage Percentage

Construction Start Date
Construction End Date
Appraisal Date
Appraised Value
Owner Occupied
Purpose Code
Notes

Property Address
Property City
Property State or Property Province
Property Zip or Postal Code
Property Lot Number
Property Subdivision Name
Property Type
NAICS Code
Parcel Number
Square Feet

Borrower Company Name
Borrower Admin First Name
Borrower Admin Last Name
Borrower Address
Borrower City
Borrower State or Borrower Province
Borrower Zip Code or Postal Code
Borrower Admin Email
Borrower Admin Home Phone Number
Borrower Admin Mobile Phone Number
Borrower Admin Office Phone Number

Builder Company Name
Builder Admin First Name
Builder Admin Last Name
Builder Address
Builder City
Builder State or Province
Builder Zip Code or Postal Code
Builder Admin Email
Builder Admin Home Phone Number
Builder Admin Mobile Phone Number
Builder Admin Office Phone Number

Equity Type
Equity Amount
Equity Amount Remaining
Equity Source Type
Equity Disbursement Rule

Disbursement Method
Disbursement Account Number
Disbursement Aba Number
Disbursement Payee Address
Disbursement Payee City
Disbursement Payee State
Disbursement Payee Zip Code
Disbursement Payee Bank Name
Disbursement Payee Bank Address
Disbursement Payee Bank City
Disbursement Payee Bank State
Disbursement Payee Bank Zip

Loan Administrator Email
Relationship Manager Email
Inspector Email

Title Company Company Name
Title Company Admin First Name
Title Company Admin Last Name
Title Company Address
Title Company City
Title Company State
Title Company Zip Code
Title Company Admin Office Phone Number
Title Company Admin Mobile Phone Number
Title Company Admin Home Phone Number
Title Company Admin Email


----

# 2025-10-09
BUILT notes
ACCTLOANLIMITHIST
- I can take inactive date desc (ignore the top null one)

ctrlpersnbr might hold
- there is the WH_ORGPERSROLE table that lists all people linked to these organizations

WHP Investments was a wierd case that hasan was discussing. Didn't fully track.
- earn out. More or a UI/BUILT issue for how they will map this.

Additions I'm going to make include:
- more fields that hasan sent. Refer to that email
- if an org, include ctrl persnbr (discussed above)
- inactivedate changes (orig inactive date)
    - I can count number of changes per loan number


- holdbacks should be included. I don't totally understand how this works
    - touch base with Chris/Dawn


TODO:
- get all of this to Andy tomorrow


# 2025-10-10

Available Balance
Net Available Balance (i.e. Available less sold participant portion)
Participant Available
% Sold
% Funded # Exclude, hasan had added this
Participant Purchased (i.e. who we sold to)
Last Advance Date (lastdisbursdate done)
Collateral Reserve Amount (i.e. hold on loan for interest carry, etc.)

Participations section:
    - ACCTUSERFIELDS
        - PARP - Purchased/Bought (boolean)
        - PAPU - Purchased %

GAMEPLAN:
There are a few pieces, which need to be tackled in this order:
- Participation section
    - Break out Balance, Available, Collateral Reserve for BCSB / Participating Banks
- Inactive Date Extension work
    - detailed above, we want # of extensions + original extension date
- Controlling person information
    - This will be account owner if primary owner is a person not an org
- Add portfolio manager


----
Here is the merged_investor df I have put together. It only applies to the loans that were participated out (sold to other banks).

I need to clean this up and join back to accounts to create a simple complementary df to attach to the extract.
- this will show when we participate a loan out, who the banks involved are.

<class 'pandas.core.frame.DataFrame'>
RangeIndex: 94 entries, 0 to 93
Data columns (total 8 columns):
 #   Column            Non-Null Count  Dtype 
---  ------            --------------  ----- 
 0   acctnbr           94 non-null     string
 1   acctgrpnbr        94 non-null     object
 2   invrstatcd        94 non-null     object
 3   pctowned          94 non-null     object
 4   originvrrate      94 non-null     object
 5   currinvrrate      94 non-null     object
 6   customer_id       94 non-null     object
 7   Participant Name  94 non-null     object
dtypes: object(7), string(1)
memory usage: 6.0+ KB

merged_investor.describe()
acctnbr,acctgrpnbr,invrstatcd,pctowned,originvrrate,currinvrrate,customer_id,Participant Name
94,94,94,94,94,94,94,94
89,49,3,25,63,62,19,19
150936915,16138,SOLD,0.06,0.06,O1009133,SOUTHSTATE BANK NA
2,22,56,32,8,5,26,26

 The invrstatcd has been filter to only = 'SOLD'.

---

pct_sold_loans = pct_sold_loans.merge(accts, how='inner', on='acctnbr')

---

Way to explain this:
totalpctsold
totalpctbought

if notebal = 100,000
sold loan (.4)
- BCSB: 60,000
- Other bank: 40,000

if bought (.4):
- BCSB: notebal = 100,000
- Total loan = 100,000 / .4 = 250,000
- Other: 150,000

---

Can use this to give them participation info directly if they want it
- individual names of participating banks

pct_sold_loans = pct_sold_loans.merge(accts, how='inner', on='acctnbr')


def generate_inactive_df(acctloanlimithist):
    """
    This takes the ACCTLOANLIMITHIST data as a raw source.

    Transforms and produces a df with 1 acctnbr per row with # of extensions (number of unique inactive dates)
    """
    # TODO

    # First drop records where inactivedate is null
    # make sure inactivedate is datetime
    # Group by acctnbr and create count nunique of inactive dates and also orig_inactive date (which would be the earliest in chronological)

    # return df


Need to create a Participation Type:
Bought/Sold/None. it will look if totalpctsold is not null = Sold, else if totalpctbought is not null = Bought, else null
<class 'pandas.core.frame.DataFrame'>
Index: 20 entries, 0 to 48
Data columns (total 49 columns):
 #   Column                    Non-Null Count  Dtype         
---  ------                    --------------  -----         
 0   effdate                   20 non-null     datetime64[us]
 1   acctnbr                   20 non-null     string        
 2   MACRO TYPE                20 non-null     object        
 3   creditlimitamt            20 non-null     float64       
 4   loanlimityn               20 non-null     object        
 5   notebal                   20 non-null     float64       
 6   Net Balance               20 non-null     float64       
 7   availbalamt               20 non-null     float64       
 8   Net Available             20 non-null     float64       
 9   credlimitclatresamt       20 non-null     float64       
 10  Net Collateral Reserve    20 non-null     float64       
 11  totalpctsold              20 non-null     float64       
 12  origdate                  20 non-null     datetime64[us]
 13  datemat                   20 non-null     datetime64[us]
 14  inactivedate              20 non-null     datetime64[us]
 15  noteintrate               20 non-null     float64       
 16  mjaccttypcd               20 non-null     object        
 17  currmiaccttypcd           20 non-null     object        
 18  product                   20 non-null     object        
 19  customer_id               20 non-null     object        
 20  Primary Borrower Name     20 non-null     object        
 21  lastdisbursdate           17 non-null     datetime64[us]
 22  Lead_Participant          7 non-null      object        
 23  Total_Participants        7 non-null      float64       
 24  totalpctbought            5 non-null      float64       
 25  lead_bank                 5 non-null      object        
 26  Full_creditlimitamt       20 non-null     float64       
 27  Full_notebal              20 non-null     float64       
 28  Full_availbalamt          20 non-null     float64       
 29  Full_credlimitclatresamt  20 non-null     float64       
 30  num_extensions            20 non-null     int64         
 31  orig_inactive_date        20 non-null     datetime64[ns]
 32  Primary Borrower Address  20 non-null     object        
 33  Primary Borrower City     20 non-null     object        
 34  Primary Borrower State    20 non-null     object        
 35  Primary Borrower Zip      20 non-null     object        
 36  propnbr                   20 non-null     string        
 37  aprsvalueamt              15 non-null     float64       
 38  aprsdate                  15 non-null     datetime64[us]
 39  proptypdesc               20 non-null     object        
 40  addrnbr                   20 non-null     string        
 41  owneroccupiedcd           8 non-null      object        
 42  owneroccupieddesc         8 non-null      object        
 43  nbrofunits                14 non-null     float64       
 44  Property Address          20 non-null     object        
 45  Property City             20 non-null     object        
 46  Property State            20 non-null     object        
 47  Primary Zip               20 non-null     object        
 48  asset_class               20 non-null     object        
dtypes: datetime64[ns](1), datetime64[us](6), float64(17), int64(1), object(21), string(3)
memory usage: 7.8+ KB

---

Append PM field

---

Also need to get phone & email

PERSPHONEVIEW
ORGPERSVIEW

We would query & get the raw date then run through cdutils.customer_dim.orgify and persify functions to turn persnbr or orgnbr into customer_id (with O+orgnbr, P+persnbr)



def fetch_phoneview():
    """
    Main data query
    """
    persphoneview = text("""
    SELECT
        a.PERSNBR,
        a.FULLPHONENBR
    FROM
        OSIBANK.PERSPHONEVIEW a
    WHERE
        a.PHONEUSECD IN ('PER','BUS')
    """)  

    orgphoneview = text("""
    SELECT
        a.PERSNBR,
        a.FULLPHONENBR
    FROM
        OSIBANK.ORGPHONEVIEW a
    WHERE
        a.PHONEUSECD = 'BUS'
    """)  


    queries = [
        {'key':'persphoneview', 'sql':persphoneview, 'engine':1},
        {'key':'orgphoneview', 'sql':orgphoneview, 'engine':1},
        
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data


---

Trying to sketch out the best way to add in this controlling person info. 

I think we should always have control person:
- firstname
- lastname
- work phone
- work email

This will be the primary borrower if it's a person or it'll be controlling person of an org

accts is main df and it will have customer_id (which is the primary borrower)
- if it has an O as prefix of customerid it's an Organization
- if it has an P as prefix, it's a person

The steps to get to this are to identify primary borrower customer_id
- if org
    - find ctrlpersnbr and attached the data associated from that pers
- if pers
    - attach data directly to that customer_id

Going one step lower to actually get the info once we have customer_id of controlling person
- pers_dim has:
    - firstname
    - lastname
    - busemail
- we can query the persphoneview to get this directly
    - src.config.BRONZE / "persphoneview"


We should primarily update the lakehouse to get everything that we need in there and easy to query.


----

The new challenge is that I get an error in the pivoting of PER and BUS on pers_dim phone number section because the table was not unique for phone numbers and there was no date last maintained field to sort in descending to figure out what is the up to date field.

We move upstream to get directly from PERSPHONE and ORGPHONE instead of PERSPHONEVIEW and ORGPHONEVIEW.

Context:
PERSPHONE
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 295406 entries, 0 to 295405
Data columns (total 12 columns):
 #   Column                Non-Null Count   Dtype         
---  ------                --------------   -----         
 0   persnbr               295406 non-null  int64         
 1   phoneusecd            295406 non-null  object        
 2   phoneseq              295406 non-null  int64         
 3   areacd                295387 non-null  object        
 4   exchange              295363 non-null  object        
 5   phonenbr              295363 non-null  object        
 6   phoneexten            236 non-null     object        
 7   datelastmaint         295406 non-null  datetime64[ns]
 8   foreignphonenbr       43 non-null      object        
 9   ctrycd                295406 non-null  object        
 10  preferredyn           295406 non-null  object        
 11  phonelastupdateddate  83563 non-null   datetime64[ns]
dtypes: datetime64[ns](2), int64(2), object(8)
memory usage: 27.0+ MB

Need to concat areacd + exchange + phonenbr to get phonenbr. We will infer workphonenbr or persphonenbr from phoneusecd

---

accts is the main df. At the spot in src.built.core where I have the TODO for the ctrlperson section, we need to implement the below:

I think we should always have control person:
- firstname
- lastname
- work phone
- work email

This will be the primary borrower (customer_id already in the accts) if it's a person or it'll be controlling person of an org

accts is main df and it will have customer_id (which is the primary borrower)
- if it has an O as prefix of customerid it's an Organization
- if it has an P as prefix, it's a person

The steps to get to this are to identify primary borrower customer_id
- if org
    - find ctrlpersnbr and attached the data associated from that pers
        - can pull in org_dim from src.config.SILVER / "org_dim" and there is ctrlpersnbr to get customer_id of the controlling person
- if pers already (P as prefix)
    - that is the ctrlpersnbr already

Going one step lower to actually get the info once we have customer_id of controlling person
- pers_dim has:
    - firstname
    - lastname
    - busemail
    - workphonenbr

Ending columns should be clear that this is CtrlPerson (prefix this and make the field names readable)


---

Ok so ctrlpersnbr didn't work property. Mostly good, but there are just nulls where we actually have contorlling people, we need to get from elsewhere.

Need to get from this table:

import cdutils.database.connect # type: ignore
from sqlalchemy import text # type: ignore
from datetime import datetime
from typing import Optional

# Define fetch data here using cdutils.database.connect
# There are often fetch_data.py files already in project if migrating
def fetch_data():
    """
    Main data query
    """
    query = text("""
    SELECT
        *
    FROM
        OSIBANK.WH_ORGPERSROLE a
    """)    

    queries = [
        {'key':'query', 'sql':query, 'engine':1},
        
        # {'key':'vieworgtaxid', 'sql':vieworgtaxid, 'engine':1},
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data

wh_orgpersrole
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 13675 entries, 0 to 13674
Data columns (total 9 columns):
 #   Column         Non-Null Count  Dtype         
---  ------         --------------  -----         
 0   orgnbr         13675 non-null  int64         
 1   rundate        13675 non-null  datetime64[ns]
 2   persrolecd     13500 non-null  object        
 3   persnbr        13500 non-null  float64       
 4   persroledesc   13500 non-null  object        
 5   orgrolecd      175 non-null    object        
 6   subjorgnbr     175 non-null    float64       
 7   orgroledesc    175 non-null    object        
 8   datelastmaint  13675 non-null  datetime64[ns]
dtypes: datetime64[ns](2), float64(2), int64(1), object(4)
memory usage: 961.7+ KB

We actually just want to replace ctrlpersnbr with the persnbr (needs to be 'persified' by cdutils.customer_dim.persify).
So customer_id in accts could be an organization 'O'+orgnbr and we already have this mostly handled, but we should filter this wh_orgpersrole to where persrolecd = 'CNOW' (controlling owner) which serves the same purpose as ctrl persnbr, but our org isn't maintaining ctrl persnbr so we need to use this other one. We can just link this persnbr (understand how persify works by looking at other examples in this file) to get link to pers_dim and the rest of that controlling person section will be the same. Just a swap out.

---

Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Commercial Lending\BUILT\src\main.py", line 29, in <module>
    main()
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Commercial Lending\BUILT\src\main.py", line 19, in main
    df = src.built.core.generate_built_extract()
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Commercial Lending\BUILT\src\built\core.py", line 505, in generate_built_extract
    cml = transform(cml)
          ^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Commercial Lending\BUILT\src\built\core.py", line 379, in transform
    accts = accts.merge(temp_pers, on='persnbr', how='left')
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\frame.py", line 10859, in merge
    return merge(
           ^^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\reshape\merge.py", line 170, in merge
    op = _MergeOperation(
         ^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\reshape\merge.py", line 794, in __init__
    ) = self._get_merge_keys()
        ^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\reshape\merge.py", line 1298, in _get_merge_keys
    right_keys.append(right._get_label_or_level_values(rk))
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\generic.py", line 1914, in _get_label_or_level_values        
    raise KeyError(key)
KeyError: 'persnbr'

Final output df:
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 39 entries, 0 to 38
Data columns (total 56 columns):
 #   Column                    Non-Null Count  Dtype
---  ------                    --------------  -----
 0   effdate                   39 non-null     datetime64[us]
 1   acctnbr                   39 non-null     string        
 2   MACRO TYPE                39 non-null     object        
 3   creditlimitamt            39 non-null     float64       
 4   loanlimityn               39 non-null     object        
 5   notebal                   39 non-null     float64
 6   Net Balance               39 non-null     float64
 7   availbalamt               39 non-null     float64
 8   Net Available             39 non-null     float64
 9   credlimitclatresamt       39 non-null     float64
 10  Net Collateral Reserve    39 non-null     float64
 11  totalpctsold              39 non-null     float64
 12  origdate                  39 non-null     datetime64[us]
 13  datemat                   39 non-null     datetime64[us]
 14  inactivedate              39 non-null     datetime64[us]
 15  noteintrate               39 non-null     float64
 16  mjaccttypcd               39 non-null     object
 17  currmiaccttypcd           39 non-null     object
 18  product                   39 non-null     object
 19  customer_id               39 non-null     object
 20  Primary Borrower Name     39 non-null     object
 21  loanofficer               39 non-null     object
 22  Portfolio Manager         20 non-null     object
 23  lastdisbursdate           32 non-null     datetime64[us]
 24  Lead_Participant          7 non-null      object
 25  Total_Participants        7 non-null      float64
 26  totalpctbought            5 non-null      float64
 27  lead_bank                 5 non-null      object
 28  Full_creditlimitamt       39 non-null     float64
 29  Full_notebal              39 non-null     float64
 30  Full_availbalamt          39 non-null     float64
 31  Full_credlimitclatresamt  39 non-null     float64
 32  num_extensions            39 non-null     int64
 33  orig_inactive_date        39 non-null     datetime64[ns]
 34  Primary Borrower Address  39 non-null     object
 35  Primary Borrower City     39 non-null     object
 36  Primary Borrower State    39 non-null     object
 37  Primary Borrower Zip      39 non-null     object
 38  CtrlPerson_FirstName      35 non-null     object
 39  CtrlPerson_LastName       35 non-null     object
 40  CtrlPerson_WorkEmail      2 non-null      object
 41  CtrlPerson_WorkPhone      28 non-null     object
 42  propnbr                   39 non-null     string
 43  aprsvalueamt              34 non-null     float64
 44  aprsdate                  34 non-null     datetime64[us]
 45  proptypdesc               39 non-null     object
 46  addrnbr                   39 non-null     string
 47  owneroccupiedcd           27 non-null     object
 48  owneroccupieddesc         27 non-null     object
 49  nbrofunits                33 non-null     float64
 50  Property Address          39 non-null     object
 51  Property City             39 non-null     object
 52  Property State            39 non-null     object
 53  Primary Zip               39 non-null     object
 54  asset_class               39 non-null     object
 55  Participation Type        39 non-null     object
dtypes: datetime64[ns](1), datetime64[us](6), float64(17), int64(1), object(28), string(3)
memory usage: 17.2+ KB


---
# 2025-10-12

holdback

acctbalhist
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 357 entries, 0 to 356
Data columns (total 5 columns):
 #   Column         Non-Null Count  Dtype         
---  ------         --------------  -----         
 0   acctnbr        357 non-null    int64         
 1   subacctnbr     357 non-null    int64         
 2   effdate        357 non-null    datetime64[ns]
 3   balamt         357 non-null    object        
 4   datelastmaint  357 non-null    datetime64[ns]
dtypes: datetime64[ns](2), int64(2), object(1)
memory usage: 14.1+ KB

acctsubacct
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 427 entries, 0 to 426
Data columns (total 16 columns):
 #   Column               Non-Null Count  Dtype         
---  ------               --------------  -----         
 0   acctnbr              427 non-null    int64         
 1   subacctnbr           427 non-null    int64         
 2   balcatcd             427 non-null    object        
 3   baltypcd             427 non-null    object        
 4   nextrcvbnbr          427 non-null    int64         
 5   nextallotnbr         427 non-null    int64         
 6   datelastmaint        427 non-null    datetime64[ns]
 7   nextearningdate      0 non-null      object        
 8   origbal              17 non-null     object        
 9   nextratechangedate   0 non-null      object        
 10  earningscalperiodcd  0 non-null      object        
 11  oddfreqnextduedate   0 non-null      object        
 12  nextpayablenbr       0 non-null      object        
 13  partagreenbr         0 non-null      object        
 14  nextaccrualdate      0 non-null      object        
 15  accrualcalperiodcd   0 non-null      object        
dtypes: datetime64[ns](1), int64(4), object(11)
memory usage: 53.5+ KB