# Transaction Data Implementation Plan

## Decision: Stick with Current Delta Lake + Python Setup (No DBT)

### Why Not DBT?

Your current setup with Delta Lake + Python is already well-suited for transaction data. Here's the comparison:

| Factor | Current Setup (Delta Lake + Python) | DBT |
|--------|-------------------------------------|-----|
| **Append-only loads** | ✅ Native support via `mode='append'` | ✅ Incremental models |
| **Incremental processing** | ✅ Manual date filtering in SQL | ✅ Built-in macros |
| **Data transformations** | ✅ Python/Pandas (full flexibility) | ⚠️ SQL only (less flexible) |
| **Custom business logic** | ✅ Full Python control | ⚠️ Limited to SQL + Jinja |
| **Partitioning** | ✅ Native Delta Lake support | ✅ Supported |
| **Testing** | ⚠️ Manual | ✅ Built-in testing framework |
| **Documentation** | ⚠️ Manual | ✅ Auto-generated docs |
| **Learning curve** | ✅ You already know it | ⚠️ New tool to learn |
| **Orchestration** | ✅ Python `main.py` | ⚠️ Needs separate orchestrator |

**Recommendation: Your current setup is perfect for this.** Complex business logic (inflow/outflow + internal/external categorization) is easier in Python than SQL, and you already have all the infrastructure you need.

---

## Implementation Approach

### Overview

Transform the current `wh_rtxn` and `wh_rtxnbal` bronze tables from full overwrites to incremental append-only pattern with:
- Date-based incremental loading (using `rundate`)
- Partitioning for performance on massive tables
- Deduplication to handle reruns
- Business logic transformations in silver layer

---

## Bronze Layer Changes

### 1. Modify `src/bronze/fetch_data.py`

**Add new function or modify `fetch_rtxn()` to support incremental loading:**

```python
def fetch_rtxn(start_date: Optional[str] = None, end_date: Optional[str] = None):
    """
    Main data query for transaction data with optional date filtering

    Args:
        start_date: Start date for incremental load (format: 'YYYY-MM-DD')
        end_date: End date for incremental load (format: 'YYYY-MM-DD')
    """

    # Build WHERE clause for incremental loading
    where_clause = ""
    if start_date:
        where_clause = f"WHERE a.RUNDATE >= TO_DATE('{start_date}', 'YYYY-MM-DD')"
        if end_date:
            where_clause += f" AND a.RUNDATE <= TO_DATE('{end_date}', 'YYYY-MM-DD')"

    # Option 1: Keep tables separate
    wh_rtxn = text(f"""
    SELECT
        *
    FROM
        OSIBANK.WH_RTXN a
    {where_clause}
    """)

    wh_rtxnbal = text(f"""
    SELECT
        *
    FROM
        OSIBANK.WH_RTXNBAL a
    {where_clause}
    """)

    queries = [
        {'key':'wh_rtxn', 'sql':wh_rtxn, 'engine':1},
        {'key':'wh_rtxnbal', 'sql':wh_rtxnbal, 'engine':1},
    ]

    data = cdutils.database.connect.retrieve_data(queries)
    return data
```

**OR Option 2: Join at bronze level into unified transaction table:**

```python
def fetch_rtxn_unified(start_date: Optional[str] = None, end_date: Optional[str] = None):
    """
    Fetch unified transaction data by joining rtxn + rtxnbal
    """

    where_clause = ""
    if start_date:
        where_clause = f"WHERE t.RUNDATE >= TO_DATE('{start_date}', 'YYYY-MM-DD')"
        if end_date:
            where_clause += f" AND t.RUNDATE <= TO_DATE('{end_date}', 'YYYY-MM-DD')"

    txn_unified = text(f"""
    SELECT
        t.*,
        b.* -- adjust to avoid column conflicts
    FROM
        OSIBANK.WH_RTXN t
    LEFT JOIN
        OSIBANK.WH_RTXNBAL b
        ON t.ACCTNBR = b.ACCTNBR
        AND t.RUNDATE = b.RUNDATE
        AND t.TXNNBR = b.TXNNBR  -- adjust join keys as needed
    {where_clause}
    """)

    queries = [
        {'key':'txn_unified', 'sql':txn_unified, 'engine':1},
    ]

    data = cdutils.database.connect.retrieve_data(queries)
    return data
```

