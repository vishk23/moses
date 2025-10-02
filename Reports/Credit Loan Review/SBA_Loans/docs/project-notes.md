Usage:
- run from monorepo
- python -m src.main

distribute manually

# 2025-09-04

Filter df['product'] on below values:
array(['Express Business SBA LOC', 'Express Business SBA Term Loan',
       'FNB - SBA Line of Credit', 'FNB - SBA Loan',
       'SBA Commercial Mortgages', 'SBA Commercial Term',
       'SBA PPP R2 LNS', 'SBA Secured Line of Credit'], dtype=object)

INTPAIDTODATE
- wh_loans

Loan numbers
- acctcommon


Next Installment Due Date
- acctloan
    - currduedate

Amount Disbursed this period


WH_TOTALPAYMENTS_DUE for Interest/Principal 


74000 where currduedate = nextduedate
10000 where they don't match

We want curr due date. Validated off COCC

Transaction codes for this, need to figure out what Joan would like to see:
PDSB
SWPI
NDSB

# 2025-09-05

I think it's just PDSB
- for LOC advances


WH_RTXN for the most recent month. That can be a tack on.
- or we add trailing month worth of transactions. 

Ok so

WH_ACCTCOMMON
- loan number
- int rate
- closing balance (net balance)

WH_ACCTLOAN
- currduedate (Next Installment Date)

WH_RTXN (Trailing Month)
- Amount disbursed this period
- PDSB RTXNTYPCD
- where RTXNSTATCD = 'C'

or Principal Adv Amt field


WH_TOTALPAYMENTSDUE
- Interest Payment
- Principal Payment

WH_LOANS
- intpaidtodate
- Interest Period To



May need to change gears on the totalpaymentsdue. That doesn't seem to show future payments, even though it's in the amortization table.
- I might need some Tom K help on this.

----

Ok I've got it now.

The Principal Paid & Interest Paid come from RTXNBAL where BAL/INT balcatcodes and rtxntypcd = 'SPMT' (standard payment)

The advances is just PDSB total for that month

This can all be done from the rtxnbal:

<class 'pandas.core.frame.DataFrame'>
RangeIndex: 1037825 entries, 0 to 1037824
Data columns (total 11 columns):
 #   Column         Non-Null Count    Dtype         
---  ------         --------------    -----         
 0   acctnbr        1037825 non-null  int64         
 1   rundate        1037825 non-null  datetime64[ns]
 2   rtxnnbr        1037825 non-null  int64         
 3   rtxntypcd      1037825 non-null  object        
 4   rtxntypdesc    1037825 non-null  object        
 5   subacctnbr     1037825 non-null  int64         
 6   balcatcd       1037825 non-null  object        
 7   baltypcd       1037825 non-null  object        
 8   balancedesc    1037825 non-null  object        
 9   amt            1037825 non-null  object        
 10  datelastmaint  1037825 non-null  datetime64[ns]
dtypes: datetime64[ns](2), int64(3), object(6)
memory usage: 87.1+ MB

Create 2 different dfs, one for spmt and one for pdsb

Group by account number. For the pdsb one, we just sum of the amt
For the smpt one, we need 2 fields, the sum of principal payments and the some of interest paid. that is by baltypcd to decipher which lines are balance/principal or interest. This is explained above.


