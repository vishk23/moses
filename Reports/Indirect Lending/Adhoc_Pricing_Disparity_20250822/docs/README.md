# Adhoc Request - Indirect Pricing Disparity Remediation

## Project Overview
See attached internal report request from Compliance officer

## Authors & Stakeholders
- **Project Lead:** Chad Doorley
- **Executive Sponsor:** 
- **Key Stakeholders:** Terry Janiero

## Project Goals
Provide accurate reporting of indirect loans from 2020-2024 to meet business/FDIC need.

## Technology Stack
- SQL
- Python

## Project Status
- [x] Set up repository (2025-08-22)
- [ ] Build report
   - Requested completion by 2025-08-27

Key
- [x] - Completed
- [-] - Partially completed 
- [ ] - TODO

## File Paths
- `src/main.py` — Main entry point for the project (python -m src.main)
- `src/config.py` — Project configuration and environment settings
- `src/_version.py` — Version information for the project
- `src/project_name/core.py` — Business logic and data processing
- `src/project_name/fetch_data.py` — Data retrieval and SQL queries
- `tests/test_*.py` — Unit tests using pytest framework
- `docs/README.md` — Project documentation and usage guide
- `notebooks/` — Jupyter notebooks for exploration and prototyping

## Documentation
- This README: project overview, business logic, and usage guide
- Inline code documentation for complex business rules and data transformations
- Unit tests in `tests/` folder provide examples of function usage and expected behavior

---

# Template Project Structure & Usage Guide

This folder provides a starter template for new report or data pipeline projects. Copy this folder and use it as a base for new work.

### Structure
```
project_name/
├── docs/                   # Documentation, notes, and guides for the project
│   └── README.md           # This file (project structure, business logic, usage guide)
├── notebooks/              # Jupyter notebooks for exploration or prototyping
├── src/                    # Source code for the project
│   ├── __init__.py         # Makes src a Python package (required for python -m src.main)
│   ├── _version.py         # Version information for the project
│   ├── config.py           # Project configuration (edit this first!)
│   ├── main.py             # Main entry point for the project (python -m src.main)
│   └── project_name/       # Project-specific logic (replace with your project name)
│       ├── __init__.py     # Makes project_name a package
│       ├── core.py         # Business logic for the report (all processing, transformation, output)
│       └── fetch_data.py   # SQL/data fetching logic (all queries and data retrieval)
└── tests/                  # Unit tests using pytest
    └── test_*.py           # Test files (import from ../src using pathlib)
```

### How to Use

1. **Copy the entire `template_project` folder** to your new project location and rename as needed.
2. **Edit `src/config.py`** to fill in your project-specific details (name, business line, schedule, owner, paths, etc). This file should:
   - Define all project metadata (REPORT_NAME, BUSINESS_LINE, SCHEDULE, OWNER)
   - Set up environment-aware paths (dev/prod) using `os.getenv('REPORT_ENV', 'dev')`
   - Create `OUTPUT_DIR` and `INPUT_DIR` using pathlib
   - Specify email recipients for production and development
   - Be the only place for configuration and environment logic
3. **Write your main logic in `src/main.py`**. This file should:
   - Import `src.config` for all configuration
   - Import `src._version` and print version information for logging
   - Print key config values for logging
   - Import and call your business logic from `src/project_name/core.py`
   - Handle output file creation and email distribution
   - Be executable as a module: `python -m src.main`
4. **Update version information in `src/_version.py`** as you develop and release new versions.
5. **Add any supporting modules** to the `src/project_name/` folder as needed (e.g., output formatting, validation).
6. **Write unit tests** in the `tests/` folder using pytest. Tests should import from the source code using pathlib:
   ```python
   import sys
   from pathlib import Path
   
   # Add src to path for imports
   src_path = Path(__file__).parent.parent / "src"
   sys.path.insert(0, str(src_path))
   
   import your_module  # Now you can import from src/
   ```
7. **Document your project** in the `docs/` folder and keep notes up to date.
8. **Use the `notebooks/` folder** for prototyping, data exploration, or sharing examples.

### Execution

- The runner will change directory into the project root and execute:
  ```
  python -m src.main
  ```
- Make sure all imports are relative to the `src/` folder and configuration is handled via `config.py`.
- The `src/__init__.py` and `src/project_name/__init__.py` files are required for Python package/module resolution.

### Testing

- Run unit tests with pytest from the project root:
  ```
  pytest tests/
  ```
- Tests should be named `test_*.py` and use pytest conventions
- Import source code modules using pathlib to navigate from `tests/` to `src/`:
  ```python
  import sys
  from pathlib import Path
  src_path = Path(__file__).parent.parent / "src"
  sys.path.insert(0, str(src_path))
  ```

### Best Practices

- Keep all project-specific settings in `config.py`.
- Update version information in `_version.py` when making releases.
- Avoid hardcoding paths or credentials in code files.
- Use the `OUTPUT_DIR` and `INPUT_DIR` variables for file operations.
- Write comprehensive unit tests for all business logic functions.
- Keep documentation and notebooks organized for future reference.
- Place all business logic in `core.py` and all data fetching in `fetch_data.py`.
- Use environment variables for dev/prod switching and path management.
- Use the provided structure for easy integration with the monorepo and report runner system.

---

## Usage
```bash
# Navigate to project directory
cd Reports/YourBusinessLine/YourReportName

# Run the main process
python -m src.main

# Run unit tests
pytest tests/

# Run tests with verbose output
pytest tests/ -v
```

**Schedule:** Daily automated execution (or as specified in config.py)

---

This template is designed to be a clean, robust, and reusable starting point for any new analytics, reporting, or ETL project in the BCSB monorepo system. Follow the structure and conventions for seamless integration and maintainability.

