"""
Ownership Key - Groups accounts by shared ownership only

Business Logic:
- Creates relationship groupings based on shared ownership (CIF matching)
- Does NOT group by address
- Useful for commercial lending concentration analysis
- Excludes IOLTA shared ownership entities (O500, O501)
"""

import src.r360.core

def main():
    """Main execution for ownership key generation"""
    print("Starting Ownership Key Generation")
    df = src.r360.core.generate_ownership_key()
    
    # Optional: Save to CSV for debugging
    from datetime import datetime
    from pathlib import Path
    
    curr_date = datetime.now().strftime('%Y%m%d')
    output_path = Path('./output') / f"r360_ownership_{curr_date}.csv"
    output_path.parent.mkdir(exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Ownership key data saved to {output_path}")
    
    return df


if __name__ == '__main__':
    main()
    print("Ownership Key Complete!")
