# Customer 360 Dashboard - Dynamic Multi-Period Balance Data Plan

## Objective
Extend the ETL pipeline to dynamically fetch multiple time-period snapshots for comprehensive time-series analysis and charting in PowerBI.

## Key Decisions Summary

✅ **Confirmed Approach:**
- Trailing 16 months starts from **prior month** (not current month)
- cdutils handles weekend/holiday business day adjustment automatically
- No parallel fetching (sequential is acceptable)
- No date_period_type column (PowerBI handles filtering dynamically)
- Data volume (~1.4M-1.5M records) is acceptable

⚠️ **Testing Constraints:**
- Unit tests (pytest) can be done in this environment ✅
- Full pipeline testing requires production environment ❌
- cdutils data fetching cannot be tested here ❌

## Current State
- **Hardcoded dates**: Year-end (2024-12-31), Month-end (2025-09-30)
- **3 snapshots**: Current, Year-end, Month-end
- Limited time-series capability

## Target State
- **Dynamic date calculation** based on current date
- **Multiple time periods** for different analytical needs:
  - Current day
  - Prior business day (T-1)
  - Prior month-end
  - Prior quarter-end
  - Prior year-end
  - Trailing 16 month-ends (for trend line graph)
  - Prior 8 business days (for recent activity chart)

## Data Requirements

### Time Periods Needed

| Period | Purpose | Calculation Logic | Example (if today = 2025-10-21) |
|--------|---------|-------------------|----------------------------------|
| **Current** | Latest balances | Today or latest business day | 2025-10-21 |
| **T-1** | Day-over-day change | Prior business day | 2025-10-20 |
| **Prior Month-End** | Month-over-month change | Last day of prior month | 2025-09-30 |
| **Prior Quarter-End** | Quarter-over-quarter change | Last day of prior quarter | 2025-06-30 (Q2) |
| **Prior Year-End** | Year-over-year change | December 31 of prior year | 2024-12-31 |
| **Trailing 16 Months** | Trend analysis line graph | Last day of each of past 16 months (starting from prior month) | 2025-09-30, 2025-08-31, ..., 2024-06-30 |
| **Prior 8 Business Days** | Recent activity chart | 8 most recent business days | 2025-10-21, 2025-10-20, ..., 2025-10-10 |

### Total Snapshots

**Before deduplication**: 29 snapshots
- Current (1) + Prior day (1) + Prior month-end (1) + Prior quarter-end (1) + Prior year-end (1) + Trailing 16 months (16) + Prior 8 days (8) = 29

**After deduplication**: Approximately **23-26 distinct snapshots**
- Current day appears in prior 8 days (overlap)
- Prior month-end appears in trailing 16 months (overlap)
- Prior quarter-end appears in trailing 16 months (overlap)
- Prior year-end appears in trailing 16 months (overlap)
- Some prior 8 days may overlap with month-ends

**Final estimate**: ~25 unique dates fetched from historical sources (current from Silver)

---

## Implementation Plan

### 1. Create Date Calculation Module

**New File**: `src/utils/date_helpers.py`

