Objective:
Create a PowerBI prototype of the Qlik account dashboard. Create PoC, integrate with the data model we are developing.


Progress:
- [x] Model the data for dashboard
- [x] Build PowerBI dashboard with account level data
- [x] Work in Portfolio metrics and set up so slicers/filters work
- [ ] Fix data model with balance in dimension table


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


C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Data Analytics\Active_Customer_Dashboard_Proto\src\deposit_dash_prototype\core.py:61: FutureWarning: DataFrameGroupBy.apply operated on the grouping columns. This behavior is deprecated, and in a future version of pandas the grouping columns will be excluded from the operation. Either pass `include_groups=False` to exclude the groupings or explicitly select the grouping columns after groupby to silence this warning.
  loan_bal = g.apply(lambda x: x.loc[x["__is_loan__"], "__net_bal__"].sum(min_count=1)).fillna(0.0)
C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Data Analytics\Active_Customer_Dashboard_Proto\src\deposit_dash_prototype\core.py:64: FutureWarning: DataFrameGroupBy.apply operated on the grouping columns. This behavior is deprecated, and in a future version of pandas the grouping columns will be excluded from the operation. Either pass `include_groups=False` to exclude the groupings or explicitly select the grouping columns after groupby to silence this warning.
  dep_bal = g.apply(lambda x: x.loc[x["__is_deposit__"], "__net_bal__"].sum(min_count=1)).fillna(0.0)
C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Data Analytics\Active_Customer_Dashboard_Proto\src\deposit_dash_prototype\core.py:68: FutureWarning: DataFrameGroupBy.apply operated on the grouping columns. This behavior is deprecated, and in a future version of pandas the grouping columns will be excluded from the operation. Either pass `include_groups=False` to exclude the groupings or explicitly select the grouping columns after groupby to silence this warning.
  uniq_loans = g.apply(lambda x: x.loc[x["__is_loan__"], "acctnbr"].nunique(dropna=True))
C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Data Analytics\Active_Customer_Dashboard_Proto\src\deposit_dash_prototype\core.py:71: FutureWarning: DataFrameGroupBy.apply operated on the grouping columns. This behavior is deprecated, and in a future version of pandas the grouping columns will be excluded from the operation. Either pass `include_groups=False` to exclude the groupings or explicitly select the grouping columns after groupby to silence this warning.
  uniq_deps = g.apply(lambda x: x.loc[x["__is_deposit__"], "acctnbr"].nunique(dropna=True))


# 2025-10-02

Refreshing this

Account PowerQuery
let
    Source = Folder.Contents(AcctFilePath),
    ToDelta = DeltaLake.Table(Source),
    GetVersions = Value.Versions(ToDelta),
    ActualData = GetVersions{[Version=null]}[Data],
    #"Filtered Rows" = Table.SelectRows(ActualData, each ([Macro Account Type] <> null)),
    #"Changed Type" = Table.TransformColumnTypes(#"Filtered Rows",{{"effdate", type datetime}})
in
    #"Changed Type"

# 2025-10-14
Need to think about data model. Was thinking I could have the customer dimension table as the way to describe accounts, but I think I actually want to have a full account dimension table here (no balances) and those tie to fact balance tables.

account_proto_deriv
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 89535 entries, 0 to 89534
Data columns (total 56 columns):
 #   Column                   Non-Null Count  Dtype              
