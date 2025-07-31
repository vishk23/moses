# Simple Testing Framework for BCSB Reports

## Overview

This is a clean, simple testing framework that:
1. Syncs input files from production when needed
2. Runs reports in dev environment
3. Validates output files are generated
4. Uses pytest for clean test reporting

## Files

Located in the `testing/` directory:
- `testing/sync_files.py` - Syncs input files from production to local dev
- `testing/test_reports.py` - Pytest-based tests for all reports
- `testing/run_tests.py` - Simple wrapper to sync + test

## How It Works

### File Sync
The sync utility:
1. Finds reports by looking for `Reports/*/*/src/config.py`
2. Imports the config module with `REPORT_ENV=prod` to get production paths
3. Copies files from production `INPUT_DIR` to local `input/` folder
4. Resets to `REPORT_ENV=dev` for testing
5. Safely handles reports without production paths or inaccessible network locations

### Testing
The pytest framework:
1. Finds all reports with `test/test_config.json` files
2. Runs each report's `main.py` in dev environment
3. Validates expected output files are generated
4. Skips reports marked with `"skip": true`
5. Shows detailed failure output immediately when tests fail

## Usage

```bash
# Test all reports (no sync)
python testing/run_tests.py

# Sync files then test all reports
python testing/run_tests.py --sync

# Test specific report
python testing/run_tests.py "Rate Scraping"

# Sync then test specific report
python testing/run_tests.py "Business_Concentration_of_Deposits" --sync

# Use pytest directly for more control
python -m pytest testing/test_reports.py -v
python -m pytest testing/test_reports.py -k "Rate_Scraping" -v

# Use sync utility directly
python testing/sync_files.py                    # Sync all reports
python testing/sync_files.py "Report Name"      # Sync specific report

# Interrupt tests
# Press Ctrl+C to cleanly interrupt running tests
```

## Test Configuration

Each report's `test/test_config.json`:

```json
{
  "description": "Test description",
  "skip": false,
  "expected_outputs": [
    "exact_filename.xlsx",
    "pattern_*.csv"
  ],
  "sync_config": {
    "expected_input_files": ["input_file.xlsx"],
    "notes": "Only needed for documentation"
  }
}
```

- `skip`: Set to `true` to skip this report
- `expected_outputs`: Files that should be generated (supports wildcards)
- `sync_config.expected_input_files`: Files needed from production (for documentation only)

## Requirements

- Python 3.6+ 
- `pytest` package (install with `pip install pytest`)

## Benefits

1. **Simple**: No complex state management or manifest files
2. **Robust**: Imports config modules directly instead of text parsing
3. **Standard**: Uses pytest for familiar test interface
4. **Fast**: Only syncs what's needed when requested
5. **Clear**: Easy to understand what each component does
6. **Safe**: Environment variables are properly managed during sync operations
7. **Cross-platform**: Works on both Windows and Unix systems with proper path handling

## File Discovery

**How sync finds reports:**
- Scans `Reports/*/*/src/config.py` files
- Imports each config with `REPORT_ENV=prod` to get production paths
- Gets `INPUT_DIR` from the imported module
- Copies files from production to local `input/` directory
- Skips reports without production paths or inaccessible network locations

**How tests find reports:**
- Scans `Reports/*/*/test/test_config.json` files
- Uses the parent directory as the report path
- Runs `src/main.py` from that directory with `REPORT_ENV=dev`

## Sync Behavior

The sync utility properly handles different scenarios:

- ✅ **Reports with production paths**: Copies files from network paths to local
- ⏭️ **Reports without INPUT_DIR**: Skipped (like Rate Scraping - uses APIs)
- ⚠️ **Network inaccessible**: Gracefully skips with warning message
- 🔒 **Environment safety**: Always resets `REPORT_ENV=dev` after import
- 🔗 **Windows clickable paths**: Network paths are shown in clickable format for easy navigation


#### Note for Windows Powershell, you set environment variable via the below syntax:
```Powershell
$env:REPORT_ENV="prod"
```