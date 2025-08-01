# SWAP PNC Report

## Project Overview
This report generates the monthly SWAP Exposure Loans analysis for Credit Loan Review, combining BCSB and PNC data sources. It stages, processes, and distributes a detailed Excel report to stakeholders.

## Authors & Stakeholders
- **Project Lead:** Business Intelligence Team
- **Executive Sponsor:** Credit Loan Review Management
- **Key Stakeholders:** Paul Kocak, Chad Doorley, Business Intelligence

## Project Goals
- Consolidate SWAP Exposure Loans data from BCSB and PNC
- Automate monthly report generation and distribution
- Provide actionable insights for loan officers and management

## Technology Stack
- Python 3.x
- pandas
- SQLAlchemy
- Custom modules: cdutils, src
- Excel for output

## Project Status
### Completed ✅
- Automated monthly execution
- Email distribution to stakeholders

### Future Enhancements
- Add more validation and error handling
- Expand reporting to additional loan categories
- Integrate with dashboard systems

## File Paths & Workflow
- **Input:** `assets/` folder (expects a single .xlsx file each run)
- **Staging:** Processed data saved to `assets/staged_data/staged_data.csv`
- **Archive:** Input .xlsx files moved to `assets/archive/`
- **Output:** Final report at `output/swap_pnc_report.xlsx`
- **Config:** All paths and recipients set in `src/config.py`

## Documentation
- See `Documentation/REPORTS_SYSTEM_DOCUMENTATION.md` for system-level details
- See `src/config.py` for all project settings

---

# SWAP PNC Project Structure & Usage Guide

This folder contains the source code and documentation for the SWAP PNC monthly report.

### Structure
```
SWAP PNC/
├── docs/                # Documentation, notes, and guides for the project
├── src/                 # Source code for the report
│   ├── config.py        # Project configuration (paths, recipients, etc.)
│   └── main.py          # Main entry point for the report workflow
├── assets/              # Input files and staging area
│   ├── archive/         # Archived input files
│   └── staged_data/     # Staged CSV data
├── output/              # Final Excel report
└── README.md            # This file (project structure and instructions)
```

### How to Use

1. Place the monthly PNC .xlsx file in the `assets/` folder.
2. Run the main process:
   ```bash
   python -m src.main
   ```
3. The workflow will:
   - Stage and archive the input file
   - Fetch and process data
   - Generate and format the Excel report
   - Email the report to recipients

### Execution & Scheduling
- Scheduled for monthly automated execution
- Can be run manually as needed

### Best Practices
- Keep all settings in `src/config.py`
- Ensure only one .xlsx file is present in `assets/` per run
- Archive and output folders are managed automatically
- Document changes and enhancements in `docs/`

---

## Usage Example
```bash
# Navigate to SWAP PNC directory
cd Reports/Credit Loan Review/SWAP PNC

# Run the report
python -m src.main
```

---

For questions, contact BusinessIntelligence@bcsbmail.com.

