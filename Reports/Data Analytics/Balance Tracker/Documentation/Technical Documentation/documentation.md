# Documentation: Balance Tracker YTD

## Table of Contents
1. Project Overview & Business Use Case
- Intended Audience
    - Project Scope and Deliverables
		  - File Paths and Links to the Project Material and Source Code available here
    - Business Use Case
    - Success Criteria
    - Stakeholders
    - System Overview and High Level Workflows
    - Project Requirements, Budget, Assumptions
2. End-User Guide
    - Manual for using the system or the outputs of the system
    - Any necessary maintenance details or human in the loop considerations
    - Filters and Business Logic used that impact end-users
        - Essential for reducing confusion and misinterpretation of what is being output from system
3. Developer Guide
    - Technical details
    - Environment setup
    - Coding standards & best practices
4. FAQs
	- Common issues
	- Troubleshooting
	- Known Limitations
5. Appendix
	- Additional resources
	- External documentatation
	- Glossary

### Project Overview & Goals
- **Intended Audience**
	- This documentation is comprehensive, including snapshot/high-level information for executives and project managers, a guide for end-users to use the system (if applicable), and technical details for members of the development team for maintenance & modifications. Parts of this documentation can be split up for separate audiences (i.e. An End-User Manual placed in a shared folder for the business line).
- **Business Use Case**
  - This is a long standing report for the head of Business Lines within Lending at Bristol County Savings Bank. It used to be a manual report, but has since been automated and gets distributed automatically. It provides a concise summary of balance totals throughout the year across subsets of the loan portfolio (Commercial, Indirect, Residential, and Concumer)
- **Project Scope and Deliverables**  
- **Success Criteria**
- **Stakeholders**
  - Executive Sponsor: 
  - Project Manager:  
  - Business Line Owner: 
  - Business Initiative/Technical Lead: 

- **System Overview and High Level Workflows**  

- **Project Requirements, Budget, Assumptions**
    1. Requirements:
        - The development team needs access to the core SQL database
        - The development team needs adequate ETL tooling (Python, Alteryx) to create data pipeline/transformations and handle input/output (I/O)
        - The network drive where this output lives needs to be available during business hours (outside of scheduled updates/maintenance) to ensure that other downstream reports/dashboards can successfully read and consume the updated data.

    2. Budget:
    - Internal Costs:
        - Data & Analytics Development Resources
    - External Costs:
        - n/a

    3. Assumptions
    - This plan is based on the following assumptions (about resources, policies, schedules, technologies, etc.):
        - There are adequate development resources
        - Current tooling does not become obsolete/unusable over time, in which case, the development team will have to adapt process to meet business needs with new tools
        - Business logic implemented is correct and validated
        - Conflicting projects do not get prioritized over this


## 2. End-User Guide
This section is not applicable, as there are no interactive end users for this system. The output is consumed programmatically by other development teams.

## 3. Developer Guide
- **Technical Details**  
  - Language: Python 3.11.9  
  - Dependencies: See project's 'pyproject.toml' file.
  - Virtual Python Environment used to isolate dependencies from global system.
  - Data Source: COCC Oracle database  
  - Output Format: `.xlsx` file written using `pandas.to_excel()`  
- **Environment Setup**  
  1. We use virtual environments and initialize these through VS Code 'Create Virtual Environment' function when opening a python file, or you can do this through command line
  2. There is a 'uv.lock' file which locks the dependencies prescriped in the pyproject.toml file. Within the venv, ensure 'uv' package manager by Astral is installed and you can run 'uv sync.' Note, there are core dependencies that are allowed and environment management questions should be elevated to the IST team.
  3. Ensure access to the Database with appropriate credentials. You can use the standard Business Intelligence libraries to connect to the standard COCC database (r1625 and 1625dm).
  4. Configure `.env` file or environment variables with DB connection strings and file output paths
- **Coding Standards & Best Practices**  
  - Follow PEP8 coding style  
  - Use logging for tracking job status and failures  
  - Modularize ETL steps: extraction, transformation, export  
  - Include docstrings and comments for all functions
    - These should include the following sections:
      - Basic description
      - Args (arguments passed into the function)
      - Returns (what is output from the function)
      - Tests/Assertions (the quality control checks and tests within the function to ensure that things are running properly in real-time)
      - If especially complex, include an 'Operations' section where you explain abnormal/complicated items that occur during the function
  - Use descriptive type hints and comment to explain code to others that may be reading it
    - It is easy to zip through a project without documenting and it is good to get it out, but it becomes a challenge for future modifications and others that need to understand the code
      - Invest the time while you are writing the code to document well
  - Use try-except blocks around DB connections and file outputs for robustness  
  - For every function, aim for 2 assertions
    - Positive Assert: A test for something that needs to be there (Ex: the datatype for an input is the correct type or the 'acctnbr' field exists)
    - Negative Assert: A test for something that should never happen, prevent unwanted states (Ex: assert that acctnbr does not contain duplicates)
    - Employing principles of defensive coding by thinking about the asserts and unit tests upfront
      - Don't write them just to get them in. Think about things that need to be there for this to run and unwanted states that you don't want to exist.
    - Scattering these around the code base will ensure there are "trip wires" for edge cases that the developer didn't expect and didn't code for. If these "trip" and throw AssertionErrors, the report will fail to generate, but this helpful for 2 reasons:
		- The developer knows exactly what failed and where it failed (due to assert description)
		- It is preferable to fail in this case and alert the maintainer of failure than to continue on and produce a report for the end user that has unexpected edge cases.
			- Continuing on in this case often results in "garbage output." Hence, we take action to prevent and monitor data throughout all stages of the pipeline.
    - There is no penalty for writing more asserts and unit tests and this is often helpful for writing maintainable/scalable code
  - Note that if you run python code in "optimized mode" with the -O or -OO flags, this will get rid of assertions to get minor speed up and memory usage benefits. This is not what we are concerned about. It is a far bigger problem to present 

- **Design/Implementation Notes**
Notes are added with timestamp and are listed in reverse chronological order (newer items are near the top). The developer should initial his/her notes next to the timestamp.
    ### Notes
    - 2025-04-23 (Chad Doorley)
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

	
    ### Changelog
    - [v1.0.0-prod] 2025-03-17
        - Author: Chad Doorley


## 4. FAQs
- **Common Issues**
  - Network drive not accessible → Check VPN or mapped drive
  - SQL connection timeout → Validate DB credentials and host access
  - Excel file not writing → Ensure output file is not open or locked
- **Troubleshooting**
  - Add logging output for each step to trace failures
  - Wrap transformation logic with logging to help debug unexpected output
- **Known Limitations**
  - Currently supports only one specific database schema
  - Output limited to Excel format – no support for CSV or database write-back
## 5. Appendix
- **Glossary**
  - **ETL**: Extract, Transform, Load  
  - **QC**: Quality Control  
  - **COCC**: Name of the source database provider
