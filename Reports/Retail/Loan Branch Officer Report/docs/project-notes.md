# 2025-08-04


2025-08-04 21:15:30 | INFO | === REPORT RUNNER SESSION START [PROD MODE] ===
2025-08-04 21:15:30 | INFO | DISCOVERY COMPLETE | Found 20 reports | Environment: PROD
2025-08-04 21:15:30 | INFO | BATCH START | 1 reports | Filter: name = Loan Branch Officer Report | Environment: PROD
2025-08-04 21:15:30 | INFO | START | Loan Branch Officer Report | Business Line: Retail | Environment: PROD
2025-08-04 21:15:30 | INFO | DEBUG | Python executable: C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Scripts\python.exe
2025-08-04 21:15:30 | INFO | DEBUG | Working directory: Reports\Retail\Loan Branch Officer Report
2025-08-04 21:15:30 | INFO | DEBUG | Command: C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Scripts\python.exe -m src.main
2025-08-04 21:17:06 | ERROR | FAILED | Loan Branch Officer Report | Runtime: 1.6 minutes
2025-08-04 21:17:06 | ERROR | Python executable: C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Scripts\python.exe
2025-08-04 21:17:06 | ERROR | Working directory: Reports\Retail\Loan Branch Officer Report
2025-08-04 21:17:06 | ERROR | Return code: 1
2025-08-04 21:17:06 | ERROR | STDOUT:
Starting Loan Branch Officer Report
Environment: prod
Fetching data from database...
Processing core transformations...
Adding primary keys...
Error in Loan Branch Officer Report: cannot access local variable 'cdutils' where it is not associated with a value
2025-08-04 21:17:06 | INFO | BATCH COMPLETE | Total: 1 | Successful: 0 | Failed: 1 | Batch Runtime: 1.6 minutes
2025-08-04 21:17:06 | INFO | === REPORT RUNNER SESSION END ===