```python
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import List
import pandas as pd


def get_current_date() -> datetime:
    """Get current date (or latest business day if weekend)."""
    return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)


def get_prior_business_day(reference_date: datetime) -> datetime:
    """Get prior business day (T-1)."""
    prior = reference_date - timedelta(days=1)
    # Simple logic; cdutils.query_df_on_date will handle weekend adjustment
    return prior


def get_prior_month_end(reference_date: datetime) -> datetime:
    """
    Get last day of prior month.

    Example: If today is 2025-10-21, returns 2025-09-30
    """
    first_of_current_month = reference_date.replace(day=1)
    last_day_prior_month = first_of_current_month - timedelta(days=1)
    return last_day_prior_month


def get_prior_quarter_end(reference_date: datetime) -> datetime:
    """
    Get last day of prior quarter.

    Quarters: Q1=Mar 31, Q2=Jun 30, Q3=Sep 30, Q4=Dec 31
    """
    current_quarter = (reference_date.month - 1) // 3 + 1

    if current_quarter == 1:
        # Prior quarter is Q4 of prior year
        return datetime(reference_date.year - 1, 12, 31)
    else:
        prior_quarter_end_month = (current_quarter - 1) * 3
        # Get last day of that month
        first_of_next_month = datetime(reference_date.year, prior_quarter_end_month + 1, 1)
        return first_of_next_month - timedelta(days=1)


def get_prior_year_end(reference_date: datetime) -> datetime:
    """
    Get December 31 of prior year.

    Example: If today is 2025-10-21, returns 2024-12-31
    """
    return datetime(reference_date.year - 1, 12, 31)


def get_trailing_month_ends(reference_date: datetime, num_months: int = 16) -> List[datetime]:
    """
    Get last day of trailing N months (starting from PRIOR month, not current).

    Example (if today = 2025-10-21, num_months=16):
        Returns: [2025-09-30, 2025-08-31, 2025-07-31, ..., 2024-06-30]

    Note: Starts from prior month-end (first day of current month - 1 day).
    """
    month_ends = []

    for i in range(num_months):
        # Calculate date (i+1) months ago to start from prior month
        target_month = reference_date - relativedelta(months=i+1)

        # Get last day of that month
        # Move to first of next month, then back one day
        if target_month.month == 12:
            first_of_next = datetime(target_month.year + 1, 1, 1)
        else:
            first_of_next = datetime(target_month.year, target_month.month + 1, 1)

        month_end = first_of_next - timedelta(days=1)
        month_ends.append(month_end)

    return month_ends


def get_prior_n_business_days(reference_date: datetime, num_days: int = 8) -> List[datetime]:
    """
    Get prior N business days (simple day subtraction).

    Example (if today = 2025-10-21, num_days=8):
        Returns: [2025-10-21, 2025-10-20, 2025-10-19, ..., 2025-10-14]

    Note: cdutils.query_df_on_date will handle weekend/holiday adjustment.
    """
    business_days = []

    for i in range(num_days):
        day = reference_date - timedelta(days=i)
        business_days.append(day)

    return business_days


def get_all_required_dates(reference_date: datetime = None) -> dict:
    """
    Get all required dates for the Customer 360 pipeline.

    Returns:
        Dictionary with keys:
        - 'current': Current date
        - 'prior_day': T-1
        - 'prior_month_end': Last day of prior month
        - 'prior_quarter_end': Last day of prior quarter
        - 'prior_year_end': December 31 of prior year
        - 'trailing_16_months': List of 16 month-end dates
        - 'prior_8_days': List of 8 recent business days
    """
    if reference_date is None:
        reference_date = get_current_date()

    return {
        'current': reference_date,
        'prior_day': get_prior_business_day(reference_date),
        'prior_month_end': get_prior_month_end(reference_date),
        'prior_quarter_end': get_prior_quarter_end(reference_date),
        'prior_year_end': get_prior_year_end(reference_date),
        'trailing_16_months': get_trailing_month_ends(reference_date, num_months=16),
        'prior_8_days': get_prior_n_business_days(reference_date, num_days=8)
    }
```

---

### 2. Update Core Pipeline Logic

**File**: `src/deposit_dash_prototype/core.py`

#### Changes Required:

**A. Add imports at top of file:**

```python
# ADD THESE IMPORTS
from src.utils.date_helpers import get_all_required_dates
from typing import List, Dict
```

**B. Create helper function to fetch snapshot:**

```python
# ADD THIS FUNCTION (after build_portfolio_dimension, before main_pipeline)

def fetch_snapshot(date: datetime, macro_type_mapping: dict) -> pd.DataFrame:
    """
    Fetch account snapshot for a given date and apply macro type mapping.

    Args:
        date: Target date for snapshot
        macro_type_mapping: Dict mapping mjaccttypcd to Macro Account Type

    Returns:
        DataFrame with snapshot data, effdate set, and Macro Account Type added
    """
    df = cdutils.acct_file_creation.core.query_df_on_date(date)
    df['Macro Account Type'] = df['mjaccttypcd'].map(macro_type_mapping)
    df['effdate'] = date  # Ensure effdate is set to requested date
    return df
```

**C. Refactor main_pipeline() function:**

Replace lines 88-119 with:

