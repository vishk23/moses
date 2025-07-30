# Template Project Structure

This folder provides a starter template for new report or data pipeline projects. Copy this folder and use it as a base for new work.

## Structure

```
template_project/
├── docs/                # Documentation, notes, and guides for the project
├── notebooks/           # Jupyter notebooks for exploration or prototyping
├── src/                 # Source code for the project
│   ├── config.py        # Project configuration (edit this first!)
│   └── main.py          # Main entry point for the project (python -m src.main)
└── README.md            # This file (project structure and instructions)
```

## How to Use

1. **Copy the entire `template_project` folder** to your new project location and rename as needed.
2. **Edit `src/config.py`** to fill in your project-specific details (name, business line, schedule, owner, paths, etc).
3. **Write your main logic in `src/main.py`**. This file should be executable as a module:  
   `python -m src.main`
4. **Add any supporting modules** to the `src/` folder as needed.
5. **Document your project** in the `docs/` folder and keep notes up to date.
6. **Use the `notebooks/` folder** for prototyping, data exploration, or sharing examples.

## Execution

- The runner will change directory into the project root and execute:
  ```
  python -m src.main
  ```
- Make sure all imports are relative to the `src/` folder and configuration is handled via `config.py`.

## Best Practices

- Keep all project-specific settings in `config.py`.
- Avoid hardcoding paths or credentials in code files.
- Use the `OUTPUT_DIR` and `INPUT_DIR` variables for file operations.
- Keep documentation and notebooks organized for future reference.

---

This template is designed to be a clean, reusable starting point for any new analytics, reporting, or ETL project.
