MRetail: Prime Time Travel Customers Report
===
This project provides information about customers that are included in Sharon Patton's Prime Time Travel program.

## Authors & Stakeholders
- Developed by: 
    - Troy Caron (troy.caron@bcsbmail.com)
- Key Stakeholders:
    - Stephanie Nordberg
    - Sharon Patton

## File Paths
- Project Home:
    - \\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Retail\Prime_Time_Travel_customers
- Input Data:
    - Fetched from database
- Output:
    - \\00-da1\Home\Share\Line of Business_Shared Services\Retail Banking\Prime_Time_Travel_customers\Production\output

## Overview of Pipeline
1. Fetch all relevant data from database
2. Keep only rows from persuserfield where the value PTTM or PTTR == Y, and create two new rows for PTTM and PTTR
3. Remove employee rows and rows with no persnbr and only keep rows in pkey where account status is ACT or NPFD
4. Merge data
5. Filter out irrelevant data and duplicates from merged dataframe
6. Sum up Net Balance (deposits) and Total Exposure (loans) for each persnbr
7. Aggregate data for final dataframe.
7. Export to excel and format.