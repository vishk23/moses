# CT Dashboard (Covenant & Ticklers)

## Project Overview

## Authors & Stakeholders
- **Project Lead:** 
- **Executive Sponsor:** 
- **Key Stakeholders:**

## Project Goals

## Technology Stack

## Project Status
- [ ] Description of tasks (YYYY-MM-DD)
   - Short description 

Key
- [x] - Completed
- [-] - Partially completed 
- [ ] - TODO

## File Paths

## Documentation

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
│   ├── config.py           # Project configuration (edit this first!)
│   ├── main.py             # Main entry point for the project (python -m src.main)
│   └── project_name/       # Project-specific logic (replace with your project name)
│       ├── __init__.py     # Makes project_name a package
│       ├── core.py         # Business logic for the report (all processing, transformation, output)
│       └── fetch_data.py   # SQL/data fetching logic (all queries and data retrieval)
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
   - Print key config values for logging
   - Import and call your business logic from `src/project_name/core.py`
   - Handle output file creation and email distribution
   - Be executable as a module: `python -m src.main`
4. **Add any supporting modules** to the `src/project_name/` folder as needed (e.g., output formatting, validation).
5. **Document your project** in the `docs/` folder and keep notes up to date.
6. **Use the `notebooks/` folder** for prototyping, data exploration, or sharing examples.

### Execution

- The runner will change directory into the project root and execute:
  ```
  python -m src.main
  ```
- Make sure all imports are relative to the `src/` folder and configuration is handled via `config.py`.
- The `src/__init__.py` and `src/project_name/__init__.py` files are required for Python package/module resolution.

### Best Practices

- Keep all project-specific settings in `config.py`.
- Avoid hardcoding paths or credentials in code files.
- Use the `OUTPUT_DIR` and `INPUT_DIR` variables for file operations.
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
```

**Schedule:** Daily automated execution (or as specified in config.py)

---

This template is designed to be a clean, robust, and reusable starting point for any new analytics, reporting, or ETL project in the BCSB monorepo system. Follow the structure and conventions for seamless integration and maintainability.

