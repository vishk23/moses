import pandas as pd
from pathlib import Path
import shutil

def process_assets_excel():
    """
    This will take in 1 excel file in the assets and stage the data, moving it to archive later on

    It will raise an error if there is more than one excel file and will print moving on if there is nothing there
    """
    # Define paths
    assets_folder = Path("assets")
    archive_folder = assets_folder / "archive"
    staged_data_path = assets_folder / "staged_data" / "staged_data.csv"
    
    # Ensure directories exist
    assets_folder.mkdir(exist_ok=True)
    archive_folder.mkdir(exist_ok=True)
    
    # Find all .xlsx files in assets folder
    xlsx_files = list(assets_folder.glob("*.xlsx"))
    
    # Assert no more than 1 .xlsx file
    assert len(xlsx_files) <= 1, f"Found {len(xlsx_files)} .xlsx files in assets folder. Expected 0 or 1."
    
    # Check if there are any .xlsx files
    if len(xlsx_files) == 0:
        print("No .xlsx files found in assets folder. Moving on.")
        return
    
    # Process the single .xlsx file
    xlsx_file = xlsx_files[0]
    print(f"Processing file: {xlsx_file.name}")
    
    try:
        # Load the Excel file as a dataframe
        df = pd.read_excel(xlsx_file)
        print(f"Successfully loaded {xlsx_file.name} with {len(df)} rows and {len(df.columns)} columns")
        
        # Write to staged_data.csv (this will replace if it exists)
        df.to_csv(staged_data_path, index=False)
        print(f"Data written to {staged_data_path}")
        
        # Move the xlsx file to archive (replace if exists)
        archive_file_path = archive_folder / xlsx_file.name
        
        # If file already exists in archive, remove it first
        if archive_file_path.exists():
            archive_file_path.unlink()
            print(f"Replaced existing file in archive: {archive_file_path.name}")
        
        # Move the file
        shutil.move(str(xlsx_file), str(archive_file_path))
        print(f"Moved {xlsx_file.name} to archive folder")
        
    except Exception as e:
        print(f"Error processing {xlsx_file.name}: {str(e)}")
        raise