### 2. Update `src/bronze/core.py`

**Add watermark tracking and modify transaction loading:**

```python
def get_last_transaction_date(delta_path: Path) -> Optional[str]:
    """
    Get the last rundate loaded into the transaction table
    Returns date string in 'YYYY-MM-DD' format or None if table doesn't exist
    """
    try:
        from deltalake import DeltaTable
        dt = DeltaTable(delta_path)
        df = dt.to_pandas()
        if len(df) > 0 and 'rundate' in df.columns:
            max_date = df['rundate'].max()
            return pd.to_datetime(max_date).strftime('%Y-%m-%d')
        return None
    except Exception as e:
        print(f"No existing transaction table found: {e}")
        return None


def load_transactions_incremental():
    """
    Load transactions incrementally with deduplication
    """
    WH_TXN_PATH = src.config.BRONZE / "transactions"
    WH_TXN_PATH.mkdir(parents=True, exist_ok=True)

    # Get last loaded date
    last_date = get_last_transaction_date(WH_TXN_PATH)

    if last_date:
        # Incremental: load from last date + 1 day
        from dateutil.relativedelta import relativedelta
        start_date = (pd.to_datetime(last_date) + relativedelta(days=1)).strftime('%Y-%m-%d')
        print(f"Incremental load: fetching transactions from {start_date}")
    else:
        # Initial load: get last 90 days (or all time - adjust as needed)
        start_date = (datetime.now() - relativedelta(days=90)).strftime('%Y-%m-%d')
        print(f"Initial load: fetching transactions from {start_date}")

    # Fetch data
    data = src.bronze.fetch_data.fetch_rtxn(start_date=start_date)

    # Join the two tables if kept separate
    wh_rtxn = data['wh_rtxn'].copy()
    wh_rtxnbal = data['wh_rtxnbal'].copy()

    # Merge the two dataframes (adjust join keys as needed)
    txn_combined = pd.merge(
        wh_rtxn,
        wh_rtxnbal,
        on=['ACCTNBR', 'RUNDATE', 'TXNNBR'],  # adjust keys
        how='left',
        suffixes=('', '_bal')
    )

    # Cast null columns
    txn_combined = cast_all_null_columns_to_string(txn_combined)

    # Add load timestamp
    txn_combined = add_load_timestamp(txn_combined)

    # Deduplicate on primary key (in case of reruns)
    # Adjust composite key as needed
    txn_combined = txn_combined.drop_duplicates(
        subset=['ACCTNBR', 'RUNDATE', 'TXNNBR'],
        keep='last'
    )

    # Write with append mode and partitioning
    from deltalake import write_deltalake

    if len(txn_combined) > 0:
        write_deltalake(
            WH_TXN_PATH,
            txn_combined,
            mode='append',
            schema_mode='merge',
            partition_by=['rundate']  # partition by transaction date for performance
        )
        print(f"Loaded {len(txn_combined)} transaction records")
    else:
        print("No new transactions to load")
```

**Add to `generate_bronze_tables()` function:**

```python
def generate_bronze_tables():
    print("Start bronze table generation")

    # ... existing code ...

    # WH_RTXN (OSIBANK) - INCREMENTAL APPEND ========================
    load_transactions_incremental()

    # ... rest of code ...
```

---

## Silver Layer Implementation

### 3. Create `src/silver/transactions/` module

**File: `src/silver/transactions/__init__.py`**
```python
# Empty or import core
```

**File: `src/silver/transactions/core.py`**

