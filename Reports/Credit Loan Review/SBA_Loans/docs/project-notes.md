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


WH_TOTALPAYMENTSDUE
- Interest Payment
- Principal Payment

WH_LOANS
- intpaidtodate
- Interest Period To




