from pathlib import Path

def cache_data(file_path, data):
    """
    Caching data tables for local development so a database call isn't necessary for every run
    """
    file_path = Path(file_path)
    file_path.mkdir(parents=True, exist_ok=True)

    for key, df in data.items():
        full_file_path = file_path / f"{key}.csv"
        df.to_csv(full_file_path, index=False)
        print(f"Saved {key} to {full_file_path}")