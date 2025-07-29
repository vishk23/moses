# Data Quality ETL Pipeline - Organization & Person Data Consolidation

A comprehensive ETL pipeline for cleaning and consolidating customer data from WH_PERS (person) and WH_ORG (organization) tables, generating unified snapshots of customer records linked to active accounts.

## 🏗️ Project Structure

```
data_quality/
├── data/                           # Data directories with placeholder files
│   ├── inputs/                     # Drop zone for Excel files to process
│   │   ├── org/                    # Organization files with additional notes
│   │   │   ├── README.md           # Instructions for org input files
│   │   │   └── SAMPLE_FORMAT.txt   # Example format (delete before use)
│   │   └── pers/                   # Person files with additional notes
│   │       ├── README.md           # Instructions for person input files
│   │       └── SAMPLE_FORMAT.txt   # Example format (delete before use)
│   ├── archive/                    # Processed files automatically moved here
│   │   └── README.md               # Archive folder documentation
│   └── README.md                   # Data directory overview
├── outputs/                        # Generated reports and processed data
│   └── README.md                   # Outputs documentation
├── notebooks/                      # Jupyter notebooks for analysis
│   └── code.ipynb                  # Development and exploration notebook
├── src/                           # Core processing logic
│   ├── main.py                     # CLI entry point
│   └── data_quality/
│       ├── __init__.py
│       └── core.py                 # ETL functions
├── tests/                         # Comprehensive test suite
│   ├── test_core.py               # 50+ tests for all functions
│   └── test_dtype_fixes.py        # Robust dtype conversion testing
├── docs/                          # Documentation
│   ├── data_sources.md            # Database schema and table definitions
│   └── NOTES.md                   # Development notes
├── .github/                       # GitHub configuration
│   └── copilot-instructions.md    # AI agent guidance
├── pyproject.toml                 # Project configuration & dependencies
├── uv.lock                        # Dependency lock file
└── README.md                      # This file
```

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone <repository-url>
cd data_quality
uv sync                           # Install dependencies
```

### 2. Ready-to-Use Structure
The repository includes placeholder files in all data directories:
- `data/inputs/org/` - Ready for organization Excel files
- `data/inputs/pers/` - Ready for person Excel files  
- `data/archive/` - Auto-populated after processing
- `outputs/` - Auto-populated with results

### 3. Process Input Files (Optional)
```bash
# Drop Excel files in data/inputs/org/ or data/inputs/pers/
# Then run:
./.venv/bin/python -m src.main
```

### 4. Run Tests
```bash
./.venv/bin/python -m pytest tests/ -v
```

## 📂 Data Processing Workflow

1. **Input Files**: Drop Excel files in `data/inputs/org/` or `data/inputs/pers/`
2. **Processing**: Run pipeline to merge with your processed data  
3. **Auto-Archive**: Input files automatically moved to `data/archive/`
4. **Results**: Final datasets saved to `outputs/` with timestamps

## 📋 Input File Requirements

### Organization Files (`data/inputs/org/`)
- Excel format (.xlsx or .xls)
- **Required**: `ORGNBR` column (uppercase)
- **Additional**: Any extra columns (NOTES, CONTACT_PERSON, etc.)
- One file at a time

### Person Files (`data/inputs/pers/`)
- Excel format (.xlsx or .xls) 
- **Required**: `PERSNBR` column (uppercase)
- **Additional**: Any extra columns (COMMENTS, PRIORITY, etc.)
- One file at a time

## 🔧 Core Functions

Located in `src/data_quality/core.py`:

- `create_org_table_with_address()` - Merges WH_ORG → ORGADDRUSE → WH_ADDR
- `create_pers_table_with_address()` - Merges WH_PERS → PERSADDRUSE → WH_ADDR  
- `filter_to_active_accounts()` - Filters to customers with active accounts
- `merge_with_input_file()` - Merges processed data with input Excel files
- `archive_input_file()` - Auto-archives processed files with original names

## 🧪 Testing

### Comprehensive Test Suite
Located in `tests/` with 50+ tests covering all functionality:

**Core ETL Tests** (`test_core.py`):
- ✅ Happy path scenarios
- ✅ Edge cases and error conditions  
- ✅ Field filtering and validation
- ✅ Input file processing and archiving
- ✅ Path object support

**Robust Dtype Conversion Tests** (`test_dtype_fixes.py`):
- ✅ **Mixed dtype scenarios**: int64 ↔ float64 ↔ object conversions
- ✅ **Decimal handling**: 1.7 → "1", 123.0 → "123" 
- ✅ **NaN preservation**: Nullable integers and missing values
- ✅ **Large numbers**: 999,999,999,999+ values
- ✅ **Edge cases**: Empty DataFrames, special characters
- ✅ **Input file merging**: All dtype combinations work seamlessly

### Running Tests
```bash
# Run all tests
uv run pytest tests/ -v

# Run specific test categories
uv run pytest tests/test_core.py -v                    # Core ETL functionality
uv run pytest tests/test_dtype_fixes.py -v             # Dtype conversion robustness

# Run comprehensive dtype testing standalone
./.venv/bin/python tests/test_dtype_fixes.py           # Full test report with summary
```

The dtype conversion fixes ensure your ETL pipeline handles real-world database inconsistencies where:
- Organization IDs might be `int64` in one table, `float64` in another
- Account numbers could be stored as strings `"1001"` or floats `1001.0`  
- Missing values create nullable integer types that break standard joins

**Result**: Zero failed joins due to dtype mismatches! 🎉

## 📚 Documentation

- **Database Schema**: See `docs/data_sources.md` for complete table definitions
- **AI Instructions**: See `.github/copilot-instructions.md` for development patterns
- **Development Notes**: See `docs/NOTES.md` for workflow details

## 🎯 Next Steps

1. **Implement Database Functions**:
   - `create_acct_df()` - Active accounts snapshot
   - `load_database_tables()` - Database connectivity

2. **Production Deployment**:
   - Configure database connections
   - Test with real data
   - Schedule automated runs

## 🛠️ Technology Stack

- **Python 3.12+** with uv dependency management
- **pandas** for data manipulation
- **pytest** for testing
- **openpyxl** for Excel file handling
- **VS Code** with Jupyter notebook support
