# 2025-08-22

2025-08-22 10:38:15 | INFO | === REPORT RUNNER SESSION START [PROD MODE] ===
2025-08-22 10:38:15 | INFO | DISCOVERY COMPLETE | Found 34 reports | Environment: PROD
2025-08-22 10:38:15 | INFO | BATCH START | 1 reports | Filter: name = Daily Account Table | Environment: PROD
2025-08-22 10:38:15 | INFO | START | Daily Account Table (Gold) | Business Line: Data Analytics | Environment: PROD
2025-08-22 10:38:15 | INFO | DEBUG | Python executable: C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Scripts\python.exe
2025-08-22 10:38:15 | INFO | DEBUG | Working directory: Reports\Data Analytics\Daily Account Table
2025-08-22 10:38:15 | INFO | DEBUG | Command: C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Scripts\python.exe -m src.main
2025-08-22 10:41:13 | ERROR | FAILED | Daily Account Table (Gold) | Runtime: 2.98 minutes
2025-08-22 10:41:13 | ERROR | Python executable: C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Scripts\python.exe
2025-08-22 10:41:13 | ERROR | Working directory: Reports\Data Analytics\Daily Account Table
2025-08-22 10:41:13 | ERROR | Return code: 1
2025-08-22 10:41:13 | ERROR | STDERR:
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Data Analytics\Daily Account Table\src\main.py", line 32, in <module>
    main()
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Data Analytics\Daily Account Table\src\main.py", line 28, in main
    df.to_parquet(OUTPUT_PATH, index=False)
  File "C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\util\_decorators.py", line 333, in wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\frame.py", line 3118, in to_parquet
    return to_parquet(
           ^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\io\parquet.py", line 482, in to_parquet
    impl.write(
  File "C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\io\parquet.py", line 229, in write
    self.api.parquet.write_table(
  File "C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pyarrow\parquet\core.py", line 1957, in write_table
    with ParquetWriter(
         ^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pyarrow\parquet\core.py", line 1064, in __init__
    sink = self.file_handle = filesystem.open_output_stream(
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "pyarrow\\_fs.pyx", line 912, in pyarrow._fs.FileSystem.open_output_stream
  File "pyarrow\\error.pxi", line 155, in pyarrow.lib.pyarrow_internal_check_status
  File "pyarrow\\error.pxi", line 92, in pyarrow.lib.check_status
PermissionError: [WinError 5] Failed to open local file '//00-da1/Home/Share/Data & Analytics Initiatives/Project Management/Data_Analytics/Daily Deposit Table/output/daily_account_table.parquet'. Detail: [Windows error 5] Access is denied.
2025-08-22 10:41:13 | ERROR | STDOUT: