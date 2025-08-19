# Documentation: 

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
    - Design
    - Implementation
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
