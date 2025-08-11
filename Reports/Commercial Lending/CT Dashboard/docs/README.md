# Project Title

Commercial Lending — CT Dashboard

## Project Overview

The CT Dashboard processes covenant and tickler tracking reports from the bank's covenant tracking system. It ingests HTML exports saved as .xls files, enriches them with loan officer and deposit officer assignments from COCC data, and produces formatted Excel tracking files for Commercial Lending teams.

Business logic:
- Data ingestion: Processes up to 3 HTML files (saved with .xls extension) from input/ folder containing covenant and tickler data exported from the tracking system.
- Report parsing: Extracts standardized data including customer names, item details, required/actual values, dates, and comments from HTML tables.
- Officer enrichment: Fetches officer assignments (loan officer, deposit officer) from OSIBANK.WH_ACCTCOMMON by customer name using statistical mode. Falls back to related entity data from WH_ALLROLES for missing assignments.
- Data merging: Combines tracking data with officer assignments, normalizes date fields, and applies business rules for officer fallback logic.
- Output generation: Creates two Excel files with multiple sheets: CT_Covenant_Tracking.xlsx (Past Due, In Default) and CT_Tickler_Tracking.xlsx (Past Due).
- Excel formatting: Applies consistent formatting including auto-fit columns, bold headers, frozen panes, and date/currency number formats.
- File archival: Moves processed HTML files to input/archive to prevent reprocessing.

## Authors & Stakeholders
- **Project Lead:** Chad Doorley
- **Executive Sponsor:** Tim Chaves
- **Key Stakeholders:** Commercial Lending (Laurie Williams), Credit Administration, Risk Management

## Project Goals
- Automate processing of covenant and tickler tracking exports to reduce manual effort
- Enrich tracking data with current officer assignments for routing and follow-up
- Provide consistent, formatted Excel outputs for Commercial Lending workflow integration
- Maintain data quality through validation and standardized column mapping

## Technology Stack
- Python, pandas, NumPy, lxml for HTML parsing
- Internal library: cdutils (database connectivity, data cleansing, deduplication)
- Data sources: Covenant tracking system HTML exports, OSIBANK tables (WH_ACCTCOMMON, WH_ALLROLES, WH_ORG, WH_PERS)
- Output: Excel via openpyxl and pywin32/COM for formatting (Windows required for advanced formatting)

## Project Status
- [x] (2025-08-11) HTML parsing and data standardization implemented
   - Extract covenant/tickler data from HTML tables with flexible column mapping
- [x] (2025-08-11) Officer assignment enrichment and fallback logic
   - COCC data fetch, mode calculation, related entity fallback for missing officers
- [x] (2025-08-11) Excel output generation and formatting
   - Multi-sheet Excel files with consistent formatting and archival of source files
- [x] (2025-08-11) Template structure compliance and configuration management
   - Proper package structure, config-driven paths, clean imports

Key
- [x] - Completed
- [-] - Partially completed 
- [ ] - TODO

## File Paths
- `src/main.py` — Main entry point, imports config and calls core business logic
- `src/config.py` — Configuration for paths, recipients, report metadata
- `src/ct_dashboard/core.py` — Main business logic: ingest → enrich → output pipeline
- `src/ct_dashboard/fetch_data.py` — COCC database queries for officer assignments
- `src/ct_dashboard/ingest.py` — HTML parsing and standardization of tracking data
- `src/ct_dashboard/rel_entity_officer.py` — Related entity officer lookup for fallback assignments
- `src/ct_dashboard/output_to_excel_multiple_sheets.py` — Excel formatting utilities
- `input/` — Input folder for HTML files (processed files moved to input/archive)
- `output/` — Generated Excel tracking files

## Documentation
- This README: project overview, business logic, and usage guide
- Inline code documentation for complex business rules and data transformations

---

# Template Project Structure & Usage Guide

This folder provides a starter template for new report or data pipeline projects. Copy this folder and use it as a base for new work.

### Structure
```
project_name/
├── docs/                   # Documentation, notes, and guides for the project
│   └── README.md           # This file (project structure, business logic, usage guide)
├── notebooks/              # Jupyter notebooks for exploration or prototyping
├── src/                    # Source code for the project
│   ├── __init__.py         # Makes src a Python package (required for python -m src.main)
│   ├── config.py           # Project configuration (edit this first!)
│   ├── main.py             # Main entry point for the project (python -m src.main)
│   └── project_name/       # Project-specific logic (replace with your project name)
│       ├── __init__.py     # Makes project_name a package
│       ├── core.py         # Business logic for the report (all processing, transformation, output)
│       └── fetch_data.py   # SQL/data fetching logic (all queries and data retrieval)
```

### How to Use

1. **Copy the entire `template_project` folder** to your new project location and rename as needed.
2. **Edit `src/config.py`** to fill in your project-specific details (name, business line, schedule, owner, paths, etc). This file should:
   - Define all project metadata (REPORT_NAME, BUSINESS_LINE, SCHEDULE, OWNER)
   - Set up environment-aware paths (dev/prod) using `os.getenv('REPORT_ENV', 'dev')`
   - Create `OUTPUT_DIR` and `INPUT_DIR` using pathlib
   - Specify email recipients for production and development
   - Be the only place for configuration and environment logic
3. **Write your main logic in `src/main.py`**. This file should:
   - Import `src.config` for all configuration
   - Print key config values for logging
   - Import and call your business logic from `src/project_name/core.py`
   - Handle output file creation and email distribution
   - Be executable as a module: `python -m src.main`
4. **Add any supporting modules** to the `src/project_name/` folder as needed (e.g., output formatting, validation).
5. **Document your project** in the `docs/` folder and keep notes up to date.
6. **Use the `notebooks/` folder** for prototyping, data exploration, or sharing examples.

### Execution

- The runner will change directory into the project root and execute:
  ```
  python -m src.main
  ```
- Make sure all imports are relative to the `src/` folder and configuration is handled via `config.py`.
- The `src/__init__.py` and `src/project_name/__init__.py` files are required for Python package/module resolution.

### Best Practices

- Keep all project-specific settings in `config.py`.
- Avoid hardcoding paths or credentials in code files.
- Use the `OUTPUT_DIR` and `INPUT_DIR` variables for file operations.
- Keep documentation and notebooks organized for future reference.
- Place all business logic in `core.py` and all data fetching in `fetch_data.py`.
- Use environment variables for dev/prod switching and path management.
- Use the provided structure for easy integration with the monorepo and report runner system.

---

## Usage
```bash
# Navigate to project directory
cd "Reports/Commercial Lending/CT Dashboard"

# Place HTML files (saved as .xls) in the input folder
# Files should be exports from covenant/tickler tracking system

# Run the main process
python -m src.main
```

**Input Requirements:**
- Up to 3 HTML files saved with .xls extension in `input/` folder
- Files should contain covenant or tickler tracking data with recognizable report titles
- Supported report types: "covenants past due", "covenants in default", "ticklers past due"

**Output Files:**
- `output/CT_Covenant_Tracking.xlsx` (sheets: Past Due, In Default)
- `output/CT_Tickler_Tracking.xlsx` (sheet: Past Due)
- Processed input files moved to `input/archive/`

**Schedule:** Monthly processing (or as needed when new tracking exports are available)

---

This template is designed to be a clean, robust, and reusable starting point for any new analytics, reporting, or ETL project in the BCSB monorepo system. Follow the structure and conventions for seamless integration and maintainability.

