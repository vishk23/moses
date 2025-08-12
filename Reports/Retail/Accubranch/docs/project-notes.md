Working directory: C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Retail\Accubranch
Output directory: C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Retail\Accubranch\output
--------------------------------------------------
Processing account data...
Fetching current account data...
Starting data cleaning pipeline for 2025-06-30
Using data source: production
Excluding organization types: ['MUNI', 'TRST']

=== Step 1: Loading supporting data ===
Loaded production data from database

=== Step 2: Generating account data for 2025-06-30 ===
Error during processing: 'function' object has no attribute 'fetch_data'
Traceback (most recent call last):
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Retail\Accubranch\src\main.py", line 36, in main
    accubranch_core.process_account_data()
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Retail\Accubranch\src\accubranch\core.py", line 312, in process_account_data
    current_data = process_current_account_data()
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Retail\Accubranch\src\accubranch\core.py", line 241, in process_current_account_data 
    data_current = src.data_cleaning_main.run_data_cleaning_pipeline(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Retail\Accubranch\src\data_cleaning_main.py", line 131, in run_data_cleaning_pipeline
    acct_df = src.accubranch.acct_file_creation.query_df_on_date(as_of_date)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Retail\Accubranch\src\accubranch\acct_file_creation.py", line 17, in query_df_on_date
    data = src.accubranch.fetch_data.fetch_data(specified_date)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'function' object has no attribute 'fetch_data'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Retail\Accubranch\src\main.py", line 57, in <module>
    main()
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Retail\Accubranch\src\main.py", line 53, in main
    sys.exit(1)
    ^^^
NameError: name 'sys' is not defined