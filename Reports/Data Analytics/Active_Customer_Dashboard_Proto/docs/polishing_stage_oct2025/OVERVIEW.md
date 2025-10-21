# Customer 360 Dashboard - Overview

## Purpose
Customer 360 is a PowerBI dashboard for analyzing loans and deposits at the account and portfolio level. It provides time-based balance comparisons and portfolio analytics.

## Architecture

**Data Pipeline Flow:**
```
Source Data → Python ETL → Delta Tables → PowerBI Dashboard
```

## Python ETL Process (src/)

**Entry Point:** `main.py`
- Orchestrates the pipeline via `deposit_dash_prototype.core.main_pipeline()`
- Outputs three Delta tables written to local C: drive for PowerBI consumption:
  - `dim_account` - Account dimension table
  - `fact_balances` - Balance facts across time periods
  - `portfolio_deriv` - Portfolio-level aggregations

**Core Pipeline Logic:** `deposit_dash_prototype/core.py`

1. **Data Acquisition** - Pulls three time-based snapshots:
   - **Current snapshot**: From Silver lakehouse Delta table (`SILVER/account`)
   - **Year-end snapshot**: December 31, 2024 (via `cdutils.acct_file_creation.core.query_df_on_date`)
   - **Prior month-end snapshot**: September 30, 2025 (via same method)

2. **Account Classification**:
   - Maps account types to Macro Account Type:
     - **Loans**: CML, MLN, CNS, MTG
     - **Deposits**: CK, SAV, TD

3. **Data Modeling** - Creates dimensional model from unioned snapshots:

   **dim_account** (Dimension Table):
   - Account attributes without balances
   - Includes: account numbers, owner names, products, dates, tax info, officers, rates, branch, location, portfolio/ownership/household keys
   - Deduped on `effdate + acctnbr`

   **fact_balances** (Fact Table):
   - Balance measures across all time periods
   - Includes: note amounts, book balance, note balance, credit limits, available balances, collateral reserves, net calculations, exposures
   - Allows time-series analysis

   **portfolio** (Portfolio Dimension):
   - Aggregated at `portfolio_key` level
   - Metrics:
     - Muni presence indicator (Y/N)
     - Category (Consumer/Business/Mixed) - derived from tax reporting fields
     - Total loan balance
     - Total deposit balance
     - Unique loan count
     - Unique deposit count

**Utilities:**
- `utils/parquet_io.py`: Adds UTC load timestamps to all output tables
- `utils/misc.py`: Column coalescing helper function

## PowerBI Layer

PowerBI connects to the Delta tables and calculates DAX measures:
- **Current Balance** - from current snapshot
- **Prior Year End Balance** - from year-end snapshot (2024-12-31)
- **Total Balance** - aggregations
- **YTD Balance Change** - delta between current and year-end

## Key Design Patterns

1. **Dimensional Modeling**: Separates attributes (dim) from measures (fact) for efficient querying
2. **Time-Based Snapshots**: Maintains historical points-in-time for comparison analysis
3. **Portfolio Aggregation**: Pre-calculates portfolio rollups for dashboard performance
4. **Delta Lake Format**: Enables schema evolution and efficient querying from PowerBI
5. **Lakehouse Architecture**: Bronze/Silver/Gold pattern (uses Silver as source)

## Data Flow Summary

```
SILVER/account (current) ─┐
Year-end query (12/31/24) ├─→ Union → Split → dim_account ──┐
Month-end query (9/30/25) ─┘                → fact_balances ├─→ PowerBI → Measures
                                            → portfolio ─────┘
```
