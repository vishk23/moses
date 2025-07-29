# 2025-07-24
Creating mono repo

# 2025-07-28 (CD)
- Initialized repo

Adding general notes here.

New output: still duplicates on schedule section
python .\testing\run_reports.py --name "R360"
=== REPORT RUNNER SESSION START [PROD MODE] ===
=== REPORT RUNNER SESSION START [PROD MODE] ===
Discovering reports...
DISCOVERY COMPLETE | Found 2 reports | Environment: PROD
Report Statistics:
   Total reports: 2
   Runnable (has main.py): 2
   Production ready: 1

By Business Line:
   Data Analytics: 1 reports
   Retail: 1 reports

By Schedule:
   Daily: 1 reports
   Monthly: 1 reports
   Monthly: 1 reports
BATCH START | 1 reports | Filter: name = R360 | Environment: PROD

   Monthly: 1 reports
   Monthly: 1 reports
   Monthly: 1 reports
BATCH START | 1 reports | Filter: name = R360 | Environment: PROD

Running 1 reports matching name: R360

[1/1] Running: R360 Customer Relationship Keys (Data Analytics)
START | R360 Customer Relationship Keys | Business Line: Data Analytics | Environment: PROD
DEBUG | Python executable: C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Scripts\python.exe
DEBUG | Working directory: Reports\Data Analytics\R360
DEBUG | Command: C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Scripts\python.exe -m src.main
SUCCESS | R360 Customer Relationship Keys | Runtime: 2.38 minutes
   Success: Success
BATCH COMPLETE | Total: 1 | Successful: 1 | Failed: 0 | Batch Runtime: 2.38 minutes

============================================================
Run Summary:
   Successful: 1
   Failed: 0
   Total Runtime: 2.38 minutes
=== REPORT RUNNER SESSION END ===