# 2025-08-26
Taking this report request

It is a bit tricky because of the caching of the database

I originally tried to take the cleaned account data as of different dates, but I have only active accounts in my df. That's the nuance.

I have many improvements to make to this reporting layer, but I think this will be a report that I'll do the old fashioned way. 
- Need to get this to Terry by tomorrow


----

Data I need
- Application ID
    - meridian link
- Account Number 
    - osibank/coccdm acctcommon
- Loan Origination Date
    - same
- Applicant Last Name 
    - pers
- Applicant First Name
    - pers
- Co-Applicant Last Name
    - pers after grouping with allroles
- Co-Applicant First Name
    - pers after grouping with allroles
- Applicant Credit Score
    - wh_pers
- Co-Applicant Credit Score
    - wh_pers
- Model Year
    - prop or prop2
- Vehicle Mileage
    - prop or prop2
- Dealer Name
    - ?
- Amount Financed
    - orig_ttl_loan_amt
- Current Balance
    - net balance
- Contract Rate
    - ?
- Buy Rate
    - ?
- Loan Paid or Open
    - status
- Date Closed
    - closedate
    - acctcommon


----