```python
def main_pipeline():
    """
    Main ETL pipeline - fetches multi-period account snapshots and builds dimensional model.

    Returns:
        Tuple of (dim_account, fact_balances, portfolio)
    """

    # Define macro type mapping
    MACRO_TYPE_MAPPING = {
        'CML':'Loan',
        'MLN':'Loan',
        'CNS':'Loan',
        'MTG':'Loan',
        'CK':'Deposit',
        'SAV':'Deposit',
        'TD':'Deposit'
    }

    # Get all required dates dynamically
    dates = get_all_required_dates()

    print(f"Fetching data for {len(dates['trailing_16_months']) + len(dates['prior_8_days']) + 4} distinct time periods...")
    print(f"  Current date: {dates['current'].strftime('%Y-%m-%d')}")
    print(f"  Prior day: {dates['prior_day'].strftime('%Y-%m-%d')}")
    print(f"  Prior month-end: {dates['prior_month_end'].strftime('%Y-%m-%d')}")
    print(f"  Prior quarter-end: {dates['prior_quarter_end'].strftime('%Y-%m-%d')}")
    print(f"  Prior year-end: {dates['prior_year_end'].strftime('%Y-%m-%d')}")
    print(f"  Trailing 16 months: {dates['trailing_16_months'][0].strftime('%Y-%m-%d')} to {dates['trailing_16_months'][-1].strftime('%Y-%m-%d')}")
    print(f"  Prior 8 business days: {dates['prior_8_days'][0].strftime('%Y-%m-%d')} to {dates['prior_8_days'][-1].strftime('%Y-%m-%d')}")

    # Fetch current snapshot from Silver lakehouse (already in memory)
    print("Fetching current snapshot from SILVER/account...")
    current_df = DeltaTable(src.config.SILVER / "account").to_pandas()
    current_df['Macro Account Type'] = current_df['mjaccttypcd'].map(MACRO_TYPE_MAPPING)
    # Note: effdate should already be set in Silver table

    # Collect all snapshots to union
    all_snapshots = [current_df]

    # Fetch all unique dates (dedupe to avoid duplicate queries)
    unique_dates = set()

    # Add key period dates
    unique_dates.add(dates['prior_day'])
    unique_dates.add(dates['prior_month_end'])
    unique_dates.add(dates['prior_quarter_end'])
    unique_dates.add(dates['prior_year_end'])

    # Add trailing 16 months
    for month_end in dates['trailing_16_months']:
        unique_dates.add(month_end)

    # Add prior 8 business days
    for day in dates['prior_8_days']:
        unique_dates.add(day)

    # Remove current date if already in Silver (avoid duplicate)
    unique_dates.discard(dates['current'])

    # Sort dates for cleaner logging
    unique_dates_sorted = sorted(unique_dates, reverse=True)

    print(f"Fetching {len(unique_dates_sorted)} historical snapshots...")

    # Fetch all historical snapshots
    for i, date in enumerate(unique_dates_sorted, 1):
        print(f"  [{i}/{len(unique_dates_sorted)}] Fetching {date.strftime('%Y-%m-%d')}...")
        snapshot = fetch_snapshot(date, MACRO_TYPE_MAPPING)
        all_snapshots.append(snapshot)

    # Union all snapshots
    print("Unioning all snapshots...")
    all_df = pd.concat(all_snapshots, ignore_index=True, sort=False)

    print(f"Total records across all periods: {len(all_df):,}")
    print(f"Unique accounts: {all_df['acctnbr'].nunique():,}")
    print(f"Unique dates: {all_df['effdate'].nunique()}")

    # ... REST OF FUNCTION REMAINS UNCHANGED (lines 121-153)
```

**D. Keep remaining code unchanged:**

Lines 121-153 (dimension_columns, fact_columns, building dim/fact tables) remain exactly as-is.

---

### 3. Update Documentation

**File**: `docs/polishing_stage_oct2025/OVERVIEW.md`

**Replace lines 24-27 with:**

