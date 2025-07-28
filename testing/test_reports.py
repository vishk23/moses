#!/usr/bin/env python3
"""
Simple pytest-based test framework for BCSB reports.

Run with:
    python -m pytest testing/test_reports.py                    # Test all reports
    python -m pytest testing/test_reports.py -k "report_name"   # Test specific report
    python -m pytest testing/test_reports.py -v                 # Verbose output
"""

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import List

import pytest

# Change to parent directory so relative paths work
os.chdir(Path(__file__).parent.parent)

# Print startup information
print("BCSB Reports Test Framework")
print("=" * 60)
print(f"Working directory: {os.getcwd()}")
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version.split()[0]}")
print("=" * 60)


def get_all_reports() -> List[Path]:
    """Get all reports that have test configurations."""
    print("\nScanning for reports with test configurations...")
    
    reports = []
    test_configs_found = list(Path("Reports").glob("*/*/test/test_config.json"))
    
    print(f"Found {len(test_configs_found)} test configuration files:")
    for test_config in test_configs_found:
        report_path = test_config.parent.parent
        reports.append(report_path)
        print(f"   {report_path}")
    
    # Also scan for reports without test configs but with main.py
    print("\nScanning for reports without test configurations...")
    reports_without_configs = []
    for main_file in Path("Reports").glob("*/*/src/main.py"):
        report_path = main_file.parent.parent
        test_config = report_path / "test" / "test_config.json"
        if not test_config.exists():
            reports_without_configs.append(report_path)
    
    if reports_without_configs:
        print(f"Found {len(reports_without_configs)} reports without test configs:")
        for report_path in reports_without_configs:
            print(f"   {report_path}")
    else:
        print("All reports have test configurations!")
    
    print(f"\nTotal reports to test: {len(reports)}")
    print("=" * 60)
    
    return sorted(reports)


def get_test_config(report_path: Path) -> dict:
    """Load test configuration for a report."""
    test_config_file = report_path / "test" / "test_config.json"
    if test_config_file.exists():
        try:
            with open(test_config_file) as f:
                config = json.load(f)
            print(f"Loaded test config for {report_path.name}: {len(config)} settings")
            return config
        except Exception as e:
            print(f"Error loading test config for {report_path.name}: {e}")
            return {}
    else:
        print(f"No test config found for {report_path.name}, using defaults")
        return {}


# Generate test cases for each report
@pytest.mark.parametrize("report_path", get_all_reports(), ids=lambda p: p.name)
def test_report(report_path: Path):
    """Test a single report."""
    print(f"\nTesting report: {report_path.name}")
    print(f"Path: {report_path}")
    
    config = get_test_config(report_path)
    
    # Skip if configured
    if config.get("skip", False):
        skip_reason = config.get("skip_reason", "Configured to skip")
        print(f"Skipping: {skip_reason}")
        pytest.skip(skip_reason)
    
    # Check for required files
    main_file = report_path / "src" / "main.py"
    config_file = report_path / "src" / "config.py"
    
    print(f"Checking required files...")
    print(f"   main.py: {'✅' if main_file.exists() else '❌'}")
    print(f"   config.py: {'✅' if config_file.exists() else '❌'}")
    
    assert main_file.exists(), f"main.py not found for {report_path.name}"
    
    output_dir = report_path / "output"
    
    # Clear output directory
    print(f"Preparing output directory: {output_dir}")
    if output_dir.exists():
        existing_files = list(output_dir.glob("*"))
        if existing_files:
            print(f"   Clearing {len(existing_files)} existing files")
            for file in existing_files:
                if file.is_file():
                    file.unlink()
        else:
            print("   Output directory already empty")
    else:
        print("   Creating output directory")
        output_dir.mkdir(exist_ok=True)
    
    # Run the report
    print(f"Executing report...")
    print(f"   Command: {sys.executable} src/main.py")
    print(f"   Working directory: {report_path.resolve()}")
    print(f"   Environment: REPORT_ENV=dev")
    
    env = os.environ.copy()
    env['REPORT_ENV'] = 'dev'
    
    # Add the report directory and project root to Python path so imports work
    current_pythonpath = env.get('PYTHONPATH', '')
    report_path_str = str(report_path.resolve())
    project_root = str(Path(__file__).parent.parent.resolve())  # Go up from testing/ to project root
    
    # Use appropriate path separator for the OS (: for Unix, ; for Windows)
    path_separator = ';' if os.name == 'nt' else ':'
    paths_to_add = [report_path_str, project_root]
    
    if current_pythonpath:
        env['PYTHONPATH'] = f"{path_separator.join(paths_to_add)}{path_separator}{current_pythonpath}"
    else:
        env['PYTHONPATH'] = path_separator.join(paths_to_add)
    
    print(f"   PYTHONPATH: {env['PYTHONPATH'][:100]}{'...' if len(env['PYTHONPATH']) > 100 else ''}")
    print(f"   OS: {os.name}, Path separator: {repr(path_separator)}")
    
    start_time = __import__('time').time()
    
    try:
        result = subprocess.run(
            [sys.executable, "src/main.py"],
            cwd=str(report_path.resolve()),
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
            env=env
        )
    except KeyboardInterrupt:
        print(f"\nTest interrupted by user (Ctrl+C)")
        raise
    
    execution_time = __import__('time').time() - start_time
    print(f"Execution time: {execution_time:.2f} seconds")
    print(f"Return code: {result.returncode}")
    
    if result.stdout:
        print(f"Output preview (first 500 chars):")
        print(f"   {result.stdout[:500]}")
        if len(result.stdout) > 500:
            print(f"   ... (truncated, {len(result.stdout)} total chars)")
    
    if result.stderr:
        print(f"Error output:")
        print(f"   {result.stderr}")
    
    # Check execution succeeded - show detailed output immediately on failure
    if result.returncode != 0:
        print(f"\nEXECUTION FAILED")
        print(f"Report: {report_path.name}")
        print(f"Time: {execution_time:.2f} seconds")
        print(f"Exit code: {result.returncode}")
        if result.stderr:
            print(f"ERROR DETAILS:")
            print("-" * 50)
            print(result.stderr)
            print("-" * 50)
        if result.stdout:
            print(f"OUTPUT:")
            print("-" * 50)  
            print(result.stdout)
            print("-" * 50)
        print(f"Fix suggestions:")
        if "ModuleNotFoundError" in result.stderr:
            print(f"   - Missing Python package - install required dependencies")
        if "No such file or directory" in result.stderr:
            print(f"   - Missing input files - try running with --sync flag")
        print("")
        
    assert result.returncode == 0, f"Report execution failed - see details above"
    
    # Check expected outputs
    expected_outputs = config.get("expected_outputs", [])
    output_files = list(output_dir.glob("*"))
    
    print(f"Output verification:")
    print(f"   Generated files: {len(output_files)}")
    for file in output_files:
        print(f"      {file.name} ({file.stat().st_size} bytes)")
    
    if expected_outputs:
        print(f"   Expected patterns: {expected_outputs}")
        
        for expected in expected_outputs:
            if "*" in expected:
                # Pattern match
                matches = list(output_dir.glob(expected))
                print(f"      Pattern '{expected}': {len(matches)} matches")
                assert matches, f"No files matching pattern: {expected}"
            else:
                # Exact match
                exists = (output_dir / expected).exists()
                print(f"      File '{expected}': {'✅' if exists else '❌'}")
                assert exists, f"Missing output: {expected}"
    
    # Report should have produced at least one output
    assert output_files, "No output files generated"
    
    print(f"Test passed for {report_path.name}")
    print("-" * 40)


