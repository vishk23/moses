# Data Directory Structure

This directory contains all data-related folders for the ETL pipeline.

## Directory Structure:
```
data/
├── inputs/          # Drop zone for Excel files to be processed
│   ├── org/         # Organization files with additional notes
│   └── pers/        # Person files with additional notes
└── archive/         # Processed files are moved here automatically
```

## Workflow:
1. **Drop files**: Place Excel files in `inputs/org/` or `inputs/pers/`
2. **Run pipeline**: Execute `python -m src.main`
3. **Auto-archive**: Processed files automatically moved to `archive/`
4. **Check outputs**: Final results saved to `outputs/` directory

## File Requirements:
- Excel format (.xlsx or .xls)
- Uppercase column headers
- Join keys: ORGNBR (org files) or PERSNBR (person files)
- Only one Excel file per folder at a time