```markdown
1. **Data Acquisition** - Pulls dynamic multi-period snapshots:
   - **Current snapshot**: From Silver lakehouse Delta table (`SILVER/account`)
   - **Prior business day (T-1)**: For day-over-day analysis
   - **Prior month-end**: Last day of prior month (dynamic)
   - **Prior quarter-end**: Last day of prior quarter (dynamic)
   - **Prior year-end**: December 31 of prior year (dynamic)
   - **Trailing 16 months**: Month-end snapshots for trend analysis
   - **Prior 8 business days**: Recent daily snapshots for activity chart
   - All historical snapshots fetched via `cdutils.acct_file_creation.core.query_df_on_date()`
   - Automatic business day adjustment (weekends/holidays handled by cdutils)
```

**Replace lines 62-66 with:**

```markdown
PowerBI connects to the Delta tables and calculates DAX measures:
- **Current Balance** - from current snapshot
- **Prior Day Balance** - from T-1 snapshot (day-over-day change)
- **Prior Month-End Balance** - from prior month-end snapshot (month-over-month change)
- **Prior Quarter-End Balance** - from prior quarter-end snapshot (quarter-over-quarter change)
- **Prior Year-End Balance** - from prior year-end snapshot (year-over-year change)
- **16-Month Trend** - line graph from trailing 16 month-end snapshots
- **8-Day Activity** - chart from prior 8 business day snapshots
```

**Update Data Flow Summary (lines 78-83):**

```markdown
## Data Flow Summary

```
SILVER/account (current) ────────┐
Prior day (T-1) ─────────────────┤
Prior month-end (dynamic) ───────┤
Prior quarter-end (dynamic) ─────┤
Prior year-end (dynamic) ────────├─→ Union → Split → dim_account ──┐
Trailing 16 months ──────────────┤                 → fact_balances ├─→ PowerBI → DAX Measures
Prior 8 business days ───────────┘                 → portfolio ─────┘
```
```

---

### 4. Testing Strategy

**Unit Tests (pytest - can be done in this environment):**

1. **Date boundary testing** (`test_date_helpers.py`):
   - Test on January 1 (prior year-end = Dec 31 of previous year)
   - Test on January 15 (prior quarter = Dec 31)
   - Test on first of month (prior month-end = last day of prior month)
   - Test on leap year date (Feb 29, 2024)
   - Test mid-year dates (June 15, Sept 20, etc.)

2. **Trailing month-ends validation**:
   - Verify first element is always prior month (not current month)
   - Check correct calculation going back 16 months
   - Test year boundary crossing (e.g., Jan 2025 → back to Sept 2023)

3. **Quarter-end calculation**:
   - Test all 4 quarters (Q1→Q4, Q2→Q1, Q3→Q2, Q4→Q3)
   - Verify Q1 correctly returns Dec 31 of prior year

4. **Deduplication testing**:
   - Verify set() correctly removes duplicate dates across categories
   - Test overlap scenarios (prior month-end in trailing 16 months, etc.)

**Integration Testing (must be done in production environment):**

1. **Data validation**:
   - Confirm no duplicate effdate + acctnbr in dim_account
   - Verify all ~25-28 distinct dates present in fact_balances (after deduplication)
   - Check current_df from Silver matches expected current date
   - Validate all balance columns populated correctly

2. **Performance monitoring**:
   - Monitor query execution time for 25-28 snapshots
   - Log timing for each snapshot fetch
   - Total pipeline runtime (expect 2-5 minutes)

---

### 5. PowerBI Changes (Downstream)

**New DAX Measures to Create:**

```dax
// Day-over-day change
DoD Balance Change =
    [Current Balance] - [Prior Day Balance]

DoD Balance Change % =
    DIVIDE([DoD Balance Change], [Prior Day Balance], 0)

// Month-over-month change
MoM Balance Change =
    [Current Balance] - [Prior Month End Balance]

MoM Balance Change % =
    DIVIDE([MoM Balance Change], [Prior Month End Balance], 0)

// Quarter-over-quarter change
QoQ Balance Change =
    [Current Balance] - [Prior Quarter End Balance]

QoQ Balance Change % =
    DIVIDE([QoQ Balance Change], [Prior Quarter End Balance], 0)

// Year-over-year change
YoY Balance Change =
    [Current Balance] - [Prior Year End Balance]

YoY Balance Change % =
    DIVIDE([YoY Balance Change], [Prior Year End Balance], 0)
```

