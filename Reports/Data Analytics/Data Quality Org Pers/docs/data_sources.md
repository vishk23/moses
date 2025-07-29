### Data Schema

#### Primary Tables
- **WH_PERS**: Person table
  - Primary Key: `persnbr`
- **WH_ORG**: Organization table
  - Primary Key: `orgnbr`

#### Tax ID View Tables (Updated Data)
- **VIEWORGTAXID**: Updated organization tax information
  - `orgnbr` (FK to WH_ORG)
  - `taxidtypcd` (updated tax ID type codes)
  - `taxid` (updated tax ID values)
  - **Processing**: Left joined early in pipeline to update WH_ORG tax fields where matches exist

- **VIEWPERSTAXID**: Updated person tax information  
  - `persnbr` (FK to WH_PERS)
  - `taxid` (updated tax ID values)
  - **Processing**: Left joined early in pipeline to update WH_PERS tax fields where matches exist

#### Address Linking Tables
- **ORGADDRUSE**: Organization address relationships
  - `orgnbr` (FK to WH_ORG)
  - `addrnbr` (FK to WH_ADDR)
  - `addrusecd` (filter: only 'PRI' records)

- **PERSADDRUSE**: Person address relationships
  - `persnbr` (FK to WH_PERS)
  - `addrnbr` (FK to WH_ADDR)
  - `addrusecd` (filter: only 'PRI' records)

#### Address Reference Table
- **WH_ADDR**: Address master table
  - Primary Key: `addrnbr`
  - Address fields:
    - `text1`, `text2`, `text3` (address lines)
    - `cityname`
    - `statecd`
    - `zipcd`, `zipsuf`
  - Metadata fields:
    - `addrlinetypdesc1`, `addrlinetypcd1` (type description/code for text1)
    - `addrlinetypdesc2`, `addrlinetypcd2` (type description/code for text2)
    - `addrlinetypdesc3`, `addrlinetypcd3` (type description/code for text3)

#### Account and Role Tables
- **acct_df**: Active account dataframe (imported via function)
  - Current snapshot of active customers (ACT/DORM/NPFM accounts)
  - Key fields:
    - `acctnbr`
    - `customername`
    - `product`
    - `major`
    - `loanofficer`
    - `acctofficer`
    - `balance`
    - `total_exposure`
    - `portfolio_key`
    - Additional reporting fields

- **WH_ALLROLES**: Account role relationships
  - Links accounts to persons and organizations
  - Fields:
    - `acctnbr` (FK to acct_df)
    - `orgnbr` (FK to WH_ORG)
    - `persnbr` (FK to WH_PERS)
    - `acctrolecd`
    - `acctroledesc` (description of acctrolecd)
  - Join later on with acct_df to filter down: Only records with active accounts from acct_df

## Processing Workflow

### Tax ID Update Phase (Early in Pipeline)
1. **Organization Tax Updates**: If `VIEWORGTAXID` table is available, perform left join with `WH_ORG` on `orgnbr` to update `taxid` and `taxidtypcd` fields where matches exist
2. **Person Tax Updates**: If `VIEWPERSTAXID` table is available, perform left join with `WH_PERS` on `persnbr` to update `taxid` field where matches exist
3. **Validation**: Both view tables are validated for duplicate keys before merging
4. **Null Safety**: Null values in view tables do not overwrite existing data

### Standard Pipeline (After Tax Updates)
1. Merge organizations/persons with address information
2. Filter to active accounts only
3. Apply additional business logic and transformations


## Raw Table Data Schema & Data Types when pulled directly from DB
data['wh_org'].info()

<class 'pandas.core.frame.DataFrame'>
RangeIndex: 17105 entries, 0 to 17104
Data columns (total 23 columns):
 #   Column            Non-Null Count  Dtype         
---  ------            --------------  -----         
 0   orgnbr            17105 non-null  int64         
 1   orgname           17105 non-null  object        
 2   orgtypcd          16930 non-null  object        
 3   orgtypcddesc      16930 non-null  object        
 4   taxid             13365 non-null  object        
 5   taxidtypcd        13516 non-null  object        
 6   rpt1099intyn      17105 non-null  object        
 7   privacycyn        17105 non-null  object        
 8   taxexemptyn       17105 non-null  object        
 9   cipratingcd       67 non-null     object        
