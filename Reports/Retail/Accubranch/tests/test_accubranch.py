"""
Test file for Accubranch functionality.

This module contains unit tests for the Accubranch project core functionality.
"""

import sys
import os
from pathlib import Path
import pytest
import pandas as pd
from datetime import datetime

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

import src.config as config
import src.accubranch.core as accubranch_core


class TestAccubranchCore:
    """Test cases for accubranch core functionality."""
    
    def test_create_primary_key(self):
        """Test primary key creation functionality."""
        # Create test data
        test_df = pd.DataFrame({
            'taxrptfororgnbr': [None, 12345, None],
            'taxrptforpersnbr': [67890, None, 11111]
        })
        
        # Apply function
        result_df = accubranch_core.create_primary_key(test_df)
        
        # Check results
        assert 'Primary Key' in result_df.columns
        assert result_df.iloc[0]['Primary Key'] == 'P67890'
        assert result_df.iloc[1]['Primary Key'] == 'O12345'
        assert result_df.iloc[2]['Primary Key'] == 'P11111'
        
    def test_create_primary_key_missing_columns(self):
        """Test primary key creation when required columns are missing."""
        # Create test data without required columns
        test_df = pd.DataFrame({
            'other_column': [1, 2, 3]
        })
        
        # Apply function
        result_df = accubranch_core.create_primary_key(test_df)
        
        # Check that Primary Key column exists with default value
        assert 'Primary Key' in result_df.columns
        assert all(result_df['Primary Key'] == 'UNKNOWN')
    
    def test_map_account_type(self):
        """Test account type mapping functionality."""
        assert accubranch_core.map_account_type('CK') == 'Checking'
        assert accubranch_core.map_account_type('SAV') == 'Savings'
        assert accubranch_core.map_account_type('CML') == 'Commercial Loan'
        assert accubranch_core.map_account_type('UNKNOWN') == 'Other'
    
    def test_create_address_field(self):
        """Test address field creation functionality."""
        # Create test data
        test_df = pd.DataFrame({
            'text1': ['123 Main St', '456 Oak Ave', None],
            'text2': ['Apt 1', None, 'Suite 200'],
            'text3': [None, 'Building B', 'Floor 3']
        })
        
        # Apply function
        result_df = accubranch_core.create_address_field(test_df)
        
        # Check results
        assert 'Address' in result_df.columns
        assert result_df.iloc[0]['Address'] == '123 Main St Apt 1'
        assert result_df.iloc[1]['Address'] == '456 Oak Ave Building B'
        # Note: pandas.NA comparison should use pd.isna()
        assert pd.isna(result_df.iloc[2]['Address']) or result_df.iloc[2]['Address'] == 'Suite 200 Floor 3'


class TestConfig:
    """Test cases for configuration settings."""
    
    def test_config_values(self):
        """Test that essential config values are set."""
        assert config.REPORT_NAME == "Accubranch Analysis"
        assert config.BUSINESS_LINE == "Retail"
        assert len(config.ACCOUNT_TYPE_MAPPING) > 0
        assert len(config.HISTORICAL_YEARS) == 5
    
    def test_output_directory_exists(self):
        """Test that output directory exists."""
        assert config.OUTPUT_DIR.exists()
        assert config.OUTPUT_DIR.is_dir()


if __name__ == "__main__":
    pytest.main([__file__])
