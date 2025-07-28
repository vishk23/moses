#!/usr/bin/env python3
"""
Report Runner - Run BCSB reports by schedule or business line

USAGE:
    python testing/run_reports.py --stats                    # Show statistics only
    python testing/run_reports.py --all                     # Run all reports
    python testing/run_reports.py --daily                   # Run daily reports
    python testing/run_reports.py --weekly                  # Run weekly reports
    python testing/run_reports.py --monthly                 # Run monthly reports
    python testing/run_reports.py --as-needed               # Run as-needed reports
    python testing/run_reports.py --business-line "Retail"  # Run by business line
    python testing/run_reports.py --name "Rate Scraping"    # Run specific report
    python testing/run_reports.py --help                    # Show this help

DESCRIPTION:
    Usage utility that can run reports individually or in groups based on:
    - Schedule: daily, weekly, monthly, as-needed
    - Business line: Commercial Lending, Retail, etc.
    - Individual reports by name

    The utility automatically discovers all reports by scanning for Reports/*/src/config.py
    files and extracts metadata including schedule, business line, owner, and production
    status. It provides detailed statistics and can execute reports with proper error
    handling and timeout management.

FEATURES:
    • Report Discovery: Automatically finds all reports with src/config.py files
    • Statistics: Shows report counts by business line and schedule
    • Flexible Filtering: Run reports by schedule, business line, or name
    • Error Handling: Proper timeout management and detailed error reporting
    • Progress Tracking: Shows real-time progress during batch runs
    • Environment Management: Automatically sets REPORT_ENV=dev for execution

EXAMPLES:
    # Show just the statistics without running anything
    python testing/run_reports.py --stats
    
    # Run all monthly reports
    python testing/run_reports.py --monthly
    
    # Run all reports for a specific business line
    python testing/run_reports.py --business-line "Commercial Lending"
    
    # Run a specific report by searching for its name
    python testing/run_reports.py --name "Rate Scraping"
    
    # Run all reports (be careful - this takes a long time!)
    python testing/run_reports.py --all

OUTPUT:
    The utility provides detailed output including:
    - Discovery phase showing total reports found
    - Statistics breakdown by business line and schedule
    - Real-time progress during execution
    - Success/failure summary with error details
    - Failed report list with specific error messages

REQUIREMENTS:
    - Python 3.6+
    - All reports must have src/config.py with metadata
    - Reports should have src/main.py to be executable
    - Proper PYTHONPATH configuration for imports
"""

import os
import sys
import subprocess
import importlib.util
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import defaultdict