10   creditscore       1644 non-null   float64       
11   siccd             331 non-null    object        
12   siccddesc         331 non-null    object        
13   sicsubcd          331 non-null    object        
14   sicsubcddesc      308 non-null    object        
15   naicscd           11415 non-null  object        
16   naicscddesc       11415 non-null  object        
17   adddate           17105 non-null  datetime64[ns]
18   datelastmaint     17105 non-null  datetime64[ns]
19   rundate           17105 non-null  datetime64[ns]
20   allowpromoyn      17105 non-null  object        
21   homeemail         2385 non-null   object        
22   busemail          5058 non-null   object        
dtypes: datetime64 , float64(1), int64(1), object(18)
memory usage: 3.0+ MB


data['wh_pers'].info()

<class 'pandas.core.frame.DataFrame'>
RangeIndex: 167287 entries, 0 to 167286
Data columns (total 26 columns):
 #   Column                Non-Null Count   Dtype         
---  ------                --------------   -----         
 0   persnbr               167287 non-null  int64         
 1   persname              167287 non-null  object        
 2   perssortname          167287 non-null  object        
 3   taxid                 161627 non-null  object        
 4   adddate               167287 non-null  datetime64[ns]
 5   datebirth             163765 non-null  datetime64[ns]
 6   datedeath             3358 non-null    datetime64[ns]
 7   age                   163765 non-null  float64       
 8   employeeyn            167287 non-null  object        
 9   privacycyn            167287 non-null  object        
10   cipratingcd           8 non-null      object        
11   naicscd               196 non-null    object        
12   naicscdesc            196 non-null    object        
13   siccd                 41 non-null     object        
14   sicdesc               41 non-null     object        
15   sicsubcd              20 non-null     object        
16   sicsubdesc            20 non-null     object        
17   creditscore           42470 non-null  float64       
18   spousepersnbr         496 non-null    int64         
19   spousepersname        496 non-null    object        
20   spouseperssortname    496 non-null    object        
21   datelastmaint         167287 non-null  datetime64[ns]
22   rundate               167287 non-null  datetime64[ns]
23   allowpromoyn          167287 non-null  object        
24   homeemail             86139 non-null  object        
25   busemail              12327 non-null  object        
dtypes: datetime64 , float64(2), int64(1), object(18)
memory usage: 33.2+ MB

data['orgaddruse'].info()

<class 'pandas.core.frame.DataFrame'>
RangeIndex: 34081 entries, 0 to 34080
Data columns (total 13 columns):
 #   Column            Non-Null Count  Dtype         
---  ------            --------------  -----         
 0   orgnbr            34081 non-null  int64         
 1   addrusecd         34081 non-null  object        
 2   addrnbr           34081 non-null  int64         
 3   startdate         6 non-null      datetime64[ns]
 4   stopdate          5 non-null      datetime64[ns]
 5   inactivedate      0 non-null      object        
 6   effdate           34081 non-null  datetime64[ns]
 7   occupancydate     0 non-null      object        
 8   startmonthcd      2 non-null      object        
 9   startdaynbr       2 non-null      float64       
10   stopmonthcd       2 non-null      object        
11   stopdaynbr        2 non-null      float64       
12   datelastmaint     34081 non-null  datetime64[ns]
dtypes: datetime64 , float64(2), int64(2), object(5)
memory usage: 3.4+ MB

data['persaddruse'].info()

<class 'pandas.core.frame.DataFrame'>
RangeIndex: 328789 entries, 0 to 328788
Data columns (total 13 columns):
 #   Column            Non-Null Count  Dtype         
