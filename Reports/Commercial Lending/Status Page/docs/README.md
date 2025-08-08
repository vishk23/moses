# Project Title

Commercial Lending — Status Page (Client Resume)

## Project Overview

The Status Page is a single‑page “client resume” that provides a full snapshot of a commercial relationship, grouped on a portfolio key, for inclusion with Commercial approval documents. It consolidates loans, deposits, related entities, and summary metrics to support underwriting, portfolio reviews, and approvals.

Business logic (high level):
- Data ingestion: Pulls month‑end snapshots from COCC data marts (OSIBANK/OSIEXTN), including: WH_ACCTCOMMON, WH_ACCTLOAN, WH_LOANS, WH_ALLROLES, VIEWPERSTAXID, VIEWORGTAXID, WH_PERS, WH_ORG, and household tables. Active statuses only (ACT, NPFM, DORM) for core accounts.
- Core model: Join ACCTCOMMON + ACCTLOAN + LOANS on acctnbr, enforce schema, and sort by Total Exposure.
- Exposure math: Adjust book balance for tax‑exempt bonds (CM45 → NOTEBAL); compute Net Balance = bookbalance − COBAL; Net Available = AVAILBALAMT × (1 − TOTALPCTSOLD); Net Collateral Reserve = CREDLIMITCLATRESAMT × (1 − TOTALPCTSOLD); Total Exposure = sum of those.
- Portfolio filter: Filter on a provided portfolio_key; optional adds/deletes are applied safely (only valid acctnbrs are added/removed).
- Stratification: Categorize loans by adjusted call codes into CRE, C&I, HOA, Residential, Consumer, Indirect; append inactive dates; split into Commercial (CML) vs Personal.
- Deposits: Select CK/SAV/TD; attach daily deposit staging fields (TTM_AvgBal, YTDAvgBal, TTM days overdrawn); separate non‑loan/non‑deposit “Other”.
- Relationship title: Determine the household/entity name by the largest Total Exposure (CML, then Personal) else largest deposit book balance.
- Related entities: From WH_ALLROLES (roles Tax Owner, GUAR, OWN, LNCO) merge to person/org names and Tax IDs from VIEWPERSTAXID/VIEWORGTAXID; deduplicate by entity.
- Summary: Compute total commitments (Total Exposure), total outstanding (Net Balance), SWAP exposure, and deposit balance labeled YTD vs TTM based on effective‑date quarter.
- Output: Render CML, Personal, and Deposit sections (with summary rows) into an Excel template via pywin32, fit to a page for attachment to approval packages.

## Authors & Stakeholders
- **Project Lead:** Chad Doorley
- **Executive Sponsor:** Tim Chaves
- **Key Stakeholders:** Commercial Lending, Credit Administration, Underwriting, Portfolio Management

## Project Goals
- Provide a reliable, one‑page relationship snapshot grouped by portfolio key for credit approval and monitoring.
- Accurately compute single‑obligor exposure using Net Balance, availability, and collateral reserve adjustments.
- Enrich the view with related entities and Tax IDs for risk visibility.
- Automate Excel output aligned to the bank’s approval packet format.

## Technology Stack
- Python, pandas, NumPy, SQLAlchemy
- Internal library: cdutils (database, joining, loans.calculations, inactive_date, daily_deposit_staging, timezone, summary_row)
- Data sources: COCC (OSIBANK.WH_*, OSIEXTN.*)
- Output: Excel via pywin32/COM (Windows required for Excel automation)

## Project Status
- [x] (2025-08-08) Data extraction and core joins implemented
   - Fetch queries and schema enforcement; joining of core loan tables
- [x] (2025-08-08) Exposure, stratification, and summary metrics
   - Total Exposure math, loan/deposit sections, summary section
- [-] (2025-08-08) Excel template mapping and formatting
   - Writing to template with pywin32; finalize template ranges/styles
- [ ] (2025-08-08) Packaging with approval docs and CLI options
   - Wire portfolio_key inputs and add/delete overrides for on‑demand runs

Key
- [x] - Completed
- [-] - Partially completed 
- [ ] - TODO

## File Paths
- `src/main.py` — Orchestrates end‑to‑end run: fetch → transform → sections → summary → Excel output
- `src/fetch_data.py` — COCC SQL definitions and `cdutils.database.connect.retrieve_data` orchestration
- `src/core_transform.py` — Pipeline and business logic:
  - `main_pipeline`, `filtering_on_pkey`, `apply_adds_deletes`
  - Sections: `loan_section`, `deposit_section`
  - Relationship: `household_title_logic`, `related_entities`, `summary_section`
  - Final views: `final_cml`, `final_personal`, `final_deposits`
- `src/transformations/calculations.py` — Exposure math and data cleaning
- `src/transformations/joining.py` — Joins across core tables and property helpers
- `src/output_to_excel.py` — Excel template writer (pywin32)
- `tests/testing_functions.py` — Test helpers and utilities
- `docs/project-notes.md` — Notes and working details

## Documentation
- Project notes: `docs/project-notes.md`
- This README: high‑level overview and business logic summary

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
cd "Reports/Commercial Lending/Status Page"

# Run the main process
python -m src.main
```

### Arguments
- --email (required): Recipient email; must end with @bcsbmail.com
- --key (required, int): Portfolio key (up to 12 digits)
- --additions (optional, list[int]): Account numbers to force-include (each up to 20 digits)
- --deletes (optional, list[int]): Account numbers to exclude (each up to 20 digits)

Examples:
```bash
# Minimal run
python -m src.main --email your.name@bcsbmail.com --key 123456

# With additions and deletes
python -m src.main --email your.name@bcsbmail.com --key 123456 --additions 1234567890 222333444 --deletes 555666777
```

**Schedule:** Daily automated execution (or as specified in config.py)

---

This template is designed to be a clean, robust, and reusable starting point for any new analytics, reporting, or ETL project in the BCSB monorepo system. Follow the structure and conventions for seamless integration and maintainability.

