# Data Catalog - BCSB: Accubranch Analysis

Files:
1. five_yr_history.parquet
2. account_data.parquet
3. transaction_cleaned.parquet

## 1. five_yr_history.parquet

## 2. account_data.parquet

## 3. transaction_cleaned.parquet
Account Type Mapping:
```
ACCOUNT_TYPE_MAPPING = {
    'CML': 'Commercial Loan',
    'MLN': 'Commercial Loan',
    'CNS': 'Consumer Loan',
    'MTG': 'Residential Loan',
    'CK': 'Checking',
    'SAV': 'Savings',
    'TD': 'CD'
}
```
Other account types (safe deposit boxes, bank checks, other things) are excluded

---

### Small business loan officers
SMALL_BUSINESS_OFFICERS = ['EBL PROGRAM ADMIN', 'SBLC LOAN OFFICER']

### Core process:
- Take the transcation table
- Enrich with branch name from organization table
- Enrich with account data for product types and loan officer to identify small business loans vs commercial loans

#### Type of Teller:
BAT - Batch Processing
ATM - ATM
WWW - Digital Banking
ONLI - In Person/Branch Transaction
API - 3rd party API/card system/vendor generated transaction
RTP - Real Time Payment Deposit
VRU - Phone Transaction

These could be grouped into different buckets. You may/may not want to exclude BAT (as COCC is the branch for 99% of records).

Note: All Digital Banking (WWW) is assigned to BCSB - Main Office
