# Loan Branch Officer Report

## Project Overview

The Loan Branch Officer Report provides a comprehensive view of the bank's loan portfolio organized by branch and loan officer. This report enables loan officer performance tracking, portfolio analysis, and supports business line reporting and management oversight.

## Authors & Stakeholders
- **Project Lead:** Business Intelligence Team
- **Executive Sponsor:** Retail Banking
- **Key Stakeholders:** Loan Officers, Branch Managers, Retail Banking Management

## Project Goals

- Generate comprehensive loan portfolio reports organized by branch and officer
- Support loan officer performance tracking and analysis
- Enable portfolio monitoring and risk assessment
- Facilitate customer relationship management through household linking
- Provide automated reporting with standardized formatting

## Technology Stack

- **Database:** OSIBANK (WH_ACCTCOMMON, WH_LOANS, WH_ACCTLOAN), OSIEXTN (HOUSEHLDACCT)
- **Processing:** Python, Pandas, cdutils libraries
- **Output:** Excel (XLSX format)
- **Distribution:** Email via cdutils.distribution

## Project Status
### Completed ✅
- Data extraction from core loan tables
- Account relationship joining and validation
- Total exposure calculations and loan categorization
- Primary key and household number assignment
- Secondary loan officer attachment
- Excel output generation with proper formatting
- Column filtering and renaming for business requirements
- Error handling and logging
- Environment-aware configuration (dev/prod)

### Future Enhancements
- Excel formatting automation (borders, bold headers, auto-fit columns)
- Additional loan categorization rules
- Performance optimization for large datasets
- Dashboard integration capabilities

## File Paths

### Development
- **Input:** `Reports/Retail/Loan Branch Officer Report/input/`
- **Output:** `Reports/Retail/Loan Branch Officer Report/output/`

### Production
- **Base Path:** `\\00-DA1\Home\Share\Line of Business_Shared Services`
- **Output File:** `loan_report_branch_officer_[Month]_[Year].xlsx` (e.g., `loan_report_branch_officer_July_2025.xlsx`)

## Documentation

### Business Logic
The report processes loan data through the following steps:
1. Fetches data from OSIBANK core tables (accounts, loans, loan details)
2. Joins tables on account number with validation
3. Calculates net balances and total exposure
4. Adds primary keys and household numbers
5. Attaches secondary loan officers
6. Categorizes loans by product type
7. Generates owner_id for customer identification (O prefix for organizations, P prefix for persons)
8. Filters to required columns and formats for output
9. Names output file with report period (previous month and year)

### Key Calculations
- **Net Balance:** Book Balance - Charged Off Balance (COBAL)
- **Total Exposure:** Net Balance + Net Available + Net Collateral Reserve
- **Tax Exempt Bonds:** Uses NOTEBAL for CM45 products instead of BOOKBALANCE
- **Owner ID:** Formatted as "O{org_number}" for organizations or "P{person_number}" for individuals

### Data Sources
- **OSIBANK.WH_ACCTCOMMON:** Core account information, balances, officers, branches
- **OSIBANK.WH_LOANS:** Loan-specific details, origination, terms
- **OSIBANK.WH_ACCTLOAN:** Credit limits, percentages sold, collateral reserves
- **OSIEXTN.HOUSEHLDACCT:** Customer household relationships

---

## Usage
```bash
# Navigate to project directory
cd "Reports/Retail/Loan Branch Officer Report"

# Run the main process
python -m src.main
```

**Schedule:** As Needed

---

**Maintained By:** BCSB Business Intelligence Team
