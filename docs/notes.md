# 2025-07-24
Creating mono repo


pytest output:
Fix suggestions:
   - Missing input files - try running with --sync flag

FileNotFoundError: [Errno 2] No such file or directory: 'C:\\Users\\w322800\\Documents\\gh\\new1\\Reports\\Commercial_Lending\\DepositPocketPricing\\assets\\DepositPocketPricing.xlsx'

--------------------------------------------------
📝 OUTPUT:
--------------------------------------------------
Starting Deposit Pocket Pricing Report

--------------------------------------------------
💡 Fix suggestions:
   - Missing input files - try running with --sync flag

--------------------------------------------------
📝 OUTPUT:
--------------------------------------------------
Starting Deposit Pocket Pricing Report

--------------------------------------------------
💡 Fix suggestions:
   - Missing input files - try running with --sync flag

Starting Deposit Pocket Pricing Report

--------------------------------------------------
💡 Fix suggestions:
   - Missing input files - try running with --sync flag


--------------------------------------------------
💡 Fix suggestions:
   - Missing input files - try running with --sync flag

💡 Fix suggestions:
   - Missing input files - try running with --sync flag

   - Missing input files - try running with --sync flag

FAILED

FAILED
testing/test_reports.py::test_report[Status Page]
FAILED
testing/test_reports.py::test_report[Status Page]
testing/test_reports.py::test_report[Status Page]
🧪 Testing report: Status Page
📁 Path: Reports\Commercial_Lending\Status Page
📋 Loaded test config for Status Page: 4 settings
🔍 Checking required files...
   main.py: ✅
   config.py: ✅
🧹 Preparing output directory: Reports\Commercial_Lending\Status Page\output
   Creating output directory
🚀 Executing report...
   Command: C:\Users\w322800\Documents\gh\new1\.venv\Scripts\python.exe src/main.py
   Working directory: C:\Users\w322800\Documents\gh\new1\Reports\Commercial_Lending\Status Page
   Environment: REPORT_ENV=dev
   PYTHONPATH: C:\Users\w322800\Documents\gh\new1\Reports\Commercial_Lending\Status Page;C:\Users\w322800\Documents...
   OS: nt, Path separator: ';'
⏱️  Execution time: 86.24 seconds
📤 Return code: 1
📝 Output preview (first 500 chars):
   Starting Status Page Report

⚠️  Error output:
   Traceback (most recent call last):
  File "C:\Users\w322800\Documents\gh\new1\Reports\Commercial_Lending\Status Page\src\main.py", line 206, in <module>
    main()
  File "C:\Users\w322800\Documents\gh\new1\Reports\Commercial_Lending\Status Page\src\main.py", line 123, in main
    filtered_data = src.core_transform.filtering_on_pkey(raw_data, key)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\new1\Reports\Commercial_Lending\Status Page\src\core_transform.py", line 67, in filtering_on_pkey
    assert (df['portfolio_key'] == key).any(), "Portfolio key does not map to any active products"
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: Portfolio key does not map to any active products


❌ EXECUTION FAILED
📋 Report: Status Page
⏱️  Time: 86.24 seconds
📤 Exit code: 1
🚨 ERROR DETAILS:
--------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\w322800\Documents\gh\new1\Reports\Commercial_Lending\Status Page\src\main.py", line 206, in <module>
    main()
  File "C:\Users\w322800\Documents\gh\new1\Reports\Commercial_Lending\Status Page\src\main.py", line 123, in main
    filtered_data = src.core_transform.filtering_on_pkey(raw_data, key)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\new1\Reports\Commercial_Lending\Status Page\src\core_transform.py", line 67, in filtering_on_pkey
    assert (df['portfolio_key'] == key).any(), "Portfolio key does not map to any active products"
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: Portfolio key does not map to any active products

--------------------------------------------------
📝 OUTPUT:
--------------------------------------------------
Starting Status Page Report

--------------------------------------------------
💡 Fix suggestions:

FAILED
testing/test_reports.py::test_report[YTD_Business_Deposits]
🧪 Testing report: YTD_Business_Deposits
📁 Path: Reports\Commercial_Lending\YTD_Business_Deposits
📋 Loaded test config for YTD_Business_Deposits: 4 settings
🔍 Checking required files...
   main.py: ✅
   config.py: ✅
🧹 Preparing output directory: Reports\Commercial_Lending\YTD_Business_Deposits\output
   Creating output directory
🚀 Executing report...
   Command: C:\Users\w322800\Documents\gh\new1\.venv\Scripts\python.exe src/main.py
   Working directory: C:\Users\w322800\Documents\gh\new1\Reports\Commercial_Lending\YTD_Business_Deposits
   Environment: REPORT_ENV=dev
   PYTHONPATH: C:\Users\w322800\Documents\gh\new1\Reports\Commercial_Lending\YTD_Business_Deposits;C:\Users\w322800...
   OS: nt, Path separator: ';'
⏱️  Execution time: 4.92 seconds
📤 Return code: 0
📝 Output preview (first 500 chars):
   Starting YTD Business Deposit Report
Development mode - email not sent. Output file: C:\Users\w322800\Documents\gh\new1\Reports\Commercial_Lending\YTD_Business_Deposits\output\business_deposit_report_2025_YTD.xlsx
Complete!

📊 Output verification:
   Generated files: 1
      📄 business_deposit_report_2025_YTD.xlsx (48392 bytes)
   Expected patterns: ['ytd_business_deposits_*.xlsx']
      Pattern 'ytd_business_deposits_*.xlsx': 0 matches
FAILED
testing/test_reports.py::test_report[Payroll_and_Vendor]
🧪 Testing report: Payroll_and_Vendor
📁 Path: Reports\Government Banking\Payroll_and_Vendor
📋 Loaded test config for Payroll_and_Vendor: 5 settings
⏭️  Skipping: Requires database connection
SKIPPED (Requires database connection)
testing/test_reports.py::test_report[Dealer Reserve Recon]
🧪 Testing report: Dealer Reserve Recon
📁 Path: Reports\Indirect_Lending\Dealer Reserve Recon
📋 Loaded test config for Dealer Reserve Recon: 4 settings
🔍 Checking required files...
   main.py: ❌
   config.py: ✅
FAILED
testing/test_reports.py::test_report[EContracts]
🧪 Testing report: EContracts
📁 Path: Reports\Indirect_Lending\EContracts
📋 Loaded test config for EContracts: 4 settings
🔍 Checking required files...
   main.py: ✅
   config.py: ✅
🧹 Preparing output directory: Reports\Indirect_Lending\EContracts\output
   Creating output directory
🚀 Executing report...
   Command: C:\Users\w322800\Documents\gh\new1\.venv\Scripts\python.exe src/main.py
   Working directory: C:\Users\w322800\Documents\gh\new1\Reports\Indirect_Lending\EContracts
   Environment: REPORT_ENV=dev
   PYTHONPATH: C:\Users\w322800\Documents\gh\new1\Reports\Indirect_Lending\EContracts;C:\Users\w322800\Documents\gh...
   OS: nt, Path separator: ';'
⏱️  Execution time: 0.87 seconds
📤 Return code: 1
📝 Output preview (first 500 chars):
   Starting EContracts Report

⚠️  Error output:
   Traceback (most recent call last):
  File "C:\Users\w322800\Documents\gh\new1\Reports\Indirect_Lending\EContracts\src\main.py", line 107, in <module>
    main()
  File "C:\Users\w322800\Documents\gh\new1\Reports\Indirect_Lending\EContracts\src\main.py", line 56, in main
    combined_funding_reports, book_to_look = grabData.grabData()
                                             ^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\new1\Reports\Indirect_Lending\EContracts\src\grabData.py", line 42, in grabData
    for filename in os.listdir(folder_path):
                    ^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [WinError 3] The system cannot find the path specified: 'C:\\Users\\w322800\\Documents\\gh\\new1\\Reports\\Indirect_Lending\\EContracts\\input'


