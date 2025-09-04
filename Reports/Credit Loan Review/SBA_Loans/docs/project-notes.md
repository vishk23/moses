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

