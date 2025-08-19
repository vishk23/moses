# Project: Project Name 
## 1. Project Overview & Goals
*   **Project Lead:** Chad Doorley
*   **Key Stakeholders:**
    - Commercial Credit & Loan Review Depts.
    - Linda Sternfelt
*   **Start Date:** [2024-01-01]
*   **Target Completion Date (Overall):** [2025-04-18]
*   **Brief Description:**
    - Early warning sign system for credit deterioration in lines of credit within a specific subset
*   **Core Objectives / Success Criteria:**
    - Working system that run on a quarterly basis
    - Robust data pipeline (Python) built out to accruately deliver data
    - Interactive PowerBI to be used during quarterly meeting to review facilities
*   **Technology Stack (Key Technologies):**
    - Python
    - SQL
    - PowerBI
*   **Relevant Links:**
    - All project materials can be found here:
    ```bash
    \\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Credit_Loan_Review\Alerts
    ```
---
## 2. Project Status 
*(This section outlines the current status of the project and individual components)*

### Done
- [x] Built out system
- [x] Connect FICO score (Xactus)
- [x] Built PowerBI dashboard
- [x] Make it pull from daily deposit data instead of building a new one during runtime

### TODO
- [ ] Improve system with FICO scores
- [ ] Use pkey instead of household number
    - for a later run because hhnbr is tightly embedded in the code

## 3. General Notes, Decisions & Thoughts
*(Newest entries at the top of this section. Use YYYY-MM-DD for dates.)*
### 2025-06-10 (Chad Doorley)
- Putting time aside today to do the actual implementation of this
- By end of week, need to have a guarantor file ready to go to have reviewed by CML/Credit to get permission to run credit, otherwise, we exclude
- Want streamlined DB to be able to do this sort of quarter over quarter analysis
### 2025-06-03 (Chad Doorley)
Continuing development today, we are going to assess state of the code, identify where modfiications and improvments can be made
- A pain point is the interface of working on the Xactus File
    - fork the main process to create this extract automatically, make sure it's ready to be sent off to them and then automate the dropping in the SFTP folder
- Permission db is just a csv with persnbr and Y (and pers name for readability)
    - Build a couple layers around this to streamline
    - We only store Y's
    - When I do my prelim run to create the Xactus file, we should kick out a separate warning file that we'd like to test these other guarantors, but we don't have permission. If I don't have permission by a certain date, that's ok and we'll just run this without them.
- We should try the duckdb interface instead of sqlite
- Played around with duckDB api, pretty easy to use. I have this mostly mapped out. Need to switch gears to another project, but I'll come back to this later today.
- Got rid of daily deposit generation at runtime and have this reference the built out pipeline for daily deposit update
    - This has been validated against COCC (random selection and backtesting by Paul Kocak)
- Might do parquet also. Doesn't have to be duckdb.
    - Either way, it should be fast, columnar and vectorized.
### 2025-05-29 (Chad Doorley)
- This was a successful launch on the Q2 facilities at the beginning of April
    - We will run Q3 meeting at the end of June
- Ahead of that meeting, there are several improvements I want to make to this
    - Make code more modular and reuse parts from cdutils
- System with FICO needs to be more streamlined
    - permission db could be better (duckdb vs sqlite)
    - the way we pop out exceptions and get on top of getting PFS should be nice and easy
- Need to make FICO have different flags (QoQ, YoY) to capture deterioration over times
- This works, but it could be much better and more flexible
- Will put aside a few hours tomorrow morning to really get into this

## 4. Changelog
*(Newest changes at the top of this section. Use YYYY-MM-DD for dates.)*
### 2025-04-18 [v2.1.8-prod] (Chad Doorley)
- Production release (used at the first live launch of Alerts)
    - previous changes are tracked in the technical documentation docs and in-code comments
- Going forward, everything will be here on changes