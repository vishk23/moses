"""
Main entry point for your project.

Replace this docstring with a description of your project's purpose and logic.
"""

import src.config
import src._version

def main():
    print(f"Running {src._version.__version__}")
    print(f"Running {src.config.REPORT_NAME} for {src.config.BUSINESS_LINE}")
    print(f"Schedule: {src.config.SCHEDULE}")
    print(f"Owner: {src.config.OWNER}")
    print(f"Environment: {src.config.ENV}")
    print(f"Output directory: {src.config.OUTPUT_DIR}")
    # Add your main project logic here
    # Example: print('Hello, world!')

    OUTPUT_PATH = src.config.OUTPUT_DIR / "file_name.parquet"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    main()