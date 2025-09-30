# 2025-09-29
```sql
WITH deduped_accounts AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY account_id ORDER BY effdate DESC) AS rn
    FROM account_snapshots
)
SELECT *
FROM deduped_accounts
WHERE rn = 1
  AND contract_date BETWEEN TO_DATE('start_date_placeholder', 'YYYY-MM-DD') 
                        AND TO_DATE('end_date_placeholder', 'YYYY-MM-DD');
```

This query assumes:
- The table is named `account_snapshots` (replace with actual table name).
- `account_id` is the column identifying each account.
- `effdate` is the effective date (snapshot date), type DATE or compatible.
- `contract_date` is the contract date, type DATE or compatible.
- Replace `'start_date_placeholder'` and `'end_date_placeholder'` with actual start and end dates in 'YYYY-MM-DD' format.

The `deduped_accounts` CTE uses `ROW_NUMBER()` to assign 1 to the most recent record per account (latest `effdate`). We then select only those and filter on `contract_date` using `BETWEEN` with `TO_DATE`. If the dates are already DATE type, you can omit `TO_DATE`. If date format differs, adjust the format string accordingly.

---

Hasan request to get for specific date range

