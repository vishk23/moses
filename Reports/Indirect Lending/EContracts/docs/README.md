Indirect Lending: E Contract Summary Report
===
This project aims to automate the process of generating the E Contract Summary Report. This process has been migrated from Alteryx to Python. 

## Authors & Stakeholders
- Developed by: 
    - Troy Caron (troy.caron@bcsbmail.com)
- Key Stakeholders:
    - Indirect Lending Dept.
    - Marlene Braganca

## File Paths
- Project Home:
    - \\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Indirect_Lending\EContracts
- Input Data:
    - \\00-da1\Home\Share\Line of Business_Shared Services\Indirect Lending\E Contract Summary Report\Production\Input
- Output:
    - \\00-da1\Home\Share\Line of Business_Shared Services\Indirect Lending\E Contract Summary Report\Production\Output

## Overview of Pipeline
1. Grab all the relevant data for the previous month (daily funding reports and book-to-look)
2. Concatenate all daily reports and merge with book-to-look on Dealer Name column
3. Change Contract Type column to 1s and 0s for easier calculations
4. Check that the number of rows from the combined funding reports is equal to the number of rows in the merged dataframe, otherwise there are probably errors in the data.
5. Build final report from relevant columns in the merged dataframe
6. Calculate totals by dealer and also grand total.
7. Export to excel and format.

### How every column is calculated:
Dealer Name -> merged dataframes on Dealer Name column <br>
Customer Name -> Applicant Name <br>
Funded Date -> Name of the daily funding report file <br>
Amt Financed -> Amount Financed <br>
\# of Apps Approved -> Application Approved <br>
\# of Apps Funded -> Count of contracts per Dealer Name (any type) <br>
\# of Econs Funded <br> -> Count of Econtracts per Dealer Name <br>
% of Econs Funded -> (# of Econs Funded) / (# of Apps Funded) per Dealer Name


#### The discrepancy between the grand total row and the numbers from the book to look recon is from the fact that I am only including the names of dealers who have at least 1 E-Contract. There are dealers in the daily funding reports that are not in this report that have contracts, but are strictly paper.
