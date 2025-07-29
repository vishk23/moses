# Outputs Directory

This directory contains the final results from the ETL pipeline.

## Generated Files:
- `org_final_YYYYMMDD_HHMMSS.xlsx` - Final organization data with addresses and notes
- `pers_final_YYYYMMDD_HHMMSS.xlsx` - Final person data with addresses and notes

## File Contents:
- **Base Data**: Clean organization/person records linked to active accounts
- **Address Data**: Primary addresses merged from WH_ADDR
- **Additional Notes**: Extra columns from input files (if provided)
- **Timestamp**: Files named with processing timestamp for version control

## Usage:
These files are ready for analysis, reporting, or data quality review.
Files are automatically generated each time the pipeline runs.
