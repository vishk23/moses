"""
Main entry point for Dealer Reserve Recon project.

This script loads configuration from config.py and runs the main pipeline.
"""

import src.config
import src.early_payoff_report
import src.daily_processing
import src.report_generator
from src._version import __version__

def main():
    print(f"Running {src.config.REPORT_NAME} for {src.config.BUSINESS_LINE}")
    print(f"Schedule: {src.config.SCHEDULE}")
    print(f"Owner: {src.config.OWNER}")
    print(f"Environment: {src.config.ENV}")
    print(f"Output directory: {src.config.OUTPUT_DIR}")
    print(f"Version: {__version__}")

    # 1. Early Payoff Report
    print("Step 1: Running Early Payoff Report...")
    src.early_payoff_report.main()

    # 2. Daily Processing
    print("Step 2: Processing daily files...")
    src.daily_processing.process_daily()

    # 3. Report Generator
    print("Step 3: Generating final report...")
    src.report_generator.generate_report()

    print("Dealer Reserve Recon pipeline complete.")

if __name__ == '__main__':
    print(f"Starting [{__version__}]")
    main()
    print("Complete!")