---  ------            --------------  -----         
 0   persnbr           328789 non-null  int64         
 1   addrusecd         328789 non-null  object        
 2   addrnbr           328789 non-null  int64         
 3   startdate         161 non-null    datetime64[ns]
 4   stopdate          94 non-null     datetime64[ns]
 5   inactivedate      0 non-null      object        
 6   effdate           328789 non-null  datetime64[ns]
 7   occupancydate     0 non-null      object        
 8   startmonthcd      35 non-null     object        
 9   startdaynbr       35 non-null     float64       
10   stopmonthcd       35 non-null     object        
11   stopdaynbr        35 non-null     float64       
12   datelastmaint     328789 non-null  datetime64[ns]
dtypes: datetime64 , float64(2), int64(2), object(5)
memory usage: 32.6+ MB

wh_allroles.info()

<class 'pandas.core.frame.DataFrame'>
RangeIndex: 769284 entries, 0 to 769283
Data columns (total 8 columns):
 #   Column         Non-Null Count  Dtype         
---  ------         --------------  -----         
 0   acctnbr        769284 non-null  int64         
 1   acctrolecd     769284 non-null  object        
 2   acctroledesc   769284 non-null  object        
 3   emplroleyn     769284 non-null  object        
 4   persnbr        735456 non-null  float64       
 5   orgnbr         33828 non-null   float64       
 6   rundate        769284 non-null  datetime64[ns]
 7   datelastmaint  769284 non-null  datetime64[ns]
dtypes: datetime64 , float64(2), int64(1), object(3)
memory usage: 47.0+ MB

data['wh_addr'].info()

<class 'pandas.core.frame.DataFrame'>
RangeIndex: 376431 entries, 0 to 376430
Data columns (total 57 columns):
 #   Column              Non-Null Count  Dtype         
---  ------              --------------  -----         
 0   addrnbr             376431 non-null  int64         
 1   linenbr             376431 non-null  int64         
 2   rundate             376431 non-null  datetime64[ns]
 3   ctrycd              376431 non-null  object        
 4   nextlinenbr         376431 non-null  int64         
 5   ctrysubdivcd        138 non-null    object        
 6   ctrymailcd          2473 non-null   object        
 7   statecd             269227 non-null object        
 8   cityname            376431 non-null object        
 9   citynamesndx        301453 non-null object        
10   zipcd               269204 non-null object        
11   zipsuf              205941 non-null object        
12   censustrtnbr        5507 non-null   object        
13   simsanbr            5410 non-null   object        
14   postnetcd           182833 non-null object        
15   addrlinetypcd1      376410 non-null object        
16   text1               376410 non-null object        
17   addrlinetypdesc1    376410 non-null object        
18   addrlinetypseq1     376410 non-null float64       
19   addrtextsndx1       301304 non-null object        
20   addrlinetypcd2      9491 non-null   object        
21   text2               9491 non-null   object        
22   addrlinetypdesc2    9491 non-null   object        
23   addrlinetypseq2     9491 non-null   float64       
24   addrtextsndx2       4420 non-null   object        
25   addrlinetypcd3      393 non-null    object        
26   text3               393 non-null    object        
27   addrlinetypdesc3    393 non-null    object        
28   addrlinetypseq3     393 non-null    float64       
29   addrtextsndx3       369 non-null    object        
30   addrlinetypcd4      2 non-null      object        
31   text4               2 non-null      object        
32   addrlinetypdesc4    2 non-null      object        
33   addrlinetypseq4     2 non-null      float64       
34   addrtextsndx4       2 non-null      object        
35   addrlinetypcd5      0 non-null      object        
36   text5               0 non-null      object        
37   addrlinetypdesc5    0 non-null      object        
38   addrlinetypseq5     0 non-null      float64       
39   addrtextsndx5       0 non-null      object        
40   addrlinetypcd6      0 non-null      object        
41   text6               0 non-null      object        
42   addrlinetypdesc6    0 non-null      object        
43   addrlinetypseq6     0 non-null      float64       
44   addrtextsndx6       0 non-null      object        
45   addrlinetypcd7      0 non-null      object        
46   text7               0 non-null      object        
47   addrlinetypdesc7    0 non-null      object        
48   addrlinetypseq7     0 non-null      float64       
49   addrtextsndx7       0 non-null      object        
50   mailaddryn          376431 non-null object        
51   mailtypcd           0 non-null      object        
52   mailtypdesc         0 non-null      object        
53   addrusecd           362870 non-null object        
54   addrusedesc         362870 non-null object        
55   electronicyyn       376431 non-null object        
56   datelastmaint       376431 non-null datetime64[ns]
dtypes: datetime64 , float64(7), int64(3), object(45)
memory usage: 163.7+ MB