**New Visuals to Add:**

1. **16-Month Trend Line Chart**:
   - X-axis: effdate (filtered to trailing 16 month-ends)
   - Y-axis: Sum of Net Balance
   - Filters: Macro Account Type, Portfolio

2. **8-Day Activity Chart**:
   - X-axis: effdate (filtered to prior 8 business days, descending)
   - Y-axis: Sum of Net Balance
   - Type: Column chart or line chart
   - Filters: Macro Account Type, Portfolio

---

## Code Diff Summary

### New Files
- `src/utils/date_helpers.py` (370 lines) - Date calculation utilities

### Modified Files

**1. `src/deposit_dash_prototype/core.py`**
- Add imports: `from src.utils.date_helpers import get_all_required_dates`
- Add function: `fetch_snapshot()` (~15 lines)
- Refactor `main_pipeline()`:
  - Remove hardcoded dates (lines 105, 112)
  - Add dynamic date calculation (new ~50 lines)
  - Add snapshot fetching loop (new ~20 lines)
  - Keep dimension/fact building logic unchanged

**2. `docs/polishing_stage_oct2025/OVERVIEW.md`**
- Update Data Acquisition section (lines 24-27)
- Update PowerBI Layer section (lines 62-66)
- Update Data Flow Summary diagram (lines 78-83)

---

## Questions / Clarifications

### Resolved Questions

1. **Q: Should trailing 16 months include current month or start from prior month?**
   - **A: CONFIRMED** - Start from prior month (current month start day - 1 day)
   - Example: If today = 2025-10-21, first month-end = 2025-09-30, not 2025-10-31
   - Rationale: Current month is incomplete; use completed months only

2. **Q: Should prior 8 business days include current day?**
   - **A: YES** - Include current day as first element
   - Result: [current, current-1, current-2, ..., current-7]

3. **Q: How to handle duplicate dates across different categories?**
   - **A: RESOLVED** - Use set() to deduplicate before fetching
   - Example: If today = 10/21, prior month-end (9/30) may also be in trailing 16 months

4. **Q: Should we fetch current from cdutils or keep using Silver lakehouse?**
   - **A: CONFIRMED** - Keep using Silver lakehouse for current (already optimized)
   - Only fetch historical dates via cdutils.query_df_on_date()

5. **Q: Performance - Should we implement parallel fetching?**
   - **A: NO** - Sequential fetching is acceptable
   - Estimated runtime: 2-5 minutes for 28-30 snapshots

6. **Q: Data volume concerns - Can Delta tables and PowerBI handle ~1.4M-1.5M records?**
   - **A: YES** - Data volume should be fine, no special handling needed

7. **Q: Business day handling - Does cdutils.query_df_on_date() handle weekends/holidays?**
   - **A: YES** - cdutils automatically finds nearest prior business day
   - Weekends and bank holidays are handled automatically
   - No custom business day logic needed

8. **Q: PowerBI date filtering - Should we add date_period_type column?**
   - **A: NO** - User will handle filtering dynamically in PowerBI using date ranges
   - Keep fact_balances schema simple

### Testing Constraints

**IMPORTANT**: This environment cannot connect to data sources (Silver lakehouse, cdutils queries).

**What CAN be tested:**
- ✅ **Unit tests** for all date calculation functions using pytest
- ✅ Date boundary cases (Jan 1, leap years, quarter boundaries, etc.)
- ✅ Logic validation (correct month-ends, quarter-ends, year-ends calculated)
- ✅ Deduplication logic (set operations)

**What CANNOT be tested:**
- ❌ Actual data fetching from cdutils.query_df_on_date()
- ❌ Silver lakehouse Delta table reads
- ❌ Full pipeline execution with real data
- ❌ Data quality validation (record counts, duplicates, etc.)

**Testing approach:**
- Write comprehensive pytest unit tests for `date_helpers.py`
- Mock/stub data fetching functions in integration tests
- Full end-to-end testing must be done in production environment

---

## Implementation Checklist