---  ------                   --------------  -----              
 0   effdate                  89535 non-null  datetime64[us]     
 1   acctnbr                  89535 non-null  object             
 2   ownersortname            89535 non-null  object             
 3   product                  89535 non-null  object             
 4   noteopenamt              89535 non-null  float64            
 5   ratetypcd                71422 non-null  object             
 6   mjaccttypcd              89535 non-null  object             
 7   currmiaccttypcd          89535 non-null  object             
 8   curracctstatcd           89535 non-null  object             
 9   noteintrate              89535 non-null  float64            
 10  bookbalance              89535 non-null  float64            
 11  notebal                  89535 non-null  float64            
 12  contractdate             89534 non-null  datetime64[us]     
 13  datemat                  32865 non-null  datetime64[us]     
 14  taxrptfororgnbr          12487 non-null  float64            
 15  taxrptforpersnbr         77048 non-null  float64            
 16  loanofficer              23363 non-null  object             
 17  acctofficer              62687 non-null  object             
 18  creditlimitamt           89535 non-null  float64            
 19  origintrate              22647 non-null  object             
 20  marginfixed              23363 non-null  object             
 21  fdiccatcd                22710 non-null  object             
 22  amortterm                23363 non-null  float64            
 23  totalpctsold             89535 non-null  float64            
 24  cobal                    89535 non-null  float64            
 25  credlimitclatresamt      89535 non-null  float64            
 26  riskratingcd             2756 non-null   object             
 27  origdate                 23185 non-null  datetime64[us]     
 28  currterm                 23363 non-null  float64            
 29  loanidx                  23353 non-null  object             
 30  rcf                      3133 non-null   object             
 31  availbalamt              89535 non-null  float64            
 32  fdiccatdesc              22710 non-null  object             
 33  origbal                  22533 non-null  float64            
 34  loanlimityn              23363 non-null  object             
 35  nextratechg              2795 non-null   datetime64[us]     
 36  Net Balance              89535 non-null  float64            
 37  Net Available            89535 non-null  float64            
 38  Net Collateral Reserve   89535 non-null  float64            
 39  Total Exposure           89535 non-null  float64            
 40  orig_ttl_loan_amt        89535 non-null  float64            
 41  portfolio_key            89535 non-null  int64              
 42  ownership_key            84958 non-null  float64            
 43  address_key              84958 non-null  float64            
 44  householdnbr             79972 non-null  float64            
 45  datelastmaint            79972 non-null  datetime64[us]     
 46  Category                 23363 non-null  object             
 47  inactivedate             2601 non-null   datetime64[us]     
 48  branchname               89535 non-null  object             
 49  primaryownercity         89512 non-null  object             
 50  primaryownerstate        89486 non-null  object             
 51  load_timestamp_utc       89535 non-null  datetime64[us, UTC]
 52  primaryownerzipcd        89486 non-null  object             
 53  Macro Account Type       86074 non-null  object             
 54  Net Balance_prior_year   89486 non-null  float64            
 55  Net Balance_prior_month  89486 non-null  float64            
dtypes: datetime64[us, UTC](1), datetime64[us](7), float64(24), int64(1), object(23)
memory usage: 38.3+ MB

portfolio_deriv
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 38926 entries, 0 to 38925
Data columns (total 8 columns):
 #   Column                 Non-Null Count  Dtype              
---  ------                 --------------  -----              
 0   portfolio_key          38926 non-null  int64              
 1   Muni_Present           38926 non-null  object             
 2   Category               38926 non-null  object             
 3   Total loan Balance     38926 non-null  float64            
 4   Total deposit Balance  38926 non-null  float64            
 5   Unique Loans           38926 non-null  int64              
 6   Unique Deposits        38926 non-null  int64              
 7   load_timestamp_utc     38926 non-null  datetime64[us, UTC]
dtypes: datetime64[us, UTC](1), float64(2), int64(3), object(2)
memory usage: 2.4+ MB

portfolio key is the link

---
I need to figure out how to model this better. Analyze the context below and recommend an approach. 

Need to think about data model. Was thinking I could have the customer dimension table as the way to describe accounts, but I think I actually want to have a full account dimension table here (no balances) and those tie to fact balance tables.

account_proto_deriv
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 89535 entries, 0 to 89534
Data columns (total 56 columns):
 #   Column                   Non-Null Count  Dtype              
---  ------                   --------------  -----              
 0   effdate                  89535 non-null  datetime64[us]     
 1   acctnbr                  89535 non-null  object             
 2   ownersortname            89535 non-null  object             
 3   product                  89535 non-null  object             
 4   noteopenamt              89535 non-null  float64            
 5   ratetypcd                71422 non-null  object             
 6   mjaccttypcd              89535 non-null  object             
 7   currmiaccttypcd          89535 non-null  object             
 8   curracctstatcd           89535 non-null  object             
 9   noteintrate              89535 non-null  float64            
 10  bookbalance              89535 non-null  float64            
 11  notebal                  89535 non-null  float64            
 12  contractdate             89534 non-null  datetime64[us]     
 13  datemat                  32865 non-null  datetime64[us]     
 14  taxrptfororgnbr          12487 non-null  float64            
 15  taxrptforpersnbr         77048 non-null  float64            
 16  loanofficer              23363 non-null  object             
 17  acctofficer              62687 non-null  object             
 18  creditlimitamt           89535 non-null  float64            
 19  origintrate              22647 non-null  object             
 20  marginfixed              23363 non-null  object             
 21  fdiccatcd                22710 non-null  object             
 22  amortterm                23363 non-null  float64            
 23  totalpctsold             89535 non-null  float64            
 24  cobal                    89535 non-null  float64            
 25  credlimitclatresamt      89535 non-null  float64            
 26  riskratingcd             2756 non-null   object             
 27  origdate                 23185 non-null  datetime64[us]     
 28  currterm                 23363 non-null  float64            
 29  loanidx                  23353 non-null  object             
 30  rcf                      3133 non-null   object             
 31  availbalamt              89535 non-null  float64            
 32  fdiccatdesc              22710 non-null  object             
 33  origbal                  22533 non-null  float64            
 34  loanlimityn              23363 non-null  object             
 35  nextratechg              2795 non-null   datetime64[us]     
 36  Net Balance              89535 non-null  float64            
 37  Net Available            89535 non-null  float64            
 38  Net Collateral Reserve   89535 non-null  float64            
 39  Total Exposure           89535 non-null  float64            
 40  orig_ttl_loan_amt        89535 non-null  float64            
 41  portfolio_key            89535 non-null  int64              
 42  ownership_key            84958 non-null  float64            
 43  address_key              84958 non-null  float64            
 44  householdnbr             79972 non-null  float64            
 45  datelastmaint            79972 non-null  datetime64[us]     
 46  Category                 23363 non-null  object             
 47  inactivedate             2601 non-null   datetime64[us]     
 48  branchname               89535 non-null  object             
 49  primaryownercity         89512 non-null  object             
 50  primaryownerstate        89486 non-null  object             
 51  load_timestamp_utc       89535 non-null  datetime64[us, UTC]
 52  primaryownerzipcd        89486 non-null  object             
 53  Macro Account Type       86074 non-null  object             
 54  Net Balance_prior_year   89486 non-null  float64            
 55  Net Balance_prior_month  89486 non-null  float64            