def setup_logging() -> logging.Logger:
    """Setup logging configuration based on environment."""
    # Get environment (same logic as reports)
    env = os.getenv('REPORT_ENV', 'dev')
    
    # Create logs directory if it doesn't exist
    logs_dir = Path(__file__).parent / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    # Choose log file based on environment
    log_file = logs_dir / f"{env}_execution.log"
    
    # Setup logger
    logger = logging.getLogger('report_runner')
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
    
    # Console handler (optional - can be disabled if too verbose)
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('%(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # Log session start
    logger.info(f"=== REPORT RUNNER SESSION START [{env.upper()} MODE] ===")
    
    return logger


def import_config(config_path: Path) -> Optional[object]:
    """Import a config.py file and return the module."""
    try:
        # Save original environment and set dev
        original_env = os.environ.get('REPORT_ENV')
        os.environ['REPORT_ENV'] = 'dev'
        
        spec = importlib.util.spec_from_file_location("config", config_path)
        if spec is None or spec.loader is None:
            print(f"Could not load spec for {config_path}")
            return None
            
        config_module = importlib.util.module_from_spec(spec)
        
        # Add required imports to module namespace
        config_module.__dict__['Path'] = Path
        config_module.__dict__['os'] = os
        
        # Suppress stdout during config execution to avoid discovery spam
        import contextlib
        with contextlib.redirect_stdout(open(os.devnull, 'w')):
            spec.loader.exec_module(config_module)
        
        # Restore original environment
        if original_env:
            os.environ['REPORT_ENV'] = original_env
        elif 'REPORT_ENV' in os.environ:
            del os.environ['REPORT_ENV']
            
        return config_module
    except Exception as e:
        print(f"Error importing config {config_path}: {e}")
        return None


def discover_reports() -> List[Dict]:
    """Discover all reports by scanning for src/config.py files."""
    reports = []
    
    # Find all reports with src/config.py
    for config_path in Path("Reports").glob("*/*/src/config.py"):
        report_path = config_path.parent.parent
        business_line = report_path.parent.name
        report_name = report_path.name
        
        # Import config to get metadata
        config = import_config(config_path)
        if not config:
            continue
            
        # Extract metadata with defaults
        schedule = getattr(config, 'SCHEDULE', 'Unknown').lower()
        owner = getattr(config, 'OWNER', 'Unknown')
        prod_ready = getattr(config, 'PROD_READY', False)
        report_title = getattr(config, 'REPORT_NAME', report_name)
        
        # Check if main.py exists
        main_py = report_path / "src" / "main.py"
        has_main = main_py.exists()
        
        reports.append({
            'name': report_name,
            'title': report_title,
            'path': report_path,
            'business_line': business_line,
            'schedule': schedule,
            'owner': owner,
            'prod_ready': prod_ready,
            'has_main': has_main,
            'config_path': config_path,
            'main_path': main_py if has_main else None
        })
    
    return sorted(reports, key=lambda x: (x['business_line'], x['name']))


def categorize_by_schedule(schedule: str) -> str:
    """Normalize schedule categories."""
    schedule = schedule.lower().strip()
    if 'daily' in schedule:
        return 'daily'
    elif 'weekly' in schedule:
        return 'weekly'
    elif 'monthly' in schedule:
        return 'monthly'
    elif 'on demand' in schedule or 'on-demand' in schedule:
        return 'on-demand'
    else:
        return 'other'


def get_venv_python() -> str:
    """Get the Python executable from the virtual environment."""
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        # We're already in a virtual environment, use current executable
        return sys.executable
    
    # Look for .venv in project root
    project_root = Path(__file__).parent.parent
    venv_paths = [
        project_root / ".venv" / "bin" / "python",      # Unix/Mac
        project_root / ".venv" / "Scripts" / "python.exe",  # Windows
        project_root / "venv" / "bin" / "python",       # Alternative name Unix/Mac
        project_root / "venv" / "Scripts" / "python.exe",   # Alternative name Windows
    ]
    
    for venv_python in venv_paths:
        if venv_python.exists():
            return str(venv_python)
    
    # Fallback to current executable if no venv found
    print("Warning: No virtual environment found, using current Python")
    return sys.executable


def print_statistics(reports: List[Dict]):
    """Print detailed statistics about discovered reports."""
    total_reports = len(reports)
    runnable_reports = len([r for r in reports if r['has_main']])
    prod_ready_reports = len([r for r in reports if r['prod_ready']])
    
    print(f"Report Statistics:")
    print(f"   Total reports: {total_reports}")
    print(f"   Runnable (has main.py): {runnable_reports}")
    print(f"   Production ready: {prod_ready_reports}")
    
    # Business line breakdown
    by_business_line = defaultdict(int)
    for report in reports:
        by_business_line[report['business_line']] += 1
    
    print(f"\nBy Business Line:")
    for business_line, count in sorted(by_business_line.items()):
        print(f"   {business_line}: {count} reports")
    
    # Schedule breakdown
    by_schedule = defaultdict(int)
    for report in reports:
        normalized_schedule = categorize_by_schedule(report['schedule'])
        by_schedule[normalized_schedule] += 1
    
    print(f"\nBy Schedule:")
    for schedule, count in sorted(by_schedule.items()):
        print(f"   {schedule.title()}: {count} reports")


def run_report(report: Dict, logger: logging.Logger) -> Tuple[bool, str]:
    """Run a single report and return success status and message."""
    if not report['has_main']:
        error_msg = "No main.py file found"
        logger.warning(f"SKIPPED | {report['title']} | {error_msg}")
        return False, error_msg
    
    # Get environment and Python executable
    env = os.getenv('REPORT_ENV', 'dev')
    python_executable = get_venv_python()
    start_time = datetime.now()
    
    # Log start
    logger.info(f"START | {report['title']} | Business Line: {report['business_line']} | Environment: {env.upper()}")
    logger.info(f"DEBUG | Python executable: {python_executable}")
    logger.info(f"DEBUG | Working directory: {report['path']}")
    logger.info(f"DEBUG | Command: {python_executable} -m src.main")
    
    try:
        # Set environment variables
        env_vars = os.environ.copy()
        env_vars['REPORT_ENV'] = env
        
        # Fix Unicode encoding issues on Windows
        env_vars['PYTHONIOENCODING'] = 'utf-8'
        
        # Run the report using the virtual environment's Python
        result = subprocess.run(
            [python_executable, "-m", "src.main"],
            capture_output=True,
            text=True,
            env=env_vars,
            cwd=str(report['path']),  # Set working directory directly
            # timeout=300  # 5 minute timeout
        )
        
        # Calculate runtime
        end_time = datetime.now()
        runtime_seconds = (end_time - start_time).total_seconds()
        runtime_minutes = round(runtime_seconds / 60, 2)
        
        if result.returncode == 0:
            success_msg = f"SUCCESS | {report['title']} | Runtime: {runtime_minutes} minutes"
            logger.info(success_msg)
            return True, "Success"
        else:
            # Log the full error details for debugging
            stderr_full = result.stderr.strip() if result.stderr else ""
            stdout_full = result.stdout.strip() if result.stdout else ""
            
            # Log full error details
            logger.error(f"FAILED | {report['title']} | Runtime: {runtime_minutes} minutes")
            logger.error(f"Python executable: {python_executable}")
            logger.error(f"Working directory: {report['path']}")
            logger.error(f"Return code: {result.returncode}")
            if stderr_full:
                logger.error(f"STDERR:\n{stderr_full}")
            if stdout_full:
                logger.error(f"STDOUT:\n{stdout_full}")
            
            # Return truncated version for summary
            error_msg = stderr_full or stdout_full or "Unknown error"
            truncated_error = error_msg[:200] + "..." if len(error_msg) > 200 else error_msg
            return False, f"Error: {truncated_error}"
            
    except subprocess.TimeoutExpired:
        end_time = datetime.now()
        runtime_seconds = (end_time - start_time).total_seconds()
        runtime_minutes = round(runtime_seconds / 60, 2)
        timeout_msg = f"TIMEOUT | {report['title']} | Runtime: {runtime_minutes} minutes (>5 minutes)"
        logger.error(timeout_msg)
        return False, "Timeout (>5 minutes)"
    except Exception as e:
        end_time = datetime.now()
        runtime_seconds = (end_time - start_time).total_seconds()
        runtime_minutes = round(runtime_seconds / 60, 2)
        exception_msg = f"EXCEPTION | {report['title']} | Runtime: {runtime_minutes} minutes | Exception: {str(e)}"
        logger.error(exception_msg)
        return False, f"Exception: {str(e)}"


def run_reports_by_filter(reports: List[Dict], filter_type: str, filter_value: str, logger: logging.Logger) -> List[Dict]:
    """Filter and run reports based on criteria."""
    filtered_reports = []
    
    if filter_type == "schedule":
        target_schedule = categorize_by_schedule(filter_value)
        filtered_reports = [r for r in reports if categorize_by_schedule(r['schedule']) == target_schedule]
    elif filter_type == "business_line":
        filtered_reports = [r for r in reports if r['business_line'].lower() == filter_value.lower()]
    elif filter_type == "name":
        filtered_reports = [r for r in reports if filter_value.lower() in r['name'].lower()]
    elif filter_type == "all":
        filtered_reports = reports
    
    if not filtered_reports:
        msg = f"No reports found matching {filter_type}: {filter_value}"
        print(msg)
        logger.warning(f"NO REPORTS FOUND | Filter: {filter_type} = {filter_value}")
        return []
    
    # Log batch start
    env = os.getenv('REPORT_ENV', 'dev')
    batch_start_msg = f"BATCH START | {len(filtered_reports)} reports | Filter: {filter_type} = {filter_value} | Environment: {env.upper()}"
    logger.info(batch_start_msg)
    
    print(f"\nRunning {len(filtered_reports)} reports matching {filter_type}: {filter_value}\n")
    
    batch_start_time = datetime.now()
    results = []
    
    for i, report in enumerate(filtered_reports, 1):
        print(f"[{i}/{len(filtered_reports)}] Running: {report['title']} ({report['business_line']})")
        
        success, message = run_report(report, logger)
        
        result = {
            'report': report,
            'success': success,
            'message': message
        }
        results.append(result)
        
        if success:
            print(f"   Success: {message}")
        else:
            print(f"   Error: {message}")
    
    # Calculate batch runtime
    batch_end_time = datetime.now()
    batch_runtime_seconds = (batch_end_time - batch_start_time).total_seconds()
    batch_runtime_minutes = round(batch_runtime_seconds / 60, 2)
    
    # Summary
    successful = len([r for r in results if r['success']])
    failed = len(results) - successful
    
    # Log batch completion
    batch_summary = f"BATCH COMPLETE | Total: {len(results)} | Successful: {successful} | Failed: {failed} | Batch Runtime: {batch_runtime_minutes} minutes"
    logger.info(batch_summary)
    
    print(f"\n{'='*60}")
    print(f"Run Summary:")
    print(f"   Successful: {successful}")
    print(f"   Failed: {failed}")
    print(f"   Total Runtime: {batch_runtime_minutes} minutes")
    
    if failed > 0:
        print(f"\nFailed Reports:")
        for result in results:
            if not result['success']:
                print(f"   {result['report']['name']}: {result['message']}")
    
    return results


def main():
    """Main entry point."""
    # Change to parent directory so relative paths work
    os.chdir(Path(__file__).parent.parent)
    
    # Setup logging first
    logger = setup_logging()
    
    args = sys.argv[1:]
    
    if not args or args[0] == "--help":
        print(__doc__)
        print("\nUsage:")
        print("  python testing/run_reports.py --stats                    # Show statistics only")
        print("  python testing/run_reports.py --all                     # Run all reports")
        print("  python testing/run_reports.py --daily                   # Run daily reports")
        print("  python testing/run_reports.py --weekly                  # Run weekly reports") 
        print("  python testing/run_reports.py --monthly                 # Run monthly reports")
        print("  python testing/run_reports.py --as-needed               # Run as-needed reports")
        print("  python testing/run_reports.py --business-line \"Commercial Lending\"  # Run by business line")
        print("  python testing/run_reports.py --name \"Rate Scraping\"    # Run specific report")
        print("  python testing/run_reports.py --help                    # Show this help")
        return
    
    # Discover all reports
    print("Discovering reports...")
    reports = discover_reports()
    
    if not reports:
        print("No reports found!")
        logger.warning("NO REPORTS DISCOVERED | No reports with src/config.py found")
        return
    
    # Log discovery results
    env = os.getenv('REPORT_ENV', 'dev')
    logger.info(f"DISCOVERY COMPLETE | Found {len(reports)} reports | Environment: {env.upper()}")
    
    # Show statistics
    print_statistics(reports)
    
    # Handle commands
    command = args[0].lower()
    
    if command == "--stats":
        logger.info("STATS ONLY | No reports executed")
        return
    elif command == "--all":
        run_reports_by_filter(reports, "all", "", logger)
    elif command == "--daily":
        run_reports_by_filter(reports, "schedule", "daily", logger)
    elif command == "--weekly":
        run_reports_by_filter(reports, "schedule", "weekly", logger)
    elif command == "--monthly":
        run_reports_by_filter(reports, "schedule", "monthly", logger)
    elif command == "--as-needed":
        run_reports_by_filter(reports, "schedule", "as-needed", logger)
    elif command == "--business-line":
        if len(args) < 2:
            print("Please specify business line name")
            logger.error("INVALID COMMAND | Missing business line name")
            return
        run_reports_by_filter(reports, "business_line", args[1], logger)
    elif command == "--name":
        if len(args) < 2:
            print("Please specify report name")
            logger.error("INVALID COMMAND | Missing report name")
            return
        run_reports_by_filter(reports, "name", args[1], logger)
    else:
        print(f"Unknown command: {command}")
        print("Use --help for usage information")
        logger.error(f"INVALID COMMAND | Unknown command: {command}")
    
    # Log session end
    logger.info("=== REPORT RUNNER SESSION END ===\n")


if __name__ == "__main__":
    main()