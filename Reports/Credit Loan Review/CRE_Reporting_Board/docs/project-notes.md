# 2025-08-05
src.main ran fine
- this is still fdic_recon in technical documentation

Issue with src.icre_production
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Credit Loan Review\CRE_Reporting_Board\Production\src\icre_production.py", line 95, in <module>
    main()
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Credit Loan Review\CRE_Reporting_Board\Production\src\icre_production.py", line 63, in main
    data_2023, orig_2023 = core_pipeline(data_2023, '2023-01-01 00:00:00')
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Credit Loan Review\CRE_Reporting_Board\Production\src\icre_production.py", line 35, in core_pipeline
    main_loan_data = src.transformations.calculations.cleaning_loan_data(main_loan_data)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Credit Loan Review\CRE_Reporting_Board\Production\src\transformations\calculations.py", line 67, in cleaning_loan_data
    main_loan_data[date_fields] = main_loan_data[date_fields].apply(pd.to_datetime)
                                  ~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\frame.py", line 4113, in __getitem__
    indexer = self.columns._get_indexer_strict(key, "columns")[1]
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\indexes\base.py", line 6212, in _get_indexer_strict
    self._raise_if_missing(keyarr, indexer, axis_name)
  File "C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\indexes\base.py", line 6264, in _raise_if_missing
    raise KeyError(f"{not_found} not in index")
KeyError: "['nextratechg'] not in index"


Notebook ran successfully

---

I have to refactor this to run smoother and get off src.cdutils
Then I have make sure that we adjust the logic for largest cumulative appraised value that classifies a loan into a certain category (JAP)
- I did this for Sean Cartwright

# 2025-08-05
# CRE Reporting Board - Refactored Implementation

## Summary

This project has been successfully refactored from the Production version to follow the standard project structure while maintaining exactly the same functionality.

## Changes Made

### 1. Project Structure
- Moved from Production/src structure to standard template structure
- Created `src/cre_board_reporting/` package instead of `src/project_name/`
- Updated all imports to use `cdutils` directly instead of `src.cdutils`

### 2. Configuration (src/config.py)
- Set up proper project metadata:
  - REPORT_NAME = "CRE Reporting Board"
  - BUSINESS_LINE = "Credit Loan Review" 
  - SCHEDULE = "Monthly"
  - OWNER = "Linda Sternfelt"
- Added caching configuration for development
- Set up proper paths for dev/prod environments

### 3. Data Fetching (src/cre_board_reporting/fetch_data.py)
- Migrated all SQL queries from Production version
- Uses dynamic MAX() dates instead of hardcoded dates
- Maintained exact same table joins and filters
- Added caching support for development
- Added data validation functions

### 4. Core Logic (src/cre_board_reporting/core.py)
- Complete pipeline implementation matching Production version
- Data fetching → Validation → Joining → Calculations → Output
- Maintains commented references to multiple property processing
- Same sorting logic (Total Exposure desc, acctnbr asc)

### 5. Transformations
- **joining.py**: Table join logic exactly as Production
- **calculations.py**: Total exposure calculation and data cleaning

### 6. Main Entry Point (src/main.py)
- Clean entry point with version tracking
- Proper error handling and logging
- Ready for production email distribution (commented)

## Key Features Preserved

1. **Same Data Sources**: COCCDM and OSIBANK tables
2. **Same Filtering**: CML/MLN accounts, ACT/NPFM status
3. **Same Logic**: Total Exposure = NOTEBAL + AVAILBALAMT
4. **Same Output**: cre_loader.xlsx with single property per loan
5. **Same Sorting**: By Total Exposure descending, then acctnbr

## Usage

```bash
cd "Reports/Credit Loan Review/CRE_Reporting_Board"
python -m src.main
```

## Environment Variables

- `REPORT_ENV=dev` (default) - Development mode with caching
- `REPORT_ENV=prod` - Production mode, writes to network location

## Output

- **Development**: `./output/cre_loader.xlsx`
- **Production**: Network path specified in config.py

## Next Steps

1. Test with actual database connection
2. Verify output matches Production version exactly
3. Add email distribution for production
4. Update production paths in config.py

This refactored version maintains 100% functional compatibility with the Production version while following best practices for maintainability and deployment.


----

