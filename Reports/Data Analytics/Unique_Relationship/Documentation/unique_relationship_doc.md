# Project: Unique Relationship 
## 1. Project Overview & Goals
*   **Project Lead:** Chad Doorley
*   **Key Stakeholders:**
    - Executive Leadership Team
    - Retail Banking
*   **Start Date:** [2025-05-07]
*   **Target Completion Date (Overall):** [2025-05-09]
*   **Brief Description:**
    - The goal is to be able to leverage the work done on grouping relationships in the R360 project, specifically the portfolio_key, to understand growth/decay of relationships at the 'Branch' level.
*   **Core Objectives / Success Criteria:**
    - Build a reliable data pipeline for provide accurate information on demand (or set schedule like every quarter)
    - Develop PowerBI Dashboard to show the data to the end users
*   **Technology Stack (Key Technologies):**
    - Python
    - SQL
    - PowerBI
*   **Relevant Links:**
    - All project materials can be found here:
    ```bash
    \\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Data_Analytics\Unique_Relationship
    ```
---
## 2. Project Status 
*(This section outlines the current status of the project and individual components)*

### Done
- [x] Requirement Analysis and Deliverable
- [x] Finalize Project Management Documentation
- [x] Data Exploration
- [x] Build Data Pipeline
- [x] Showcase to end users and make modifications
    - Sent to John, he wants to see it segmented by address also.
- [x] Create this with address_only key to compare vs the super household

### In Progress

### On-Deck
- [ ] Test edge cases and enhance unit tests
- [ ] Finalize project documentation to ensure all requirements were met


## 3. General Notes, Decisions & Thoughts
*(Newest entries at the top of this section. Use YYYY-MM-DD for dates.)*

### 2025-05-08 [v1.0.0] (Chad Doorley)
- Sent to John yesterday. He liked it, but I pointed out that this is the super household and shared business relationships (separate families) would count as 1 household.
    - I'm going to tweak this to also do it by address. This will involve either the creation of another key, or use a piece of the R360 workflow to create the address unique identifier as an additional field.
    - Working on this in the afternoon and I'll have this done.
- This will be run on a quarterly basis. Since it's low friction, I may not code the full dynamic pipeline for this because it's relatively easy to do.

### 2025-05-07 [v0] (Chad Doorley)
- Initiating this project
- Reviving old UniqueTIN with newer portfolio key to accurately measure branch growth/decay
    - This was passed to Tito for Retail Dashboard development, but I have taken this project back
- Can leverage a lot of the work done already in other projects to get this Quarter over quarter comparison
- Spoke with John today:
    - nunique(df['portfolio_key']) when grouping by the branchname
    - 2025-03-31 vs 2024-12-31
- Will expand to be PowerBI dashboard, but it is the numbers he is interested in up front

## 4. Changelog
*(Newest changes at the top of this section. Use YYYY-MM-DD for dates.)*
### 2025-05-08 [v1.0.0-dev] (Chad Doorley)
- This was easy enough to do quickly in a notebook so I didn't build a dynamic pipeline.    
    - Added a second version today with address key.
    - Now there is a portfolio key and address key version