data['vieworgtaxid'].info()

# Output:
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 13297 entries, 0 to 13296
# Data columns (total 3 columns):
#  #   Column       Non-Null Count  Dtype  
# ---  ------       --------------  -----  
#  0   orgnbr       13297 non-null  int64  
#  1   taxidtypcd   13297 non-null  object 
#  2   taxid        13145 non-null  object 
# dtypes: int64(1), object(2)
# memory usage: 311.8+ KB

data['viewperstaxid'].info()

# Output:
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 167288 entries, 0 to 167287
# Data columns (total 2 columns):
#  #   Column   Non-Null Count  Dtype  
# ---  ------   --------------  -----  
#  0   persnbr  167288 non-null  int64  
#  1   taxid    161379 non-null  object 
# dtypes: int64(1), object(1)
# memory usage: 2.6+ MB



## Not from DB: acct_df
acct_df.info()

<class 'pandas.core.frame.DataFrame'>
RangeIndex: 91019 entries, 0 to 91018
Data columns (total 47 columns):
 #   Column                  Non-Null Count  Dtype         
---  ------                  --------------  -----         
 0   effdate                 91019 non-null  datetime64[ns]
 1   acctnbr                 91019 non-null  object        
 2   ownersortname           91019 non-null  object        
 3   product                 91019 non-null  object        
 4   noteopenamt             91019 non-null  float64       
 5   ratetypcd               72634 non-null  object        
 6   mjaccttypcd             91019 non-null  object        
 7   currimaccttypcd         91019 non-null  object        
 8   curracctstatcd          91019 non-null  object        
 9   notenitrate             91019 non-null  float64       
10   bookbalance             91019 non-null  float64       
11   notebal                 91019 non-null  float64       
12   contractdate            91019 non-null  datetime64[ns]
13   datemat                 34802 non-null  datetime64[ns]
14   taxrptfororgnbr         12589 non-null  float64       
15   taxrptforpersnbr        78436 non-null  float64       
16   loanofficer             27590 non-null  object        
17   acctofficer             48964 non-null  object        
18   creditlimitamt          91019 non-null  float64       
19   origintrate             26959 non-null  object        
20   marginfixed             27608 non-null  object        
21   fdiccatcd               26977 non-null  object        
22   amortterm               27608 non-null  float64       
23   totalpctsold            91019 non-null  float64       
24   cobal                   91019 non-null  float64       
25   creditlimitclatresamt   91019 non-null  float64       
26   riskratingcd            3175 non-null   object        
27   origdate                27248 non-null  datetime64[ns]
28   currterm                27608 non-null  float64       
29   loanidx                 27601 non-null  object        
30   rcf                     2782 non-null   object        
31   availbalamt             91019 non-null  float64       
32   fdiccatdesc             26977 non-null  object        
33   origbal                 25956 non-null  float64       
34   loanlimitryn            27608 non-null  float64       
35   Net Balance             91019 non-null  object        
36   Net Available           91019 non-null  float64       
37   Net Collateral Reserve  91019 non-null  float64       
38   Total Exposure          91019 non-null  float64       
39   orig_ttl_loan_amt       91019 non-null  float64       
40   portfolio_key           76584 non-null  float64       
41   ownership_key           76584 non-null  float64       
42   address_key             76584 non-null  float64       
43   householdnbr           70282 non-null  float64       
44   datelastmaint          70282 non-null  datetime64[ns]
45   Category               27608 non-null  object        
46   inactivedate           2381 non-null   datetime64[ns]
dtypes: datetime64 , float64(23), object(18)
memory usage: 32.6+ MB

