import pytest
import pandas as pd
import numpy as np
from src.data_quality.core import merge_org_with_view_taxid, merge_pers_with_view_taxid


class TestMergeOrgWithViewTaxid:
    """Test merging organization data with view tax ID data"""

    def test_successful_merge_with_updates(self):
        """Test successful merge that updates existing tax information"""
        wh_org = pd.DataFrame({
            'orgnbr': [1, 2, 3],
            'orgname': ['Company A', 'Company B', 'Company C'],
            'taxid': ['111-11-1111', '222-22-2222', '333-33-3333'],
            'taxidtypcd': ['FEIN', 'FEIN', 'FEIN']
        })
        
        vieworgtaxid = pd.DataFrame({
            'orgnbr': [1, 2],  # Only update first two organizations
            'taxidtypcd': ['BOON', 'SPEC'],
            'taxid': ['UPDATED-1', 'UPDATED-2']
        })
        
        result = merge_org_with_view_taxid(wh_org, vieworgtaxid)
        
        # Check that updates were applied
        assert result.loc[result['orgnbr'] == 1, 'taxid'].iloc[0] == 'UPDATED-1'
        assert result.loc[result['orgnbr'] == 1, 'taxidtypcd'].iloc[0] == 'BOON'
        assert result.loc[result['orgnbr'] == 2, 'taxid'].iloc[0] == 'UPDATED-2'
        assert result.loc[result['orgnbr'] == 2, 'taxidtypcd'].iloc[0] == 'SPEC'
        
        # Check that org 3 was not updated (no match in view)
        assert result.loc[result['orgnbr'] == 3, 'taxid'].iloc[0] == '333-33-3333'
        assert result.loc[result['orgnbr'] == 3, 'taxidtypcd'].iloc[0] == 'FEIN'
        
        # Ensure all original columns are preserved
        assert len(result) == 3
        assert set(result.columns) == set(wh_org.columns)

    def test_no_matches_returns_original(self):
        """Test that when no orgnbr matches exist, original data is returned"""
        wh_org = pd.DataFrame({
            'orgnbr': [1, 2, 3],
            'orgname': ['Company A', 'Company B', 'Company C'],
            'taxid': ['111-11-1111', '222-22-2222', '333-33-3333'],
            'taxidtypcd': ['FEIN', 'FEIN', 'FEIN']
        })
        
        vieworgtaxid = pd.DataFrame({
            'orgnbr': [4, 5],  # No matches
            'taxidtypcd': ['BOON', 'SPEC'],
            'taxid': ['UPDATED-1', 'UPDATED-2']
        })
        
        result = merge_org_with_view_taxid(wh_org, vieworgtaxid)
        
        # Should be identical to original
        pd.testing.assert_frame_equal(result.reset_index(drop=True), wh_org.reset_index(drop=True))

    def test_handles_null_values_in_view(self):
        """Test that null values in view table don't overwrite existing data"""
        wh_org = pd.DataFrame({
            'orgnbr': [1, 2],
            'orgname': ['Company A', 'Company B'],
            'taxid': ['111-11-1111', '222-22-2222'],
            'taxidtypcd': ['FEIN', 'FEIN']
        })
        
        vieworgtaxid = pd.DataFrame({
            'orgnbr': [1, 2],
            'taxidtypcd': ['BOON', None],  # Null value should not overwrite
            'taxid': [None, 'UPDATED-2']   # Null value should not overwrite
        })
        
        result = merge_org_with_view_taxid(wh_org, vieworgtaxid)
        
        # Only non-null updates should be applied
        assert result.loc[result['orgnbr'] == 1, 'taxid'].iloc[0] == '111-11-1111'  # Not overwritten
        assert result.loc[result['orgnbr'] == 1, 'taxidtypcd'].iloc[0] == 'BOON'    # Updated
        assert result.loc[result['orgnbr'] == 2, 'taxid'].iloc[0] == 'UPDATED-2'    # Updated
        assert result.loc[result['orgnbr'] == 2, 'taxidtypcd'].iloc[0] == 'FEIN'    # Not overwritten

    def test_dtype_conversion_for_join(self):
        """Test that dtype mismatches are handled correctly"""
        wh_org = pd.DataFrame({
            'orgnbr': [1, 2, 3],  # int
            'orgname': ['Company A', 'Company B', 'Company C'],
            'taxid': ['111-11-1111', '222-22-2222', '333-33-3333']
        })
        
        vieworgtaxid = pd.DataFrame({
            'orgnbr': [1.0, 2.0],  # float
            'taxid': ['UPDATED-1', 'UPDATED-2']
        })
        
        result = merge_org_with_view_taxid(wh_org, vieworgtaxid)
        
        # Should successfully merge despite dtype difference
        assert result.loc[result['orgnbr'] == '1', 'taxid'].iloc[0] == 'UPDATED-1'
        assert result.loc[result['orgnbr'] == '2', 'taxid'].iloc[0] == 'UPDATED-2'

    def test_duplicate_orgnbr_in_view_raises_error(self):
        """Test that duplicate orgnbr values in view table raise an error"""
        wh_org = pd.DataFrame({
            'orgnbr': [1, 2, 3],
            'orgname': ['Company A', 'Company B', 'Company C'],
            'taxid': ['111-11-1111', '222-22-2222', '333-33-3333']
        })
        
        vieworgtaxid = pd.DataFrame({
            'orgnbr': [1, 1, 2],  # Duplicate orgnbr = 1
            'taxid': ['UPDATED-1A', 'UPDATED-1B', 'UPDATED-2']
        })
        
        with pytest.raises(ValueError, match="Duplicate orgnbr values found"):
            merge_org_with_view_taxid(wh_org, vieworgtaxid)

    def test_no_overlapping_columns_returns_original(self):
        """Test that when no columns overlap (except join key), original is returned"""
        wh_org = pd.DataFrame({
            'orgnbr': [1, 2, 3],
            'orgname': ['Company A', 'Company B', 'Company C'],
            'taxid': ['111-11-1111', '222-22-2222', '333-33-3333']
        })
        
        vieworgtaxid = pd.DataFrame({
            'orgnbr': [1, 2],
            'different_column': ['Value1', 'Value2']  # No overlap with wh_org columns
        })
        
        result = merge_org_with_view_taxid(wh_org, vieworgtaxid)
        
        # Should be identical to original since no columns overlap
        pd.testing.assert_frame_equal(result.reset_index(drop=True), wh_org.reset_index(drop=True))

    def test_validation_assertions(self):
        """Test that proper validation assertions work"""
        wh_org = pd.DataFrame({
            'orgnbr': [1, 2, 3],
            'orgname': ['Company A', 'Company B', 'Company C']
        })
        
        vieworgtaxid = pd.DataFrame({
            'orgnbr': [1, 2],
            'taxid': ['UPDATED-1', 'UPDATED-2']
        })
        
        # Test None inputs
        with pytest.raises(AssertionError, match="wh_org DataFrame must not be None"):
            merge_org_with_view_taxid(None, vieworgtaxid)
            
        with pytest.raises(AssertionError, match="vieworgtaxid DataFrame must not be None"):
            merge_org_with_view_taxid(wh_org, None)
        
        # Test missing join columns
        wh_org_bad = pd.DataFrame({'wrong_col': [1, 2, 3]})
        with pytest.raises(AssertionError, match="wh_org must have 'orgnbr' column"):
            merge_org_with_view_taxid(wh_org_bad, vieworgtaxid)
            
        vieworgtaxid_bad = pd.DataFrame({'wrong_col': [1, 2]})
        with pytest.raises(AssertionError, match="vieworgtaxid must have 'orgnbr' column"):
            merge_org_with_view_taxid(wh_org, vieworgtaxid_bad)


