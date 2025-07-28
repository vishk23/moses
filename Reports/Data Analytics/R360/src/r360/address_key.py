"""
Address Key - Groups accounts by shared address only

Business Logic:
- Creates household-level groupings based on shared addresses
- Does NOT group by ownership relationships
- Useful for household analysis and geographic customer insights
- Excludes specific problematic addresses (IOLTA, 29 Broadway)
"""

import src.r360.core

def main():
    """Main execution for address key generation"""
    print("Starting Address Key Generation")
    df = src.r360.core.generate_address_key()
    
    # Optional: Save to CSV for debugging
    from datetime import datetime
    from pathlib import Path
    
    curr_date = datetime.now().strftime('%Y%m%d')
    output_path = Path('./output') / f"r360_address_{curr_date}.csv"
    output_path.parent.mkdir(exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Address key data saved to {output_path}")
    
    return df


if __name__ == '__main__':
    main()
    print("Address Key Complete!")
