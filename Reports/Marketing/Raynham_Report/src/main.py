"""
Main entry point for your project.

Replace this docstring with a description of your project's purpose and logic.
"""

import src.config
import src._version
import src.raynham_report.core

def main():
    print(f"Running {src._version.__version__}")
    print(f"Running {src.config.REPORT_NAME} for {src.config.BUSINESS_LINE}")
    print(f"Schedule: {src.config.SCHEDULE}")
    print(f"Owner: {src.config.OWNER}")
    print(f"Environment: {src.config.ENV}")
    print(f"Output directory: {src.config.OUTPUT_DIR}")

    df = src.raynham_report.core.generate_raynham_report()

    OUTPUT_PATH = src.config.OUTPUT_DIR / "raynham_report.parquet"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUTPUT_PATH, index=False)

    OUTPUT_PATH = src.config.OUTPUT_DIR / "raynham_report.xlsx"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(OUTPUT_PATH, index=False)


if __name__ == "__main__":
    main()