# New Loan Report LR Credit

## Project Overview

Weekly loan report that provides a 45-day lookback of new loans for the Credit Loan Review team. The report includes two sections: NEW LOAN (all new loans) and CRA (Community Reinvestment Act relevant loans). This rebuilt version follows the template structure and uses the centralized cdutils package.

## Authors & Stakeholders
- **Project Lead:** Chad Doorley
- **Executive Sponsor:** Credit Loan Review Team
- **Key Stakeholders:**
  - Paul Kocak (paul.kocak@bcsbmail.com)
  - Linda Clark (linda.clark@bcsbmail.com)

## Project Goals

- Generate weekly report of new loans within 45-day lookback period
- Provide NEW LOAN section with all qualifying new loans
- Provide CRA section for Community Reinvestment Act compliance tracking
- Automate data fetching from COCC warehouse tables
- Format output as Excel file with multiple sheets
- Distribute report via email to stakeholders

## Technology Stack

- **Python 3.x** - Core programming language
- **pandas** - Data manipulation and analysis
- **SQLAlchemy** - Database connectivity and SQL queries
- **openpyxl** - Excel file generation
- **win32com** - Excel formatting and email distribution (Windows only)
- **cdutils** - Custom utility package for database connections and data processing
- **pytest** - Unit testing framework

## Project Status
- [x] Project structure rebuilt using template (2025-08-12)
- [x] Configuration updated with report-specific settings (2025-08-12)
- [x] Data fetching module created with all required tables (2025-08-12)
- [x] Core business logic migrated from Production code (2025-08-12)
- [x] Main entry point updated with proper flow (2025-08-12)
- [x] Unit tests created for core functionality (2025-08-12)
- [ ] Production testing and validation
- [ ] Email distribution testing
- [ ] Excel formatting validation
- [ ] Deploy to production environment

Key
- [x] - Completed
- [-] - Partially completed 
- [ ] - TODO

## File Paths
- `src/main.py` — Main entry point for the project (python -m src.main)
- `src/config.py` — Project configuration and environment settings
- `src/_version.py` — Version information for the project
- `src/new_loan_credit_lr/core.py` — Business logic and data processing
- `src/new_loan_credit_lr/fetch_data.py` — Data retrieval and SQL queries
- `tests/test_new_loan_report.py` — Unit tests using pytest framework
- `docs/README.md` — Project documentation and usage guide
- `notebooks/` — Jupyter notebooks for exploration and prototyping

## Documentation

### Business Logic

This report generates two primary outputs:

1. **NEW LOAN Sheet**: Contains all new loans from the last 45 days with the following filters:
   - Account types: CML (Commercial), MTG (Mortgage), MLN (Medical Loans)
   - Excludes CI07 minor account type codes
   - Only loans with origination dates within the last 45 days

2. **CRA Sheet**: Community Reinvestment Act relevant loans for compliance tracking

### Data Sources

The report pulls data from multiple COCC warehouse tables:
- `wh_acctcommon`: Account common information (names, addresses, balances)
- `wh_loans`: Loan-specific details (origination dates, loan amounts, FDIC categories)
- `wh_acctloan`: Account loan relationships (credit limits, risk ratings)
- `wh_org`: Organization details for business accounts
- `wh_prop`: Property information (part 1)
- `wh_prop2`: Property information (part 2)
- `househldacct`: Household account relationships for exposure calculations

### Key Features

- **45-Day Lookback**: Automatically calculates and filters for loans originated in the last 45 days
- **Exposure Calculations**: Uses pkey lookup database to calculate total exposures by household and primary key
- **Multi-Sheet Excel Output**: Formatted Excel file with NEW LOAN and CRA sheets
- **Email Distribution**: Automated email delivery to stakeholders (Windows/Outlook only)
- **Environment Awareness**: Different behavior for dev vs production environments

### Configuration

The report uses environment variables and configuration files:
- `REPORT_ENV=prod` for production mode
- SQLite pkey database path configurable via `PKEY_DB_PATH`
- Email recipients configured in `config.py`
- Output directory automatically created if it doesn't exist

---

## Usage
```bash
# Navigate to project directory
cd "Reports/Credit Loan Review/NewLoanReport_LR_Credit"

# Run the main process
python -m src.main

# Run unit tests
pytest tests/

# Run tests with verbose output
pytest tests/ -v
```

**Schedule:** Weekly automated execution

---

## Migration from Production Code

This report has been rebuilt from the Production folder code using the standardized template structure:

### Changes Made:
- Migrated from `src.cdutils` (local copy) to `cdutils` (package from venv)
- Updated data fetching to use current cdutils database connector
- Restructured business logic into modular `core.py` file
- Added comprehensive configuration via `config.py`
- Created proper unit tests with mocking
- Added environment-aware behavior (dev/prod)
- Maintained all original business logic and filtering rules

### Key Improvements:
- **Standardized Structure**: Follows template for consistency with other reports
- **Better Testing**: Comprehensive unit tests with mocking for database calls
- **Environment Separation**: Clear dev/prod behavior differences
- **Documentation**: Thorough documentation of business logic and data sources
- **Maintainability**: Modular structure makes updates and debugging easier

The core business logic remains identical to the Production version, ensuring continuity of report outputs while providing a more maintainable and testable codebase.
- Use environment variables for dev/prod switching and path management.
- Use the provided structure for easy integration with the monorepo and report runner system.

---

## Usage
```bash
# Navigate to project directory
cd Reports/YourBusinessLine/YourReportName

# Run the main process
python -m src.main

# Run unit tests
pytest tests/

# Run tests with verbose output
pytest tests/ -v
```

**Schedule:** Daily automated execution (or as specified in config.py)

---

This template is designed to be a clean, robust, and reusable starting point for any new analytics, reporting, or ETL project in the BCSB monorepo system. Follow the structure and conventions for seamless integration and maintainability.

