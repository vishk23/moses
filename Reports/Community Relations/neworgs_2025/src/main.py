"""
Main entry point for your project.

Replace this docstring with a description of your project's purpose and logic.
"""

import src.config
import src._version
import src.neworgs_2025.core

def main():
    print(f"Running {src._version.__version__}")
    print(f"Running {src.config.REPORT_NAME} for {src.config.BUSINESS_LINE}")
    print(f"Schedule: {src.config.SCHEDULE}")
    print(f"Owner: {src.config.OWNER}")
    print(f"Environment: {src.config.ENV}")
    print(f"Output directory: {src.config.OUTPUT_DIR}")
    # Add your main project logic here

    df = src.neworgs_2025.core.main_pipeline()

    OUTPUT_PATH = src.config.OUTPUT_DIR / "new_orgs_2025.xlsx"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(OUTPUT_PATH, index=False)
    print("Complete!")

if __name__ == "__main__":
    main()