#!/usr/bin/env python3
"""
Simple file sync utility for BCSB reports.

Syncs input files from production to local development environment.
"""

import os
import shutil
import sys
import importlib.util
from pathlib import Path
from typing import Optional, Dict, List


def import_config(config_path: Path) -> Optional[object]:
    """Import a config.py file and return the module."""
    try:
        # Import config while preventing directory creation during module loading
        
        # Set production environment to get production paths
        os.environ['REPORT_ENV'] = 'prod'
        
        # Create a module object and set up the namespace
        spec = importlib.util.spec_from_file_location("config", config_path)
        config_module = importlib.util.module_from_spec(spec)
        
        # Add Path to the module's namespace so it can be used
        config_module.__dict__['Path'] = Path
        config_module.__dict__['os'] = os
        
        # Execute the config module
        spec.loader.exec_module(config_module)
        
        # Reset to dev environment immediately after loading for safety
        os.environ['REPORT_ENV'] = 'dev'
        
        return config_module
    except Exception as e:
        print(f"ERROR: Error importing config: {e}")
        # Ensure env is reset even on error
        os.environ['REPORT_ENV'] = 'dev'
        return None


def sync_report(report_path: Path, verbose: bool = True) -> Dict:
    """Sync files for a single report."""
    report_name = report_path.name
    config_file = report_path / "src" / "config.py"
    
    result = {
        "report": report_name,
        "status": "SUCCESS",
        "files_synced": 0,
        "message": ""
    }
    
    if not config_file.exists():
        result["status"] = "SKIP"
        result["message"] = "No config.py found"
        return result
    
    # Import the config to get actual paths
    config = import_config(config_file)
    if not config:
        result["status"] = "ERROR"
        result["message"] = "Failed to import config"
        return result
    
    # Check if report has production path
    if not hasattr(config, 'INPUT_DIR'):
        if verbose:
            print(f"\nSyncing: {report_name}")
            print(f"   No INPUT_DIR - report doesn't need input files")
        result["status"] = "NO_INPUT"
        result["message"] = "No INPUT_DIR in config"
        return result
    
    prod_input_dir = Path(config.INPUT_DIR)
    local_input_dir = report_path / "input"
    
    if verbose:
        print(f"\nSyncing: {report_name}")
        # Windows-only path formatting
        prod_path_display = str(prod_input_dir).replace('/', '\\')
        local_path_display = str(local_input_dir.resolve()).replace('/', '\\')
        
        print(f"   From: {prod_path_display}")
        print(f"   To:   {local_path_display}")
    
    # Check if production directory exists and count files
    if not prod_input_dir.exists():
        if verbose:
            print(f"   Directory not found")
        result["status"] = "SKIP"
        result["message"] = "Production directory not accessible"
        return result
    else:
        # Count files in production directory
        file_count = len([f for f in prod_input_dir.glob("*") if f.is_file()])
        if verbose:
            print(f"   Directory found - {file_count} files available")
    
    # Create local directory
    local_input_dir.mkdir(exist_ok=True)
    
    # Copy files
    files_copied = 0
    try:
        for file in prod_input_dir.glob("*"):
            if file.is_file():
                dest = local_input_dir / file.name
                shutil.copy2(file, dest)
                if verbose:
                    print(f"   Copied: {file.name}")
                files_copied += 1
        
        result["files_synced"] = files_copied
        if files_copied == 0:
            result["message"] = "No files to sync"
        else:
            result["message"] = f"Synced {files_copied} files"
        
        if verbose:
            print(f"   Total: {files_copied} files")
            
    except Exception as e:
        result["status"] = "ERROR"
        result["message"] = f"Error copying files: {e}"
        if verbose:
            print(f"   Error: {e}")
    
    return result


def sync_all_reports(filter_pattern: Optional[str] = None) -> List[Dict]:
    """Sync files for all reports."""
    results = []
    
    # Find all reports
    report_paths = []
    for path in Path("Reports").glob("*/*/"):
        if (path / "src" / "config.py").exists():
            if filter_pattern and filter_pattern.lower() not in path.name.lower():
                continue
            report_paths.append(path)
    
    print(f"Syncing files for {len(report_paths)} reports\n")
    
    for report_path in sorted(report_paths):
        result = sync_report(report_path)
        results.append(result)
    
    # Summary
    print("\n" + "=" * 60)
    print("Sync Summary:")
    
    success = sum(1 for r in results if r["status"] == "SUCCESS")
    skipped = sum(1 for r in results if r["status"] == "SKIP")
    no_input = sum(1 for r in results if r["status"] == "NO_INPUT")
    errors = sum(1 for r in results if r["status"] == "ERROR")
    total_reports = len(results)
    total_files = sum(r["files_synced"] for r in results)
    
    print(f"   Total reports: {total_reports}")
    print(f"   Success: {success} reports")
    print(f"   No input needed: {no_input} reports")
    print(f"   Skipped (dir not found): {skipped} reports")
    print(f"   Errors: {errors} reports")
    print(f"   Total files synced: {total_files}")
    
    # Show reports without input directories
    no_input_reports = [r for r in results if r["status"] == "NO_INPUT"]
    if no_input_reports:
        print("\nReports with no input files needed:")
        for r in no_input_reports:
            print(f"   {r['report']}")
    
    # Show errors if any
    error_reports = [r for r in results if r["status"] == "ERROR"]
    if error_reports:
        print("\nFailed syncs:")
        for r in error_reports:
            print(f"   {r['report']}: {r['message']}")
    
    # Show network locations summary
    print("\nNetwork Locations:")
    network_paths = set()
    for report_path in sorted(report_paths):
        config_file = report_path / "src" / "config.py"
        if config_file.exists():
            try:
                config = import_config(config_file)
                if config and hasattr(config, 'INPUT_DIR'):
                    prod_path = Path(config.INPUT_DIR)
                    if str(prod_path).startswith('\\\\'):  # Network path
                        network_paths.add(str(prod_path.parent))
            except:
                continue
    
    for path in sorted(network_paths):
        display_path = path.replace('/', '\\')
        print(f"   {display_path}")
    
    return results


def main():
    """Main entry point."""
    # Change to parent directory so relative paths work
    os.chdir(Path(__file__).parent.parent)
    
    args = sys.argv[1:]
    
    if not args:
        # Sync all reports
        sync_all_reports()
    elif args[0] == "--help":
        print(__doc__)
        print("\nUsage:")
        print("  python testing/sync_files.py              # Sync all reports")
        print("  python testing/sync_files.py ReportName   # Sync specific report")
        print("  python testing/sync_files.py --help       # Show this help")
    else:
        # Sync specific report
        report_name = args[0]
        
        # Find the report
        report_path = None
        for path in Path("Reports").glob(f"*/{report_name}"):
            if (path / "src" / "config.py").exists():
                report_path = path
                break
        
        if report_path:
            sync_report(report_path, verbose=True)
        else:
            print(f"ERROR: Report '{report_name}' not found")
            print("\nAvailable reports:")
            for path in sorted(Path("Reports").glob("*/*/src/config.py")):
                print(f"   {path.parent.parent.name}")


if __name__ == "__main__":
    main()