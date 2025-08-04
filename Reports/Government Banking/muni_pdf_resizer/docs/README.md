# Muni Statement PDF Resizer
===
This project looks through all the Muni Statement pdfs for the previous month and adds a larger margin. This fixes a previous issue where data was getting cut off when printing these pdfs
<br>

## Authors & Stakeholders
- Developed by: 
    - Troy Caron (troy.caron@bcsbmail.com)
- Key Stakeholders:
    - Government Banking team

## File Paths
- Project Home:
    - \\00-da1\Home\Share\Line of Business_Shared Services\Government Banking\Muni Statements\Production\Output
- Input Data:
    - \\00-da1\Home\Share\Line of Business_Shared Services\Government Banking\Muni Statements\Production\Output\{year of previous month} - {previous month}
- Output:
    - \\00-da1\Home\Share\Line of Business_Shared Services\Government Banking\Muni Statements\Production\Output\{year of previous month} - {previous month}\resized

## Overview of Pipeline
1. Iterate through all pdf files in the input directory
2. Use PyMuPDF to add 20 margin points to each pdf file
3. Save each pdf to new resized directory