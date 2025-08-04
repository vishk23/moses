# Patch Dashboard Technical Documentation

## Overview
The Patch Dashboard pipeline automates the ingestion, processing, and aggregation of raw patch management data from ManageEngine, producing a clean dataset for PowerBI dashboarding and IT reporting.

---

## Pipeline Flow

1. **Input Data Acquisition**
    - Raw patch data is exported from ManageEngine as a CSV file and placed in the input directory (`INPUT_DIR`).
    - The pipeline expects exactly one CSV file per run.

2. **Directory Setup**
    - The script ensures all required directories exist, including input, output, and archive folders.

3. **Data Loading & Archiving**
    - The input CSV is loaded into a pandas DataFrame.
    - After loading, the input file is moved to the input archive folder for record-keeping.

4. **Data Processing**
    - Device type is calculated: If `Remote Office` is 'Domain Controllers' or 'Member Servers', the device is classified as 'Server'; otherwise, 'Workstation'.
    - Date fields (`Deployed Date`, `Release Date`) are converted to datetime objects.
    - Compliance flag is calculated: If a patch is missing and its release date is more than 30 days old, the flag is set to 1 (out of compliance); otherwise, 0 (compliant).

5. **Output Generation**
    - The processed DataFrame is written to `patch_data.csv` in the output directory (`OUTPUT_DIR`).
    - Previous output files are archived before writing new results.

---

## Main Processing Steps

- **Device Type Calculation**
    ```python
    df['Device Type'] = np.where(
        df['Remote Office'].isin(['Domain Controllers', 'Member Servers']),
        'Server',
        'Workstation'
    )
    ```
- **Date Conversion**
    ```python
    for col in ['Deployed Date', 'Release Date']:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    ```
- **Compliance Flag**
    ```python
    df['Compliance Flag'] = np.where(
        (df['Release Date'] < thirty_days_ago) & (df['Patch Status'] == 'Missing'),
        1,
        0
    )
    ```

---

## Output Files
- `patch_data.csv`: Cleaned and processed patch data for PowerBI dashboarding.
- Archived input and output files for traceability.

---

## Execution Instructions

1. Place the raw ManageEngine CSV file in the input directory.
2. Run the main script:
    ```bash
    python -m src.main
    ```
3. The processed output will be available in the output directory.

---

## Configuration
- All project-specific settings (paths, environment, business line, etc.) are managed in `src/config.py`.
- Avoid hardcoding paths or credentials in code files.

---

## Best Practices
- Archive all input and output files for audit and traceability.
- Keep documentation and notebooks organized in the `docs/` and `notebooks/` folders.
- Use version control for all code and documentation.

---

## Contact
- For technical questions, contact the Project Lead or refer to the README for stakeholders.
