# 2025-07-24
Creating mono repo

# 2025-07-28 (CD)
- Initialized repo

Adding general notes here.

# 2025-07-29 (CD)

python .\testing\run_reports.py --list
=== REPORT RUNNER SESSION START [PROD MODE] ===
Discovering reports...
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
Available Reports (use with --name):
==================================================

Data Analytics:
  • R360
    Title: R360 Customer Relationship Keys
    Schedule: Daily
    Status: ✓ Runnable | PROD
    Usage: python testing/run_reports.py --name "R360"


Retail:
  • Active Account Analysis
    Title: Active Account Analysis
    Schedule: Monthly
    Status: ✓ Runnable | DEV
    Usage: python testing/run_reports.py --name "Active Account Analysis"