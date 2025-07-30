This project generates daily posting sheets by parsing txt files that are dropped in the input folder.

## Authors & Stakeholders
- Developed by: 
    - Troy Caron (troy.caron@bcsbmail.com)
- Key Stakeholders:
    - Risk Management

## File Paths
- Project Home:
    - \\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Risk Management\Daily Mismatched Debit Card Txns
- Input Data:
    - \\00-da1\Home\Share\Line of Business_Shared Services\Risk Management\Daily Mismatched Debit Card Txns\input
- Output:
    - \\00-da1\Home\Share\Line of Business_Shared Services\Risk Management\Daily Mismatched Debit Card Txns\output

## Overview of Pipeline
1. Ensure there is only one txt file in input folder and read in the contents
2. Parse it
    - use .split() on contents to split by whitespace and initialize a deque on that data
    - initialize lists to hold the relevant data
    - append relevant data to lists and continually pop from the front of the deque until you have reached the footer
3. Now that the file has been parsed, move it to the input/archive folder
4. Use parsed data to fill in the template
5. Move all files currently in output folder (previous daily sheet) to output/archive folder
6. Save daily posting sheet to output folder