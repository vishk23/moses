# Project Title

Credit Loan Review — CRE Reporting Board

## Project Overview

The CRE Reporting Board project generates comprehensive Commercial Real Estate portfolio analysis for semi-annual board presentations. It processes loan portfolio data from the COCC data mart, performs complex property consolidation, applies FDIC call code categorization, and produces multiple specialized reports for PowerBI dashboard visualization and board reporting.

Business logic:
- Data ingestion: Queries COCC data mart tables including WH_ACCTCOMMON, WH_LOANS, WH_ACCTLOAN, WH_PROP, and WH_PROP2 as of specific reporting dates (e.g., June 30, 2025).
- Portfolio filtering: Excludes SWAP Exposure (CM09) and ACH Manager (CI07) products, focuses on CRE, C&I, and HOA loan categories.
- Property consolidation: For loans with multiple properties, selects the property type with highest total appraised value per account to ensure one-to-one loan-to-property relationships.
- Call code categorization: Groups FDIC call codes into business-meaningful categories (1-4 Family Construction, Construction, I-CRE, C&I, etc.) for reporting consistency.
- Construction loan identification: Enhanced filtering for construction loans includes both Cleaned Call Code = 'Construction' OR specific account types (CM07, CM08, CM79, CM81, ML02) to capture all construction-related lending.
- Property type grouping: Consolidates detailed property descriptions into standardized categories (Retail, Industrial, Hospitality, Mixed Use, etc.) for analysis.
- Balance calculations: Computes Net Balance (book balance - charged off amount), Total Exposure (net balance + net available + net collateral reserve), with special handling for Tax Exempt bonds (CM45).
- I-CRE production analysis: Tracks Income-Producing Commercial Real Estate (RENO/REMU) loan originations and balances across multiple years for trend analysis.
- Interest rate analysis: Identifies variable rate CML loans with upcoming rate changes versus hard maturity dates for PowerBI visualization using DAX logic.
- Report generation: Creates multiple Excel outputs including main CRE loader, I-CRE production summaries, call code totals, and construction loan details.

## Authors & Stakeholders
- **Project Lead:** Chad Doorley (chad.doorley@bcsbmail.com)
- **Executive Sponsor:** Tim Chaves
- **Key Stakeholders:** Linda Sternfelt, Credit & Loan Review

## Project Goals
- Automate semi-annual CRE portfolio reporting for board presentations
- Provide standardized categorization of loan and property types for consistent analysis
- Enable PowerBI dashboard refresh with clean, consolidated data
- Facilitate reconciliation with Federal Call Report numbers
- Track I-CRE production trends and portfolio growth over time

## Technology Stack
- Python, pandas, NumPy for data processing and analysis
- Internal library: cdutils (database connectivity, account file creation, input cleansing)
- Data sources: COCC data mart (COCCDM/OSIBANK tables)
- PowerBI for dashboard visualization with DAX calculations
- Alteryx for CML Variable Rate analysis (legacy component)
- Output: Multiple Excel files feeding PowerBI dashboard

## Project Status
- [x] (2025-02-15) Pipeline overhaul and consolidation [v2.0.0-prod]
   - Rebuilt complete processing pipeline for easier maintenance
   - Integrated CML Variable Rate logic into main pipeline
   - Updated paths post-drive conversion
- [x] (2025-02-15) Interest rate change analysis integration [v2.0.1-prod]
   - Eliminated separate Alteryx workflow for CML Variable Rate
   - Added rate change vs maturity flag logic directly in cre_loader.xlsx
   - Enhanced PowerBI visualization capabilities for interest rate analysis
- [x] (2025-08-11) Template compliance and version management
   - Updated to follow monorepo template structure
   - Added version tracking and standardized configuration

Key
- [x] - Completed
- [-] - Partially completed 
- [ ] - TODO

## File Paths
- `src/main.py` — Main entry point, orchestrates complete CRE reporting pipeline
- `src/config.py` — Configuration for FDIC call codes, property types, analysis years, paths
- `src/_version.py` — Version information for the project
- `src/cre_board_reporting/core.py` — Core business logic: data processing, property consolidation, categorization
- `src/cre_board_reporting/fetch_data.py` — COCC database queries for loan and property data
- `output/cre_loader.xlsx` — Main consolidated CRE portfolio data for PowerBI
- `output/icre_production.xlsx` — I-CRE loan origination analysis by year
- `output/icre_balances.xlsx` — I-CRE portfolio balance trends by year
- `output/total_cml.xlsx` — CML totals by call code categories
- `dashboard/CRE_Dashboard.pbix` — PowerBI dashboard for board presentations
- `bin/CML VAR with Rate Change_v2.yxmd` — Alteryx workflow (legacy)

## Documentation
- This README: project overview, business logic, and usage guide
- [Technical Documentation](./Technical/technical_doc.md): Comprehensive technical details, filters, calculations, and changelog
- [Daily Notes](./Technical/daily_notes.md): Development activities, technical decisions, and ongoing updates
- Inline code documentation for complex business rules and data transformations

---

## Usage
```bash
# Navigate to project directory
cd "Reports/Credit Loan Review/CRE_Reporting_Board"

# Run the complete CRE reporting pipeline
python -m src.main

# This generates all output files:
# - cre_loader.xlsx (main portfolio data)
# - icre_production.xlsx (I-CRE origination analysis)
# - icre_balances.xlsx (I-CRE balance trends)
# - total_cml.xlsx (call code summaries)
# - icre.xlsx (detailed I-CRE current portfolio)
# - construction.xlsx (construction loan details)

# After Python processing, refresh PowerBI dashboard:
# Open dashboard/CRE_Dashboard.pbix and refresh data sources
```

**Input Requirements:**
- COCC data mart access for loan and property tables
- Reporting date configuration in core.py (currently set to June 30, 2025)
- FDIC call code and property type groupings defined in config.py

**Output Files:**
- `output/cre_loader.xlsx` — Main consolidated dataset for PowerBI dashboard
- `output/icre_production.xlsx` — I-CRE origination trends (2022-2024)
- `output/icre_balances.xlsx` — I-CRE balance growth analysis
- `output/total_cml.xlsx` — CML totals by call code categories
- `output/icre.xlsx` — Current I-CRE portfolio details
- `output/construction.xlsx` — Construction loan portfolio analysis (includes Cleaned Call Code = 'Construction' OR account types CM07, CM08, CM79, CM81, ML02)

**Schedule:** Semi-annual execution (upon request from Tim Chaves/Linda Sternfelt)

**Validation:** Reconcile total CML figures with Federal Call Report numbers using provided accounting worksheets

---

This project streamlines CRE portfolio reporting by automating data consolidation, standardizing categorization, and feeding clean data into PowerBI dashboards for executive presentations. The pipeline handles complex property relationships, applies business rules for loan categorization, and generates multiple analytical views of the Commercial Real Estate portfolio.

