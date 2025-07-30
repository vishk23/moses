# Daily Deposit Update Project

This project follows the standard template for BCSB analytics/reporting projects.

## Structure

```
Daily Deposit Update/
├── docs/                # Documentation, notes, and guides for the project
├── notebooks/           # Jupyter notebooks for exploration or prototyping
├── src/                 # Source code for the project
│   ├── config.py        # Project configuration (edit this first!)
│   └── main.py          # Main entry point for the project (python -m src.main)
└── README.md            # This file (project structure and instructions)
```

## How to Use

1. **Edit `src/config.py`** to fill in your project-specific details (name, business line, schedule, owner, paths, etc).
2. **Write your main logic in `src/main.py`**. This file should be executable as a module:  
   `python -m src.main`
3. **Add any supporting modules** to the `src/` folder as needed.
4. **Document your project** in the `docs/` folder and keep notes up to date.
5. **Use the `notebooks/` folder** for prototyping, data exploration, or sharing examples.

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
