# Accubranch Analysis Project

## Project Overview

The Accubranch Analysis project generates comprehensive account and transaction data for AccuBranch client analysis. This project processes banking data to create:

1. **Account Data**: Current account information with customer details, addresses, and account types
2. **Transaction Data**: Transaction history with customer mapping and branch information  
3. **Historical Analysis**: 5-year deposit history analysis by branch

## Authors & Stakeholders
- **Project Lead:** Data Analytics Team
- **Business Line:** Retail  
- **Owner:** Francine Ferguson
- **Key Stakeholders:** AccuBranch Analysis Team

## Project Goals

- Generate clean, comprehensive account data for AccuBranch analysis
- Process transaction data with proper customer identification
- Provide historical deposit trends by branch for 5-year analysis
- Maintain data quality through proper filtering and transformation

## Technology Stack

- **Python 3.x** with pandas, numpy
- **Database connectivity** via cdutils
- **cdutils.acct_file_creation** for account data generation
- **SQL queries** for data retrieval
- **CSV output** for client delivery

## Project Status
- [x] Account data processing pipeline (2025-08-12)
   - Current account data with customer details using cdutils
- [x] Transaction data processing pipeline (2025-08-12) 
   - Transaction history with customer mapping
- [x] Historical analysis functionality (2025-08-12)
   - 5-year branch deposit analysis
- [x] Project structure refactoring (2025-08-12)
   - Organized into proper template structure
   - Removed duplicate code, using cdutils.acct_file_creation

## File Paths
- `src/main.py` — Main entry point for the project (python -m src.main)
- `src/config.py` — Project configuration and environment settings
- `src/_version.py` — Version information for the project
- `src/accubranch/core.py` — Account data business logic and processing
- `src/accubranch/annual_deposit_history.py` — Historical deposit analysis
- `src/accubranch/join_functions.py` — Data joining utilities
- `src/transactions/core.py` — Transaction data business logic and processing
- `src/transactions/fetch_data.py` — Transaction data SQL queries and retrieval
- `tests/test_*.py` — Unit tests using pytest framework
- `docs/README.md` — Project documentation and usage guide
- `notebooks/` — Jupyter notebooks for exploration and prototyping
- `output/` — Generated CSV files for client delivery

## Configuration

All project settings are centralized in `src/config.py`:

```python
# Date configurations
CURRENT_DATA_DATE = None  # None = use latest, or set specific datetime
TRANSACTION_START_DATE = datetime(2024, 6, 30)
TRANSACTION_END_DATE = datetime(2025, 6, 30)

# Historical analysis years
HISTORICAL_YEARS = [
    {'year': 2020, 'date': '2020-12-31'},
    {'year': 2021, 'date': '2021-12-31'},
    # ... etc
]
```

## Usage

```bash
# Navigate to project directory
cd Reports/Retail/Accubranch

# Run the main process (generates both account and transaction data)
python -m src.main

# Run unit tests
pytest tests/

# Run tests with verbose output
pytest tests/ -v
```

## Output Files

The project generates three main output files:

1. **account_data.csv** - Current account information including:
   - Customer Primary Key (Tax Owner ID)
   - Address, City, State, Zip
   - Branch Association
   - Account Type (mapped to friendly names)
   - Date Account Opened
   - Current Balance
   - Original Balance (for loans)
   - Date of Birth

2. **transaction.csv** - Transaction data including:
   - Customer Unique ID
   - Date and Time of Transaction
   - Branch of Transaction
   - Type of Teller
   - Type of Transaction
   - Account Type

3. **five_yr_history.csv** - Historical deposit analysis:
   - 5-year deposit trends by branch
   - Time series analysis of deposit balances

## Data Processing Notes

### Account Data Processing
- **Uses cdutils.acct_file_creation.core.query_df_on_date()** for data generation
- Filters to loans and deposits only (CML, MLN, CNS, MTG, CK, SAV, TD)
- Excludes Municipal and Trust accounts (MUNI, TRST)
- Excludes ACH Manager products (CI07)
- Maps account types to friendly names
- Handles Small Business Loans separately
- Creates consolidated customer Primary Key
- Builds complete address fields

### Transaction Data Processing  
- Fetches transactions for configured date window
- Merges transaction data with account information
- Creates Customer Unique ID for tracking
- Parses datetime into separate date/time fields
- Maps account types consistently with account data

### Historical Analysis
- Processes 5 years of historical data (2020-2024)
- Uses same cdutils account generation for consistency
- Creates time series analysis for deposit trends
- Focuses on deposit account types for branch analysis

## Architecture Changes

### Refactoring from Original Structure

**Before:**
- Separate `main_account.py` and `main_transaction.py` files
- Duplicated fetch_data, core_transform, additional_fields modules
- Data_cleaning_main at root level
- Mixed logic in multiple locations

**After:**
- Single `src/main.py` entry point
- Centralized `src/config.py` for all settings
- Organized modules:
  - `src/accubranch/` - Account-specific logic
  - `src/transactions/` - Transaction-specific logic
- Uses `cdutils.acct_file_creation.core` instead of duplicated code
- Follows standard template structure

### Key Benefits

1. **Eliminates Code Duplication**: Uses cdutils instead of local copies
2. **Single Entry Point**: One command runs everything
3. **Centralized Configuration**: Easy to modify dates and settings
4. **Template Compliance**: Follows organizational standards
5. **Maintainable**: Clear separation of concerns

## Schedule
On-demand execution for AccuBranch analysis requests

## Documentation
- This README: project overview, business logic, and usage guide
- Inline code documentation for complex business rules and data transformations
- Unit tests in `tests/` folder provide examples of function usage and expected behavior
