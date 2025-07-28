"""
Portfolio Key - Groups accounts by shared address OR ownership

Business Logic:
- Creates comprehensive customer relationship groupings
- Groups by EITHER shared address OR shared ownership
- Most comprehensive view of customer relationships
- Used as primary relationship identifier across business lines
- Maintains persistence across runs using historical key data
"""

import src.r360.core

def main():
    """Main execution for portfolio key generation"""
    print("Starting Portfolio Key Generation")
    df = src.r360.core.generate_portfolio_key()
    
    # Optional: Save to CSV for debugging
    from datetime import datetime
    from pathlib import Path
    
    curr_date = datetime.now().strftime('%Y%m%d')
    output_path = Path('./output') / f"r360_portfolio_{curr_date}.csv"
    output_path.parent.mkdir(exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Portfolio key data saved to {output_path}")
    
    return df


if __name__ == '__main__':
    main()
    print("Portfolio Key Complete!")
