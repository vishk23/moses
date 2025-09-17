Objective:
Create a PowerBI prototype of the Qlik account dashboard. Create PoC, integrate with the data model we are developing.

# 2025-09-16 (CD)
Build out first part of this today. Data model integrates nicely with this.

// TODO
Adjust balances to be an append only fact table
- account balances
    - easy to aggregate things off of this. 

| acctnbr | balance | effdate |
| --------------- | --------------- | --------------- |
| 123 | 1000 | 2024-12-31 |
| 123 | 2000 | 2025-09-16 |
| 222 | 50000 | 2025-09-16 |


Something like that. Easy for aggregations.
SCD might make things easy for lookups.
- especially on PowerBI side, we might have that be the ideal way to do things.

Can use scd 2 for dimensions
if you had customers, you'd want to see consolidated view of all customers, past/present

customer_dim:
| CustomerID | Name | Active (Y/N) | Status |
| --------------- | --------------- | --------------- | ---- |


vs our snapshotting.
- I heard an argument for just using snapshots instead of SCD type 2 because equal joins are better than range joins. 

We would just be showing what the customer base looks like as of a certain point in time.
- could do standard snapshotting and you tie a dimension Date only field to effdate and that is your consistent slicer


We would actually just have multiple versions and we'd do something like SELECT * to get all snapshots together in 1 table. Maybe nuance in the implementation

# 2025-09-17

# Absent of proper portfolio silver dimension table
# Separate field for presence of Muni (Y/N)
# We group by portfolio key and come up with a dimension
# Example: portfolio key is primary key and then I have a calculated field (agg, probably lambda function)
    # - Category
    #     - if taxrptfororgnbr is all null, 'Consumer', if taxrptforpersnbr is all null, 'Business'
    #     - else, 'Mixed'
    # - Total loan Balance
    #     - sum up 'Net Balance' on records (acctnbr) where df['Macro Account Type'] = Loan
    # - Total deposit Balance
    #     - sum up 'Net Balance' on records (acctnbr) where df['Macro Account Type'] = Deposit
    # - Unique Loans
    #     - nunique Loans (use logic above)
    # - Unqiue Deposits
    #     - nunique deposits (use logic above)
