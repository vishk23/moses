2025-08-08 10:52:11 | INFO | === REPORT RUNNER SESSION START [PROD MODE] ===
2025-08-08 10:52:11 | INFO | DISCOVERY COMPLETE | Found 24 reports | Environment: PROD
2025-08-08 10:52:11 | INFO | BATCH START | 1 reports | Filter: name = Daily Mismatched Debit Card Txns | Environment: PROD
2025-08-08 10:52:11 | INFO | START | Daily Mismatched Debit Card Txns | Business Line: Risk Management | Environment: PROD
2025-08-08 10:52:11 | INFO | DEBUG | Python executable: C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Scripts\python.exe
2025-08-08 10:52:11 | INFO | DEBUG | Working directory: Reports\Risk Management\Daily Mismatched Debit Card Txns
2025-08-08 10:52:11 | INFO | DEBUG | Command: C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Scripts\python.exe -m src.main
2025-08-08 10:52:16 | ERROR | FAILED | Daily Mismatched Debit Card Txns | Runtime: 0.08 minutes
2025-08-08 10:52:16 | ERROR | Python executable: C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Scripts\python.exe
2025-08-08 10:52:16 | ERROR | Working directory: Reports\Risk Management\Daily Mismatched Debit Card Txns
2025-08-08 10:52:16 | ERROR | Return code: 1
2025-08-08 10:52:16 | ERROR | STDERR:
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Risk Management\Daily Mismatched Debit Card Txns\src\main.py", line 179, in <module>
    main()
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Risk Management\Daily Mismatched Debit Card Txns\src\main.py", line 144, in main
    filename = "Daily Posting Sheet " + date_str + ".xlsx"
               ~~~~~~~~~~~~~~~~~~~~~~~^~~~~~~~~~
TypeError: can only concatenate str (not "numpy.float64") to str
2025-08-08 10:52:16 | ERROR | STDOUT:
Starting [v1.0.0-prod]
PKID: 7730674
Downloaded and saved latest CO_VSUS file to INPUT_DIR: \\00-da1\Home\Share\Line of Business_Shared Services\Risk Management\Daily Mismatched Debit Card Txns\input\CO_VSUS_7730674.txt
Moved CO_VSUS_7730674.txt to input/archive directory.
2025-08-08 10:52:16 | INFO | BATCH COMPLETE | Total: 1 | Successful: 0 | Failed: 1 | Batch Runtime: 0.08 minutes
2025-08-08 10:52:16 | INFO | === REPORT RUNNER SESSION END ===

