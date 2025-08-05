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

