"""
Unit tests for New Loan Report LR Credit

Tests the main functionality of the report including data fetching,
processing, and output generation.
"""

import sys
from pathlib import Path
import pandas as pd
import pytest
from unittest.mock import Mock, patch

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

import src.config
from src.new_loan_credit_lr import core, fetch_data


class TestCore:
    """Test the core business logic functions"""
    
    def test_filter_acctcommon(self):
        """Test the acctcommon filtering function"""
        # Create sample data
        sample_data = pd.DataFrame({
            'mjaccttypcd': ['CML', 'CNS', 'MTG', 'OTHER'],
            'currmiaccttypcd': ['IL01', 'IL02', 'CI07', 'IL01'],
            'nameaddr1': ['123 Main St', '456 Oak Ave', '789 Pine St', '321 Elm St'],
            'nameaddr2': ['Apt 1', '', 'Suite 200', ''],
            'nameaddr3': ['', 'Unit B', '', '']
        })
        
        result = core.filter_acctcommon(sample_data)
        
        # Should filter out 'OTHER' and 'CI07'
        assert len(result) == 2
        assert 'OTHER' not in result['mjaccttypcd'].values
        assert 'CI07' not in result['currmiaccttypcd'].values
        
        # Should have primary_address column
        assert 'primary_address' in result.columns
        assert result.iloc[0]['primary_address'] == '123 Main StApt 1'
    
    def test_filter_wh_loans(self):
        """Test the wh_loans filtering function"""
        # Create sample data with dates
        from datetime import datetime, timedelta
        
        today = datetime.now()
        old_date = today - timedelta(days=60)
        recent_date = today - timedelta(days=30)
        
        sample_data = pd.DataFrame({
            'acctnbr': ['12345', '67890', '11111'],
            'origdate': [old_date, recent_date, today],
            'notebal': [100000, 250000, 50000]
        })
        
        result = core.filter_wh_loans(sample_data)
        
        # Should only include loans from last 45 days
        assert len(result) == 2  # recent_date and today
        assert old_date not in result['origdate'].values
    
    def test_combine_property_data(self):
        """Test property data combination"""
        prop1 = pd.DataFrame({
            'acctnbr': ['12345', '67890'],
            'aprsvalueamt': [500000, 750000]
        })
        
        prop2 = pd.DataFrame({
            'acctnbr': ['12345', '11111'],
            'aprsvalueamt': [600000, 400000]
        })
        
        result = core.combine_property_data(prop1, prop2)
        
        # Should combine both datasets
        assert len(result) >= 2
        assert '12345' in result['acctnbr'].values
        assert '67890' in result['acctnbr'].values
        assert '11111' in result['acctnbr'].values


class TestFetchData:
    """Test the data fetching functions"""
    
    @patch('cdutils.database.connect.retrieve_data')
    def test_fetch_data(self, mock_retrieve):
        """Test the main fetch_data function"""
        # Mock the database response
        mock_retrieve.return_value = {
            'wh_acctcommon': pd.DataFrame({'acctnbr': ['12345']}),
            'wh_loans': pd.DataFrame({'acctnbr': ['12345']}),
            'wh_acctloan': pd.DataFrame({'acctnbr': ['12345']}),
            'wh_org': pd.DataFrame({'orgnbr': ['12345']}),
            'wh_prop': pd.DataFrame({'acctnbr': ['12345']}),
            'wh_prop2': pd.DataFrame({'acctnbr': ['12345']}),
            'househldacct': pd.DataFrame({'acctnbr': ['12345']})
        }
        
        result = fetch_data.fetch_data()
        
        # Verify all expected tables are returned
        expected_tables = ['wh_acctcommon', 'wh_loans', 'wh_acctloan', 
                          'wh_org', 'wh_prop', 'wh_prop2', 'househldacct']
        
        for table in expected_tables:
            assert table in result
            assert isinstance(result[table], pd.DataFrame)
        
        # Verify the database function was called
        mock_retrieve.assert_called_once()


class TestMainPipeline:
    """Test the main data pipeline"""
    
    def test_main_pipeline_structure(self):
        """Test that main_pipeline returns correct structure"""
        # Create mock data
        mock_data = {
            'wh_acctcommon': pd.DataFrame({
                'acctnbr': ['12345', '67890'],
                'mjaccttypcd': ['CML', 'MTG'],
                'currmiaccttypcd': ['IL01', 'IL02'],
                'nameaddr1': ['123 Main', '456 Oak'],
                'nameaddr2': ['', ''],
                'nameaddr3': ['', ''],
                'ownersortname': ['John Doe', 'Jane Smith'],
                'noteopenamt': [100000, 250000],
                'taxrptfororgnbr': ['ORG001', 'ORG002']
            }),
            'wh_loans': pd.DataFrame({
                'acctnbr': ['12345', '67890'],
                'origdate': [pd.Timestamp.now() - pd.Timedelta(days=30), 
                           pd.Timestamp.now() - pd.Timedelta(days=20)],
                'fdiccatdesc': ['Commercial', 'Residential']
            }),
            'wh_acctloan': pd.DataFrame({
                'acctnbr': ['12345', '67890'],
                'creditlimitamt': [150000, 300000]
            }),
            'wh_org': pd.DataFrame({
                'orgnbr': ['ORG001', 'ORG002'],
                'orgname': ['ABC Corp', 'XYZ Inc']
            }),
            'wh_prop': pd.DataFrame({
                'acctnbr': ['12345'],
                'aprsvalueamt': [500000]
            }),
            'wh_prop2': pd.DataFrame({
                'acctnbr': ['67890'],
                'aprsvalueamt': [750000]
            }),
            'househldacct': pd.DataFrame({
                'acctnbr': ['12345', '67890'],
                'householdnbr': ['HH001', 'HH002']
            })
        }
        
        with patch('cdutils.pkey_sqlite.create_sqlite_engine'), \
             patch('cdutils.pkey_sqlite.query_current_db') as mock_pkey:
            
            # Mock pkey data
            mock_pkey.return_value = pd.DataFrame({
                'acctnbr': ['12345', '67890'],
                'pkey': ['PK001', 'PK002']
            })
            
            new_loan_page, cra_page = core.main_pipeline(mock_data)
            
            # Verify return types
            assert isinstance(new_loan_page, pd.DataFrame)
            assert isinstance(cra_page, pd.DataFrame)
            
            # Verify data is not empty (should have filtered loan data)
            assert len(new_loan_page) > 0
            assert len(cra_page) > 0


class TestConfiguration:
    """Test the configuration settings"""
    
    def test_config_values(self):
        """Test that configuration values are set correctly"""
        assert src.config.REPORT_NAME == "New Loan Report LR Credit"
        assert src.config.BUSINESS_LINE == "Credit Loan Review"
        assert src.config.SCHEDULE == "Weekly"
        assert src.config.OWNER == "Chad Doorley"
        assert src.config.PROD_READY == True
        
        # Test email lists are not empty
        assert len(src.config.EMAIL_TO) > 0
        assert len(src.config.EMAIL_CC) > 0


if __name__ == "__main__":
    pytest.main([__file__])
