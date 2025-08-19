Lee & Mason
===

Meta Information
---
- Developed by CD
- v.0.0.2-dev
- Key Stakeholders:
    - Kelly Abernathy
- Overview
    - Portfolio of real estate loans for insurance tracking, includes residential, commercial and Home equity loans in a flood zone.
    - Operational Reporting

Done- 
- Meet with Kelly for clarifying questions
- Build data retrieval and data cleaning pipeline

To-do:
- Get clarification on how to handle multiple insurance policies per 
- get borrower address correctly via taxrptorg or pers
- isolate heloc and drop the rest of the CNS loans



Notes
---
### 2025-01-29
- Met with Kelly earlier this week to discuss this request
- This will use the PROPINS table to match the insurance screen that she can see on COCC
- Okay to have multiple line items per acctnbr
- Collateral type does not need to be pre-bucketed (we can filter once I supply her with the report)
- Use PROPINS table
    - Boolean Escrow field
- Spent 1 hr this morning working on this

- The table is ACCTPROPINS from OSIBANK
- INTRPOLICYNBR is a field in many tables: 
    - ACCTPROPINS
    - WH_INSPOLICY
    - INSPOLICYDETAIL
    - INSPOLICY
- This request is a bit more challenging because the tables are not normalized. In ACCTPROPINS table, there is no primary key. There exists duplicates accross acctnbr, insurance number and property tables. Deduplication and care is necessary when working with 1:M and sometimes M:M joins to avoid unintended consequences
```
---------------------------------------------------------------------------
AssertionError                            Traceback (most recent call last)
Cell In[55], line 1
----> 1 assert acctpropins['intrpolicynbr'].is_unique, "Duplicates"

AssertionError: Duplicates
```
This is due to the acctpropins table not being cleared out properly. I've identified a couple loans that are since closed out, yet they are still linked via this table.

- Spend 2 more hours working on this from 12:30-14:30.

- We have a subset of acctnbrs that we are interest in
- We have acctnbrs that are linked to multiple properties
- Some properties have multiple policies
- Nameaddr1 is not the most reliable for primary address and I can get this from the other tables for org/pers similar to how alerts functions

- Spend 15:00-15:30 working on this

### 2025-01-30 [v1.0.0-prod]
- Spoke to Kelly, she wants it broken out for every policy per property
- It needs to be a left join, because we could have properties securing loans and they don't have insurance
- We don't need CNS
    - HELOCs are MTG and there are 4 different products that are Home Equity, have Kelly filter down at the end.
- Wrapped up early version today, will send to Kelly and get her feedback next week on Monday
- v1.0.0-prod is built.