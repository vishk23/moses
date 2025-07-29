#!/usr/bin/env python3
"""
Test script to validate dtype conversion fixes in core.py functions.
Tests various edge cases and data type combinations that could cause join failures.
"""

import pandas as pd
import numpy as np
import pytest
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.data_quality.core import (
    create_org_table_with_address, 
    create_pers_table_with_address,
    filter_to_active_accounts
)

def test_float64_nan_conversion():
    """Test that NaN values in float64 columns are handled correctly during conversion"""
    
    # Create test data with NaN values
    wh_org = pd.DataFrame({
        'orgnbr': [1, 2, 3],  # int64
        'orgname': ['Org1', 'Org2', 'Org3']
    })
    
    orgaddruse = pd.DataFrame({
        'orgnbr': [1.0, np.nan, 3.0],  # float64 with NaN
        'addrnbr': [101.0, 102.0, 103.0],  # float64
        'addrusecd': ['PRI', 'PRI', 'PRI']
    })
    
    wh_addr = pd.DataFrame({
        'addrnbr': [101, 102, 103],  # int64
        'text1': ['Address 1', 'Address 2', 'Address 3'],
        'cityname': ['City1', 'City2', 'City3']
    })
    
    # This should work without crashing due to dtype conversions
    result = create_org_table_with_address(wh_org, orgaddruse, wh_addr)
    
    # Should have 3 orgs (all from wh_org)
    assert len(result) == 3
    
    # Org 1 and 3 should have addresses, org 2 should not (due to NaN in orgaddruse)
    org1_record = result[result['orgnbr'] == '1']
    assert len(org1_record) == 1
    assert pd.notnull(org1_record.iloc[0]['text1'])
    
    org3_record = result[result['orgnbr'] == '3']
    assert len(org3_record) == 1
    assert pd.notnull(org3_record.iloc[0]['text1'])


def test_mixed_dtype_conversion():
    """Test conversion between different integer and float types"""
    
    wh_org = pd.DataFrame({
        'orgnbr': [1, 2, 3],  # int64
        'orgname': ['Org1', 'Org2', 'Org3']
    })
    
    orgaddruse = pd.DataFrame({
        'orgnbr': np.array([1, 2, 3], dtype='int32'),  # int32
        'addrnbr': [101.0, 102.0, 103.0],  # float64
        'addrusecd': ['PRI', 'PRI', 'PRI']
    })
    
    wh_addr = pd.DataFrame({
        'addrnbr': np.array([101, 102, 103], dtype='int64'),  # int64
        'text1': ['Address 1', 'Address 2', 'Address 3'],
        'cityname': ['City1', 'City2', 'City3']
    })
    
    # Should handle dtype conversions correctly
    result = create_org_table_with_address(wh_org, orgaddruse, wh_addr)
    
    assert len(result) == 3
    assert all(pd.notnull(result['text1']))  # All should have addresses


def test_filter_preserves_original_columns():
    """Test that filter_to_active_accounts only returns org/pers + address columns, no account info"""
    
    # Create test data
    wh_org = pd.DataFrame({
        'orgnbr': [1, 2, 3],
        'orgname': ['Org1', 'Org2', 'Org3'],
        'text1': ['Addr1', 'Addr2', 'Addr3'],
        'cityname': ['City1', 'City2', 'City3']
    })
    
    acct_df = pd.DataFrame({
        'acctnbr': [1001, 1002]
    })
    
    wh_allroles = pd.DataFrame({
        'acctnbr': [1001, 1002, 1003],
        'orgnbr': [1, 2, 3],
        'acctrolecd': ['OWN', 'OWN', 'OWN'],
        'acctroledesc': ['Owner', 'Owner', 'Owner']
    })
    
    result = filter_to_active_accounts(acct_df, wh_allroles, org_with_address=wh_org)
    
    # Should only have orgs 1 and 2 (linked to active accounts)
    assert len(result) == 2
    assert set(result['orgnbr']) == {1, 2}  # integers, not strings since no conversion was needed
    
    # Should NOT have account/role columns
    assert 'acctnbr' not in result.columns
    assert 'acctrolecd' not in result.columns
    assert 'acctroledesc' not in result.columns
    
    # Should have original org columns
    assert 'orgname' in result.columns
    assert 'text1' in result.columns
    assert 'cityname' in result.columns


def test_string_number_conversion():
    """Test conversion of string numbers to ensure consistent joins"""
    
    wh_org = pd.DataFrame({
        'orgnbr': ['1', '2', '3'],  # string
        'orgname': ['Org1', 'Org2', 'Org3']
    })
    
    orgaddruse = pd.DataFrame({
        'orgnbr': [1.0, 2.0, 3.0],  # float64
        'addrnbr': ['101', '102', '103'],  # string
        'addrusecd': ['PRI', 'PRI', 'PRI']
    })
    
    wh_addr = pd.DataFrame({
        'addrnbr': [101, 102, 103],  # int64
        'text1': ['Address 1', 'Address 2', 'Address 3'],
        'cityname': ['City1', 'City2', 'City3']
    })
    
    # Should handle string/number conversions
    result = create_org_table_with_address(wh_org, orgaddruse, wh_addr)
    
    assert len(result) == 3
    assert all(pd.notnull(result['text1']))  # All should have addresses
