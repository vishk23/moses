"""
Execution Code Snippet
v2.0.0
"""

from datetime import datetime
import importlib.util
import sys
from pathlib import Path

def import_function(file_path, orig_function_name, new_function_name):
    module_name = Path(file_path).stem
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    target_module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = target_module
    spec.loader.exec_module(target_module)
    func = getattr(target_module, orig_function_name)
    func.__name__ = new_function_name
    return func

def execution_loop(functions):
    """
    This is the control center for month end reports. This will attempt to run all functions, logging all clean runs/errors and timestamping.

    Args:
        functions (list): Pass in a list of functions. 

    Returns:
        None

    Operations:
        - Create empty lists to store errors & clean runs
        - Loop through all functions
        - Append to a log.txt file all details about the run (time, which reports, success or failure)
    """
    errors = [] # List to store any reports that failed to complete successfully
    clean_runs = [] # List to store successful report runs

    for func in functions:
        try:
            print(f"\nRunning: {func.__name__}")
            func()
            success_message = f"{func.__name__} ran successfully"
            clean_runs.append((func.__name__, success_message))
        except Exception as e:
            error_message = f"Error in {func.__name__}: {e}"
            print(error_message)
            errors.append((func.__name__, error_message))

    # Logging
    log = []
    current_time = datetime.now()

    print(f"\n== Execution Summary - {current_time}")
    log.append("")
    log.append(f"\n== Execution Summary - {current_time}\n")

    if errors:
        print(f"\nThe following functions had errors:")
        log.append(f"\nThe following functions had errors:\n")
        for name, error in errors:
            print(f"- {name}: {error}")
            log.append(f"- {name}: {error}\n")
        if clean_runs:
            print(f"The following ran successfully:")
            log.append(f"\nThe following ran successfully:\n")
            for name, success in clean_runs:
                print(f"- {name}: {success}")
                log.append(f"- {name}: {success}\n")

    else:
        print(f"\nAll reports ran without error.")
        log.append(f"\nAll reports ran without error.\n")
        log.append(f"\nThe following ran successfully:\n")
        for name, success in clean_runs:
            print(f"- {name}: {success}")
            log.append(f"- {name}: {success}\n")

    log_location = r'C:\Users\w322800\Documents\coding3\temp\log.txt'
    with open(log_location, 'a') as logging_file:
        logging_file.write('\n')
        for item in log:
            logging_file.write(item)
    
    

if __name__ == "__main__":
    # Import delinquency report
    FUNCTIONS_MAP = {
        # Weekly Loan Report
        r"\\10.161.85.66\Home\Share\Data & Analytics Initiatives\Project Management\Chad Projects\Weekly Reports\NewLoanReport_LR_Credit\Production\Workflow\weekly_loan_report_45_lookback.py":
        {"original":"main", "new_name":"weekly_loan_report"},
    }    
    functions_to_run = []

for file_path, function_details in FUNCTIONS_MAP.items():
    file_path = Path(file_path)
    if file_path.exists():
        original_name = function_details['original']
        new_name = function_details['new_name']
        func = import_function(file_path, original_name, new_name)
        functions_to_run.append(func)
    else:
        print(f"File {file_path} not found")

    execution_loop(functions_to_run)