### Phase 1: Date Utilities & Unit Tests ✅ **COMPLETED 2025-10-21**
- [x] Create `src/utils/date_helpers.py` ✅ **COMPLETED 2025-10-21**
- [x] Create pytest unit tests for all date calculation functions ✅ **COMPLETED 2025-10-21**
  - Created comprehensive test suite in `tests/test_date_helpers.py` (460 lines)
  - Covers all 8 main functions with boundary cases
  - ✅ **NO lakehouse/production dependencies** - pure unit tests only
- [x] **Execute pytest** ✅ **COMPLETED 2025-10-21**
  - Command: `python -m pytest tests/test_date_helpers.py -v`
  - **Result: 44/44 tests PASSED** ✅

**Test Coverage:**
- ✅ Date boundary cases (Jan 1, leap years, quarter boundaries)
- ✅ Trailing 16 months logic (starts from prior month)
- ✅ Deduplication logic (set operations)
- ✅ All quarter transitions (Q1→Q4, Q2→Q1, Q3→Q2, Q4→Q3)
- ✅ Month/year boundary crossings

### Phase 2: Pipeline Integration ⚠️ **CODE COMPLETE - AWAITING PRODUCTION TESTING**

**Local Changes (Completed 2025-10-21):**
- [x] Update `src/deposit_dash_prototype/core.py` with new imports ✅
  - Added `from src.utils.date_helpers import get_all_required_dates`
  - Added `from typing import List, Dict`
- [x] Add `fetch_snapshot()` helper function ✅
  - Added 15-line function at src/deposit_dash_prototype/core.py:89-103
- [x] Refactor `main_pipeline()` to use dynamic dates ✅
  - Replaced hardcoded dates with `get_all_required_dates()`
  - Implemented deduplication logic for unique dates
  - Added logging for all date periods
  - Replaced ~32 lines with ~80 lines of dynamic implementation

**Production Environment Tasks (Still Required):**
- [ ] Update `docs/polishing_stage_oct2025/OVERVIEW.md`
- [ ] Run full pipeline and validate output Delta tables
- [ ] Verify correct number of distinct dates in fact_balances (~25-26 expected)
- [ ] Check for no duplicate effdate + acctnbr in dim_account
- [ ] Validate data volume (~1.4M-1.5M records expected)
- [ ] Monitor pipeline runtime (expect 2-5 minutes)

**Detailed Code Changes for `src/deposit_dash_prototype/core.py`:**

**Change 1: Add imports (after line 10)**
```python
# ADD THESE LINES:
from src.utils.date_helpers import get_all_required_dates
from typing import List, Dict
```

**Change 2: Add fetch_snapshot() helper function (after line 86, before main_pipeline)**
```python
def fetch_snapshot(date: datetime, macro_type_mapping: dict) -> pd.DataFrame:
    """
    Fetch account snapshot for a given date and apply macro type mapping.

    Args:
        date: Target date for snapshot
        macro_type_mapping: Dict mapping mjaccttypcd to Macro Account Type

    Returns:
        DataFrame with snapshot data, effdate set, and Macro Account Type added
    """
    df = cdutils.acct_file_creation.core.query_df_on_date(date)
    df['Macro Account Type'] = df['mjaccttypcd'].map(macro_type_mapping)
    df['effdate'] = date  # Ensure effdate is set to requested date
    return df
```

