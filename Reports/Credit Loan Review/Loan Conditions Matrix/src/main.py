"""
Main entry point for Loan Conditions Matrix project.
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

if __name__ == "__main__":
    main()
