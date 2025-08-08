# Daily Mismatched Debit Card Txns

## Project Overview
Generates a daily posting sheet for mismatched debit card transactions. The job:
- Fetches the latest CO_VSUS report from Identifi via API and saves it as a .txt into INPUT_DIR.
- Parses the text to extract transaction details and prepares a clean table.
- Fills an Excel template and saves the "Daily Posting Sheet MM-DD-YYYY.xlsx" to OUTPUT_DIR.
- Moves processed input files to INPUT_DIR/archive and previous workbooks to OUTPUT_DIR/archive.

## Authors & Stakeholders
- Project Lead: Patrick Quinn
- Developed by: Troy Caron (troy.caron@bcsbmail.com), Chad Doorley (chad.doorley@bcsbmail.com)
- Key Stakeholders: Risk Management, Deposit Operations

## Project Goals
- Automate creation of a consistent daily posting sheet from CO_VSUS.
- Reduce manual handling of text/PRN files and archiving.
- Prepare distribution-ready output for operations.

## Technology Stack
- Python 3.11+
- pandas, numpy, openpyxl
- requests, python-dotenv

## Project Status
- [x] Fetch latest CO_VSUS via API and save as .txt to INPUT_DIR
- [x] Parse and transform to posting sheet format
- [x] Archive rotation for input/output
- [-] Hardening and observability (error messages, logging)
- [ ] Automate distribution to Deposit Operations

Key
- [x] - Completed
- [-] - Partially completed
- [ ] - TODO

## File Paths
- Project Home:
  - \\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Risk Management\Daily Mismatched Debit Card Txns
- Input Data:
  - \\00-da1\Home\Share\Line of Business_Shared Services\Risk Management\Daily Mismatched Debit Card Txns\input
- Output:
  - \\00-da1\Home\Share\Line of Business_Shared Services\Risk Management\Daily Mismatched Debit Card Txns\output

## Documentation
- Project notes and recent run logs: ./project-notes.md

## Pipeline Steps (high level)
1) Download latest input
    - Use API search to get the newest CO_VSUS document (sorted by StorageDate descending).
    - Download the binary content from `/api/document/1/{PKID}/content`.
    - Save to INPUT_DIR as `CO_VSUS_{PKID}.txt`.
2) Select input file
    - Choose the newest .txt in INPUT_DIR; archive any older .txt files.
3) Parse and transform
    - Fixed-width read of key columns, filtering, grouping, and reshaping.
    - Compute debit/credit sign and enrich merchant values.
4) Archive input
    - Move the processed .txt to INPUT_DIR/archive.
5) Populate Excel template
    - Fill template cells with computed values and date.
6) Rotate and write output
    - Move prior workbooks in OUTPUT_DIR to OUTPUT_DIR/archive.
    - Save the new workbook as "Daily Posting Sheet MM-DD-YYYY.xlsx".

## Configuration & Security
- Configuration: `src/config.py` defines BASE_PATH, INPUT_DIR, OUTPUT_DIR, and environment awareness.
- API credentials: `src/daily_mismatch_txns/.env` (not committed); set:
  - IDENTIFI_API_KEY (and IDENTIFI_KEY_HEADER_NAME / IDENTIFI_USE_BEARER as required)
  - Optional: IDENTIFI_REFERER, IDENTIFI_ORIGIN, IDENTIFI_UA
- The downloader enforces HTTPS and does not log secrets.