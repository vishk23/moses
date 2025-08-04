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


def create_summary_dataframes(df):
    """Create summary DataFrames for analysis."""
    print("Creating summary DataFrames...")
    
    # Summary 1: Machine count and patch score by device type
    summary1 = df.groupby('Device Type').agg({
        'Computer Name': 'nunique'
    }).rename(columns={'Computer Name': 'Total_Machines'})
    
    # Count out of compliance machines (machines with any compliance flag = 1)
    out_of_compliance = df[df['Compliance Flag'] == 1].groupby('Device Type')['Computer Name'].nunique().reindex(summary1.index, fill_value=0)
    summary1['Out_of_Compliance_Machines'] = out_of_compliance
    
    # Calculate patch score: 1 - (out of compliance / total)
    summary1['Patch_Score'] = 1 - (summary1['Out_of_Compliance_Machines'] / summary1['Total_Machines'])
    summary1 = summary1.reset_index()
    
    # Summary 2: Count of machines out of compliance by device type
    summary2 = df[df['Compliance Flag'] == 1].groupby('Device Type')['Computer Name'].nunique().reset_index()
    summary2.columns = ['Device Type', 'Out_of_Compliance_Machines']
    
    # Fill in device types that might have 0 out of compliance machines
    all_device_types = df['Device Type'].unique()
    summary2 = summary2.set_index('Device Type').reindex(all_device_types, fill_value=0).reset_index()
    
    # Summary 3: Machine count by device type and age category
    current_date = pd.Timestamp.now()
    
    # For each computer, find the oldest missing patch (most out of date)
    missing_patches = df[df['Patch Status'] == 'Missing'].copy()
    oldest_patch_per_computer = missing_patches.groupby(['Computer Name', 'Device Type'])['Release Date'].min().reset_index()
    
    # Calculate age categories
    oldest_patch_per_computer['Days_Old'] = (current_date - oldest_patch_per_computer['Release Date']).dt.days
    oldest_patch_per_computer['Age_Category'] = pd.cut(
        oldest_patch_per_computer['Days_Old'],
        bins=[0, 30, 90, float('inf')],
        labels=['<30 days', '30-90 days', '>90 days'],
        include_lowest=True
    )
    
    # Count unique computers by device type and age category
    summary3 = oldest_patch_per_computer.groupby(['Device Type', 'Age_Category'])['Computer Name'].nunique().reset_index()
    summary3.columns = ['Device Type', 'Age_Category', 'Machine_Count']
    
    # Pivot to get age categories as columns
    summary3 = summary3.pivot(index='Device Type', columns='Age_Category', values='Machine_Count').fillna(0).reset_index()
    
    print(f"Summary 1 shape: {summary1.shape}")
    print(f"Summary 2 shape: {summary2.shape}")
    print(f"Summary 3 shape: {summary3.shape}")
    
    return summary1, summary2, summary3


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
    
    # Create summary DataFrames
    summary1, summary2, summary3 = create_summary_dataframes(df_processed)
    
    # Archive existing output files
    archive_output_files()
    
    # Write processed data to output
    output_file = config.OUTPUT_DIR / "patch_data.csv"
    df_processed.to_csv(output_file, index=False)
    print(f"Written processed data to: {output_file}")
    
    # Write summary files
    summary1_file = config.OUTPUT_DIR / "summary1.csv"
    summary1.to_csv(summary1_file, index=False)
    print(f"Written summary1 (machine count and patch score) to: {summary1_file}")
    
    summary2_file = config.OUTPUT_DIR / "summary2.csv"
    summary2.to_csv(summary2_file, index=False)
    print(f"Written summary2 (out of compliance count) to: {summary2_file}")
    
    summary3_file = config.OUTPUT_DIR / "summary3.csv"
    summary3.to_csv(summary3_file, index=False)
    print(f"Written summary3 (age category breakdown) to: {summary3_file}")
    
    print("Patch Dashboard processing complete.")
    print(f"Final data shape: {df_processed.shape}")
    print(f"Summary 1 preview:\n{summary1}")
    print(f"Summary 2 preview:\n{summary2}")
    print(f"Summary 3 preview:\n{summary3}")


if __name__ == "__main__":
    main()