dtypes: datetime64[us, UTC](1), datetime64[us](7), float64(24), int64(1), object(23)
memory usage: 38.3+ MB

portfolio_deriv
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 38926 entries, 0 to 38925
Data columns (total 8 columns):
 #   Column                 Non-Null Count  Dtype              
---  ------                 --------------  -----              
 0   portfolio_key          38926 non-null  int64              
 1   Muni_Present           38926 non-null  object             
 2   Category               38926 non-null  object             
 3   Total loan Balance     38926 non-null  float64            
 4   Total deposit Balance  38926 non-null  float64            
 5   Unique Loans           38926 non-null  int64              
 6   Unique Deposits        38926 non-null  int64              
 7   load_timestamp_utc     38926 non-null  datetime64[us, UTC]
dtypes: datetime64[us, UTC](1), float64(2), int64(3), object(2)
memory usage: 2.4+ MB

portfolio key is the link

Code:
# Core logic specific to project/report
#

from deltalake import DeltaTable
import pandas as pd
from pathlib import Path
import src.config
import cdutils.acct_file_creation.core # type: ignore
from src.utils.parquet_io import add_load_timestamp
from datetime import datetime
import numpy as np


def build_portfolio_dimension(df: pd.DataFrame, portfolio_col: str = "portfolio_key") -> pd.DataFrame:
    """
    Create a portfolio-level dimension table.

    Expects columns:
      - portfolio key:      portfolio_col (default 'portfolio_key')
      - product:            'product'
      - Macro Account Type: 'Macro Account Type' (values like 'Loan' / 'Deposit')
      - Net Balance:        'Net Balance'
      - account number:     'acctnbr'
      - tax fields:         'taxrptfororgnbr', 'taxrptforpersnbr'
    """

    # --- Normalize helpful helper columns ---
    df = df.copy()

    # Numeric balance
    df["__net_bal__"] = pd.to_numeric(df["Net Balance"], errors="coerce")

    # Macro Account Type normalized to lower-case strings
    mat = df["Macro Account Type"].astype(str).str.casefold()
    df["__is_loan__"] = mat.eq("loan")
    df["__is_deposit__"] = mat.eq("deposit")

    # Muni presence logic
    df["__is_muni__"] = (
        df["product"].str.contains("muni", case=False, na=False) &
        (~df["product"].str.contains("Community", case=False, na=False))
    )

    g = df.groupby(portfolio_col, dropna=False)

    # --- Muni presence (Y/N) ---
    muni_present = g["__is_muni__"].any().map({True: "Y", False: "N"})
    muni_present.name = "Muni_Present"

    # --- Category ---
    # if taxrptfororgnbr is all null -> 'Consumer'
    # elif taxrptforpersnbr is all null -> 'Business'
    # else 'Mixed'
    org_all_null  = g["taxrptfororgnbr"].apply(lambda s: s.isna().all())
    pers_all_null = g["taxrptforpersnbr"].apply(lambda s: s.isna().all())
    category = np.where(org_all_null, "Consumer",
                        np.where(pers_all_null, "Business", "Mixed"))
    category = pd.Series(category, index=org_all_null.index, name="Category")

    # --- Balances ---
    loan_bal = g.apply(lambda x: x.loc[x["__is_loan__"], "__net_bal__"].sum(min_count=1)).fillna(0.0)
    loan_bal.name = "Total loan Balance"

    dep_bal = g.apply(lambda x: x.loc[x["__is_deposit__"], "__net_bal__"].sum(min_count=1)).fillna(0.0)
    dep_bal.name = "Total deposit Balance"

    # --- Unique counts ---
    uniq_loans = g.apply(lambda x: x.loc[x["__is_loan__"], "acctnbr"].nunique(dropna=True))
    uniq_loans.name = "Unique Loans"

    uniq_deps = g.apply(lambda x: x.loc[x["__is_deposit__"], "acctnbr"].nunique(dropna=True))
    uniq_deps.name = "Unique Deposits"

    # --- Assemble dimension ---
    dim = pd.concat(
        [muni_present, category, loan_bal, dep_bal, uniq_loans, uniq_deps],
        axis=1
    ).reset_index()

    return dim