```python
"""
Transaction dimension with business logic for inflow/outflow and internal/external classification
"""
import pandas as pd
from pathlib import Path
from deltalake import DeltaTable, write_deltalake
import src.config
from src.utils.parquet_io import add_load_timestamp, cast_all_null_columns_to_string


def classify_inflow_outflow(row):
    """
    Business logic to classify transaction as inflow or outflow

    Args:
        row: DataFrame row with transaction data

    Returns:
        'INFLOW' or 'OUTFLOW'
    """
    # Example logic - adjust based on your actual fields
    amount = row.get('AMOUNT', 0) or 0
    txn_type = row.get('TXNTYPCD', '')

    # Custom business logic here
    if amount > 0:
        return 'INFLOW'
    elif amount < 0:
        return 'OUTFLOW'
    else:
        return 'NEUTRAL'


def classify_internal_external(row, internal_account_list=None):
    """
    Business logic to classify transaction as internal or external

    Args:
        row: DataFrame row with transaction data
        internal_account_list: Set of internal account numbers (optional)

    Returns:
        'INTERNAL' or 'EXTERNAL'
    """
    # Example logic - adjust based on your actual business rules
    txn_type = row.get('TXNTYPCD', '')
    from_acct = row.get('FROMACCTNBR', None)
    to_acct = row.get('TOACCTNBR', None)

    # Example: if both accounts are in your bank, it's internal
    if internal_account_list:
        if from_acct in internal_account_list and to_acct in internal_account_list:
            return 'INTERNAL'

    # Example: certain transaction types are always internal
    if txn_type in ['TRANSFER', 'XFER']:
        return 'INTERNAL'

    return 'EXTERNAL'


def generate_transaction_dimension():
    """
    Generate silver layer transaction dimension with business classifications
    """
    print("Generating transaction dimension...")

    # Read from bronze
    BRONZE_TXN_PATH = src.config.BRONZE / "transactions"
    SILVER_TXN_PATH = src.config.SILVER / "transaction_dim"
    SILVER_TXN_PATH.mkdir(parents=True, exist_ok=True)

    # Load bronze data
    dt = DeltaTable(BRONZE_TXN_PATH)
    txn_df = dt.to_pandas()

    print(f"Processing {len(txn_df)} transactions...")

    # Optional: Load internal account list for classification
    # ACCT_DIM_PATH = src.config.SILVER / "account_dim"
    # acct_dt = DeltaTable(ACCT_DIM_PATH)
    # acct_df = acct_dt.to_pandas()
    # internal_accounts = set(acct_df['ACCTNBR'].unique())
    internal_accounts = None  # Or load from account dimension

    # Apply business logic
    txn_df['inflow_outflow_flag'] = txn_df.apply(classify_inflow_outflow, axis=1)
    txn_df['internal_external_flag'] = txn_df.apply(
        lambda row: classify_internal_external(row, internal_accounts),
        axis=1
    )

    # Add calculated fields
    txn_df['net_amount'] = txn_df.get('AMOUNT', 0)
    txn_df['transaction_year'] = pd.to_datetime(txn_df['rundate']).dt.year
    txn_df['transaction_month'] = pd.to_datetime(txn_df['rundate']).dt.month
    txn_df['transaction_yearmonth'] = pd.to_datetime(txn_df['rundate']).dt.to_period('M').astype(str)

    # Clean and prepare
    txn_df = cast_all_null_columns_to_string(txn_df)
    txn_df = add_load_timestamp(txn_df)

    # Deduplicate
    txn_df = txn_df.drop_duplicates(
        subset=['ACCTNBR', 'rundate', 'TXNNBR'],
        keep='last'
    )

    # Write to silver with partitioning by year-month for query performance
    write_deltalake(
        SILVER_TXN_PATH,
        txn_df,
        mode='overwrite',  # Or 'append' if you want incremental silver too
        schema_mode='merge',
        partition_by=['transaction_yearmonth']
    )

    print(f"Transaction dimension generated: {len(txn_df)} records")
    return txn_df
```

### 4. Update `src/silver/core.py`

Add to the `generate_silver_tables()` function:

```python
def generate_silver_tables():
    print("Start silver table generation")

    # ... existing code ...

    # Transaction Dimension ========================
    from src.silver.transactions.core import generate_transaction_dimension
    generate_transaction_dimension()

    # ... rest of code ...
```

---

## Configuration Updates

### 5. Add to `src/config.py`

```python
# Transaction loading configuration
TRANSACTION_INITIAL_LOAD_DAYS = 90  # How many days to load on initial run
TRANSACTION_BATCH_SIZE = 100000  # Optional: for chunked processing of large datasets
```

