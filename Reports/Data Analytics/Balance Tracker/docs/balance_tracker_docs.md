# Project: Project Name 
## 1. Project Overview & Goals
*   **Project Lead:** Chad Doorley
*   **Key Stakeholders:**
    - Executive Leadership Team
        - Tim Chaves
*   **Start Date:** []
*   **Target Completion Date (Overall):** []
*   **Brief Description:**
    - This is a long standing report for the head of Business Lines within Lending at Bristol County Savings Bank. It used to be a manual report, but has since been automated and gets distributed automatically. It provides a concise summary of balance totals throughout the year across subsets of the loan portfolio (Commercial, Indirect, Residential, and Concumer)
*   **Core Objectives / Success Criteria:**
*   **Technology Stack (Key Technologies):**
    - Python
    - SQL
*   **Relevant Links:**
    - All project materials can be found here:
    ```bash
    \\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Data_Analytics\Balance Tracker
    ```
---
## 2. Project Status 
*(This section outlines the current status of the project and individual components)*

### Done
- [x] Develop automated solution to prior manual process of compiling this report
- [x] Validate balance fields against Tom K's Portfolio Summary & FDIC Call report
- [x] Validate unadvanced funds against Portfolio Summary
- [x] Validate total loan yield
- [x] Program new loan yield

### In Progress
- [ ] Make the feature totals part of the program rather than relying on formulas in Excel
    - pretty easy to just calculate these total rows and just hardcode the cells to output to
- [ ] Rectify small difference on indirect

### On-Deck
- [ ] Come up with a way for this to dynamically create a new sheet at year end without manual adjustment
    - A bit complex and may not be worth the effort for 15 mins of adjustment once a year to create the new sheet and remap the output

## 3. General Notes, Decisions & Thoughts
*(Newest entries at the top of this section. Use YYYY-MM-DD for dates.)*

### 2025-05-12 (Chad Doorley)
- Got this all the way through today. Fully built out. Small difference on Indirect vs Tom's report, but likely just something I can review with him quickly and identify where this differs.
    - This is in a good spot. I'll revisit with Tom. 

### 2025-05-09 (Chad Doorley)
- Going to validate fields against Tom's reports
    - I made some good progress before I went away on vacation and now I'm going to finalize this.

Today:
- Update doc
- Dive into code and validate


Double checked and the other 2 fields tick/tie out


151165563
IL12 loan that doesn't show up for me

Fixed this by removing the filtering on current account status upfront. This will have no impact on the balances because the net balances will be 0 for closed accounts. This way, we can capture new loans booked that are immediately paid off (like that indirect loan above)

For the transaction table, we can take the new loans df, get the start/end date of month, dynamically create the transaction df
- from there, we label disbursements as positive and receipts as negative and create a calculated column
    - here transaction number is primary key
- apply a group by on acctnbr, summing up this new calculated column for net disbursements/advances
- merge this back to new_loan_df and I have my field that I need for the weighted average


One more challenge is how do we get the weighted average amount
- I think I have to do this programatically and just write out the totals as values
- not a big deal and I can do this for the other columns as well

Ok, got most of the advanced to match, I think there's an additional business rule that Tom may need to tell me about, or I did somethign wrong. This is in 2.0.3-dev right now. 

Probably another few hours at this and will get solved.
- Want to get this set, because it's important to Tim/John and need to make sure it ties back to Tom's.


### 2025-04-23 (Chad Doorley)
    - Need to get the additional fields to the right matching up to Tom K's portfolio summary
    - Tom sent me a list of items here:
    ```
        Indirect:
        - not noteintrate
        - dealer split rate SPLT
            - noteintrate - this field


        equity lines of credit (resi)
        - MG48
        - MG50
        - MG52
        - MG55
        - MG60

        principle 
        trancode disbursement NDMB
        - CWT

        ACH manager - shadow account for deposit accts

        unadvanced - avail to customer (AVAILBALAMT)
        - sum 

        CML:
        - for 3 products
            - CM06, CM30, CM52
            - net them out
            - disbursements
                - PDSB (princpal disbursed)
                - SWPI (sweep principle increase)
            - recipts
                - prct (principal receipt)
                - swpr (sweep princple receipt)

    The other advance formula is in a screenshot located in the 'bin'
    ```
    - Need to create calculated column for 'modified int rate' and then based on all the little tweaks, we can get this to work

