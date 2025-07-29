Credit Loan Review: Portfolio Report
===
This project provides information about the deposits and loans relevant to Nancy Cabral, David Ferreira, and George Mendros.

## Authors & Stakeholders
- Developed by: 
    - Troy Caron (troy.caron@bcsbmail.com)
- Key Stakeholders:
    - Credit
    - Nancy Cabral, David Ferreira, George Mendros

## File Paths
- Project Home:
    - \\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Credit_Loan_Review\SBRM_Portfolio
- Input Data:
    - Fetched from database
- Output:
    - \\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Credit_Loan_Review\SBRM_Portfolio\\Production\output

## Overview of Pipeline
1. Fetch all relevant data from database
2. Filter wh_pers for 'acctrolecd' == 'SELO'
3. Left-join all data
4. Filter out where 'curracctstatcd' == 'CLS' or 'CO'
5. Split into a deposit dataframe and a loan dataframe where acctofficer and secondary officer (respectively) are Nancy, Dave, or George
6. Calculate summary dataframe for each Officer
7. Make individual dataframes for each Officer and their deposits/loans, sorted by descending bookbalance
8. Format and save all to a .xlsx file.

***The alteryx workflow in the ../Development/ folder is very helpful for a visual representation***