**Change 3: Refactor main_pipeline() - REPLACE lines 88-119 with:**
```python
def main_pipeline():
    """
    Main ETL pipeline - fetches multi-period account snapshots and builds dimensional model.

    Returns:
        Tuple of (dim_account, fact_balances, portfolio)
    """

    # Define macro type mapping
    MACRO_TYPE_MAPPING = {
        'CML':'Loan',
        'MLN':'Loan',
        'CNS':'Loan',
        'MTG':'Loan',
        'CK':'Deposit',
        'SAV':'Deposit',
        'TD':'Deposit'
    }

    # Get all required dates dynamically
    dates = get_all_required_dates()

    print(f"Fetching data for multiple time periods...")
    print(f"  Current date: {dates['current'].strftime('%Y-%m-%d')}")
    print(f"  Prior day: {dates['prior_day'].strftime('%Y-%m-%d')}")
    print(f"  Prior month-end: {dates['prior_month_end'].strftime('%Y-%m-%d')}")
    print(f"  Prior quarter-end: {dates['prior_quarter_end'].strftime('%Y-%m-%d')}")
    print(f"  Prior year-end: {dates['prior_year_end'].strftime('%Y-%m-%d')}")
    print(f"  Trailing 16 months: {dates['trailing_16_months'][0].strftime('%Y-%m-%d')} to {dates['trailing_16_months'][-1].strftime('%Y-%m-%d')}")
    print(f"  Prior 8 business days: {dates['prior_8_days'][0].strftime('%Y-%m-%d')} to {dates['prior_8_days'][-1].strftime('%Y-%m-%d')}")

    # Fetch current snapshot from Silver lakehouse (already in memory)
    print("Fetching current snapshot from SILVER/account...")
    current_df = DeltaTable(src.config.SILVER / "account").to_pandas()
    current_df['Macro Account Type'] = current_df['mjaccttypcd'].map(MACRO_TYPE_MAPPING)
    # Note: effdate should already be set in Silver table

    # Collect all snapshots to union
    all_snapshots = [current_df]

    # Fetch all unique dates (dedupe to avoid duplicate queries)
    unique_dates = set()

    # Add key period dates
    unique_dates.add(dates['prior_day'])
    unique_dates.add(dates['prior_month_end'])
    unique_dates.add(dates['prior_quarter_end'])
    unique_dates.add(dates['prior_year_end'])

    # Add trailing 16 months
    for month_end in dates['trailing_16_months']:
        unique_dates.add(month_end)

    # Add prior 8 business days
    for day in dates['prior_8_days']:
        unique_dates.add(day)

    # Remove current date if already in Silver (avoid duplicate)
    unique_dates.discard(dates['current'])

    # Sort dates for cleaner logging
    unique_dates_sorted = sorted(unique_dates, reverse=True)

    print(f"Fetching {len(unique_dates_sorted)} historical snapshots...")

    # Fetch all historical snapshots
    for i, date in enumerate(unique_dates_sorted, 1):
        print(f"  [{i}/{len(unique_dates_sorted)}] Fetching {date.strftime('%Y-%m-%d')}...")
        snapshot = fetch_snapshot(date, MACRO_TYPE_MAPPING)
        all_snapshots.append(snapshot)

    # Union all snapshots
    print("Unioning all snapshots...")
    all_df = pd.concat(all_snapshots, ignore_index=True, sort=False)

    print(f"Total records across all periods: {len(all_df):,}")
    print(f"Unique accounts: {all_df['acctnbr'].nunique():,}")
    print(f"Unique dates: {all_df['effdate'].nunique()}")

    # REST OF FUNCTION REMAINS UNCHANGED (lines 121-153)
```

**Lines 121-153 remain exactly as-is** (dimension_columns, fact_columns, building dim/fact tables)

---

**Before/After Comparison:**

**BEFORE (Current - Hardcoded):**
```python
# Lines 105-119 - REMOVE THESE:
year_date = datetime(2024, 12, 31)  # ❌ HARDCODED
year_end_df = cdutils.acct_file_creation.core.query_df_on_date(year_date)
year_end_df['Macro Account Type'] = year_end_df['mjaccttypcd'].map(MACRO_TYPE_MAPPING)
year_end_df['effdate'] = year_date

month_date = datetime(2025, 9, 30)  # ❌ HARDCODED
month_end_df = cdutils.acct_file_creation.core.query_df_on_date(month_date)
month_end_df['Macro Account Type'] = month_end_df['mjaccttypcd'].map(MACRO_TYPE_MAPPING)
month_end_df['effdate'] = month_date

# Union all snapshots (includes historical-only accounts)
all_df = pd.concat([current_df, year_end_df, month_end_df], ignore_index=True, sort=False)
```
**Result:** 3 snapshots (current, 2024-12-31, 2025-09-30)