❌ EXECUTION FAILED
📋 Report: EContracts
⏱️  Time: 0.87 seconds
📤 Exit code: 1
🚨 ERROR DETAILS:
--------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\w322800\Documents\gh\new1\Reports\Indirect_Lending\EContracts\src\main.py", line 107, in <module>
    main()
  File "C:\Users\w322800\Documents\gh\new1\Reports\Indirect_Lending\EContracts\src\main.py", line 56, in main
    combined_funding_reports, book_to_look = grabData.grabData()
                                             ^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\new1\Reports\Indirect_Lending\EContracts\src\grabData.py", line 42, in grabData
    for filename in os.listdir(folder_path):
                    ^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [WinError 3] The system cannot find the path specified: 'C:\\Users\\w322800\\Documents\\gh\\new1\\Reports\\Indirect_Lending\\EContracts\\input'

--------------------------------------------------
📝 OUTPUT:
--------------------------------------------------
Starting EContracts Report

--------------------------------------------------
💡 Fix suggestions:

FAILED
testing/test_reports.py::test_report[Rate Scraping]
🧪 Testing report: Rate Scraping
📁 Path: Reports\Operations\Rate Scraping
📋 Loaded test config for Rate Scraping: 5 settings
🔍 Checking required files...
   main.py: ✅
   config.py: ✅
🧹 Preparing output directory: Reports\Operations\Rate Scraping\output
   Creating output directory
🚀 Executing report...
   Command: C:\Users\w322800\Documents\gh\new1\.venv\Scripts\python.exe src/main.py
   Working directory: C:\Users\w322800\Documents\gh\new1\Reports\Operations\Rate Scraping
   Environment: REPORT_ENV=dev
   PYTHONPATH: C:\Users\w322800\Documents\gh\new1\Reports\Operations\Rate Scraping;C:\Users\w322800\Documents\gh\ne...
   OS: nt, Path separator: ';'
⏱️  Execution time: 6.29 seconds
📤 Return code: 1
📝 Output preview (first 500 chars):
   Running Rate Scraper

