"""
Main entry point for your project.

Replace this docstring with a description of your project's purpose and logic.
"""

import src.config
import src._version
import src.sba_loans.core
import src.sba_loans.output_to_excel

def main():
    print(f"Running {src._version.__version__}")
    print(f"Running {src.config.REPORT_NAME} for {src.config.BUSINESS_LINE}")
    print(f"Schedule: {src.config.SCHEDULE}")
    print(f"Owner: {src.config.OWNER}")
    print(f"Environment: {src.config.ENV}")
    print(f"Output directory: {src.config.OUTPUT_DIR}")

    df = src.sba_loans.core.main_report_creation()

    OUTPUT_PATH = src.config.OUTPUT_DIR / "SBA_Loans.xlsx"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    df.to_excel(OUTPUT_PATH, index=False)
    src.sba_loans.output_to_excel.export_df_to_excel(df, OUTPUT_PATH)
    print("Complete!")

if __name__ == "__main__":
    main()