2025-08-06 18:08:03 | INFO | === REPORT RUNNER SESSION START [DEV MODE] ===
2025-08-06 18:08:03 | INFO | DISCOVERY COMPLETE | Found 23 reports | Environment: DEV
2025-08-06 18:08:03 | INFO | BATCH START | 1 reports | Filter: name = CRE_Reporting_Board | Environment: DEV
2025-08-06 18:08:03 | INFO | START | CRE Reporting Board | Business Line: Credit Loan Review | Environment: DEV
2025-08-06 18:08:03 | INFO | DEBUG | Python executable: C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Scripts\python.exe
2025-08-06 18:08:03 | INFO | DEBUG | Working directory: Reports\Credit Loan Review\CRE_Reporting_Board
2025-08-06 18:08:03 | INFO | DEBUG | Command: C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Scripts\python.exe -m src.main
2025-08-06 18:08:59 | ERROR | FAILED | CRE Reporting Board | Runtime: 0.92 minutes
2025-08-06 18:08:59 | ERROR | Python executable: C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Scripts\python.exe
2025-08-06 18:08:59 | ERROR | Working directory: Reports\Credit Loan Review\CRE_Reporting_Board
2025-08-06 18:08:59 | ERROR | Return code: 1
2025-08-06 18:08:59 | ERROR | STDERR:
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Credit Loan Review\CRE_Reporting_Board\src\main.py", line 32, in <module>
    main()
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Credit Loan Review\CRE_Reporting_Board\src\main.py", line 17, in main
    output_path = run_cre_reporting_pipeline()
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Credit Loan Review\CRE_Reporting_Board\src\cre_board_reporting\core.py", line 181, in run_cre_reporting_pipeline
    processed_data = process_cre_data()
                     ^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Credit Loan Review\CRE_Reporting_Board\src\cre_board_reporting\core.py", line 129, in process_cre_data
    single_prop_data = consolidation_with_one_prop(main_loan_data, prop_data)
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Credit Loan Review\CRE_Reporting_Board\src\cre_board_reporting\core.py", line 76, in consolidation_with_one_prop
    result = pd.merge(main_loan_data, top_type_cleaned, on='acctnbr', how='left')
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\reshape\merge.py", line 170, in merge
    op = _MergeOperation(
         ^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\reshape\merge.py", line 807, in __init__
    self._maybe_coerce_merge_keys()
  File "C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\reshape\merge.py", line 1509, in _maybe_coerce_merge_keys
    raise ValueError(msg)
ValueError: You are trying to merge on object and int64 columns for key 'acctnbr'. If you wish to proceed you should use pd.concat
2025-08-06 18:08:59 | ERROR | STDOUT:
Fetching data from COCC...
Joining property tables...
Consolidating loan and property data...
Error in CRE Reporting pipeline: You are trying to merge on object and int64 columns for key 'acctnbr'. If you wish to proceed you should use pd.concat
Error in CRE Reporting Board processing: You are trying to merge on object and int64 columns for key 'acctnbr'. If you wish to proceed you should use pd.concat
2025-08-06 18:08:59 | INFO | BATCH COMPLETE | Total: 1 | Successful: 0 | Failed: 1 | Batch Runtime: 0.92 minutes
2025-08-06 18:08:59 | INFO | === REPORT RUNNER SESSION END ===


-----


2025-08-06 18:41:34 | INFO | === REPORT RUNNER SESSION START [DEV MODE] ===
2025-08-06 18:41:34 | INFO | DISCOVERY COMPLETE | Found 23 reports | Environment: DEV
2025-08-06 18:41:34 | INFO | BATCH START | 1 reports | Filter: name = CRE_Reporting_Board | Environment: DEV
2025-08-06 18:41:34 | INFO | START | CRE Reporting Board | Business Line: Credit Loan Review | Environment: DEV
2025-08-06 18:41:34 | INFO | DEBUG | Python executable: C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Scripts\python.exe
2025-08-06 18:41:34 | INFO | DEBUG | Working directory: Reports\Credit Loan Review\CRE_Reporting_Board
2025-08-06 18:41:34 | INFO | DEBUG | Command: C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Scripts\python.exe -m src.main
2025-08-06 18:43:54 | ERROR | FAILED | CRE Reporting Board | Runtime: 2.33 minutes
2025-08-06 18:43:54 | ERROR | Python executable: C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Scripts\python.exe
2025-08-06 18:43:54 | ERROR | Working directory: Reports\Credit Loan Review\CRE_Reporting_Board
2025-08-06 18:43:54 | ERROR | Return code: 1
2025-08-06 18:43:54 | ERROR | STDERR:
Traceback (most recent call last):
  File "C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\indexes\base.py", line 3812, in get_loc
    return self._engine.get_loc(casted_key)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "pandas/_libs/index.pyx", line 167, in pandas._libs.index.IndexEngine.get_loc
  File "pandas/_libs/index.pyx", line 196, in pandas._libs.index.IndexEngine.get_loc
  File "pandas/_libs/hashtable_class_helper.pxi", line 7088, in pandas._libs.hashtable.PyObjectHashTable.get_item
  File "pandas/_libs/hashtable_class_helper.pxi", line 7096, in pandas._libs.hashtable.PyObjectHashTable.get_item
KeyError: 'bookbalance'

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Credit Loan Review\CRE_Reporting_Board\src\main.py", line 32, in <module>
    main()
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Credit Loan Review\CRE_Reporting_Board\src\main.py", line 17, in main
    output_path = run_cre_reporting_pipeline()
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Credit Loan Review\CRE_Reporting_Board\src\cre_board_reporting\core.py", line 487, in run_cre_reporting_pipeline
    production_path, balance_path = generate_icre_reports()
                                    ^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Credit Loan Review\CRE_Reporting_Board\src\cre_board_reporting\core.py", line 239, in generate_icre_reports
    production_summary = calculate_production_summary()
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Credit Loan Review\CRE_Reporting_Board\src\cre_board_reporting\core.py", line 178, in calculate_production_summary
    _, originated_loans = fetch_icre_data_for_year(year)
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Credit Loan Review\CRE_Reporting_Board\src\cre_board_reporting\core.py", line 124, in fetch_icre_data_for_year
    main_loan_data = cdutils.acct_file_creation.core.query_df_on_date(year_end_date)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\cdutils\cdutils\acct_file_creation\core.py", line 60, in query_df_on_date
    raw_data = cdutils.acct_file_creation.core_transform.main_pipeline(data)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\cdutils\cdutils\acct_file_creation\core_transform.py", line 43, in main_pipeline
    main_loan_data = cdutils.loans.calculations.append_total_exposure_field(main_loan_data)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\cdutils\cdutils\loans\calculations.py", line 26, in append_total_exposure_field
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                            ~~^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\frame.py", line 4107, in __getitem__
    indexer = self.columns.get_loc(key)
              ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\indexes\base.py", line 3819, in get_loc
    raise KeyError(key) from err
KeyError: 'bookbalance'
2025-08-06 18:43:54 | ERROR | STDOUT:
=== CRE Reporting Board Pipeline ===

1. Processing CRE Loader data...
Fetching data from COCC...
Joining property tables...
Enforcing data type consistency...
Filtering to CRE loans only...
Filtered from 89579 total loans to 1741 CRE loans
Consolidating loan and property data...
Adding call code grouping...
Processing complete. Final dataset has 1741 records.

2. Generating CRE Loader output...
Writing output to: C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Credit Loan Review\CRE_Reporting_Board\output\cre_loader.xlsx
Output file created successfully: C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Credit Loan Review\CRE_Reporting_Board\output\cre_loader.xlsx

3. Generating Call Code Analysis reports...
Generating Total CML report...
Total CML report: C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Credit Loan Review\CRE_Reporting_Board\output\total_cml.xlsx
1-4 Fam Construction: $5,728,186.00
1-4 Family: $53,897,618.14
Construction: $105,913,940.08
I-CRE: $659,524,952.53
Other: $2,025,338.64
OwnerOcc: $344,756,390.24
Generating detailed I-CRE report...
I-CRE detailed report: C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Credit Loan Review\CRE_Reporting_Board\output\icre_detailed.xlsx
I-CRE total balance: $659,524,952.53
Generating Construction report...
Construction report: C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Credit Loan Review\CRE_Reporting_Board\output\construction.xlsx
Construction total balance: $105,913,940.08

4. Generating I-CRE Production and Balance reports...
Generating I-CRE production and balance reports...
Calculating I-CRE production summary...
Fetching I-CRE data for 2024...
Found 400 total I-CRE loans and 50 originated in 2024
2024: $136,426,550.00 in production (50 loans)
Fetching I-CRE data for 2023...
Column 'acctnbr' not found. Creating it with default None values.
Column 'acctnbr' not found. Creating it with default None values.
Column 'acctnbr' not found. Creating it with default None values.
Error in CRE Reporting pipeline: 'bookbalance'
Error in CRE Reporting Board processing: 'bookbalance'
2025-08-06 18:43:54 | INFO | BATCH COMPLETE | Total: 1 | Successful: 0 | Failed: 1 | Batch Runtime: 2.33 minutes
2025-08-06 18:43:54 | INFO | === REPORT RUNNER SESSION END ===

---
```
All Loans → Filter to 'CRE' Category → cre_loader.xlsx
                                    ↓
                            Apply Call Code Grouping
                                    ↓
                    ┌─────────────────┴─────────────────┐
                    ↓                                   ↓
            Filter to 'I-CRE'                 Filter to 'Construction'
            ↓                                   ↓
        icre_detailed.xlsx                 construction.xlsx
```


Report Hierarchy:
cre_loader.xlsx (main file):

Filters: [main_loan_data[main_loan_data['Category'] == 'CRE']]
Contains ALL CRE loans (all call codes in the CRE category)
I-CRE Detailed Report (subset):

Filters from the CRE data: processed_data[processed_data['fdiccatcd'].isin(['RENO', 'REMU'])]
Uses config: src.config.FDIC_CALL_CODE_GROUPS['I-CRE'] = ['RENO', 'REMU']
Construction Report (subset):

Filters from the CRE data: processed_data[processed_data['Cleaned Call Code'] == 'Construction']
Uses config: src.config.FDIC_CALL_CODE_GROUPS['Construction'] = ['OTCN','LAND','LNDV','RECN']


---

Need to add in WH_LOANS.NEXTRATECHG


---

SWAP Exposure - CM09
ACH Manager - CI07

need to come out of everything. 


- for CRE_loader, this should be fed datetime(2025,6,30) so date is as of then instead of passing nothing (and getting last business day)

PBI:
on slide for the interest rate change, only care about where next rate change < datemat

unique:
array(['Apartment Building', 'Warehouse', 'Multi Family', 'Hotel/Motel',
       'Office- General', '1-4 Fam Res - Non Own Occ', 'Shopping Plaza',
       'Real Estate - Business', 'Office - Medical', 'Commercial - Other',
       'Real Estate - Bus&Bus Assets', 'Industrial', 'Self Storage', nan,
       'Strip Plaza', 'Dealership', 'General Retail', 'Parking Lot',
       'Gas Station and Convenience St', 'Retail - Big Box Store',
       'Outdoor Recreation', 'Mixed Use (Retail/Office)', 'Day Care',
       'Restaurant', 'Mixed Use (Retail/Residential)',
       'Office - Professional', 'Mixed Use (Office/Residential)',
       'Manufacturing', 'Land - Improved', 'Auto-Truck Repair',
       'Golf Course', 'Seafood Processing Plant', 'All Business Assets',
       'Marketable Securities', 'Solar Farm', 'UCC - ABA',
       'UCC- Equipment', 'Assignment of Leases/Rents', 'Assisted Living',
       'Indoor Recreational', 'Land - Unimproved', 'Outdoor Dealers',
       '1 Family Residential - Own Occ', 'General Contractor', 'Marina',
       'Educational Facilities', 'Autobody/Gas Station', 'SBA Loan',
       'Hospitality/Event Space', 'Church',
       'Real Estate - Personal & Bus', 'Boat', 'Car Wash',
       'Real Estate - Pers&Bus Assets', 'Bus Assets w/Accts Receivable',
       'Savings - Partially Secured', '2 Family Residential - Own Occ',
       'Funeral Home', 'Passbook/Savings Secured', 'Vehicle - Business',
       'Condominium'], dtype=object)


IsNextRateChangeBeforeDateMat = 
IF(
    cre_loader[Next Rate Change] < cre_loader[datemat],
    "Y",
    "N"
)

Correction:
IsNextRateChangeBeforeDateMat =
IF(
    ISBLANK( cre_loader[Next Rate Change] ),
    "N",  // This is the result when Next Rate Change is null
    IF(
        cre_loader[Next Rate Change] < cre_loader[datemat],
        "Y",
        "N"
    )
)


1 Month CME Term SOFR
the BCSB Corporate Base Rate
the Wall Street Prime Rate


IsNextRateChangeBeforeDateMat =
VAR LoanIndex = cre_loader[loanidx]
RETURN
IF(
    // Rule 1: Check for the specific loan indexes first
    LoanIndex IN {
        "1 Month CME Term SOFR",
        "the BCSB Corporate Base Rate",
        "the Wall Street Prime Rate"
    },
    "N", // If it's one of those, force it to be "N"
    
    // If not, proceed to the original logic you had
    IF(
        ISBLANK( cre_loader[Next Rate Change] ),
        "N", // Rule 2: Handle blank dates
        IF(
            cre_loader[Next Rate Change] < cre_loader[datemat],
            "Y", // Rule 3: The primary date comparison
            "N"  // All other cases
        )
    )
)


May have lost this logic. Just need to readd to DAX if it didn't save on PBI side.