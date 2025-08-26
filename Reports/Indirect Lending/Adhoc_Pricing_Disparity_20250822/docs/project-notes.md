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

---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
Cell In[6], line 1
----> 1 df = src.account_data_adhoc.core.query_df_on_date()

File c:\Users\w322800\Documents\gh\bcsb-prod\Reports\Indirect Lending\Adhoc_Pricing_Disparity_20250822\src\account_data_adhoc\core.py:55, in query_df_on_date(specified_date)
     52     assert isinstance(specified_date, datetime), "Specified date must be a datetime object"
     53     specified_date = get_last_business_day(specified_date)
---> 55 data = src.account_data_adhoc.fetch_data.fetch_data(specified_date)
     57 # # # Core transformation pipeline
     58 raw_data = src.account_data_adhoc.core_transform.main_pipeline(data)

TypeError: fetch_data() takes 0 positional arguments but 1 was given

----

Do you by any chance have the data we provided the 3rd party for their analysis so I can tie back to my data. I tried to request meridian link data and was told they would have to open a ticket and it be $15k per year's worth of data which sounds absolutely absurd....
