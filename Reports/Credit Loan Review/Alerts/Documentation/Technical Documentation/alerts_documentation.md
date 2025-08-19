# Documentation: Portfolio Alerts 

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
- **Project Scope and Deliverables** 
    - Portfolio Alerts is an internally developed system that pulls data from several sources, performs data cleaning and transformations, and then creates a flat file that powers a PowerBI dashboard. This dashboard is dynamic and updates everytime the data is refreshed (quarterly)
    - File Path to Project Directory:
        ```
        \\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Chad Projects\Alerts
        ```
- **Business Use Case**  
    - The Portfolio Alerts project is an internally developed system to monitor a subset of the loan portfolio for early warning signs and deterioration of credit quality. Data is pulled from several sources and transformed to provide the Credit & Loan Review teams to test facilities on specific pre-determined criteria, such as delinquency, credit score deterioration, total relationship deposit decreases & more. - This is utlizied on a quarterly basis by the Alerts Committee (run by the Chief Credit Officer) to determine the outcome of loans that are eligible for the Portfolio Alerts System. 
- **Success Criteria**
    - The script runs as performed
    - A dashboard is created that serves the Business Line's needs
        - It is easy to use, accurate, and dynamic
    - The system provides verifiable and accurate measure of loan performance
- **Stakeholders**
  - Executive Sponsor: Tim Chaves
  - Project Manager: Bill Muto 
  - Business Line Owner: Linda Sternfelt
  - Business Initiative/Technical Lead: Chad Doorley

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

### Red Flags (Quick Guide)
- Deposit Change <= -%30
    - Relationship needs have to have $250,000 in deposits to be test on this flag
    - Will be trailing 3 months vs trailing 12 months
- TTM Overdrafts >= 5
- TTM Past Due >= 3
- TTM Past Due 30 Days >= 1
- 30 Day Cleanup Provision (N)
- Utilization Limit >= 60%
- FICO Score < 680 or Delta <= -10% (period over period)  

### Definitions
- **Deposit Decrease**: Check if average deposit balance for the relationship over trailing 3 months has declined by 30% or greater when compared to trailing 12 month average balance. Relationships with total deposits <= $50,000 are excluded from this test (to exclude flagging accounts where deposits decrease from $10,000 to $2,000 for example).
- **TTM Overdrafts**: Check on COCC if there has been more than 5 overdrafts in any deposit accounts in the relationship in the last trailing 12 months. The measure is the days overdrawn statistic from COCC.
- **Past Due**: Check if the account has been past due 15-29 days 3x or more within the trailing 12 months or 30+ days 1x over the same period.
- **TTM Utilization**: Assess whether line utilization has been greater than 70% over trailing 12 months. 
- **30-Day Cleanup Provision**: Check on COCC if the line has been paid to 0 for at least 30 days during the trailing 12 months.
- **FICO**: Check if any of the guarantors on the account have a FICO score < 680 or if current credit score has decreased 10% vs the credit score in the prior period. Due to lack of historical data, this currently only captures the credit score floor of 680 set in place, with deterioration over time being added once we have more data to work with.

### Data Sources
- Deposit Decrease
    - COCC
        - Tables Utilized: 
            - WH_ACCTCOMMON
            - ACCTSTATISTICHIST
            - WH_DEPOSITS
        - For the trailing 3 month and 12 month balance, the NOTEMTDAVGBAL field is used (which is an average balance for that month). The data is pulled in for n number of months (3 & 12 are passed in as) on month end and an average is taken over that specific range to generate the avg balance for that range. This was a modification to use the short term average balance vs the trailing 12 month average instead of spot balances because deposit accounts can be volatile
            - Note that the household number is used to group related accounts and the sum of all the deposit accounts in the household is used in this metric
- TTM Overdrafts 
    - COCC
        - For the Overdrafts flag: this is the DOD code in the ACCTSTATISTICHIST (account statistics in COCC). This is the code for 'Days Overdrawn'. This is the 'statistictypcd' field.
            - During the specified period, we take the sum of the DOD occurences
            - The specified period takes the date of running the script - 1 year and goes to the beginning of the month.
                - If today is April 7, it will capture everything from April 1 of prior year through date of running the script.
- TTM Past Due & TTM Past Due 30+
    - COCC
        - Similar to the Overdrafts, this utilized the 'statistictypcd' field in ACCTSTATISTICHIST (COCC) and it looks at the PD and PD30 codes, which correspond to late 15-29 days and 30-59 respectively.
            - During the specified period, we take the sum of the occurences of the statistic codes
            - The specified period takes the date of running the script - 1 year and goes to the beginning of the month.
                - If today is April 7, it will capture everything from April 1 of prior year through date of running the script.
- Utilization Limit & Cleanup provision
    - COCC
        - Utilization
            - Date comes from WH_ACCTCOMMON (bookbalance) and ACCTLOANLIMITHIST (creditlimitamt)
            - Calculate every business day within the specified period (Trailing 12 months)
            - if creditlimitamt is null, replace with 0
                    - Calculate line utilization:
                        - ttm line utilization = bookbalance / creditlimit amount
                        - fill na values with 0 (0/0) and inf with 100 (credit limit = 0, bookbalance > 0)
                        - group by acctnbr and take average line utilization
        - 30 Day Cleanup
            - Using bookbalance from WH_ACCTCOMMON, check every day within specified period if bookbalance = 0
            - Use a rolling window of 30 days in a row to check for 0
                - Realizing that this is 30 business days (where we have data), not 30 calendar days. This should be brought up and discussed.
- FICO Score < 680 or Delta <= -10% (period over period) 
    - Xactus
        - We receive an extract file with a list of guarantors that gets loaded into the system
        - Iterate through the extract file for each record
            - Check if either of the guarantors experience a deterioration in score period over period (not yet used due to lack of historical data) or if either guarantor has a score below 680

### Current Parameters for Products Tested:
- Lines of Credit under $500M & under $1MM in total relationship exposure

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
    - Design
    - Implementation
    ### Changelog
    - [v1.0.0-prod] 2025-03-17
        - Author: Chad Doorley
            - Will shore up documentation and make some refactors to come soon to this process
            - Getting things on cdutils/more consistent staging
            - Pulling out ELOCs
            - For Q3 run, pulling out A&L + Farland due to info from people. 


## 4. FAQs
- **Q**: What happens if a line that should have been eligible is not included in Alerts and it should have been (and the inactive date falls within that quarter)?
    - **A**: If there truly was a facility that was eligible and it was not captured (household number was not tied properly making relationship too large, etc...), please fill out a 90 Day Temporary Extension with the reason as "Facility should be eligible for Alerts and maintenance was done to ensure that is will be on the future runs." This will be covered in the next Alerts meeting that will take place at the beginning of the following quarter.
## 5. Appendix
- **Glossary**
  - **ETL**: Extract, Transform, Load  
  - **QC**: Quality Control  
  - **COCC**: Name of the source database provider
