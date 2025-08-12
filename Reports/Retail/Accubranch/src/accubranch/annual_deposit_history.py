"""
Annual deposit history module for Accubranch project.

This module provides simple, black-box functionality to calculate deposit balances by branch
for deposit account types (Checking, Savings, Time Deposits) and create time series analysis.
"""

import pandas as pd
from typing import List


def calculate_deposit_balances_by_branch(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate total deposit balances by branch for deposit account types.
    
    Filters the dataframe to include only deposit account types (Checking, Savings, Time Deposits)
    and then groups by branch to sum the Net Balance amounts.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Account data containing at least the following columns:
        - 'mjaccttypcd': Major account type code
        - 'branchname': Branch name 
        - 'Net Balance': Net balance amount
        
    Returns:
    --------
    pd.DataFrame
        Summary dataframe with columns:
        - 'branchname': Branch name
        - 'total_deposit_balance': Total net balance for deposit accounts
        
    Example:
    --------
    >>> # Load account data
    >>> acct_df = pd.read_csv('assets/mock_data/acct_df.csv')
    >>> 
    >>> # Calculate deposit balances by branch
    >>> branch_deposits = calculate_deposit_balances_by_branch(acct_df)
    >>> 
    >>> # Display results
    >>> print(branch_deposits.sort_values('total_deposit_balance', ascending=False))
    """
    
    # Define deposit account types
    deposit_account_types = ['CK', 'SAV', 'TD']
    
    # Filter to deposit accounts only
    deposit_accounts = df[df['mjaccttypcd'].isin(deposit_account_types)].copy()
    
    # Group by branch and sum Net Balance
    branch_summary = deposit_accounts.groupby('branchname')['Net Balance'].sum().reset_index()
    
    # Rename the column for clarity
    branch_summary = branch_summary.rename(columns={'Net Balance': 'total_deposit_balance'})
    
    # Sort by total deposit balance descending
    branch_summary = branch_summary.sort_values('total_deposit_balance', ascending=False)
    
    return branch_summary


def create_time_series_analysis(
    dataframes: List[pd.DataFrame], 
    date_labels: List[str]
) -> pd.DataFrame:
    """
    Create a time series analysis by combining multiple dataframes side by side.
    
    Takes a list of dataframes and processes each one through calculate_deposit_balances_by_branch,
    then combines them into a time series view with branches as index and dates as columns.
    
    Parameters:
    -----------
    dataframes : List[pd.DataFrame]
        List of dataframes, each representing data for a specific date
    date_labels : List[str]
        List of date labels corresponding to each dataframe (e.g., ['2020-12-31', '2021-12-31'])
        
    Returns:
    --------
    pd.DataFrame
        Time series dataframe with:
        - Index: branch names
        - Columns: date labels
        - Values: total deposit balances for each branch on each date
        
    Raises:
    -------
    ValueError
        If dataframes and date_labels lists have different lengths
        If either list is empty
        
    Example:
    --------
    >>> # Create 5-year analysis
    >>> df_2020 = pd.read_csv('data_2020.csv')
    >>> df_2021 = pd.read_csv('data_2021.csv') 
    >>> df_2022 = pd.read_csv('data_2022.csv')
    >>> 
    >>> dataframes = [df_2020, df_2021, df_2022]
    >>> dates = ['2020-12-31', '2021-12-31', '2022-12-31']
    >>> 
    >>> time_series = create_time_series_analysis(dataframes, dates)
    >>> print(time_series)
    """
    
    # Precondition checks
    if not dataframes:
        raise ValueError("Dataframes list cannot be empty")
    
    if not date_labels:
        raise ValueError("Date labels list cannot be empty")
    
    if len(dataframes) != len(date_labels):
        raise ValueError(f"Number of dataframes ({len(dataframes)}) must match number of date labels ({len(date_labels)})")
    
    print(f"Creating time series analysis for {len(dataframes)} periods")
    
    # Dictionary to store results for each date
    branch_balances_by_date = {}
    
    # Process each dataframe
    for i, (df, date_label) in enumerate(zip(dataframes, date_labels)):
        print(f"Processing period {i+1}/{len(dataframes)}: {date_label}")
        
        try:
            # Calculate deposit balances by branch for this dataframe
            branch_deposits = calculate_deposit_balances_by_branch(df)

            # Enforce to upper case names
            branch_deposits['branchname'] = branch_deposits['branchname'].str.upper()
            
            # Store results with date label as key
            branch_balances_by_date[date_label] = branch_deposits.set_index('branchname')['total_deposit_balance']
            
            print(f"  - Found {len(branch_deposits)} branches")
            
        except Exception as e:
            print(f"  - Error processing {date_label}: {str(e)}")
            # Create empty series to maintain structure
            branch_balances_by_date[date_label] = pd.Series(dtype=float, name='total_deposit_balance')
    
    # Combine all dates into a single DataFrame
    time_series_df = pd.DataFrame(branch_balances_by_date)
    
    # Fill NaN values with 0 (branches that didn't exist on certain dates)
    time_series_df = time_series_df.fillna(0)
    
    # Sort by most recent total (last column) descending
    if len(time_series_df.columns) > 0:
        last_col = time_series_df.columns[-1]
        time_series_df = time_series_df.sort_values(last_col, ascending=False)
    
    print(f"\nTime series analysis complete:")
    print(f"- {len(time_series_df)} branches analyzed")
    print(f"- {len(time_series_df.columns)} time periods")
    
    return time_series_df


def analyze_branch_growth(time_series_df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze branch growth patterns from time series data.
    
    Parameters:
    -----------
    time_series_df : pd.DataFrame
        Time series dataframe from create_time_series_analysis
        
    Returns:
    --------
    pd.DataFrame
        Growth analysis with columns:
        - 'branch': Branch name
        - 'start_balance': Balance at first date
        - 'end_balance': Balance at last date
        - 'total_growth': Absolute growth (end - start)
        - 'growth_rate': Percentage growth rate
        - 'avg_balance': Average balance across all periods
        
    Example:
    --------
    >>> growth_analysis = analyze_branch_growth(time_series_df)
    >>> # Show branches with highest growth rates
    >>> print(growth_analysis.sort_values('growth_rate', ascending=False))
    """
    if len(time_series_df.columns) < 2:
        raise ValueError("Time series data must have at least 2 dates for growth analysis")
    
    # Get first and last columns (dates)
    first_date = time_series_df.columns[0]
    last_date = time_series_df.columns[-1]
    
    growth_df = pd.DataFrame({
        'branch': time_series_df.index,
        'start_balance': time_series_df[first_date],
        'end_balance': time_series_df[last_date],
    })
    
    # Calculate growth metrics
    growth_df['total_growth'] = growth_df['end_balance'] - growth_df['start_balance']
    
    # Calculate growth rate (handle division by zero)
    growth_df['growth_rate'] = growth_df.apply(
        lambda row: (row['total_growth'] / row['start_balance'] * 100) if row['start_balance'] > 0 else 0,
        axis=1
    )
    
    # Calculate average balance across all periods
    growth_df['avg_balance'] = time_series_df.mean(axis=1).values
    
    # Sort by growth rate descending
    growth_df = growth_df.sort_values('growth_rate', ascending=False)
    
    return growth_df


if __name__ == "__main__":
    # Simple testing
    import os
    
    def test_basic_functionality():
        """Test basic functionality with mock data."""
        print("=== Testing Basic Functionality ===")
        
        if not os.path.exists('assets/mock_data/acct_df.csv'):
            print("Mock data not found. Run 'python -m tests.utility' first.")
            return False
        
        # Load and prepare data
        acct_df = pd.read_csv('assets/mock_data/acct_df.csv')
        print(f"Loaded {len(acct_df)} accounts")
        
        # Add branch names if not present
        if 'branchname' not in acct_df.columns:
            print("Adding sample branch names...")
            import random
            random.seed(42)
            branches = ['Downtown', 'Westside', 'Corporate', 'North Branch', 'South Branch']
            acct_df['branchname'] = [random.choice(branches) for _ in range(len(acct_df))]
        
        # Test single dataframe analysis
        print("\n1. Testing single dataframe analysis...")
        try:
            branch_deposits = calculate_deposit_balances_by_branch(acct_df)
            print(f"✓ Found {len(branch_deposits)} branches")
            print(branch_deposits.head())
        except Exception as e:
            print(f"✗ Single dataframe test failed: {e}")
            return False
        
        return True
    
    def test_time_series_functionality():
        """Test time series functionality."""
        print("\n=== Testing Time Series Functionality ===")
        
        if not os.path.exists('assets/mock_data/acct_df.csv'):
            print("Mock data not available.")
            return False
        
        # Load and prepare data
        acct_df = pd.read_csv('assets/mock_data/acct_df.csv')
        
        # Add branch names if not present
        if 'branchname' not in acct_df.columns:
            import random
            random.seed(42)
            branches = ['Downtown', 'Westside', 'Corporate', 'North Branch', 'South Branch']
            acct_df['branchname'] = [random.choice(branches) for _ in range(len(acct_df))]
        
        # Create multiple dataframes by slightly modifying the data
        # (In real use, these would be different dates of data)
        df1 = acct_df.copy()
        df2 = acct_df.copy()
        df3 = acct_df.copy()
        
        # Simulate growth by increasing balances
        df2['Net Balance'] = df2['Net Balance'] * 1.05  # 5% growth
        df3['Net Balance'] = df3['Net Balance'] * 1.12  # 12% growth
        
        dataframes = [df1, df2, df3]
        date_labels = ['2022-12-31', '2023-12-31', '2024-12-31']
        
        # Test precondition checks
        print("\n1. Testing precondition checks...")
        try:
            # Test empty lists
            try:
                create_time_series_analysis([], [])
                print("✗ Should have raised ValueError for empty lists")
                return False
            except ValueError:
                print("✓ Empty lists check passed")
            
            # Test mismatched lengths
            try:
                create_time_series_analysis([df1], ['2022-12-31', '2023-12-31'])
                print("✗ Should have raised ValueError for mismatched lengths")
                return False
            except ValueError:
                print("✓ Mismatched lengths check passed")
                
        except Exception as e:
            print(f"✗ Precondition checks failed: {e}")
            return False
        
        # Test time series creation
        print("\n2. Testing time series creation...")
        try:
            time_series = create_time_series_analysis(dataframes, date_labels)
            print(f"✓ Time series created: {time_series.shape}")
            print("Sample data:")
            print(time_series.head())
            
            # Test growth analysis
            print("\n3. Testing growth analysis...")
            growth_analysis = analyze_branch_growth(time_series)
            print(f"✓ Growth analysis completed")
            print("Top 3 branches by growth:")
            print(growth_analysis.head(3)[['branch', 'start_balance', 'end_balance', 'growth_rate']].round(2))
            
            return True
            
        except Exception as e:
            print(f"✗ Time series test failed: {e}")
            return False
    
    def test_example_usage():
        """Show example of how to use for 5-year analysis."""
        print("\n=== Example: 5-Year Analysis Usage ===")
        
        print("Example code for 5-year analysis:")
        print("""
# Load your data for different years
df_2020 = load_data_for_date('2020-12-31')
df_2021 = load_data_for_date('2021-12-31') 
df_2022 = load_data_for_date('2022-12-31')
df_2023 = load_data_for_date('2023-12-31')
df_2024 = load_data_for_date('2024-12-31')

# Create time series analysis
dataframes = [df_2020, df_2021, df_2022, df_2023, df_2024]
dates = ['2020-12-31', '2021-12-31', '2022-12-31', '2023-12-31', '2024-12-31']

time_series = create_time_series_analysis(dataframes, dates)
print(time_series)

# Analyze growth
growth = analyze_branch_growth(time_series)
print(growth.head())
        """)
    
    # Run tests
    success = test_basic_functionality()
    if success:
        success = test_time_series_functionality()
    
    test_example_usage()
    
    print(f"\n{'='*50}")
    print(f"Testing {'PASSED' if success else 'FAILED'}")