⚠️  Error output:
   Traceback (most recent call last):
  File "C:\Users\w322800\Documents\gh\new1\Reports\Operations\Rate Scraping\src\main.py", line 391, in <module>
    cme_data = get_cme_term_sofr_data()
               ^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\new1\Reports\Operations\Rate Scraping\src\main.py", line 116, in get_cme_term_sofr_data
    browser = p.chromium.launch(headless=False)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\new1\.venv\Lib\site-packages\playwright\sync_api\_generated.py", line 14494, in launch
    self._sync(
  File "C:\Users\w322800\Documents\gh\new1\.venv\Lib\site-packages\playwright\_impl\_sync_base.py", line 115, in _sync
    return task.result()
           ^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\new1\.venv\Lib\site-packages\playwright\_impl\_browser_type.py", line 98, in launch
    await self._channel.send(
  File "C:\Users\w322800\Documents\gh\new1\.venv\Lib\site-packages\playwright\_impl\_connection.py", line 69, in send
    return await self._connection.wrap_api_call(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\new1\.venv\Lib\site-packages\playwright\_impl\_connection.py", line 558, in wrap_api_call
    raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
playwright._impl._errors.Error: BrowserType.launch: Executable doesn't exist at C:\Users\w322800\AppData\Local\ms-playwright\chromium-1181\chrome-win\chrome.exe
\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557
\u2551 Looks like Playwright was just installed or updated.       \u2551
\u2551 Please run the following command to download new browsers: \u2551
\u2551                                                            \u2551
\u2551     playwright install                                     \u2551
\u2551                                                            \u2551
\u2551 <3 Playwright Team                                         \u2551
\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d


❌ EXECUTION FAILED
📋 Report: Rate Scraping
⏱️  Time: 6.29 seconds
📤 Exit code: 1
🚨 ERROR DETAILS:
--------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\w322800\Documents\gh\new1\Reports\Operations\Rate Scraping\src\main.py", line 391, in <module>
    cme_data = get_cme_term_sofr_data()
               ^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\new1\Reports\Operations\Rate Scraping\src\main.py", line 116, in get_cme_term_sofr_data
    browser = p.chromium.launch(headless=False)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\new1\.venv\Lib\site-packages\playwright\sync_api\_generated.py", line 14494, in launch
    self._sync(
  File "C:\Users\w322800\Documents\gh\new1\.venv\Lib\site-packages\playwright\_impl\_sync_base.py", line 115, in _sync
    return task.result()
           ^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\new1\.venv\Lib\site-packages\playwright\_impl\_browser_type.py", line 98, in launch
    await self._channel.send(
  File "C:\Users\w322800\Documents\gh\new1\.venv\Lib\site-packages\playwright\_impl\_connection.py", line 69, in send
    return await self._connection.wrap_api_call(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\new1\.venv\Lib\site-packages\playwright\_impl\_connection.py", line 558, in wrap_api_call
    raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
playwright._impl._errors.Error: BrowserType.launch: Executable doesn't exist at C:\Users\w322800\AppData\Local\ms-playwright\chromium-1181\chrome-win\chrome.exe
\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557
\u2551 Looks like Playwright was just installed or updated.       \u2551
\u2551 Please run the following command to download new browsers: \u2551
\u2551                                                            \u2551
\u2551     playwright install                                     \u2551
\u2551                                                            \u2551
\u2551 <3 Playwright Team                                         \u2551
\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d

--------------------------------------------------
📝 OUTPUT:
--------------------------------------------------
Running Rate Scraper

--------------------------------------------------
💡 Fix suggestions:

FAILED
testing/test_reports.py::test_report[Trial Balance Ops]
🧪 Testing report: Trial Balance Ops
📁 Path: Reports\Operations\Trial Balance Ops
📋 Loaded test config for Trial Balance Ops: 4 settings
🔍 Checking required files...
   main.py: ✅
   config.py: ✅
🧹 Preparing output directory: Reports\Operations\Trial Balance Ops\output
   Creating output directory
🚀 Executing report...
   Command: C:\Users\w322800\Documents\gh\new1\.venv\Scripts\python.exe src/main.py
   Working directory: C:\Users\w322800\Documents\gh\new1\Reports\Operations\Trial Balance Ops
   Environment: REPORT_ENV=dev
   PYTHONPATH: C:\Users\w322800\Documents\gh\new1\Reports\Operations\Trial Balance Ops;C:\Users\w322800\Documents\g...
   OS: nt, Path separator: ';'
⏱️  Execution time: 36.60 seconds
📤 Return code: 0
📝 Output preview (first 500 chars):
   Starting Trial Balance Ops Report
Development mode - email not sent. Output files: C:\Users\w322800\Documents\gh\new1\Reports\Operations\Trial Balance Ops\output\CML_Trial_Balance_Ops_20250630.xlsx, C:\Users\w322800\Documents\gh\new1\Reports\Operations\Trial Balance Ops\output\CML_Trial_Balance_Ops_MultipleProperties20250630.xlsx
Complete!

📊 Output verification:
   Generated files: 2
      📄 CML_Trial_Balance_Ops_20250630.xlsx (821782 bytes)
      📄 CML_Trial_Balance_Ops_MultipleProperties20250630.xlsx (2442220 bytes)
   Expected patterns: ['daily_trial_balance_report_*.xlsx', 'trial_balance_ops_*.xlsx']
      Pattern 'daily_trial_balance_report_*.xlsx': 0 matches
FAILED
testing/test_reports.py::test_report[Classifieds]
🧪 Testing report: Classifieds
📁 Path: Reports\Resolution Committee Automation\Classifieds
📋 Loaded test config for Classifieds: 4 settings
🔍 Checking required files...
   main.py: ✅
   config.py: ✅
🧹 Preparing output directory: Reports\Resolution Committee Automation\Classifieds\output
   Creating output directory
🚀 Executing report...
   Command: C:\Users\w322800\Documents\gh\new1\.venv\Scripts\python.exe src/main.py
   Working directory: C:\Users\w322800\Documents\gh\new1\Reports\Resolution Committee Automation\Classifieds
   Environment: REPORT_ENV=dev
   PYTHONPATH: C:\Users\w322800\Documents\gh\new1\Reports\Resolution Committee Automation\Classifieds;C:\Users\w322...
   OS: nt, Path separator: ';'
⏱️  Execution time: 48.87 seconds
📤 Return code: 0
📝 Output preview (first 500 chars):
   Starting Resolution Committee Classifieds Report
Report generated: C:\Users\w322800\Documents\gh\new1\Reports\Resolution Committee Automation\Classifieds\output\2025-06-30classifieds_report.xlsx
Development mode - email not sent
Complete!

📊 Output verification:
   Generated files: 1
      📄 2025-06-30classifieds_report.xlsx (16470 bytes)
   Expected patterns: ['*_classifieds_report.xlsx']
      Pattern '*_classifieds_report.xlsx': 0 matches
FAILED
testing/test_reports.py::test_report[Delinquency]
🧪 Testing report: Delinquency
📁 Path: Reports\Resolution Committee Automation\Delinquency
📋 Loaded test config for Delinquency: 4 settings
🔍 Checking required files...
   main.py: ✅
   config.py: ✅
🧹 Preparing output directory: Reports\Resolution Committee Automation\Delinquency\output
   Creating output directory
🚀 Executing report...
   Command: C:\Users\w322800\Documents\gh\new1\.venv\Scripts\python.exe src/main.py
   Working directory: C:\Users\w322800\Documents\gh\new1\Reports\Resolution Committee Automation\Delinquency
   Environment: REPORT_ENV=dev
   PYTHONPATH: C:\Users\w322800\Documents\gh\new1\Reports\Resolution Committee Automation\Delinquency;C:\Users\w322...
   OS: nt, Path separator: ';'
⏱️  Execution time: 87.79 seconds
📤 Return code: 0
📝 Output preview (first 500 chars):
   Starting Resolution Committee Delinquency Report
Report saved to C:\Users\w322800\Documents\gh\new1\Reports\Resolution Committee Automation\Delinquency\output\Delinquency_063025.xlsx
Email prepared successfully in Outlook!
Complete!

📊 Output verification:
   Generated files: 1
      📄 Delinquency_063025.xlsx (80208 bytes)
   Expected patterns: ['*_delinquency_report.xlsx']
      Pattern '*_delinquency_report.xlsx': 0 matches
FAILED
testing/test_reports.py::test_report[Financial Difficulty Modifications]
🧪 Testing report: Financial Difficulty Modifications
📁 Path: Reports\Resolution Committee Automation\Financial Difficulty Modifications
📋 Loaded test config for Financial Difficulty Modifications: 4 settings
🔍 Checking required files...
   main.py: ✅
   config.py: ✅
🧹 Preparing output directory: Reports\Resolution Committee Automation\Financial Difficulty Modifica tions\output
   Creating output directory
🚀 Executing report...
   Command: C:\Users\w322800\Documents\gh\new1\.venv\Scripts\python.exe src/main.py
   Working directory: C:\Users\w322800\Documents\gh\new1\Reports\Resolution Committee Automation\Financial Difficulty Modifications
   Environment: REPORT_ENV=dev
   PYTHONPATH: C:\Users\w322800\Documents\gh\new1\Reports\Resolution Committee Automation\Financial Difficulty Modi...
   OS: nt, Path separator: ';'
⏱️  Execution time: 83.92 seconds
📤 Return code: 0
📝 Output preview (first 500 chars):
   Starting Resolution Committee Financial Difficulty Modifications Report
Report generated: C:\Users\w322800\Documents\gh\new1\Reports\Resolution Committee Automation\Financial Difficulty Modifications\output\2025-06-30_FDM_report.xlsx
Development mode - email not sent
Complete!

⚠️  Error output:
   C:\Users\w322800\Documents\gh\new1\Reports\Resolution Committee Automation\Financial Difficulty Modifications\src\main.py:509: FutureWarning: The default 
of observed=False is deprecated and will be changed to True in a future version of pandas. Pass observed=False to retain current behavior or observed=True to adopt the future default and silence this warning.
  summary = df.groupby(['bucket','Major'])['Net Balance'].sum().reset_index()
C:\Users\w322800\Documents\gh\new1\Reports\Resolution Committee Automation\Financial Difficulty Modifications\src\main.py:509: FutureWarning: The default of 
observed=False is deprecated and will be changed to True in a future version of pandas. Pass observed=False to retain current behavior or observed=True to adopt the future default and silence this warning.
  summary = df.groupby(['bucket','Major'])['Net Balance'].sum().reset_index()
C:\Users\w322800\Documents\gh\new1\Reports\Resolution Committee Automation\Financial Difficulty Modifications\src\main.py:485: FutureWarning: The default of 
observed=False is deprecated and will be changed to True in a future version of pandas. Pass observed=False to retain current behavior or observed=True to adopt the future default and silence this warning.
  summary = df.groupby(['bucket','Major'])['Account Number'].nunique().reset_index()
C:\Users\w322800\Documents\gh\new1\Reports\Resolution Committee Automation\Financial Difficulty Modifications\src\main.py:485: FutureWarning: The default of 
observed=False is deprecated and will be changed to True in a future version of pandas. Pass observed=False to retain current behavior or observed=True to adopt the future default and silence this warning.
  summary = df.groupby(['bucket','Major'])['Account Number'].nunique().reset_index()
C:\Users\w322800\Documents\gh\new1\Reports\Resolution Committee Automation\Financial Difficulty Modifications\src\main.py:588: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
  summary_combined_df = pd.concat([completed_summary_cml, empty_row, completed_summary_cns, empty_row, completed_summary_mtg], ignore_index=True)

📊 Output verification:
   Generated files: 1
      📄 2025-06-30_FDM_report.xlsx (8236 bytes)
   Expected patterns: ['*_FDM_report.xlsx']
      Pattern '*_FDM_report.xlsx': 1 matches
✅ Test passed for Financial Difficulty Modifications
----------------------------------------
PASSED
testing/test_reports.py::test_report[Non Accruals]
🧪 Testing report: Non Accruals
📁 Path: Reports\Resolution Committee Automation\Non Accruals
📋 Loaded test config for Non Accruals: 4 settings
🔍 Checking required files...
   main.py: ✅
   config.py: ✅
🧹 Preparing output directory: Reports\Resolution Committee Automation\Non Accruals\output
   Creating output directory
🚀 Executing report...
   Command: C:\Users\w322800\Documents\gh\new1\.venv\Scripts\python.exe src/main.py
   Working directory: C:\Users\w322800\Documents\gh\new1\Reports\Resolution Committee Automation\Non Accruals
   Environment: REPORT_ENV=dev
   PYTHONPATH: C:\Users\w322800\Documents\gh\new1\Reports\Resolution Committee Automation\Non Accruals;C:\Users\w32...
   OS: nt, Path separator: ';'
⏱️  Execution time: 212.30 seconds
📤 Return code: 0
📝 Output preview (first 500 chars):
   Starting Resolution Committee Non Accrual Report
\\00-DA1\Home\Share\\Data & Analytics Initiatives\\Project Management\\Credit_Loan_Review\\Resolution Committee Automation\\Non Accruals\\Production\\Output\NonAccruals July 2025.xlsx
Report saved to \\00-DA1\Home\Share\\Data & Analytics Initiatives\\Project Management\\Credit_Loan_Review\\Resolution Committee Automation\\Non Accruals\\Production\\Output\NonAccruals July 2025.xlsx
Script took 0.5359201431274414 seconds.
Development mode - email no
   ... (truncated, 517 total chars)
📊 Output verification:
   Generated files: 0
   Expected patterns: ['*_non_accruals_report.xlsx']
      Pattern '*_non_accruals_report.xlsx': 0 matches
FAILED
testing/test_reports.py::test_report[New_Business_Checking]
🧪 Testing report: New_Business_Checking
📁 Path: Reports\Retail\New_Business_Checking
📋 Loaded test config for New_Business_Checking: 4 settings
🔍 Checking required files...
   main.py: ✅
   config.py: ✅
🧹 Preparing output directory: Reports\Retail\New_Business_Checking\output
   Creating output directory
🚀 Executing report...
   Command: C:\Users\w322800\Documents\gh\new1\.venv\Scripts\python.exe src/main.py
   Working directory: C:\Users\w322800\Documents\gh\new1\Reports\Retail\New_Business_Checking
   Environment: REPORT_ENV=dev
   PYTHONPATH: C:\Users\w322800\Documents\gh\new1\Reports\Retail\New_Business_Checking;C:\Users\w322800\Documents\g...
   OS: nt, Path separator: ';'
⏱️  Execution time: 0.63 seconds
📤 Return code: 1
📝 Output preview (first 500 chars):
   Starting New Business Checking Report

⚠️  Error output:
   Traceback (most recent call last):
  File "C:\Users\w322800\Documents\gh\new1\Reports\Retail\New_Business_Checking\src\main.py", line 78, in <module>
    main()
  File "C:\Users\w322800\Documents\gh\new1\Reports\Retail\New_Business_Checking\src\main.py", line 41, in main
    data = cdutils.database.fetch_data()
           ^^^^^^^
UnboundLocalError: cannot access local variable 'cdutils' where it is not associated with a value


❌ EXECUTION FAILED
📋 Report: New_Business_Checking
⏱️  Time: 0.63 seconds
📤 Exit code: 1
🚨 ERROR DETAILS:
--------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\w322800\Documents\gh\new1\Reports\Retail\New_Business_Checking\src\main.py", line 78, in <module>
    main()
  File "C:\Users\w322800\Documents\gh\new1\Reports\Retail\New_Business_Checking\src\main.py", line 41, in main
    data = cdutils.database.fetch_data()
           ^^^^^^^
UnboundLocalError: cannot access local variable 'cdutils' where it is not associated with a value

--------------------------------------------------
📝 OUTPUT:
--------------------------------------------------
Starting New Business Checking Report

--------------------------------------------------
💡 Fix suggestions:

FAILED
testing/test_reports.py::test_report[New_Consumer_Checking]
🧪 Testing report: New_Consumer_Checking
📁 Path: Reports\Retail\New_Consumer_Checking
📋 Loaded test config for New_Consumer_Checking: 4 settings
🔍 Checking required files...
   main.py: ✅
   config.py: ✅
🧹 Preparing output directory: Reports\Retail\New_Consumer_Checking\output
   Creating output directory
🚀 Executing report...
   Command: C:\Users\w322800\Documents\gh\new1\.venv\Scripts\python.exe src/main.py
   Working directory: C:\Users\w322800\Documents\gh\new1\Reports\Retail\New_Consumer_Checking
   Environment: REPORT_ENV=dev
   PYTHONPATH: C:\Users\w322800\Documents\gh\new1\Reports\Retail\New_Consumer_Checking;C:\Users\w322800\Documents\g...
   OS: nt, Path separator: ';'
⏱️  Execution time: 0.59 seconds
📤 Return code: 1
📝 Output preview (first 500 chars):
   Starting New Consumer Checking Report

⚠️  Error output:
   Traceback (most recent call last):
  File "C:\Users\w322800\Documents\gh\new1\Reports\Retail\New_Consumer_Checking\src\main.py", line 80, in <module>
    main()
  File "C:\Users\w322800\Documents\gh\new1\Reports\Retail\New_Consumer_Checking\src\main.py", line 42, in main
    data = cdutils.database.fetch_data()
           ^^^^^^^
UnboundLocalError: cannot access local variable 'cdutils' where it is not associated with a value


❌ EXECUTION FAILED
📋 Report: New_Consumer_Checking
⏱️  Time: 0.59 seconds
📤 Exit code: 1
🚨 ERROR DETAILS:
--------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\w322800\Documents\gh\new1\Reports\Retail\New_Consumer_Checking\src\main.py", line 80, in <module>
    main()
  File "C:\Users\w322800\Documents\gh\new1\Reports\Retail\New_Consumer_Checking\src\main.py", line 42, in main
    data = cdutils.database.fetch_data()
           ^^^^^^^
UnboundLocalError: cannot access local variable 'cdutils' where it is not associated with a value

--------------------------------------------------
📝 OUTPUT:
--------------------------------------------------
Starting New Consumer Checking Report

--------------------------------------------------
💡 Fix suggestions:

FAILED
testing/test_reports.py::test_report[NewLoanReport_Francine]
🧪 Testing report: NewLoanReport_Francine
📁 Path: Reports\Retail\NewLoanReport_Francine
📋 Loaded test config for NewLoanReport_Francine: 4 settings
🔍 Checking required files...
   main.py: ✅
   config.py: ✅
🧹 Preparing output directory: Reports\Retail\NewLoanReport_Francine\output
   Creating output directory
🚀 Executing report...
   Command: C:\Users\w322800\Documents\gh\new1\.venv\Scripts\python.exe src/main.py
   Working directory: C:\Users\w322800\Documents\gh\new1\Reports\Retail\NewLoanReport_Francine
   Environment: REPORT_ENV=dev
   PYTHONPATH: C:\Users\w322800\Documents\gh\new1\Reports\Retail\NewLoanReport_Francine;C:\Users\w322800\Documents\...
   OS: nt, Path separator: ';'
⏱️  Execution time: 0.64 seconds
📤 Return code: 1
⚠️  Error output:
   Traceback (most recent call last):
  File "C:\Users\w322800\Documents\gh\new1\Reports\Retail\NewLoanReport_Francine\src\main.py", line 41, in <module>
    import cdutils.database.fdic_recon # type: ignore
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\new1\cdutils\cdutils\database\fdic_recon.py", line 10, in <module>
    import src.cdutils.database.connect
ModuleNotFoundError: No module named 'src.cdutils'


❌ EXECUTION FAILED
📋 Report: NewLoanReport_Francine
⏱️  Time: 0.64 seconds
📤 Exit code: 1
🚨 ERROR DETAILS:
--------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\w322800\Documents\gh\new1\Reports\Retail\NewLoanReport_Francine\src\main.py", line 41, in <module>
    import cdutils.database.fdic_recon # type: ignore
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\new1\cdutils\cdutils\database\fdic_recon.py", line 10, in <module>
    import src.cdutils.database.connect
ModuleNotFoundError: No module named 'src.cdutils'

--------------------------------------------------
💡 Fix suggestions:
   - Missing Python package - install required dependencies

FAILED
testing/test_reports.py::test_report[Prime_Time_Travel_customers]
🧪 Testing report: Prime_Time_Travel_customers
📁 Path: Reports\Retail\Prime_Time_Travel_customers
📋 Loaded test config for Prime_Time_Travel_customers: 4 settings
🔍 Checking required files...
   main.py: ✅
   config.py: ✅
🧹 Preparing output directory: Reports\Retail\Prime_Time_Travel_customers\output
   Creating output directory
🚀 Executing report...
   Command: C:\Users\w322800\Documents\gh\new1\.venv\Scripts\python.exe src/main.py
   Working directory: C:\Users\w322800\Documents\gh\new1\Reports\Retail\Prime_Time_Travel_customers
   Environment: REPORT_ENV=dev
   PYTHONPATH: C:\Users\w322800\Documents\gh\new1\Reports\Retail\Prime_Time_Travel_customers;C:\Users\w322800\Docum...
   OS: nt, Path separator: ';'
⏱️  Execution time: 115.09 seconds
📤 Return code: 0
📝 Output preview (first 500 chars):
   Starting Prime Time Travel Customers Report
Report generated: C:\Users\w322800\Documents\gh\new1\Reports\Retail\Prime_Time_Travel_customers\output\Prime Time Travel Customers July 24 2025.xlsx
No email distribution configured
Complete!

📊 Output verification:
   Generated files: 1
      📄 Prime Time Travel Customers July 24 2025.xlsx (213089 bytes)
   Expected patterns: ['Prime Time Travel Customers *.xlsx']
      Pattern 'Prime Time Travel Customers *.xlsx': 1 matches
✅ Test passed for Prime_Time_Travel_customers
----------------------------------------
PASSED
testing/test_reports.py::test_report[small_business_partnership_ma]
🧪 Testing report: small_business_partnership_ma
📁 Path: Reports\Retail\small_business_partnership_ma
📋 Loaded test config for small_business_partnership_ma: 4 settings
🔍 Checking required files...
   main.py: ✅
   config.py: ✅
🧹 Preparing output directory: Reports\Retail\small_business_partnership_ma\output
   Creating output directory
🚀 Executing report...
   Command: C:\Users\w322800\Documents\gh\new1\.venv\Scripts\python.exe src/main.py
   Working directory: C:\Users\w322800\Documents\gh\new1\Reports\Retail\small_business_partnership_ma
   Environment: REPORT_ENV=dev
   PYTHONPATH: C:\Users\w322800\Documents\gh\new1\Reports\Retail\small_business_partnership_ma;C:\Users\w322800\Doc...
   OS: nt, Path separator: ';'
⏱️  Execution time: 25.48 seconds
📤 Return code: 1
📝 Output preview (first 500 chars):
   Starting Small Business Partnership MA Report

⚠️  Error output:
   Traceback (most recent call last):
  File "C:\Users\w322800\Documents\gh\new1\Reports\Retail\small_business_partnership_ma\src\main.py", line 112, in <module>
    main()
  File "C:\Users\w322800\Documents\gh\new1\Reports\Retail\small_business_partnership_ma\src\main.py", line 66, in main
    raw_data = cdutils.pkey_sqlite.add_pkey(raw_data)
               ^^^^^^^
UnboundLocalError: cannot access local variable 'cdutils' where it is not associated with a value


❌ EXECUTION FAILED
📋 Report: small_business_partnership_ma
⏱️  Time: 25.48 seconds
📤 Exit code: 1
🚨 ERROR DETAILS:
--------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\w322800\Documents\gh\new1\Reports\Retail\small_business_partnership_ma\src\main.py", line 112, in <module>
    main()
  File "C:\Users\w322800\Documents\gh\new1\Reports\Retail\small_business_partnership_ma\src\main.py", line 66, in main
    raw_data = cdutils.pkey_sqlite.add_pkey(raw_data)
               ^^^^^^^
UnboundLocalError: cannot access local variable 'cdutils' where it is not associated with a value

--------------------------------------------------
📝 OUTPUT:
--------------------------------------------------
Starting Small Business Partnership MA Report

--------------------------------------------------
💡 Fix suggestions:

FAILED
testing/test_reports.py::test_all_reports_have_configs
🔧 Verifying all reports have proper configurations...
   ✅ Has config: Reports\Commercial_Lending\Business_Concentration_of_Deposits
   ✅ Has config: Reports\Commercial_Lending\CLO_ActivePortfolio_Officer_Report
   ✅ Has config: Reports\Commercial_Lending\Deposit Dash
   ✅ Has config: Reports\Commercial_Lending\Deposit Deep Dive
   ✅ Has config: Reports\Commercial_Lending\DepositPocketPricing
   ✅ Has config: Reports\Commercial_Lending\Status Page
   ✅ Has config: Reports\Commercial_Lending\YTD_Business_Deposits
   ✅ Has config: Reports\Government Banking\Payroll_and_Vendor
   ✅ Has config: Reports\Indirect_Lending\Dealer Track - Route One Reconciliaton
   ✅ Has config: Reports\Indirect_Lending\EContracts
   ✅ Has config: Reports\Indirect_Lending\Monthly Goal Report
   ✅ Has config: Reports\Operations\Rate Scraping
   ✅ Has config: Reports\Operations\Trial Balance Ops
   ✅ Has config: Reports\Resolution Committee Automation\Classifieds
   ✅ Has config: Reports\Resolution Committee Automation\Delinquency
   ✅ Has config: Reports\Resolution Committee Automation\Financial Difficulty Modifications
   ✅ Has config: Reports\Resolution Committee Automation\Non Accruals
   ✅ Has config: Reports\Retail\NewLoanReport_Francine
   ✅ Has config: Reports\Retail\New_Business_Checking
   ✅ Has config: Reports\Retail\New_Consumer_Checking
   ✅ Has config: Reports\Retail\Prime_Time_Travel_customers
   ✅ Has config: Reports\Retail\small_business_partnership_ma

📊 Configuration Summary:
   Total reports found: 22
   Reports with configs: 22
   Reports missing configs: 0
✅ All reports have proper configurations!
PASSED
testing/test_reports.py::test_sync_configuration
🔄 Verifying sync configurations...

🔍 Scanning for reports with test configurations...
📁 Found 21 test configuration files:
   ✅ Reports\Commercial_Lending\Business_Concentration_of_Deposits
   ✅ Reports\Commercial_Lending\CLO_ActivePortfolio_Officer_Report
   ✅ Reports\Commercial_Lending\Deposit Dash
   ✅ Reports\Commercial_Lending\Deposit Deep Dive
   ✅ Reports\Commercial_Lending\DepositPocketPricing
   ✅ Reports\Commercial_Lending\Status Page
   ✅ Reports\Commercial_Lending\YTD_Business_Deposits
   ✅ Reports\Government Banking\Payroll_and_Vendor
   ✅ Reports\Indirect_Lending\Dealer Reserve Recon
   ✅ Reports\Indirect_Lending\EContracts
   ✅ Reports\Operations\Rate Scraping
   ✅ Reports\Operations\Trial Balance Ops
   ✅ Reports\Resolution Committee Automation\Classifieds
   ✅ Reports\Resolution Committee Automation\Delinquency
   ✅ Reports\Resolution Committee Automation\Financial Difficulty Modifications
   ✅ Reports\Resolution Committee Automation\Non Accruals
   ✅ Reports\Retail\NewLoanReport_Francine
   ✅ Reports\Retail\New_Business_Checking
   ✅ Reports\Retail\New_Consumer_Checking
   ✅ Reports\Retail\Prime_Time_Travel_customers
   ✅ Reports\Retail\small_business_partnership_ma

🔍 Scanning for reports without test configurations...
⚠️  Found 2 reports without test configs:
   📝 Reports\Indirect_Lending\Dealer Track - Route One Reconciliaton
   📝 Reports\Indirect_Lending\Monthly Goal Report

📊 Total reports to test: 21
============================================================
📋 Loaded test config for Business_Concentration_of_Deposits: 5 settings
   🔄 Business_Concentration_of_Deposits expects 1 input files
      ✅ Config loadable
📋 Loaded test config for CLO_ActivePortfolio_Officer_Report: 4 settings
   📝 CLO_ActivePortfolio_Officer_Report has no sync requirements
📋 Loaded test config for Deposit Dash: 5 settings
   🔄 Deposit Dash expects 2 input files
      ✅ Config loadable
📋 Loaded test config for Deposit Deep Dive: 4 settings
   📝 Deposit Deep Dive has no sync requirements
📋 Loaded test config for DepositPocketPricing: 5 settings
   📝 DepositPocketPricing has no sync requirements
📋 Loaded test config for Status Page: 4 settings
   📝 Status Page has no sync requirements
📋 Loaded test config for YTD_Business_Deposits: 4 settings
   📝 YTD_Business_Deposits has no sync requirements
📋 Loaded test config for Payroll_and_Vendor: 5 settings
   📝 Payroll_and_Vendor has no sync requirements
📋 Loaded test config for Dealer Reserve Recon: 4 settings
   📝 Dealer Reserve Recon has no sync requirements
📋 Loaded test config for EContracts: 4 settings
   📝 EContracts has no sync requirements
📋 Loaded test config for Rate Scraping: 5 settings
   📝 Rate Scraping has no sync requirements
📋 Loaded test config for Trial Balance Ops: 4 settings
   📝 Trial Balance Ops has no sync requirements
📋 Loaded test config for Classifieds: 4 settings
   📝 Classifieds has no sync requirements
📋 Loaded test config for Delinquency: 4 settings
   📝 Delinquency has no sync requirements
📋 Loaded test config for Financial Difficulty Modifications: 4 settings
   📝 Financial Difficulty Modifications has no sync requirements
📋 Loaded test config for Non Accruals: 4 settings
   📝 Non Accruals has no sync requirements
📋 Loaded test config for New_Business_Checking: 4 settings
   📝 New_Business_Checking has no sync requirements
📋 Loaded test config for New_Consumer_Checking: 4 settings
   📝 New_Consumer_Checking has no sync requirements
📋 Loaded test config for NewLoanReport_Francine: 4 settings
   📝 NewLoanReport_Francine has no sync requirements
📋 Loaded test config for Prime_Time_Travel_customers: 4 settings
   📝 Prime_Time_Travel_customers has no sync requirements
📋 Loaded test config for small_business_partnership_ma: 4 settings
   📝 small_business_partnership_ma has no sync requirements

📊 Sync Configuration Summary:
   Reports with sync needs: 2
   Sync configs tested: 2
✅ All sync configurations verified!
PASSED

========================================================================= FAILURES ========================================================================= 
_____________________________________________________ test_report[Business_Concentration_of_Deposits] ______________________________________________________ 
testing\test_reports.py:205: in test_report
    assert result.returncode == 0, f"Report execution failed - see details above"
E   AssertionError: Report execution failed - see details above
E   assert 1 == 0
E    +  where 1 = CompletedProcess(args=['C:\\Users\\w322800\\Documents\\gh\\new1\\.venv\\Scripts\\python.exe', 'src/main.py'], returncode=1, stdout='Starting Business Concentration of Deposits Report\n', stderr='Traceback (most recent call last):\n  File "C:\\Users\\w322800\\Documents\\gh\\new1\\Reports\\Commercial_Lending\\Business_Concentration_of_Deposits\\src\\main.py", line 297, in <module>\n    main()\n  File "C:\\Users\\w322800\\Documents\\gh\\new1\\Reports\\Commercial_Lending\\Business_Concentration_of_Deposits\\src\\main.py", line 48, in main\n    data = pd.read_excel(src.config.INPUT_DIR / staging_file)\n     
      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\w322800\\Documents\\gh\\new1\\.venv\\Lib\\site-packages\\pandas\\io\\excel\\_base.py", line 495, in read_excel\n    io = ExcelFile(\n         ^^^^^^^^^^\n  File "C:\\Users\\w322800\\Documents\\gh\\new1\\.venv\\Lib\\site-packages\\pandas\\io\\excel\\_base.py", line 1550, in __init__\n    ext = inspect_excel_format(\n          ^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\w322800\\Documents\\gh\\new1\\.venv\\Lib\\site-packages\\pandas\\io\\excel\\_base.py", line 1402, in inspect_excel_format\n    with get_handle(\n         ^^^^^^^^^^^\n  File "C:\\Users\\w322800\\Documents\\gh\\new1\\.venv\\Lib\\site-packages\\pandas\\io\\common.py", line 882, in get_handle\n    handle = open(handle, ioargs.mode)\n       
      ^^^^^^^^^^^^^^^^^^^^^^^^^\nFileNotFoundError: [Errno 2] No such file or directory: \'C:\\\\Users\\\\w322800\\\\Documents\\\\gh\\\\new1\\\\Reports\\\\Commercial_Lending\\\\Business_Concentration_of_Deposits\\\\input\\\\DailyDeposit_staging.xlsx\'\n').returncode
_____________________________________________________ test_report[CLO_ActivePortfolio_Officer_Report] ______________________________________________________ 
testing\test_reports.py:205: in test_report
    assert result.returncode == 0, f"Report execution failed - see details above"
E   AssertionError: Report execution failed - see details above
E   assert 1 == 0
E    +  where 1 = CompletedProcess(args=['C:\\Users\\w322800\\Documents\\gh\\new1\\.venv\\Scripts\\python.exe', 'src/main.py'], returncode=1, stdout='Starting CLO Active Portfolio Officer Report\n', stderr='Traceback (most recent call last):\n  File "C:\\Users\\w322800\\Documents\\gh\\new1\\Reports\\Commercial_Lending\\CLO_ActivePortfolio_Officer_Report\\src\\main.py", line 234, in <module>\n    main()\n  File "C:\\Users\\w322800\\Documents\\gh\\new1\\Reports\\Commercial_Lending\\CLO_ActivePortfolio_Officer_Report\\src\\main.py", line 69, in main\n    raw_data = cdutils.pkey_sqlite.add_pkey(raw_data)\n               ^^^^^^^\nUnboundLocalError: cannot access local variable \'cdutils\' where it is not associated with a value\n').returncode
________________________________________________________________ test_report[Deposit Dash] _________________________________________________________________ 
testing\test_reports.py:205: in test_report
    assert result.returncode == 0, f"Report execution failed - see details above"
E   AssertionError: Report execution failed - see details above
E   assert 1 == 0
E    +  where 1 = CompletedProcess(args=['C:\\Users\\w322800\\Documents\\gh\\new1\\.venv\\Scripts\\python.exe', 'src/main.py'], returncode=1, stdout='Running Deposit Dash Report\n', stderr='Traceback (most recent call last):\n  File "C:\\Users\\w322800\\Documents\\gh\\new1\\Reports\\Commercial_Lending\\Deposit Dash\\src\\main.py", line 87, in <module>\n    main()\n  File "C:\\Users\\w322800\\Documents\\gh\\new1\\Reports\\Commercial_Lending\\Deposit Dash\\src\\main.py", line 52, in main\n    raise FileNotFoundError(f"No DailyDeposit file found in {src.config.INPUT_DIR}")\nFileNotFoundError: No DailyDeposit file found in C:\\Users\\w322800\\Documents\\gh\\new1\\Reports\\Commercial_Lending\\Deposit Dash\\input\n').returncode
____________________________________________________________ test_report[DepositPocketPricing] _____________________________________________________________ 
testing\test_reports.py:205: in test_report
    assert result.returncode == 0, f"Report execution failed - see details above"
E   AssertionError: Report execution failed - see details above
E   assert 1 == 0
E    +  where 1 = CompletedProcess(args=['C:\\Users\\w322800\\Documents\\gh\\new1\\.venv\\Scripts\\python.exe', 'src/main.py'], returncode=1, stdout='Starting Deposit Pocket Pricing Report\n', stderr='Traceback (most recent call last):\n  File "C:\\Users\\w322800\\Documents\\gh\\new1\\Reports\\Commercial_Lending\\DepositPocketPricing\\src\\main.py", line 101, in <module>\n    main()\n  File "C:\\Users\\w322800\\Documents\\gh\\new1\\Reports\\Commercial_Lending\\DepositPocketPricing\\src\\main.py", line 53, in main\n    df = pd.read_excel(INPUT_PATH)\n         ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\w322800\\Documents\\gh\\new1\\.venv\\Lib\\site-packages\\pandas\\io\\excel\\_base.py", line 495, in read_excel\n    io = ExcelFile(\n         ^^^^^^^^^^\n  File "C:\\Users\\w322800\\Documents\\gh\\new1\\.venv\\Lib\\site-packages\\pandas\\io\\excel\\_base.py", line 1550, in __init__\n    ext = inspect_excel_format(\n          ^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\w322800\\Documents\\gh\\new1\\.venv\\Lib\\site-packages\\pandas\\io\\excel\\_base.py", line 1402, in inspect_excel_format\n    with get_handle(\n         ^^^^^^^^^^^\n  File "C:\\Users\\w322800\\Documents\\gh\\new1\\.venv\\Lib\\site-packages\\pandas\\io\\common.py", line 882, in get_handle\n    handle = open(handle, ioargs.mode)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\nFileNotFoundError: [Errno 2] No such file or directory: \'C:\\\\Users\\\\w322800\\\\Documents\\\\gh\\\\new1\\\\Reports\\\\Commercial_Lending\\\\DepositPocketPricing\\\\assets\\\\DepositPocketPricing.xlsx\'\n').returncode
_________________________________________________________________ test_report[Status Page] _________________________________________________________________ 
testing\test_reports.py:205: in test_report
    assert result.returncode == 0, f"Report execution failed - see details above"
E   AssertionError: Report execution failed - see details above
E   assert 1 == 0
E    +  where 1 = CompletedProcess(args=['C:\\Users\\w322800\\Documents\\gh\\new1\\.venv\\Scripts\\python.exe', 'src/main.py'], returncode=1, stdout='Starting Status Page Report\n', stderr='Traceback (most recent call last):\n  File "C:\\Users\\w322800\\Documents\\gh\\new1\\Reports\\Commercial_Lending\\Status Page\\src\\main.py", line 206, in <module>\n    main()\n  File "C:\\Users\\w322800\\Documents\\gh\\new1\\Reports\\Commercial_Lending\\Status Page\\src\\main.py", line 123, in main\n    filtered_data = src.core_transform.filtering_on_pkey(raw_data, key)\n                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\w322800\\Documents\\gh\\new1\\Reports\\Commercial_Lending\\Status Page\\src\\core_transform.py", line 67, in filtering_on_pkey\n    assert (df[\'portfolio_key\'] == key).any(), "Portfolio key does not map to any active products"\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nAssertionError: Portfolio key does not map to any active products\n').returncode
____________________________________________________________ test_report[YTD_Business_Deposits] ____________________________________________________________ 
testing\test_reports.py:224: in test_report
    assert matches, f"No files matching pattern: {expected}"
E   AssertionError: No files matching pattern: ytd_business_deposits_*.xlsx
E   assert []
____________________________________________________________ test_report[Dealer Reserve Recon] _____________________________________________________________ 
testing\test_reports.py:108: in test_report
    assert main_file.exists(), f"main.py not found for {report_path.name}"
E   AssertionError: main.py not found for Dealer Reserve Recon
E   assert False
E    +  where False = exists()
E    +    where exists = WindowsPath('Reports/Indirect_Lending/Dealer Reserve Recon/src/main.py').exists
_________________________________________________________________ test_report[EContracts] __________________________________________________________________ 
testing\test_reports.py:205: in test_report
    assert result.returncode == 0, f"Report execution failed - see details above"
E   AssertionError: Report execution failed - see details above
E   assert 1 == 0
E    +  where 1 = CompletedProcess(args=['C:\\Users\\w322800\\Documents\\gh\\new1\\.venv\\Scripts\\python.exe', 'src/main.py'], returncode=1, stdout='Starting EContracts Report\n', stderr='Traceback (most recent call last):\n  File "C:\\Users\\w322800\\Documents\\gh\\new1\\Reports\\Indirect_Lending\\EContracts\\src\\main.py", line 107, in <module>\n    main()\n  File "C:\\Users\\w322800\\Documents\\gh\\new1\\Reports\\Indirect_Lending\\EContracts\\src\\main.py", line 
56, in main\n    combined_funding_reports, book_to_look = grabData.grabData()\n                                             ^^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\w322800\\Documents\\gh\\new1\\Reports\\Indirect_Lending\\EContracts\\src\\grabData.py", line 42, in grabData\n    for filename in os.listdir(folder_path):\n                    ^^^^^^^^^^^^^^^^^^^^^^^\nFileNotFoundError: [WinError 3] The system cannot find the path specified: \'C:\\\\Users\\\\w322800\\\\Documents\\\\gh\\\\new1\\\\Reports\\\\Indirect_Lending\\\\EContracts\\\\input\'\n').returncode
________________________________________________________________ test_report[Rate Scraping] ________________________________________________________________ 
testing\test_reports.py:205: in test_report
    assert result.returncode == 0, f"Report execution failed - see details above"
E   AssertionError: Report execution failed - see details above
E   assert 1 == 0
E    +  where 1 = CompletedProcess(args=['C:\\Users\\w322800\\Documents\\gh\\new1\\.venv\\Scripts\\python.exe', 'src/main.py'], returncode=1, stdout='Running Rate Scraper\n', stderr='Traceback (most recent call last):\n  File "C:\\Users\\w322800\\Documents\\gh\\new1\\Reports\\Operations\\Rate Scraping\\src\\main.py", line 391, in <module>\n    cme_data = get_cme_term_sofr_data()\n               ^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\w322800\\Documents\\gh\\new1\\Reports\\Operations\\Rate Scraping\\src\\main.py", line 116, in get_cme_term_sofr_data\n    browser = p.chromium.launch(headless=False)\n              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\w322800\\Documents\\gh\\new1\\.venv\\Lib\\site-packages\\playwright\\sync_api\\_generated.py", line 14494, 
in launch\n    self._sync(\n  File "C:\\Users\\w322800\\Documents\\gh\\new1\\.venv\\Lib\\site-packages\\playwright\\_impl\\_sync_base.py", line 115, in _sync\n    return task.result()\n           ^^^^^^^^^^^^^\n  File "C:\\Users\\w322800\\Documents\\gh\\new1\\.venv\\Lib\\site-packages\\playwright\\_impl\\_browser_type.py", line 98, in launch\n    await self._channel.send(\n  File "C:\\Users\\w322800\\Documents\\gh\\new1\\.venv\...50\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2557\n\\u2551 Looks like Playwright was just installed or updated.       \\u2551\n\\u2551 Please run the following command to download new browsers: \\u2551\n\\u2551
                \\u2551\n\\u2551     playwright install                                     \\u2551\n\\u2551
           \\u2551\n\\u2551 <3 Playwright Team                                         \\u2551\n\\u255a\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u255d\n').returncode
______________________________________________________________ test_report[Trial Balance Ops] ______________________________________________________________ 
testing\test_reports.py:224: in test_report
    assert matches, f"No files matching pattern: {expected}"
E   AssertionError: No files matching pattern: daily_trial_balance_report_*.xlsx
E   assert []
_________________________________________________________________ test_report[Classifieds] _________________________________________________________________ 
testing\test_reports.py:224: in test_report
    assert matches, f"No files matching pattern: {expected}"
E   AssertionError: No files matching pattern: *_classifieds_report.xlsx
E   assert []
_________________________________________________________________ test_report[Delinquency] _________________________________________________________________ 
testing\test_reports.py:224: in test_report
    assert matches, f"No files matching pattern: {expected}"
E   AssertionError: No files matching pattern: *_delinquency_report.xlsx
E   assert []
________________________________________________________________ test_report[Non Accruals] _________________________________________________________________ 
testing\test_reports.py:224: in test_report
    assert matches, f"No files matching pattern: {expected}"
E   AssertionError: No files matching pattern: *_non_accruals_report.xlsx
E   assert []
____________________________________________________________ test_report[New_Business_Checking] ____________________________________________________________ 
testing\test_reports.py:205: in test_report
    assert result.returncode == 0, f"Report execution failed - see details above"
E   AssertionError: Report execution failed - see details above
E   assert 1 == 0
E    +  where 1 = CompletedProcess(args=['C:\\Users\\w322800\\Documents\\gh\\new1\\.venv\\Scripts\\python.exe', 'src/main.py'], returncode=1, stdout='Starting New Business Checking Report\n', stderr='Traceback (most recent call last):\n  File "C:\\Users\\w322800\\Documents\\gh\\new1\\Reports\\Retail\\New_Business_Checking\\src\\main.py", line 78, in <module>\n    main()\n  File "C:\\Users\\w322800\\Documents\\gh\\new1\\Reports\\Retail\\New_Business_Checking\\src\\main.py", line 41, in main\n    data = cdutils.database.fetch_data()\n           ^^^^^^^\nUnboundLocalError: cannot access local variable \'cdutils\' where it is not associated with a value\n').returncode
____________________________________________________________ test_report[New_Consumer_Checking] ____________________________________________________________ 
testing\test_reports.py:205: in test_report
    assert result.returncode == 0, f"Report execution failed - see details above"
E   AssertionError: Report execution failed - see details above
E   assert 1 == 0
E    +  where 1 = CompletedProcess(args=['C:\\Users\\w322800\\Documents\\gh\\new1\\.venv\\Scripts\\python.exe', 'src/main.py'], returncode=1, stdout='Starting New Consumer Checking Report\n', stderr='Traceback (most recent call last):\n  File "C:\\Users\\w322800\\Documents\\gh\\new1\\Reports\\Retail\\New_Consumer_Checking\\src\\main.py", line 80, in <module>\n    main()\n  File "C:\\Users\\w322800\\Documents\\gh\\new1\\Reports\\Retail\\New_Consumer_Checking\\src\\main.py", line 42, in main\n    data = cdutils.database.fetch_data()\n           ^^^^^^^\nUnboundLocalError: cannot access local variable \'cdutils\' where it is not associated with a value\n').returncode
___________________________________________________________ test_report[NewLoanReport_Francine] ____________________________________________________________ 
testing\test_reports.py:205: in test_report
    assert result.returncode == 0, f"Report execution failed - see details above"
E   AssertionError: Report execution failed - see details above
E   assert 1 == 0
E    +  where 1 = CompletedProcess(args=['C:\\Users\\w322800\\Documents\\gh\\new1\\.venv\\Scripts\\python.exe', 'src/main.py'], returncode=1, stdout='', stderr='Traceback (most recent call last):\n  File "C:\\Users\\w322800\\Documents\\gh\\new1\\Reports\\Retail\\NewLoanReport_Francine\\src\\main.py", line 41, in 
<module>\n    import cdutils.database.fdic_recon # type: ignore\n    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\w322800\\Documents\\gh\\new1\\cdutils\\cdutils\\database\\fdic_recon.py", line 10, in <module>\n    import src.cdutils.database.connect\nModuleNotFoundError: No module named \'src.cdutils\'\n').returncode
________________________________________________________ test_report[small_business_partnership_ma] ________________________________________________________ 
testing\test_reports.py:205: in test_report
    assert result.returncode == 0, f"Report execution failed - see details above"
E   AssertionError: Report execution failed - see details above
E   assert 1 == 0
E    +  where 1 = CompletedProcess(args=['C:\\Users\\w322800\\Documents\\gh\\new1\\.venv\\Scripts\\python.exe', 'src/main.py'], returncode=1, stdout='Starting Small Business Partnership MA Report\n', stderr='Traceback (most recent call last):\n  File "C:\\Users\\w322800\\Documents\\gh\\new1\\Reports\\Retail\\small_business_partnership_ma\\src\\main.py", line 112, in <module>\n    main()\n  File "C:\\Users\\w322800\\Documents\\gh\\new1\\Reports\\Retail\\small_business_partnership_ma\\src\\main.py", line 66, in main\n    raw_data = cdutils.pkey_sqlite.add_pkey(raw_data)\n               ^^^^^^^\nUnboundLocalError: cannot access local variable \'cdutils\' where it is not associated with a value\n').returncode
================================================================= short test summary info ================================================================== 
FAILED testing/test_reports.py::test_report[Business_Concentration_of_Deposits] - AssertionError: Report execution failed - see details above
FAILED testing/test_reports.py::test_report[CLO_ActivePortfolio_Officer_Report] - AssertionError: Report execution failed - see details above
FAILED testing/test_reports.py::test_report[Deposit Dash] - AssertionError: Report execution failed - see details above
FAILED testing/test_reports.py::test_report[DepositPocketPricing] - AssertionError: Report execution failed - see details above
FAILED testing/test_reports.py::test_report[Status Page] - AssertionError: Report execution failed - see details above
FAILED testing/test_reports.py::test_report[YTD_Business_Deposits] - AssertionError: No files matching pattern: ytd_business_deposits_*.xlsx
FAILED testing/test_reports.py::test_report[Dealer Reserve Recon] - AssertionError: main.py not found for Dealer Reserve Recon
FAILED testing/test_reports.py::test_report[EContracts] - AssertionError: Report execution failed - see details above
FAILED testing/test_reports.py::test_report[Rate Scraping] - AssertionError: Report execution failed - see details above
FAILED testing/test_reports.py::test_report[Trial Balance Ops] - AssertionError: No files matching pattern: daily_trial_balance_report_*.xlsx
FAILED testing/test_reports.py::test_report[Classifieds] - AssertionError: No files matching pattern: *_classifieds_report.xlsx
FAILED testing/test_reports.py::test_report[Delinquency] - AssertionError: No files matching pattern: *_delinquency_report.xlsx
FAILED testing/test_reports.py::test_report[Non Accruals] - AssertionError: No files matching pattern: *_non_accruals_report.xlsx
FAILED testing/test_reports.py::test_report[New_Business_Checking] - AssertionError: Report execution failed - see details above
FAILED testing/test_reports.py::test_report[New_Consumer_Checking] - AssertionError: Report execution failed - see details above
FAILED testing/test_reports.py::test_report[NewLoanReport_Francine] - AssertionError: Report execution failed - see details above
FAILED testing/test_reports.py::test_report[small_business_partnership_ma] - AssertionError: Report execution failed - see details above
=================================================== 17 failed, 5 passed, 1 skipped in 949.94s (0:15:49) ===================================