### 2025-01-31
- Since it is now the new years and we are getting our first item for the balance tracker, we will need to create a new sheet
- Tim called me and he has new budget goals to add and a couple new sections
    - Wants:
        - new loan avg yield
        - average yield
        - for the Commercial + C&I, these should be broken out into:
            - Own Occ CRE
            - Non Own Occ CRE
            - C&I Term
            - C&I LOC
            - HOA
    - Reference against Tom K Fiscal YTD report, loan portfolio summary (Crystal)
    - I currently get the summary pieces from that report, but the breakout will need to be more indepth
- Plan:
    - Re-do template and get Tim's approval
    - Have tom remap to new sections or I can remap to new sections.
- This report won't go out Monday, as Tim said to take the time to fix it up. He doesn't need until Feb 24

### 2025-02-12
- Needs to be done before the board presentation so Tim can report on this
- I have the updated budget stuff from Jen St Pierre
```
Budget Loan Projections
CRE: 75,000,000
C&I: 10,000,000
HOA: 40,000,000
Residential: 16,000,000
Indirect: -29,000,000
Equities: 1,000,000
Consumer: 8,000,000
Total: $121,000,000
```

### 2025-02-15
Done with CRE presentation visuals and will focus on this

Note that there is a rounding error or some issue with filters with current balance tracker. We want to be exact so I'm going to recode this from scratch
- Should be able to leverage the CRE pipeline as a starting place because it's mostly there, but we just need to include things outside of commercial

Going to run this on all of acctcommon and drop where no fdic category code.
- This way, we get all loans active/NPFM that would show up on call report and we use that as a starting place for this.

The process will be create a month over month using MONTHENDYN trailing 2 records to inject back into new SQL query, like some other reports do. Based on our FDIC groupings, we can slice up the portfolio into correct groups, find the net balance delta 

Aside from Tax Exempt bonds, $12MM net balance difference, I get exactly what is the ledger balance for Call Report before their manual adjustments
- 12/31/24: $2,429,561,165.60 (exact match)
    - Maybe I should just pull zero out tax exempt bonds to get this equal.
    - I didn't make the call to do the manual override for Tax Exempt bonds, so I should just get this out in the open.

Pretty much ready to go, let's get clarification on this and I also need to engineer the system itself.
- on the call report validation excel sheet, I made a process workflow diagram on how this works. Not too challenging.


### 2025-02-19
New sections are:
- CRE
    - CML major
    - Construction call codes (CNFM, OTCN, LAND, RECN)
    - Farmland (REFM)
    - OwnerOcc/NonOwnerOcc/1-4 Fam/Multi-Fam (REOE, REFI, REJU, REMU, REOW, RENO)
    - Other call codes (OTAL, LENO, AGPR)
        - Includes Commercial Leases/Agriculture
    - Tax exempt bonds go in here too as other
- C&I
    - CML major + MLN
    - CIUS fed call code
    - minus CM15 & CM16
    - minus HOA
- HOA
    - CML Major
    - CIUS major, only the HOA product(s)
        - Community Assoc. Term Loan + Community Assoc. Draw to Term
            - CM46, CM47
- Residential
    - All MTG major
    - Possible FDIC codes
        - array(['REFI', 'REOE', 'CNFM', 'OTCN', 'REJU'], dtype=object)
- Consumer
    - CNS
    - minus anything with AUTO call code
        - except for Used Auto and New Auto (IL09, IL10), which are indirect loans originated by bank, not a dealer
    - Possible FDIC codes
        - 'CNOT', 'CNCR'
- Indirect
    - Possible Majors: CNS + CML (only a portion)
    - AUTO call code + CML indirect (CM15, CM16)

Note that things without an FDIC code get caught in the OTAL (Commercial/Other) category
- I'll have this as a data dump every run just to monitor and stay on top of this

Plan here is to do the year end analysis and then we can use the same ETL process for each month end period. We'll just need to dynamically feed in the months throughout the year here.

Just need to program this out now into balance tracker system. Now I have everything reconciling.

Reconcilation:
- Reconciling mine with Tom K's portfolio summary, he classifies Used Auto and New Auto (which have FDIC Category Code AUTO as Installment/Consumer, where I have this as indirect with all the other AUTO loan types)

Workflow is kind of fragile, as I just adjust the database query date manually right now and then run it through the pipeline

I'll fix this up, but I just did the report manually because I know there is a time crunch with getting it in the board portal.

