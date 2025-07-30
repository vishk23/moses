This project provides Commercial Lending Officer (CLO) active portfolio analysis organized 
by responsibility officer with subtotals and detailed loan information.

## Authors & Stakeholders
- Developed by: 
    - Troy Caron (troy.caron@bcsbmail.com)
- Key Stakeholders:
    - Commercial Lending

## File Paths
- Project Home:
    - \\00-DA1\Home\Share\\Data & Analytics Initiatives\\Project Management\\Commercial_Lending\\CLO_ActivePortfolio_Officer_Report
- Input Data:
    - Fetched from database
- Output:
    - \\00-DA1\Home\Share\\Data & Analytics Initiatives\\Project Management\\Commercial_Lending\\CLO_ActivePortfolio_Officer_Report\\Production\\output

## Overview of Pipeline
1. Follow the pkey pipeline from cdutils (with a few extra columns and filters selected in src.fetch_data), for reference, view bottom of spreadsheet file in Documentation
2. Append SBA Expiration Date column from wh_acctuserfields table
3. Rename columns for readability
4. Keep relevant columns, and then sort
5. Build row for totals for each Responsibility Officer
6. Export and format dataframe