# 2025-09-04

Filter df['product'] on below values:
array(['Express Business SBA LOC', 'Express Business SBA Term Loan',
       'FNB - SBA Line of Credit', 'FNB - SBA Loan',
       'SBA Commercial Mortgages', 'SBA Commercial Term',
       'SBA PPP R2 LNS', 'SBA Secured Line of Credit'], dtype=object)

INTPAIDTODATE
- wh_loans

Loan numbers
- acctcommon


Next Installment Due Date
- acctloan
    - currduedate

Amount Disbursed this period


WH_TOTALPAYMENTS_DUE for Interest/Principal 


74000 where currduedate = nextduedate
10000 where they don't match

We want curr due date. Validated off COCC

Transaction codes for this, need to figure out what Joan would like to see:
PDSB
SWPI
NDSB

# 2025-09-05

I think it's just PDSB
- for LOC advances


WH_RTXN for the most recent month. That can be a tack on.
- or we add trailing month worth of transactions. 

Ok so

WH_ACCTCOMMON
- loan number
- int rate
- closing balance (net balance)

WH_ACCTLOAN
- currduedate (Next Installment Date)

WH_RTXN (Trailing Month)
- Amount disbursed this period
- PDSB RTXNTYPCD
- where RTXNSTATCD = 'C'

or Principal Adv Amt field


WH_TOTALPAYMENTSDUE
- Interest Payment
- Principal Payment

WH_LOANS
- intpaidtodate
- Interest Period To



May need to change gears on the totalpaymentsdue. That doesn't seem to show future payments, even though it's in the amortization table.
- I might need some Tom K help on this.

----

Ok I've got it now.

The Principal Paid & Interest Paid come from RTXNBAL where BAL/INT balcatcodes and rtxntypcd = 'SPMT' (standard payment)

The advances is just PDSB total for that month

This can all be done from the rtxnbal:

<class 'pandas.core.frame.DataFrame'>
RangeIndex: 1037825 entries, 0 to 1037824
Data columns (total 11 columns):
 #   Column         Non-Null Count    Dtype         
---  ------         --------------    -----         
 0   acctnbr        1037825 non-null  int64         
 1   rundate        1037825 non-null  datetime64[ns]
 2   rtxnnbr        1037825 non-null  int64         
 3   rtxntypcd      1037825 non-null  object        
 4   rtxntypdesc    1037825 non-null  object        
 5   subacctnbr     1037825 non-null  int64         
 6   balcatcd       1037825 non-null  object        
 7   baltypcd       1037825 non-null  object        
 8   balancedesc    1037825 non-null  object        
 9   amt            1037825 non-null  object        
 10  datelastmaint  1037825 non-null  datetime64[ns]
dtypes: datetime64[ns](2), int64(3), object(6)
memory usage: 87.1+ MB

Create 2 different dfs, one for spmt and one for pdsb

Group by account number. For the pdsb one, we just sum of the amt
For the smpt one, we need 2 fields, the sum of principal payments and the some of interest paid. that is by baltypcd to decipher which lines are balance/principal or interest. This is explained above.