The overall strategy will be:
1.  **Prepare the Data**: Convert the `amt` column to a numeric type for calculations.
2.  **Filter and Aggregate**: Create the three separate DataFrames based on your specified conditions (`rtxntypcd` and `balcatcd`). This is a classic "split-apply-combine" approach. [datacamp.com](https://www.datacamp.com/tutorial/pandas-split-apply-combine-groupby)
3.  **Merge**: Join these new aggregated DataFrames to your main DataFrame.

### Sample Data
First, let's create a sample `rtxnbal` DataFrame that mimics your data structure for a runnable example.

```python
import pandas as pd
import numpy as np

# Create a sample DataFrame similar to your 'rtxnbal'
data = {
    'acctnbr': [101, 101, 101, 101, 102, 102, 102, 103, 103, 104],
    'rundate': pd.to_datetime(['2023-01-15']*10),
    'rtxntypcd': ['SPMT', 'SPMT', 'PDSB', 'PDSB', 'SPMT', 'SPMT', 'PDSB', 'PDSB', 'PDSB', 'SPMT'],
    'balcatcd': ['BAL', 'INT', 'FEE', 'FEE', 'BAL', 'INT', 'FEE', 'FEE', 'FEE', 'INT'],
    'amt': ['500.25', '50.10', '1000.00', '25.00', '450.80', '45.90', '2000.00', '300.00', '400.00', '33.33']
}
rtxnbal = pd.DataFrame(data)

# --- This is our hypothetical main DataFrame to merge with ---
merged_df = pd.DataFrame({'acctnbr': ['101', '102', '103', '105'], 
                          'customer_name': ['Alice', 'Bob', 'Charlie', 'David']})

print("Original rtxnbal DataFrame:")
print(rtxnbal.info())
```

### Step 1: Data Preparation
Before we can perform calculations, the `amt` column must be converted from `object` to a numeric type, like `float`.

```python
# Convert 'amt' column to a numeric type. 
# errors='coerce' will turn any non-numeric values into NaN (Not a Number)
rtxnbal['amt'] = pd.to_numeric(rtxnbal['amt'], errors='coerce')

# It's good practice to fill any resulting NaN values, for instance with 0
rtxnbal['amt'] = rtxnbal['amt'].fillna(0)
```

### Step 2: Create the Aggregated DataFrames

Here we will create the three separate DataFrames you requested.

#### DataFrame 1: Advances from `PDSB`

This DataFrame will contain the total sum of `amt` for all `PDSB` transactions, grouped by account.

```python
# 1. Filter for 'PDSB' transaction types
advances_raw = rtxnbal[rtxnbal['rtxntypcd'] == 'PDSB'].copy()

# 2. Group by account number and sum the amount
df_advances = advances_raw.groupby('acctnbr')['amt'].sum().reset_index()

# 3. Rename the column for clarity
df_advances = df_advances.rename(columns={'amt': 'Advances'})

# 4. Convert acctnbr to string for merging
df_advances['acctnbr'] = df_advances['acctnbr'].astype(str)

print("\n--- Advances DataFrame (df_advances) ---")
print(df_advances)
```

#### DataFrames 2 & 3: Principal and Interest from `SPMT`

A highly efficient way to do this is to filter for `SPMT` transactions once, then group by both account and balance category. We can then `unstack` the results to create separate columns for Principal (`BAL`) and Interest (`INT`).

```python
# 1. Filter for 'SPMT' transaction types
spmt_raw = rtxnbal[rtxnbal['rtxntypcd'] == 'SPMT'].copy()

# 2. Group by account and balance category, then sum the amounts
payments = spmt_raw.groupby(['acctnbr', 'balcatcd'])['amt'].sum()

# 3. Unstack the 'balcatcd' level to turn 'BAL' and 'INT' into columns
df_payments = payments.unstack(level='balcatcd').fillna(0).reset_index()

# 4. Rename columns for clarity
df_payments = df_payments.rename(columns={
    'BAL': 'Principal Paid',
    'INT': 'Interest Paid'
})

# 5. Convert acctnbr to string for merging
df_payments['acctnbr'] = df_payments['acctnbr'].astype(str)

print("\n--- Combined Payments DataFrame ---")
print(df_payments)
```

From this combined DataFrame, you can easily create the two separate ones if you prefer, although merging the combined one is more efficient.

```python
# Optional: Create two fully separate DataFrames as requested
df_principal = df_payments[['acctnbr', 'Principal Paid']].copy()
df_interest = df_payments[['acctnbr', 'Interest Paid']].copy()

print("\n--- Principal Paid DataFrame (df_principal) ---")
print(df_principal)

print("\n--- Interest Paid DataFrame (df_interest) ---")
print(df_interest)
```

### Step 3: Append Aggregated Fields to Your Existing `merged_df`

Now you can use `pd.merge()` with a `left` join to add these new columns to your main `merged_df`. A left join ensures you keep all records from your main DataFrame, even if an account has no corresponding transactions in the aggregated data.

```python
# Ensure the key in the main DataFrame is also a string
merged_df['acctnbr'] = merged_df['acctnbr'].astype(str)

# 1. Merge the advances
final_df = pd.merge(merged_df, df_advances, on='acctnbr', how='left')

# 2. Merge the payments (using the combined df_payments is more efficient)
final_df = pd.merge(final_df, df_payments, on='acctnbr', how='left')

# 3. After merging, fill any NaN values with 0
# This handles accounts that were in merged_df but had no payments/advances
final_df[['Advances', 'Principal Paid', 'Interest Paid']] = final_df[['Advances', 'Principal Paid', 'Interest Paid']].fillna(0)


print("\n--- Final Merged DataFrame ---")
print(final_df)
```

This code provides a clean and efficient way to perform the required aggregations and attach them as new fields to your primary DataFrame.


