"""
Patch Dashboard Main Entry Point

This script loads raw patch data from ManageEngine, cleans and aggregates it, and outputs results for PowerBI dashboarding.
"""
import pandas as pd
import numpy as np
from pathlib import Path
import shutil
import glob
import src.config as config
import src._version


def ensure_directories():
    """Ensure all required directories exist."""
    config.INPUT_DIR.mkdir(parents=True, exist_ok=True)
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (config.INPUT_DIR / "archive").mkdir(parents=True, exist_ok=True)
    (config.OUTPUT_DIR / "archive").mkdir(parents=True, exist_ok=True)


def load_and_archive_input():
    """Load the single CSV file from input directory and move it to archive."""
    # Find all CSV files in input directory
    csv_files = list(config.INPUT_DIR.glob("*.csv"))
    
    # Assert only one CSV file exists
    assert len(csv_files) == 1, f"Expected exactly 1 CSV file in input directory, found {len(csv_files)}: {csv_files}"
    
    input_file = csv_files[0]
    print(f"Loading file: {input_file}")
    
    # Load the data
    df = pd.read_csv(input_file)
    
    # Move file to archive (overwrite if exists)
    archive_path = config.INPUT_DIR / "archive" / input_file.name
    shutil.move(str(input_file), str(archive_path))
    print(f"Moved input file to: {archive_path}")
    
    return df


def process_patch_data(df):
    """Process and clean the patch data."""
    print("Processing patch data...")
    
    # Create Device Type calculated field
    df['Device Type'] = np.where(
        df['Remote Office'].isin(['Domain Controllers', 'Member Servers']),
        'Server',
        'Workstation'
    )
    
    # Convert date fields to datetime
    date_columns = ['Deployed Date', 'Release Date']
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            print(f"Converted {col} to datetime")
    
    # Create Compliance Flag calculated field
    current_date = pd.Timestamp.now()
    thirty_days_ago = current_date - pd.Timedelta(days=30)
    
    df['Compliance Flag'] = np.where(
        (df['Release Date'] < thirty_days_ago) & (df['Patch Status'] == 'Missing'),
        1,  # Fail - release date is more than 30 days old AND patch is missing
        0   # Pass - otherwise
    )
    
    print(f"Added Device Type and Compliance Flag fields. Data shape: {df.shape}")
    print(f"Device Type distribution:\n{df['Device Type'].value_counts()}")
    print(f"Compliance Flag distribution:\n{df['Compliance Flag'].value_counts()}")
    
    return df


def archive_output_files():
    """Move all existing files in output directory to archive."""
    output_files = [f for f in config.OUTPUT_DIR.iterdir() if f.is_file()]
    
    if output_files:
        print(f"Archiving {len(output_files)} existing output files...")
        for file_path in output_files:
            archive_path = config.OUTPUT_DIR / "archive" / file_path.name
            shutil.move(str(file_path), str(archive_path))
            print(f"Moved {file_path.name} to archive")
    else:
        print("No existing output files to archive")


def main():
    """Main processing function."""
    print(f"Running {src._version.__version__}")
    print(f"Patch Dashboard - Environment: {config.ENV}")
    print(f"Business Line: {config.BUSINESS_LINE}")
    print(f"Input directory: {config.INPUT_DIR}")
    print(f"Output directory: {config.OUTPUT_DIR}")
    
    # Ensure all directories exist
    ensure_directories()
    
    # Load input data and move to archive
    df = load_and_archive_input()
    
    # Process the data
    df_processed = process_patch_data(df)
    
    # Archive existing output files
    archive_output_files()
    
    # Write processed data to output
    output_file = config.OUTPUT_DIR / "patch_data.csv"
    df_processed.to_csv(output_file, index=False)
    print(f"Written processed data to: {output_file}")
    
    print("Patch Dashboard processing complete.")
    print(f"Final data shape: {df_processed.shape}")


if __name__ == "__main__":
    main()
