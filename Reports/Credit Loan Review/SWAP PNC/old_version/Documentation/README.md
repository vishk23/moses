# Project: SWAP Report
## 1. Project Overview & Goals
*   **Project Lead:** Chad Doorley
*   **Key Stakeholders:**
    - Paul Kocak
*   **Start Date:** [2025-06-17]
*   **Target Completion Date (Overall):** [2025-06-20]
*   **Brief Description:**
    - Automate a manual process for loan review for analyzing SWAP exposure loans. There is a common PNC userfield that serves as the link and we'll automate a highly manual process to provide a robust report for Loan Review Team
*   **Core Objectives / Success Criteria:**
    - Running report
*   **Technology Stack (Key Technologies):**
    - Python
    - SQL
*   **Relevant Links:**
    - All project materials can be found here:
    ```bash
    \\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Credit_Loan_Review\SWAP_PNC
    ```
---
## 2. Project Status 
*(This section outlines the current status of the project and individual components)*

### Done
- [x] Understand requirements of the report
- [x] Create report from COCC data
- [x] Create a staging/cleansing script to accept downloaded PNC data
- [x] Sort output alphabetical on Customer name

### In Progress

### On-Deck
- [ ] Look on second sheet of PNC report 
- [ ] Review with PK

## 3. General Notes, Decisions & Thoughts
*(Newest entries at the top of this section. Use YYYY-MM-DD for dates.)*
### 2025-06-19 (Chad Doorley)
- Grouping by dealer id (PNC user field) to get the two loans together
- Will have to find the anomalies and handle conflicts/duplicates cleanly if there are

- Looks like inactivedate and the datemat are the same for 189 cs prop
- They use origdate (date it hits our system as the open date), not contract date

They want month end loan balance for the loan piece of this. Wondering if I should be just pulling from a staging table for my normal pipeline as of month end for or doing this dynamically in practice. It's probably pretty easy to do the former here. 
- If I just use pipeline as is, I get last business day and this actually has no bearing if I run this on the first of the month, which is the plan I believe. Let's do this because it's the most effective way to do this right now

Use orig_ttl_loan amt & net balance when we join

On the staging piece, there should always be a most current file in that folder. When I run script, if there's a file in there, we can update the staging data
- Pretty clean way to things.

Finished this.
- used current pywin32 for excel formatting. Need to think about the transition of this for future infra/containerization for running in parallel, but will work fine now.

I think this is working well, let's test output.

### 2025-06-17 (Chad Doorley)
- The PNC userfield links both
    - unsure of how to handle the specific duplicate and tranched swap exposure, but I can just show the data as it comes out
- Inputs will be raw data -> staging (for PNC) & COCC data


## 4. Changelog
*(Newest changes at the top of this section. Use YYYY-MM-DD for dates.)*
### 2025-06-17 [v0] (Chad Doorley)
- Initialize project
