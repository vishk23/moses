Example output log:
2025-07-30 23:37:53 | INFO | === REPORT RUNNER SESSION START [PROD MODE] ===
2025-07-30 23:37:53 | INFO | DISCOVERY COMPLETE | Found 16 reports | Environment: PROD
2025-07-30 23:37:53 | INFO | BATCH START | 1 reports | Filter: name = Dealer Reserve Recon | Environment: PROD
2025-07-30 23:37:53 | INFO | START | Dealer Reserve Recon | Business Line: Indirect Lending | Environment: PROD
2025-07-30 23:37:53 | INFO | DEBUG | Python executable: C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Scripts\python.exe
2025-07-30 23:37:53 | INFO | DEBUG | Working directory: Reports\Indirect Lending\Dealer Reserve Recon
2025-07-30 23:37:53 | INFO | DEBUG | Command: C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Scripts\python.exe -m src.main
2025-07-30 23:39:29 | INFO | SUCCESS | Dealer Reserve Recon | Runtime: 1.59 minutes
2025-07-30 23:39:29 | INFO | BATCH COMPLETE | Total: 1 | Successful: 1 | Failed: 0 | Batch Runtime: 1.59 minutes
2025-07-30 23:39:29 | INFO | === REPORT RUNNER SESSION END ===

2025-07-30 23:43:00 | INFO | === REPORT RUNNER SESSION START [PROD MODE] ===
2025-07-30 23:43:00 | INFO | DISCOVERY COMPLETE | Found 16 reports | Environment: PROD
2025-07-30 23:43:00 | INFO | BATCH START | 1 reports | Filter: name = Daily Deposit Update | Environment: PROD
2025-07-30 23:43:00 | INFO | START | Daily Deposit Update | Business Line: Data Analytics | Environment: PROD
2025-07-30 23:43:00 | INFO | DEBUG | Python executable: C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Scripts\python.exe
2025-07-30 23:43:00 | INFO | DEBUG | Working directory: Reports\Data Analytics\Daily Deposit Update
2025-07-30 23:43:00 | INFO | DEBUG | Command: C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Scripts\python.exe -m src.main
2025-07-30 23:43:01 | ERROR | FAILED | Daily Deposit Update | Runtime: 0.02 minutes
2025-07-30 23:43:01 | ERROR | Python executable: C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Scripts\python.exe
2025-07-30 23:43:01 | ERROR | Working directory: Reports\Data Analytics\Daily Deposit Update
2025-07-30 23:43:01 | ERROR | Return code: 1
2025-07-30 23:43:01 | ERROR | STDERR:
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Data Analytics\Daily Deposit Update\src\main.py", line 44, in <module>
    main()
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Data Analytics\Daily Deposit Update\src\main.py", line 16, in main
    print(f"Environment: {src.config.ENV}")
                          ^^^^^^^^^^^^^^
AttributeError: module 'src.config' has no attribute 'ENV'
2025-07-30 23:43:01 | ERROR | STDOUT:
Starting [v2.0.1-prod]
Running Daily Deposit Update for Data Analytics
Schedule: Daily
Owner: Chad Doorley
2025-07-30 23:43:01 | INFO | BATCH COMPLETE | Total: 1 | Successful: 0 | Failed: 1 | Batch Runtime: 0.02 minutes
2025-07-30 23:43:01 | INFO | === REPORT RUNNER SESSION END ===

