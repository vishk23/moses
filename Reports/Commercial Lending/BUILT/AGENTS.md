# Agent Guidelines for BCSB BUILT Extract Project

## Build/Lint/Test Commands

### Testing
- **Run all tests**: `python -m pytest testing/test_reports.py -v`
- **Run single test**: `python -m pytest testing/test_reports.py -k "report_name" -v`
- **Run tests for this specific report**: `python -m pytest tests/ -v`
- **Run test runner for all reports**: `python testing/run_tests.py`
- **Run test runner for this report**: `python testing/run_tests.py "BUILT"`

### Execution
- **Run main script**: `python -m src.main`
- **Run with dev environment**: `REPORT_ENV=dev python -m src.main`

### Linting/Formatting
- No specific linting tools configured
- Code follows PEP 8 conventions
- Use type hints where appropriate

## Code Style Guidelines

### Imports
- Standard library imports first
- Third-party imports second (pandas, pathlib, etc.)
- Local imports last (src.*, cdutils.*)
- Use absolute imports within the project
- Group imports with blank lines between groups

### Naming Conventions
- **Functions/Methods**: snake_case (e.g., `generate_built_extract`, `add_asset_class`)
- **Variables**: snake_case (e.g., `acctnbr`, `merged_investor`)
- **Constants**: UPPER_CASE (e.g., `REPORT_NAME`, `BUSINESS_LINE`)
- **Classes**: PascalCase (if any)
- **Files**: snake_case with underscores (e.g., `core.py`, `fetch_data.py`)

### Code Structure
- Use pathlib.Path for all file/path operations
- Functions should have docstrings explaining purpose and parameters
- Use type hints for function parameters and return values
- Prefer functional programming style with pandas operations
- Use assert statements for data validation and business logic checks

### Data Handling
- Use pandas for data manipulation
- Cast columns to appropriate types using `cdutils.input_cleansing.cast_columns`
- Handle missing data with `.fillna()`, `.dropna()`, or conditional logic
- Use `.copy()` when creating new DataFrames to avoid SettingWithCopyWarning
- Validate data integrity with assert statements

### Error Handling
- Use try/except blocks for external operations (file I/O, database connections)
- Use assert statements for business logic validation
- Log important operations and errors
- Fail fast on data integrity issues

### Documentation
- Add docstrings to all functions explaining their purpose
- Include parameter descriptions and return value information
- Document complex business logic inline with comments
- Keep project notes in `docs/project-notes.md`

### File Organization
- `src/main.py`: Entry point, configuration printing, and orchestration
- `src/config.py`: All configuration variables and environment logic
- `src/core.py`: Business logic and data transformations
- `src/fetch_data.py`: Data retrieval and SQL queries
- `tests/test_*.py`: Unit tests using pytest framework
- `docs/`: Documentation and project notes
- `notebooks/`: Exploratory analysis and prototyping

### Dependencies
- Use existing libraries already imported in the project
- Check `cdutils` package for utility functions before implementing new ones
- Avoid adding new dependencies without approval

### Version Control
- Update `_version.py` when making releases
- Commit working code only
- Use descriptive commit messages following project conventions