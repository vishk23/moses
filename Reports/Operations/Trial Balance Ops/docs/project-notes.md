Objective:
The goal is to provide Operations department with an OBT style (one big table), flattened and standardized report with loan data to assist them with their maintenance and current processes.

Structure:
In the src folder, scripts pull from the data lakehouse and perform transformations and joins to build this report for the operations department

There are 2 outputs: 1 with unique account number and the other one joins on property so they will see multiple properties associated with specific accounts.

# 2025-09-07

Beginning refactor of this

Previous notes:
```
Commercial Trial Balance for Operations
===

Developed by CD

v ? 

Meta Information
---
Key Stakeholders: 
    - Kelly Abernathy
    - Zach Cabral

Overview:
    - Provide operations with a COCC data extract that they can use to reconcile with the trial balance and improve Business processes

Notes
---
### 2025-02-03
- Input connector needs to be updated
- This is a notebook (which is operational), but this needs to be refactored so it will run in an orchestration platform with my other reports as modules. 


```

I had built this for Kelly A/Zach in the past and Kelly M put in report request a while back to get this report and they have agreed that it makes sense to just expand what I had created for them. This is going to be most of the loan fields and they created a sample output of where everything is.

I'll do tests to ensure this is working as well. 

---

PAPU
PARP

Both above are user fields on particpation bought loans

I don't know how to get Investor on typical participation sold loan. I can get bought/sold. This can be part of the silver table, but I don't know where that is. We don't use Participation Inquiry screen. i can see Power 250 has a 29% sold (on my silver table and on insight on Master File), but I don't know where this field is.

I'm a bit overdue on this so I need to get moving. I am also overdue on some other projects so bringing to the forefront of my attention because I now have time to devote to getting them done.



---

<class 'pandas.core.frame.DataFrame'>
RangeIndex: 1 entries, 0 to 0
Data columns (total 70 columns):
 #   Column                           Non-Null Count  Dtype  
---  ------                           --------------  -----  
 0   Loan Number                      0 non-null      float64
 1   Owner                            0 non-null      float64
 2   Major                            0 non-null      float64
 3   Minor Code                       0 non-null      float64
 4   Minor Description                0 non-null      float64
 5   Status                           0 non-null      float64
 6   Rate                             0 non-null      float64
 7   Principal Balance                0 non-null      float64
 8   Book Balance                     0 non-null      float64
 9   Investor Balance                 0 non-null      float64
 10  Investor                         0 non-null      float64
 11  Investor Percentage Sold         0 non-null      float64
 12  Investor Loan Rate               0 non-null      float64
 13  Branch                           0 non-null      float64
 14  Loan Officer                     0 non-null      float64
 15  Contract Date                    0 non-null      float64
 16  Maturity Date                    0 non-null      float64
 17  Payment Due Date                 0 non-null      float64
 18  Amount Due                       0 non-null      float64
 19  Credit Limit                     0 non-null      float64
 20  Revolving Credit Limit           0 non-null      float64
 21  Credit Limit Loan                0 non-null      float64
 22  Loan Funds Held for Reserve      0 non-null      float64
 23  Rate Change Frequency            0 non-null      float64
 24  Next Rate Change Date            0 non-null      float64
 25  Rate Change Lead Days            0 non-null      float64
 26  Change Payment with Rate Change  0 non-null      float64
 27  Rate Schedule                    0 non-null      float64
 28  Interest Method                  0 non-null      float64
 29  Days Method                      0 non-null      float64
 30  Interest Base                    0 non-null      float64
 31  Rate Type                        0 non-null      float64
 32  Margin                           0 non-null      float64
 33  Margin Percent                   0 non-null      float64
 34  Rate Round Method                0 non-null      float64
 35  Min Int Rate                     0 non-null      float64
 36  Max Int Rate                     0 non-null      float64
 37  Max Rate Change Up               0 non-null      float64
 38  Max Rate Change Down             0 non-null      float64
 39  Amortization Term                0 non-null      float64
 40  FDIC Category                    0 non-null      float64
 41  Risk Rating                      0 non-null      float64
 42  Credit Report Type               0 non-null      float64
 43  Loan Purpose                     0 non-null      float64
 44  Escrow Change Month              0 non-null      float64
 45  Escrow Payment                   0 non-null      float64
 46  Escrow Balance                   0 non-null      float64
 47  Escrow Cushion                   0 non-null      float64
 48  Escrow Taxes                     0 non-null      float64
 49  Escrow Insurance                 0 non-null      float64
 50  Collateral Type                  0 non-null      float64
 51  Collateral Description           0 non-null      float64
 52  Vehicle ID Number                0 non-null      float64
 53  Appraised Value                  0 non-null      float64
 54  Occupancy Status                 0 non-null      float64
 55  Purchase Price                   0 non-null      float64
 56  Book Number                      0 non-null      float64
 57  Page Number                      0 non-null      float64
 58  Flood Zone                       1 non-null      object 
 59  Flood Zone.1                     0 non-null      float64
 60  NAICS Industry Code              0 non-null      float64
 61  HHNU                             1 non-null      object 
 62  SCRA                             0 non-null      float64
 63  ASST                             0 non-null      float64
 64  DTYP                             0 non-null      float64
 65  Mail Restriction                 0 non-null      float64
 66  Deferred Fee Original            0 non-null      float64
 67  Deferred Fee Current             0 non-null      float64
 68  Deferred Cost Original           0 non-null      float64
 69  Deferred Cost Current            0 non-null      float64
