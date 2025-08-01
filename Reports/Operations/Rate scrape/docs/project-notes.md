
2025-08-01 11:07:51 | INFO | === REPORT RUNNER SESSION START [PROD MODE] ===
2025-08-01 11:07:51 | INFO | DISCOVERY COMPLETE | Found 18 reports | Environment: PROD
2025-08-01 11:07:51 | INFO | BATCH START | 1 reports | Filter: name = Rate Scrape | Environment: PROD
2025-08-01 11:07:51 | INFO | START | Rate Scraping Report | Business Line: Operations | Environment: PROD
2025-08-01 11:07:51 | INFO | DEBUG | Python executable: C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Scripts\python.exe
2025-08-01 11:07:51 | INFO | DEBUG | Working directory: Reports\Operations\Rate Scrape
2025-08-01 11:07:51 | INFO | DEBUG | Command: C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Scripts\python.exe -m src.main
2025-08-01 11:08:06 | ERROR | FAILED | Rate Scraping Report | Runtime: 0.26 minutes
2025-08-01 11:08:06 | ERROR | Python executable: C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Scripts\python.exe
2025-08-01 11:08:06 | ERROR | Working directory: Reports\Operations\Rate Scrape
2025-08-01 11:08:06 | ERROR | Return code: 1
2025-08-01 11:08:06 | ERROR | STDERR:
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Operations\Rate Scrape\src\main.py", line 517, in <module>
    export_rate_table_to_excel(fred_data, cme_data, fhlb_data)
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Operations\Rate Scrape\src\main.py", line 486, in export_rate_table_to_excel
    cdutils.distribution.email_out(
TypeError: email_out() got an unexpected keyword argument 'cc_recipients'
2025-08-01 11:08:06 | ERROR | STDOUT:
Running Rate Scraper
Excel table written to C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Operations\Rate Scrape\output\Rate_Report_Aug_01_25_1108.xlsx
Excel table written to PDF C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Operations\Rate Scrape\output\Rate_Report_Aug_01_25_1108.pdf
2025-08-01 11:08:06 | INFO | BATCH COMPLETE | Total: 1 | Successful: 0 | Failed: 1 | Batch Runtime: 0.26 minutes
2025-08-01 11:08:06 | INFO | === REPORT RUNNER SESSION END ===


I fixed this issue. Just had to switch cc to bcc.