# Inflows/Outflows Reconciliation Project

## Objective
Verify that account balances can be reconciled using transaction data:
```
Starting Balance (1/1/2025) + Sum(Transaction Amounts) = Ending Balance (Current)
```

## Table Schemas

### WH_ACCTCOMMON
Daily snapshot table of account information.

**Key Fields:**
- `ACCTNBR` - Account number
- `EFFDATE` - Effective date (daily snapshot date)
- `NOTEBAL` - Account balance

**Notes:**
- Daily snapshots mean we need specific date filters to avoid full table scans
- Only concerned with dates >= 2025-01-01

### WH_RTXN
Daily snapshot table of retail transactions.

**Key Fields:**
- `ACCTNBR` - Account number
- `SUBACCTNBR` - Sub-account number
- `RTXNNBR` - Transaction number
- `RUNDATE` - Run date (should match EFFDATE in other tables)
- `TRANAMT` - Transaction amount

**Notes:**
- Daily snapshots
- Only concerned with dates >= 2025-01-01
- RTXNNBR alone is NOT unique

### WH_RTXNBAL
Daily snapshot table of retail transaction balances.

**Key Fields:**
- `ACCTNBR` - Account number
- `SUBACCTNBR` - Sub-account number (implied from composite key requirement)
- `RTXNNBR` - Transaction number
- `RUNDATE` - Run date
- `AMT` - Amount

**Notes:**
- Daily snapshots
- RTXNNBR alone is NOT unique

## Important: Composite Key
To uniquely identify transactions, use composite key:
```
ACCTNBR + SUBACCTNBR + RTXNNBR
```

## Data Scope
- **Date Range:** 2025-01-01 onwards
- **Why:** These are massive tables with daily snapshots; limiting scope improves performance