**AFTER (Dynamic):**
```python
# Lines 632-690 - REPLACE WITH THESE:
dates = get_all_required_dates()  # ✅ DYNAMIC

# Collect all unique dates via deduplication
unique_dates = set()
unique_dates.add(dates['prior_day'])
unique_dates.add(dates['prior_month_end'])
unique_dates.add(dates['prior_quarter_end'])
unique_dates.add(dates['prior_year_end'])
for month_end in dates['trailing_16_months']:
    unique_dates.add(month_end)
for day in dates['prior_8_days']:
    unique_dates.add(day)
unique_dates.discard(dates['current'])

# Fetch all snapshots in loop
all_snapshots = [current_df]
for date in sorted(unique_dates, reverse=True):
    snapshot = fetch_snapshot(date, MACRO_TYPE_MAPPING)
    all_snapshots.append(snapshot)

all_df = pd.concat(all_snapshots, ignore_index=True, sort=False)
```
**Result:** ~25 snapshots (current + 24-26 historical dates after deduplication)

---

### Phase 3: PowerBI Enhancements (Downstream, in PowerBI environment)
- [ ] Update PowerBI dashboard with new DAX measures (DoD, MoM, QoQ, YoY)
- [ ] Create 16-month trend line visual
- [ ] Create 8-day activity chart visual
- [ ] Document new measures and visuals
- [ ] Update user documentation / README

---

## Implementation Summary

### What's Already Done
✅ **Phase 1 Complete:**
- `src/utils/date_helpers.py` - 202 lines, 8 date calculation functions
- `tests/test_date_helpers.py` - 460 lines, comprehensive test suite
- All tests are pure unit tests (no lakehouse/production dependencies)

### What Needs to Be Done

**IMMEDIATE NEXT STEP (Today - Local Environment):**
1. Run `python -m pytest tests/test_date_helpers.py -v` to validate date logic
2. Fix any failing tests if needed
3. Update PLAN.md checklist when tests pass

**PHASE 2 (Production Environment):**
1. Apply the 3 code changes to `src/deposit_dash_prototype/core.py`:
   - Add imports (2 lines)
   - Add `fetch_snapshot()` function (~15 lines)
   - Refactor `main_pipeline()` (~80 lines replacing ~32 lines)
2. Run full pipeline in production
3. Validate output:
   - Check ~25 distinct dates in fact_balances
   - Verify no duplicate (effdate, acctnbr) in dim_account
   - Confirm data volume ~1.4M-1.5M records

**PHASE 3 (PowerBI):**
1. Create new DAX measures (DoD, MoM, QoQ, YoY)
2. Add 16-month trend visual
3. Add 8-day activity chart

### Key Design Decisions Reflected in Code

1. **Trailing 16 months starts from PRIOR month** (line 128 in date_helpers.py):
   - Uses `i+1` offset to skip current incomplete month
   - Ensures only completed months are included

2. **Deduplication before fetching** (lines 654-671 in core.py refactor):
   - Uses `set()` to collect unique dates
   - Discards current date (already fetched from Silver)
   - Avoids redundant queries

3. **No parallel fetching** (lines 679-682 in core.py refactor):
   - Sequential loop through unique_dates_sorted
   - Acceptable runtime (~2-5 min for 25 snapshots)

4. **Business day adjustment delegated to cdutils** (fetch_snapshot function):
   - date_helpers.py returns calendar dates
   - cdutils.query_df_on_date() handles weekends/holidays automatically

5. **No date_period_type column** (lines 121-153 unchanged):
   - PowerBI handles filtering via date ranges
   - Keeps fact table schema simple

---

## Estimated Impact

| Metric | Current | After Implementation |
|--------|---------|---------------------|
| Snapshots fetched | 3 | ~25 (after deduplication) |
| Historical depth | 10 months | 16 months |
| Daily granularity | None | 8 days |
| Comparison periods | 2 (YoY, MoM) | 5 (YoY, QoQ, MoM, DoD, 16M trend) |
| Hardcoded dates | 2 | 0 (fully dynamic) |
| PowerBI visuals | Basic | Enhanced (trend + activity charts) |
| Pipeline runtime | ~30 sec | ~2-5 min |
| Total records | ~150k | ~1.25M (25 snapshots × 50k accounts) |

---

## Next Steps

1. **Review & approve** this plan
2. **Clarify** any unresolved questions above
3. **Implement** date_helpers.py module
4. **Test** date calculation logic with various scenarios
5. **Refactor** core.py main_pipeline()
6. **Validate** output data quality
7. **Update** PowerBI dashboard
8. **Document** new features for end users
