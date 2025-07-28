#!/usr/bin/env python3
"""
Simple test runner for BCSB reports.
MAIN ENTRY POINT FOR TESTING ALL REPORTS
Usage:
    python testing/run_tests.py                    # Test all reports
    python testing/run_tests.py --sync             # Sync files then test all
    python testing/run_tests.py "Report Name"      # Test specific report
    python testing/run_tests.py "Report Name" --sync  # Sync then test specific
"""

import sys
import subprocess
import logging
import os
from datetime import datetime
from pathlib import Path


def setup_logging() -> logging.Logger:
    """Setup logging configuration based on environment."""
    # Get environment (same logic as reports)
    env = os.getenv('REPORT_ENV', 'dev')
    
    # Create logs directory if it doesn't exist
    logs_dir = Path(__file__).parent / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    # Choose log file based on environment
    log_file = logs_dir / f"{env}_test_execution.log"
    
    # Setup logger
    logger = logging.getLogger('test_runner')
    logger.setLevel(logging.INFO)
    
    # Remove existing handlers to avoid duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # File handler
    file_handler = logging.FileHandler(log_file, mode='a')
    file_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Log session start
    logger.info(f"=== TEST RUNNER SESSION START [{env.upper()} MODE] ===")
    
    return logger


def main():
    # Change to parent directory so relative paths work
    os.chdir(Path(__file__).parent.parent)
    
    # Setup logging
    logger = setup_logging()
    
    args = sys.argv[1:]
    
    # Check for help
    if "--help" in args or "-h" in args:
        print(__doc__)
        return
    
    # Check for sync flag
    do_sync = "--sync" in args
    if do_sync:
        args.remove("--sync")
    
    # Get environment
    env = os.getenv('REPORT_ENV', 'dev')
    start_time = datetime.now()
    
    # Log test session details
    if args:
        logger.info(f"TEST SESSION START | Specific Report: {args[0]} | Sync: {do_sync} | Environment: {env.upper()}")
    else:
        logger.info(f"TEST SESSION START | All Reports | Sync: {do_sync} | Environment: {env.upper()}")
    
    # Get script paths
    script_dir = Path(__file__).parent
    sync_script = script_dir / "sync_files.py"
    test_script = script_dir / "test_reports.py"
    
    # Handle sync
    if do_sync:
        sync_start_time = datetime.now()
        print("Syncing files from production...\n")
        logger.info("SYNC START | Syncing files from production")
        
        if args:
            # Sync specific report
            result = subprocess.run([sys.executable, str(sync_script), args[0]])
            logger.info(f"SYNC SPECIFIC | Report: {args[0]} | Return Code: {result.returncode}")
        else:
            # Sync all
            result = subprocess.run([sys.executable, str(sync_script)])
            logger.info(f"SYNC ALL | Return Code: {result.returncode}")
        
        sync_end_time = datetime.now()
        sync_runtime = round((sync_end_time - sync_start_time).total_seconds() / 60, 2)
        logger.info(f"SYNC COMPLETE | Runtime: {sync_runtime} minutes")
        print("\n" + "=" * 60 + "\n")
    
    # Run tests
    test_start_time = datetime.now()
    print("Running tests...\n")
    logger.info("TESTS START | Beginning pytest execution")
    
    if args:
        # Test specific report - replace spaces with underscores for pytest filter
        report_filter = args[0].replace(' ', '_')
        result = subprocess.run([sys.executable, "-m", "pytest", str(test_script), "-v", "-s", "--tb=short", "-k", report_filter])
        logger.info(f"TESTS SPECIFIC | Report Filter: {report_filter} | Return Code: {result.returncode}")
    else:
        # Test all  
        result = subprocess.run([sys.executable, "-m", "pytest", str(test_script), "-v", "-s", "--tb=short"])
        logger.info(f"TESTS ALL | Return Code: {result.returncode}")
    
    # Calculate total runtime
    end_time = datetime.now()
    total_runtime = round((end_time - start_time).total_seconds() / 60, 2)
    
    # Log session completion
    logger.info(f"TEST SESSION COMPLETE | Total Runtime: {total_runtime} minutes | Final Return Code: {result.returncode}")
    logger.info("=== TEST RUNNER SESSION END ===\n")


if __name__ == "__main__":
    main()