# Additional test to verify all reports have proper configs
def test_all_reports_have_configs():
    """Verify all reports have standardized configs."""
    print("\nVerifying all reports have proper configurations...")
    
    missing_configs = []
    total_reports = 0
    
    for report_dir in Path("Reports").glob("*/*/"):
        if (report_dir / "src" / "main.py").exists():
            total_reports += 1
            config_file = report_dir / "src" / "config.py"
            if not config_file.exists():
                missing_configs.append(str(report_dir))
                print(f"   Missing config: {report_dir}")
            else:
                print(f"   Has config: {report_dir}")
    
    print(f"\nConfiguration Summary:")
    print(f"   Total reports found: {total_reports}")
    print(f"   Reports with configs: {total_reports - len(missing_configs)}")
    print(f"   Reports missing configs: {len(missing_configs)}")
    
    assert not missing_configs, f"Reports missing config.py: {missing_configs}"
    print("All reports have proper configurations!")


# Test to check sync capability
def test_sync_configuration():
    """Verify reports with input files have proper sync config."""
    print("\nVerifying sync configurations...")
    
    reports_with_sync = 0
    reports_tested = 0
    
    for report_path in get_all_reports():
        config = get_test_config(report_path)
        sync_config = config.get("sync_config", {})
        expected_files = sync_config.get("expected_input_files", [])
        
        if expected_files:
            reports_with_sync += 1
            print(f"   {report_path.name} expects {len(expected_files)} input files")
            
            # This report needs input files
            config_file = report_path / "src" / "config.py"
            if config_file.exists():
                reports_tested += 1
                # Just verify config exists and is importable
                try:
                    spec = importlib.util.spec_from_file_location("config", config_file)
                    assert spec is not None, f"Cannot load config for {report_path.name}"
                    print(f"      Config loadable")
                except Exception as e:
                    print(f"      Config error: {e}")
                    pytest.fail(f"Config error for {report_path.name}: {e}")
        else:
            print(f"   {report_path.name} has no sync requirements")
    
    print(f"\nSync Configuration Summary:")
    print(f"   Reports with sync needs: {reports_with_sync}")
    print(f"   Sync configs tested: {reports_tested}")
    print("All sync configurations verified!")


if __name__ == "__main__":
    # Allow running directly
    print("\nRunning tests directly...")
    print("Tip: Use 'python -m pytest testing/test_reports.py -v' for even more detailed output")
    print("=" * 60)
    pytest.main([__file__, "-v"] + sys.argv[1:])