### 2025-02-21 [v2.0.0-prod] 
No more PPP beacuse so insignificant $25k. No more forgiveness, let's just classify these as regular Commercial loans and they are paying as normal and if we need to adjust this per executive request, we can.

Built this end to end. Complete today. We'll produce a new version


### 2025-02-26
Tim wants a few additional fields that are on Tom's portfolio summary report
- Will need to have this done for Monday.


### 2025-02-28 [v2.0.1-prod]
Added the additional fields today
- took a while
- mapped out new process with these additional requirements
    - reflected in the new diagram
- the loan yield is a bit of a mess, with hardcoded updates on consumer loans
    - the way this was explained to me is that the heat loans are booked with 0% interest, but we collected from separate program upon origination (so we aren't really getting paid interest from customer here)
    - it is a proxy, but we take prime + 1 and update it every time it changes. There is a cap at 7% now for TMLP
- no easy way to program this, so I just copied what Tom K did
```python
df['noteintrate'] = np.where(
    (df['currmiaccttypcd'] == 'IL33') & (df['contractdate'] >= pd.Timestamp(2025,1,1)), .07,
    np.where((df['currmiaccttypcd'].isin(['IL21','IL31','IL33'])) & (df['contractdate'] >= pd.Timestamp(2024,12,19)), .085,
    np.where((df['currmiaccttypcd'].isin(['IL21','IL31','IL33'])) & (df['contractdate'] >= pd.Timestamp(2024,12,19)), .085,
    np.where((df['currmiaccttypcd'].isin(['IL21','IL31','IL33'])) & (df['contractdate'] >= pd.Timestamp(2024,11,8)), .0875,
    np.where((df['currmiaccttypcd'].isin(['IL21','IL31','IL33'])) & (df['contractdate'] >= pd.Timestamp(2024,9,19)), .09,
    np.where((df['currmiaccttypcd'].isin(['IL21','IL31','IL33'])) & (df['contractdate'] >= pd.Timestamp(2023,7,27)), .095,
    np.where((df['currmiaccttypcd'].isin(['IL21','IL31','IL33'])) & (df['contractdate'] >= pd.Timestamp(2023,5,4)), .0925,
    np.where((df['currmiaccttypcd'].isin(['IL21','IL31','IL33'])) & (df['contractdate'] >= pd.Timestamp(2023,3,23)), .09,
    np.where((df['currmiaccttypcd'].isin(['IL21','IL31','IL33'])) & (df['contractdate'] >= pd.Timestamp(2023,2,2)), .0875,
    np.where((df['currmiaccttypcd'].isin(['IL21','IL31','IL33'])) & (df['contractdate'] >= pd.Timestamp(2022,12,16)), .085,
    np.where((df['currmiaccttypcd'].isin(['IL21','IL31','IL33'])) & (df['contractdate'] >= pd.Timestamp(2022,11,3)), .08,
    np.where((df['currmiaccttypcd'].isin(['IL21','IL31','IL33'])) & (df['contractdate'] >= pd.Timestamp(2022,9,22)), .0725,
    np.where((df['currmiaccttypcd'].isin(['IL21','IL31','IL33'])) & (df['contractdate'] >= pd.Timestamp(2022,7,28)), .065,
    np.where((df['currmiaccttypcd'].isin(['IL21','IL31','IL33'])) & (df['contractdate'] >= pd.Timestamp(2022,6,16)), .0575,
    np.where((df['currmiaccttypcd'].isin(['IL21','IL31','IL33'])), .05,
    df['noteintrate']))))))))))))))
    )
```
- Additionally, we used weighted average rate
    - I take new loans and Net Balance
    - need to check requirements here

## 4. Changelog
*(Newest changes at the top of this section. Use YYYY-MM-DD for dates.)*


### 2025-04-01 [v2.0.2-prod] (Chad Doorley)
- Skipped a few releases but minor tweaks have been made
- There are 3 additional fields now to the right most side of the sheet:
    - New Loan Yield
    - Total Loan Yield
    - Unadvanced Funds
- These tie back to Tom K's portfolio summary as a check
    - The formulas/tweaks are described in the notes section above
    - There are several little adjustment that need to be made:
        - Dealer splits
        - Advances formula
        - Special formula for 3 loan products (disbursements vs receipts)


### 2024-03-17 [v1.0.0-prod] (Chad Doorley)
- First version of automated solution
