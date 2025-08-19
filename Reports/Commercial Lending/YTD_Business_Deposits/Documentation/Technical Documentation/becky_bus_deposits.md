Business Deposit Report
===

Meta Information
---
- Developed by CD
- [v0.5.0-dev]
- Business Line: Commercial Lending
- Key Stakeholders:
    - Becky Velasquez
    - Hasan Ali
- Overview:
    - Capture new business deposits accounts during time period (monthly basis)
    - Addtional custom date range to assist in analyzing deposits that are being brought in by the lending team

Notes
---
### 2025-02-13
Starting work on this. Report will be simpler than I had thought because I was originally told it would need to be the opening balance of all accounts, but some accounts are $0 when account is opened and money added later that week, etc...

We'll do period 2023-11-01 -> 2024-12-31
- Current balance
- Stratefied by Region and Lender

SQL query
```python
acctcommon = text("""
SELECT 
    a.ACCTNBR, 
    a.EFFDATE, 
    a.MJACCTTYPCD, 
    a.PRODUCT, 
    a.CURRMIACCTTYPCD, 
    a.BOOKBALANCE, 
    a.ACCTOFFICER, 
    a.OWNERSORTNAME, 
    a.CURRACCTSTATCD, 
    a.CONTRACTDATE, 
    a.BRANCHNAME,
    a.NOTEINTRATE,
    a.PRIMARYOWNERCITY,
    a.PRIMARYOWNERSTATE
FROM 
    COCCDM.WH_ACCTCOMMON a
WHERE 
    a.CURRACCTSTATCD IN ('ACT','DORM') AND
    (a.MJACCTTYPCD IN ('CK','SAV','TD')) AND
    (a.CONTRACTDATE BETWEEN TO_DATE('2023-11-01 00:00:00', 'yyyy-mm-dd hh24:mi:ss') AND
    TO_DATE('2024-12-31 00:00:00', 'yyyy-mm-dd hh24:mi:ss')) AND
    (a.EFFDATE = TO_DATE('2024-12-31 00:00:00','yyyy-mm-dd hh24:mi:ss'))
""")
```

Note sure about:
'CK34': ICS Shadow - Business - Demand

Minors included:
```python
minors = [
    'CK24', # 1st Business Checking
    'CK12', # Business Checking
    'CK25', # Simple Business Checking
    'CK30', # Business Elite Money Market
    'CK19', # Business Money Market
    'CK22', # Business Premium Plus MoneyMkt
    'CK23', # Premium Business Checking
    'CK40', # Community Assoc Reserve
    'CD67', # Commercial Negotiated Rate
    'CD01', # 1 Month Business CD
    'CD07', # 3 Month Business CD
    'CD17', # 6 Month Business CD
    'CD31', # 1 Year Business CD
    'CD35', # 1 Year Business CD
    'CD37', # 18 Month Business CD
    'CD38', # 2 Year Business CD
    'CD50', # 3 Year Business CD
    'CD53', # 4 Year Business CD
    'CD59', # 5 Year Business CD
    'CD76', # 9 Month Business CD
    'CD84', # 15 Month Business CD
    'CD95', # Business <12 Month Simple CD
    'CD96', # Business >12 Month Simple CD
    'CK28', # Investment Business Checking
    'CK33', # Specialty Business Checking
    'CK34', # ICS Shadow - Business - Demand
    'SV06' # Business Select High Yield
]
```

Sent this over to them to review.

Need to set this up with monthly version to add to YTD (easy fix with just adjusting date ranges)