---

## Key Technical Decisions

### Partitioning Strategy
- **Bronze**: Partition by `rundate` (transaction date) for efficient incremental queries
- **Silver**: Partition by `transaction_yearmonth` for analytical query performance

### Deduplication
- Use composite key: `(ACCTNBR, RUNDATE, TXNNBR)` - adjust based on actual unique identifiers
- Keep `last` record in case of reruns

### Incremental Loading
- Track last loaded date using Delta Lake metadata
- On each run, fetch only new transactions (rundate > last_loaded_date)
- Initial load: configurable lookback period (default 90 days)

### Business Logic Flexibility
- Keep classification functions separate and configurable
- Easy to adjust rules without changing core pipeline logic
- Can reference account dimension for internal/external classification

---

## Performance Considerations

### For Massive Transaction Tables

1. **Partitioning**: Essential for query performance on billions of rows
2. **Chunked processing**: If memory is an issue, process in date-based chunks
3. **Predicate pushdown**: Delta Lake will skip partitions based on date filters
4. **Z-ordering**: Consider adding Z-order on frequently queried columns (account number)

### Example: Z-Ordering (optional optimization)

```python
from deltalake import DeltaTable

dt = DeltaTable(WH_TXN_PATH)
dt.optimize.z_order(['ACCTNBR'])  # Cluster data by account for faster account-based queries
```

---

## Testing Strategy

1. **Initial load test**: Run with small date range first (e.g., 7 days)
2. **Incremental test**: Run twice to verify append behavior
3. **Deduplication test**: Run same date range twice, verify no duplicates
4. **Classification validation**: Sample transactions and verify inflow/outflow + internal/external flags
5. **Performance test**: Monitor load times and query performance

---

## Migration Path

### Phase 1: Bronze Incremental (Week 1)
- [ ] Implement incremental fetch function
- [ ] Add watermark tracking
- [ ] Test with 7-day load
- [ ] Validate append behavior

### Phase 2: Silver Transformations (Week 2)
- [ ] Create transaction dimension module
- [ ] Implement classification logic
- [ ] Test business rules
- [ ] Validate against sample data

### Phase 3: Optimization (Week 3)
- [ ] Add partitioning to bronze/silver
- [ ] Test query performance
- [ ] Add Z-ordering if needed
- [ ] Document business rules

### Phase 4: Production (Week 4)
- [ ] Full historical load (if needed)
- [ ] Schedule daily incremental runs
- [ ] Monitor performance metrics
- [ ] Create dashboards/reports

---

## Estimated Effort

- **Bronze layer changes**: ~100 lines of code, 4-6 hours
- **Silver layer implementation**: ~150 lines of code, 6-8 hours
- **Testing & validation**: 4-6 hours
- **Documentation**: 2 hours

**Total**: ~2-3 days of development + testing

---

## Why This Approach Works

✅ **Incremental**: Only loads new data each run (efficient)
✅ **Idempotent**: Can rerun safely with deduplication
✅ **Scalable**: Partitioning handles billions of rows
✅ **Flexible**: Business logic in Python is easy to modify
✅ **Consistent**: Follows existing architectural patterns
✅ **No new dependencies**: Uses tools you already have

---

## Questions to Answer Before Implementation

1. **Join keys**: What are the exact join keys between `wh_rtxn` and `wh_rtxnbal`?
2. **Primary key**: What uniquely identifies a transaction (for deduplication)?
3. **Business rules**: What fields determine inflow/outflow and internal/external?
4. **Historical data**: Do you need to load all historical transactions or just recent?
5. **Run frequency**: Daily? Hourly? On-demand?
6. **Data volume**: Approximately how many transactions per day?

---

## Alternative: If You Still Want DBT

If you decide DBT is worth it despite the above analysis, here's what you'd need:

1. Install DBT with DeltaLake adapter
2. Create `models/bronze/` with incremental SQL models
3. Create `models/silver/` with transformation logic (limited to SQL + Jinja)
4. Lose Python flexibility for complex business logic
5. Add orchestration layer (Airflow/Dagster) to run DBT

**Bottom line**: Adds complexity without significant benefits for your use case.