dtypes: float64(68), object(2)
memory usage: 692.0+ bytes

Above is the requested output


['Loan Number', ACCTCOMMON
 'Owner', ACCTCOMMON
 'Major', ACCTCOMMON
 'Minor Code', ACCTCOMMON
 'Minor Description', ACCTCOMMON
 'Status', ACCTCOMMON
 'Rate', ACCTCOMMON
 'Principal Balance', ACCTCOMMON
 'Book Balance', ACCTCOMMON
 'Investor Balance', Calculated Field, diff between notebal and bookbal
 'Investor', ?
 'Investor Percentage Sold', totalpctsold, ACCTLOAN
 'Investor Loan Rate', ? # There is an investor table
 'Branch', ACCTCOMMON
 'Loan Officer', ACCTCOMMON
 'Contract Date', ACCTCOMMON
 'Maturity Date', ACCTCOMMON
 'Payment Due Date', currduedate, WH_ACCTLOAN
 'Amount Due', ? prob WH_ACCTLOAN
 'Credit Limit', WH_ACCTLOAN
 'Revolving Credit Limit', WH_ACCTLOAN, creditlimitamt
 'Credit Limit Loan', LOAN something YN - I think this is in the status page
    - Yeah it's LOANLIMITYN
 'Loan Funds Held for Reserve', clatresamt
 'Rate Change Frequency', rcf, WH_ACCTLOAN
 'Next Rate Change Date', nextratechg, WH_LOANS?
 'Rate Change Lead Days', ?, calculated field maybe
 'Change Payment with Rate Change', ?
 'Rate Schedule', ?
 'Interest Method', WH_ACCTLOAN I think
 'Days Method', ?
 'Interest Base', ?
 'Rate Type', ?
 'Margin', WH_ACCTLOAN I think
 'Margin Percent', again acctloan
 'Rate Round Method', acctloan ?
 'Min Int Rate', ?
 'Max Int Rate', ?
 'Max Rate Change Up', ?
 'Max Rate Change Down', ?
 'Amortization Term', ?
 'FDIC Category', fdiccatcd or desc
 'Risk Rating', riskratingcd
 'Credit Report Type', ?
 'Loan Purpose', ?
 'Escrow Change Month', ?
 'Escrow Payment', ?
 'Escrow Balance', ?
 'Escrow Cushion', ?
 'Escrow Taxes', ?
 'Escrow Insurance', ?
 'Collateral Type', cleaned prop table
 'Collateral Description', cleaned prop table
 'Vehicle ID Number', cleaned prop table
 'Appraised Value', cleaned prop
 'Occupancy Status', cleaned prop
 'Purchase Price', cleaned prop
 'Book Number', ?
 'Page Number', ?
 'Flood Zone', insurance/prop? (Y/N)
 'Flood Zone.1', insurance/prop?
 'NAICS Industry Code', naicscd, on acctlvl, org leve and pers level
 'HHNU', my user field, append portfolio_key as well
 'SCRA', user field
 'ASST', user field
 'DTYP', userfield 
 'Mail Restriction', allowpromoyn (org/pers?)
 'Deferred Fee Original', prob acctloan
 'Deferred Fee Current', prob acctloan
 'Deferred Cost Original', prob acctloan
 'Deferred Cost Current'], prob acctloan

----

Did a good amount of reviewing data catalog and meta data on this. Most of it is directly from bronze tables. I'll give more than needed when in doubt and ask Kelly for her thoughts on some of these fields.

A lot is ACCTLOAN.

Debating whether I build directly from silver table or if I just go from Bronze. I think silver layer has to be the interface into all of this stuff.

It's bronze -> OBT -> downstream analysis. Hard though because there are all sorts of things that we could potentially need, but I think the silver table handles all. Silver table at this current point in time doesn't come from bronze tables though, so need to think a little bit about this.


---
# 2025-09-15

Big time overdue on this. Can't put this on the super hold while I build everything else out. This is something to deliver asap. Why not just build it exactly as you think it would need to function and then from there, you can always refactor and adapt. The optimal solution/perfect data model isn't ready off the shelf to use so might as well just build it exactly to spec and refactor later on



