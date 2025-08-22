Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Risk Management\Daily Mismatched Debit Card Txns\src\main.py", line 298, in <module>
    main()
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Risk Management\Daily Mismatched Debit Card Txns\src\main.py", line 269, in main
    separator_line = "".join(["-" * (col_widths[col] - padding)].ljust(col_widths[col]) for col in df.columns)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Risk Management\Daily Mismatched Debit Card Txns\src\main.py", line 269, in <genexpr>
    separator_line = "".join(["-" * (col_widths[col] - padding)].ljust(col_widths[col]) for col in df.columns)
                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'list' object has no attribute 'ljust'
2025-08-22 11:41:49 | ERROR | STDOUT: