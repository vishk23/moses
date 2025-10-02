"""
Main entry point for your project.

Replace this docstring with a description of your project's purpose and logic.
"""
from calendar import month_name
from datetime import datetime
import src.config
import src._version
import src.loan_trial.core

def main():
    print(f"Running {src._version.__version__}")
    print(f"Running {src.config.REPORT_NAME} for {src.config.BUSINESS_LINE}")
    print(f"Schedule: {src.config.SCHEDULE}")
    print(f"Owner: {src.config.OWNER}")
    print(f"Environment: {src.config.ENV}")
    print(f"Output directory: {src.config.OUTPUT_DIR}")

    df = src.loan_trial.core.main_pipeline()

    OUTPUT_PATH = src.config.OUTPUT_DIR / "loan_trial.parquet"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUTPUT_PATH, index=False)

    # grabbing date for filename
    today = datetime.today()
    current_first_day = today.replace(day=1)
    prev_year = current_first_day.year - 1 if current_first_day == 1 else current_first_day.year
    prev_month = 12 if current_first_day.month == 1 else current_first_day.month - 1
    prev_month_name = month_name[prev_month] + " " + str(prev_year)
    filename_string = 'Loan Trial_' + prev_month_name + '.xlsx'

    OUTPUT_PATH = src.config.OUTPUT_DIR / filename_string
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(OUTPUT_PATH, index=False)    
    print("Complete!")

if __name__ == "__main__":
    main()