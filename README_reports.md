# Report Management System

A simple system for managing and running reports with consistent configuration.

## Quick Start

### 1. Add Configuration to Reports

Each report needs a `config.py` file in its `src/` directory:

```python
# Reports/YourBusinessLine/YourReport/src/config.py
import os
from pathlib import Path

# Basic setup
ENV = os.getenv('REPORT_ENV', 'dev')
REPORT_DIR = Path(__file__).parent.parent

# Report metadata
NAME = "Your Report Name"
SCHEDULE = "daily"  # daily, weekly, monthly, yearly, manual

# Paths
if ENV == 'prod':
    OUTPUT_DIR = Path(r"\\network\path\to\production\output")
    INPUT_DIR = Path(r"\\network\path\to\production\input")
else:
    OUTPUT_DIR = REPORT_DIR / "output"
    INPUT_DIR = REPORT_DIR / "input"

# Email recipients
if ENV == 'prod':
    EMAIL_TO = ["stakeholder@bcsbmail.com"]
    EMAIL_CC = ["businessintelligence@bcsbmail.com"]
else:
    EMAIL_TO = []
    EMAIL_CC = ["businessintelligence@bcsbmail.com"]
```

### 2. Update Your main.py

```python
# Reports/YourBusinessLine/YourReport/src/main.py
from datetime import datetime
import config
import cdutils.distribution as dist

def main():
    # Ensure output directory exists
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Your report logic here...
    output_file = config.OUTPUT_DIR / f"report_{datetime.now().strftime('%Y%m%d')}.xlsx"
    
    # Send email (works with empty recipient lists)
    dist.email_out(
        config.EMAIL_TO,
        config.EMAIL_CC,
        f"{config.NAME} - {datetime.now().strftime('%Y-%m-%d')}",
        f"Attached is the {config.NAME}.",
        [output_file]
    )

if __name__ == "__main__":
    main()
```

## Running Reports

### Individual Reports

```bash
# Development mode (local paths, no emails)
python run_report.py --report delinquency --env dev

# Production mode (network paths, real emails)
python run_report.py --report delinquency --env prod

# List all available reports
python run_report.py --list
```

### Scheduled Reports

```bash
# Run all daily reports
python scheduler.py daily

# Run all monthly reports in dev mode
python scheduler.py monthly --env dev

# See what would run without actually running
python scheduler.py weekly --dry-run
```

## Directory Structure

```
Reports/
  BusinessLine/
    ReportName/
      input/          # Dev input files (created automatically)
      output/         # Dev output files (created automatically)
      src/
        config.py     # Report configuration
        main.py       # Report entry point
        ...           # Other report files
```

## Environment Control

- **Development**: `REPORT_ENV=dev` or default
  - Uses local `input/` and `output/` directories
  - No emails sent (empty recipient lists)
  - Safe for testing

- **Production**: `REPORT_ENV=prod`
  - Uses network drive paths
  - Sends emails to real recipients
  - Used by scheduler

## Scheduling

Set the `SCHEDULE` in your config.py:
- `"daily"` - Runs every day
- `"weekly"` - Runs on Mondays
- `"monthly"` - Runs on 1st of month
- `"yearly"` - Runs on January 1st
- `"manual"` - Only runs when explicitly called

## Automation with Cron/Task Scheduler

Add to crontab or Windows Task Scheduler:

```bash
# Daily reports at 6 AM
0 6 * * * cd /path/to/repo && python scheduler.py daily

# Monthly reports at 7 AM on 1st of month
0 7 1 * * cd /path/to/repo && python scheduler.py monthly
```

## Benefits

- **Consistent**: Same pattern for all reports
- **Simple**: Minimal configuration needed
- **Safe**: Dev mode prevents accidental emails/overwrites
- **Flexible**: Easy to test individual reports or run in batches
- **Maintainable**: Clear separation of config and logic