# Example usage:
# dim_table = build_portfolio_dimension(df, portfolio_col="portfolio_key")
# display(dim_table.head())



def main_pipeline():
# Main account table
    df = DeltaTable(src.config.SILVER / "account").to_pandas()
# Create loans/deposits distinction
    MACRO_TYPE_MAPPING = {
        'CML':'Loan',
        'MLN':'Loan',
        'CNS':'Loan',
        'MTG':'Loan',
        'CK':'Deposit',
        'SAV':'Deposit',
        'TD':'Deposit'
    }


    df['Macro Account Type'] = df['mjaccttypcd'].map(MACRO_TYPE_MAPPING)
    

    # # Year end data
    specified_date = datetime(2024, 12, 31)
    year_end_df = cdutils.acct_file_creation.core.query_df_on_date(specified_date)

    # # Prior month end data
    specified_date = datetime(2025, 9, 30)
    month_end_df = cdutils.acct_file_creation.core.query_df_on_date(specified_date)

    year_end_df = year_end_df[[
        'acctnbr',
        'Net Balance'
    ]].copy()

    month_end_df = month_end_df[[
        'acctnbr',
        'Net Balance'
    ]].copy()

    merged_history_df = year_end_df.merge(month_end_df, how='outer', on='acctnbr', suffixes=('_prior_year','_prior_month'))

    merged_history_df = merged_history_df.fillna(0)

    df = df.merge(merged_history_df, how='left', on='acctnbr').copy()

    portfolio = build_portfolio_dimension(df, portfolio_col="portfolio_key")

    return df, portfolio


Basically, my situation is that my join with the historical (prior year end data) is a left join instead of an outer. When I sum up the YTD balances (with slicer) or do balance changes, it's not truly balance because it missing accounts that were active then and not now (because I have current account table). Provide the specific modifications to this to make it. abetter data model to feed the powerBI

Ok so given my code, propose the specific changes (diffs) to give to a coding agent to make this change and achieve my result. I want to have account df at each date with effdate because we could have dimensions that change (loan officer, product). So we can always go through fact/dim on effdate. Equal joins are easier than range joins which is why we avoid SCD.

---
C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Data Analytics\Active_Customer_Dashboard_Proto\src\deposit_dash_prototype\core.py:61: FutureWarning: DataFrameGroupBy.apply operated on the grouping columns. This behavior is deprecated, and in a future version of pandas the grouping columns will be excluded from the operation. Either pass `include_groups=False` to exclude the groupings or explicitly select the grouping columns after groupby to silence this warning.
  loan_bal = g.apply(lambda x: x.loc[x["__is_loan__"], "__net_bal__"].sum(min_count=1)).fillna(0.0)
C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Data Analytics\Active_Customer_Dashboard_Proto\src\deposit_dash_prototype\core.py:64: FutureWarning: DataFrameGroupBy.apply operated on the grouping columns. This behavior is deprecated, and in a future version of pandas the grouping columns will be excluded from the operation. Either pass `include_groups=False` to exclude the groupings or explicitly select the grouping columns after groupby to silence this warning.
  dep_bal = g.apply(lambda x: x.loc[x["__is_deposit__"], "__net_bal__"].sum(min_count=1)).fillna(0.0)
C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Data Analytics\Active_Customer_Dashboard_Proto\src\deposit_dash_prototype\core.py:68: FutureWarning: DataFrameGroupBy.apply operated on the grouping columns. This behavior is deprecated, and in a future version of pandas the grouping columns will be excluded from the operation. Either pass `include_groups=False` to exclude the groupings or explicitly select the grouping columns after groupby to silence this warning.
  uniq_loans = g.apply(lambda x: x.loc[x["__is_loan__"], "acctnbr"].nunique(dropna=True))
C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Data Analytics\Active_Customer_Dashboard_Proto\src\deposit_dash_prototype\core.py:71: FutureWarning: DataFrameGroupBy.apply operated on the grouping columns. This behavior is deprecated, and in a future version of pandas the grouping columns will be excluded from the operation. Either pass `include_groups=False` to exclude the groupings or explicitly select the grouping columns after groupby to silence this warning.
  uniq_deps = g.apply(lambda x: x.loc[x["__is_deposit__"], "acctnbr"].nunique(dropna=True))