class TestMergePersWithViewTaxid:
    """Test merging person data with view tax ID data"""

    def test_successful_merge_with_updates(self):
        """Test successful merge that updates existing tax information"""
        wh_pers = pd.DataFrame({
            'persnbr': [1, 2, 3],
            'persname': ['John Doe', 'Jane Smith', 'Bob Johnson'],
            'taxid': ['111-11-1111', '222-22-2222', '333-33-3333']
        })
        
        viewperstaxid = pd.DataFrame({
            'persnbr': [1, 2],  # Only update first two persons
            'taxid': ['UPDATED-1', 'UPDATED-2']
        })
        
        result = merge_pers_with_view_taxid(wh_pers, viewperstaxid)
        
        # Check that updates were applied
        assert result.loc[result['persnbr'] == 1, 'taxid'].iloc[0] == 'UPDATED-1'
        assert result.loc[result['persnbr'] == 2, 'taxid'].iloc[0] == 'UPDATED-2'
        
        # Check that person 3 was not updated (no match in view)
        assert result.loc[result['persnbr'] == 3, 'taxid'].iloc[0] == '333-33-3333'
        
        # Ensure all original columns are preserved
        assert len(result) == 3
        assert set(result.columns) == set(wh_pers.columns)

    def test_no_matches_returns_original(self):
        """Test that when no persnbr matches exist, original data is returned"""
        wh_pers = pd.DataFrame({
            'persnbr': [1, 2, 3],
            'persname': ['John Doe', 'Jane Smith', 'Bob Johnson'],
            'taxid': ['111-11-1111', '222-22-2222', '333-33-3333']
        })
        
        viewperstaxid = pd.DataFrame({
            'persnbr': [4, 5],  # No matches
            'taxid': ['UPDATED-1', 'UPDATED-2']
        })
        
        result = merge_pers_with_view_taxid(wh_pers, viewperstaxid)
        
        # Should be identical to original
        pd.testing.assert_frame_equal(result.reset_index(drop=True), wh_pers.reset_index(drop=True))

    def test_handles_null_values_in_view(self):
        """Test that null values in view table don't overwrite existing data"""
        wh_pers = pd.DataFrame({
            'persnbr': [1, 2],
            'persname': ['John Doe', 'Jane Smith'],
            'taxid': ['111-11-1111', '222-22-2222']
        })
        
        viewperstaxid = pd.DataFrame({
            'persnbr': [1, 2],
            'taxid': [None, 'UPDATED-2']   # Null value should not overwrite
        })
        
        result = merge_pers_with_view_taxid(wh_pers, viewperstaxid)
        
        # Only non-null updates should be applied
        assert result.loc[result['persnbr'] == 1, 'taxid'].iloc[0] == '111-11-1111'  # Not overwritten
        assert result.loc[result['persnbr'] == 2, 'taxid'].iloc[0] == 'UPDATED-2'    # Updated

    def test_duplicate_persnbr_in_view_raises_error(self):
        """Test that duplicate persnbr values in view table raise an error"""
        wh_pers = pd.DataFrame({
            'persnbr': [1, 2, 3],
            'persname': ['John Doe', 'Jane Smith', 'Bob Johnson'],
            'taxid': ['111-11-1111', '222-22-2222', '333-33-3333']
        })
        
        viewperstaxid = pd.DataFrame({
            'persnbr': [1, 1, 2],  # Duplicate persnbr = 1
            'taxid': ['UPDATED-1A', 'UPDATED-1B', 'UPDATED-2']
        })
        
        with pytest.raises(ValueError, match="Duplicate persnbr values found"):
            merge_pers_with_view_taxid(wh_pers, viewperstaxid)

    def test_validation_assertions(self):
        """Test that proper validation assertions work"""
        wh_pers = pd.DataFrame({
            'persnbr': [1, 2, 3],
            'persname': ['John Doe', 'Jane Smith', 'Bob Johnson']
        })
        
        viewperstaxid = pd.DataFrame({
            'persnbr': [1, 2],
            'taxid': ['UPDATED-1', 'UPDATED-2']
        })
        
        # Test None inputs
        with pytest.raises(AssertionError, match="wh_pers DataFrame must not be None"):
            merge_pers_with_view_taxid(None, viewperstaxid)
            
        with pytest.raises(AssertionError, match="viewperstaxid DataFrame must not be None"):
            merge_pers_with_view_taxid(wh_pers, None)
        
        # Test missing join columns
        wh_pers_bad = pd.DataFrame({'wrong_col': [1, 2, 3]})
        with pytest.raises(AssertionError, match="wh_pers must have 'persnbr' column"):
            merge_pers_with_view_taxid(wh_pers_bad, viewperstaxid)
            
        viewperstaxid_bad = pd.DataFrame({'wrong_col': [1, 2]})
        with pytest.raises(AssertionError, match="viewperstaxid must have 'persnbr' column"):
            merge_pers_with_view_taxid(wh_pers, viewperstaxid_bad)
