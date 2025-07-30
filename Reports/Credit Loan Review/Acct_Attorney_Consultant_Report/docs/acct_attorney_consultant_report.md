Accountant/Attorney/Consultant/Engineer Report
===
This project provides information of all extensions of credit to accountants, lawyers, consultants, appraisers, or similar individuals who have provided professional services to the institution since the last FDIC examination.

## Authors & Stakeholders
- Developed by: 
    - Troy Caron (troy.caron@bcsbmail.com)
- Key Stakeholders:
    - Credit Loan Review
    - Paul Kocak

## File Paths
- Project Home:
    - \\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Credit_Loan_Review\Acct_Attorney_Consultant_Report\
- Input Data:
    - Fetched from database
- Output:
    - \\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Credit_Loan_Review\Acct_Attorney_Consultant_Report\Production\output

## Overview of Pipeline
1. Go through cdutils pkey pipeline
2. Fetch other relevant data
3. Merge wh_persuserfields with wh_allroles on persnbr
4. Pull in names to merge on persnbr drop duplicate instances of acctnbrs with the same names on them, so that each person only shows up once per acctnbr
5. Merge previous dataframe with pkey workflow
6. Select and rename relevant columns
7. Filter out columns where Loan Customer Name is null
8. Sort by account number and then inside each account number group it is sorted by Loan Customer Name
9. Format and save to a .xlsx file.