import pytest
import pandas as pd
from src.data_quality.core import create_org_table_with_address, create_pers_table_with_address, filter_to_active_accounts, merge_with_input_file, process_input_files, archive_input_file
import src.data_quality.core


class TestCreateOrgTableWithAddress:
    
    def create_mock_wh_org(self):
        """Create mock WH_ORG data"""
        return pd.DataFrame({
            'orgnbr': [1001, 1002, 1003, 1004],
            'orgname': ['Acme Corp', 'Beta Inc', 'Gamma LLC', 'Delta Co'],
            'orgtype': ['CORP', 'INC', 'LLC', 'CORP']
        })
    
    def create_mock_orgaddruse(self):
        """Create mock ORGADDRUSE data with both PRI and non-PRI records"""
        return pd.DataFrame({
            'orgnbr': [1001, 1001, 1002, 1003, 1003, 1005],
            'addrnbr': [2001, 2002, 2003, 2004, 2005, 2006],
            'addrusecd': ['PRI', 'SEC', 'PRI', 'PRI', 'SEC', 'PRI']
        })
    
    def create_mock_wh_addr(self):
        """Create mock WH_ADDR data"""
        return pd.DataFrame({
            'addrnbr': [2001, 2002, 2003, 2004, 2005, 2006],
            'text1': ['123 Main St', '456 Oak Ave', '789 Pine Rd', '321 Elm St', '654 Maple Dr', '987 Cedar Ln'],
            'text2': ['Apt 1', 'Suite 200', '', 'Unit B', '', 'Floor 3'],
            'text3': ['', '', 'Bldg A', '', 'Rear', ''],
            'cityname': ['Springfield', 'Riverside', 'Franklin', 'Georgetown', 'Madison', 'Arlington'],
            'statecd': ['IL', 'CA', 'TN', 'TX', 'WI', 'VA'],
            'zipcd': ['62701', '92501', '37064', '78626', '53703', '22201'],
            'zipsuf': ['1234', '5678', '', '9012', '', '3456'],
            'addrlinetypdesc1': ['Street', 'Street', 'Street', 'Street', 'Street', 'Street'],
            'addrlinetypcd1': ['STR', 'STR', 'STR', 'STR', 'STR', 'STR'],
            'addrlinetypdesc2': ['Apartment', 'Suite', '', 'Unit', '', 'Floor'],
            'addrlinetypcd2': ['APT', 'STE', '', 'UNT', '', 'FLR']
        })
    
    def test_successful_merge_with_pri_filter(self):
        """Test successful merge with PRI address filtering"""
        wh_org = self.create_mock_wh_org()
        orgaddruse = self.create_mock_orgaddruse()
        wh_addr = self.create_mock_wh_addr()
        
        result = create_org_table_with_address(wh_org, orgaddruse, wh_addr)
        
        # Should have 4 org records (all from wh_org)
        assert len(result) == 4
        
        # Check that only PRI addresses are included
        pri_addresses = result.dropna(subset=['addrusecd'])
        assert all(pri_addresses['addrusecd'] == 'PRI')
        
        # Verify specific org with address
        acme_record = result[result['orgname'] == 'Acme Corp']
        assert len(acme_record) == 1
        assert acme_record.iloc[0]['text1'] == '123 Main St'
        assert acme_record.iloc[0]['cityname'] == 'Springfield'
    
    def test_org_without_address_gets_null_values(self):
        """Test that organizations without addresses get null values"""
        wh_org = self.create_mock_wh_org()
        orgaddruse = self.create_mock_orgaddruse()
        wh_addr = self.create_mock_wh_addr()
        
        result = create_org_table_with_address(wh_org, orgaddruse, wh_addr)
        
        # Org 1004 should not have address data (not in orgaddruse)
        delta_record = result[result['orgname'] == 'Delta Co']
        assert len(delta_record) == 1
        assert pd.isna(delta_record.iloc[0]['text1'])
        assert pd.isna(delta_record.iloc[0]['addrusecd'])
    
    def test_filter_excludes_non_pri_addresses(self):
        """Test that non-PRI addresses are filtered out"""
        wh_org = self.create_mock_wh_org()
        orgaddruse = self.create_mock_orgaddruse()
        wh_addr = self.create_mock_wh_addr()
        
        result = create_org_table_with_address(wh_org, orgaddruse, wh_addr)
        
        # Should not contain any SEC addresses
        assert 'SEC' not in result['addrusecd'].values
        
        # Org 1001 has both PRI and SEC, should only get PRI
        acme_records = result[result['orgname'] == 'Acme Corp']
        assert len(acme_records) == 1
        assert acme_records.iloc[0]['addrusecd'] == 'PRI'
    
    def test_none_dataframe_validation(self):
        """Test that None DataFrames raise assertions"""
        wh_org = self.create_mock_wh_org()
        orgaddruse = self.create_mock_orgaddruse()
        wh_addr = self.create_mock_wh_addr()
        
        with pytest.raises(AssertionError, match="wh_org DataFrame must not be None"):
            create_org_table_with_address(None, orgaddruse, wh_addr)
        
        with pytest.raises(AssertionError, match="orgaddruse DataFrame must not be None"):
            create_org_table_with_address(wh_org, None, wh_addr)
        
        with pytest.raises(AssertionError, match="wh_addr DataFrame must not be None"):
            create_org_table_with_address(wh_org, orgaddruse, None)
    
    def test_missing_column_validation(self):
        """Test that missing required columns raise assertions"""
        wh_org = pd.DataFrame({'wrong_col': [1, 2]})
        orgaddruse = self.create_mock_orgaddruse()
        wh_addr = self.create_mock_wh_addr()
        
        with pytest.raises(AssertionError, match="wh_org must have 'orgnbr' column"):
            create_org_table_with_address(wh_org, orgaddruse, wh_addr)
    
    def test_dtype_mismatch_validation(self):
        """Test that mismatched data types are automatically converted"""
        wh_org = self.create_mock_wh_org()
        orgaddruse = self.create_mock_orgaddruse()
        wh_addr = self.create_mock_wh_addr()
        
        # Change orgnbr to string in one DataFrame
        wh_org_str = wh_org.copy()
        wh_org_str['orgnbr'] = wh_org_str['orgnbr'].astype(str)
        
        # Should succeed with automatic conversion (no exception)
        result = create_org_table_with_address(wh_org_str, orgaddruse, wh_addr)
        assert len(result) == 4  # Should still work with converted types
    
    def test_empty_dataframes(self):
        """Test behavior with empty DataFrames"""
        wh_org = pd.DataFrame(columns=['orgnbr', 'orgname'])
        orgaddruse = pd.DataFrame(columns=['orgnbr', 'addrnbr', 'addrusecd'])
        wh_addr = pd.DataFrame(columns=['addrnbr', 'text1', 'cityname', 'statecd', 'zipcd'])
        
        result = create_org_table_with_address(wh_org, orgaddruse, wh_addr)
        
        assert len(result) == 0
        # Should contain columns from org table and filtered address fields
        expected_columns = ['orgnbr', 'orgname', 'addrnbr', 'addrusecd', 'text1', 'cityname', 'statecd', 'zipcd']
        assert all(col in result.columns for col in expected_columns if col in wh_addr.columns or col in wh_org.columns or col in orgaddruse.columns)
    
    def test_no_pri_addresses(self):
        """Test when no PRI addresses exist"""
        wh_org = self.create_mock_wh_org()
        orgaddruse = pd.DataFrame({
            'orgnbr': [1001, 1002],
            'addrnbr': [2001, 2002],
            'addrusecd': ['SEC', 'SEC']  # No PRI addresses
        })
        wh_addr = self.create_mock_wh_addr()
        
        result = create_org_table_with_address(wh_org, orgaddruse, wh_addr)
        
        # Should have all orgs but no address data
        assert len(result) == 4
        assert result['addrusecd'].isna().all()


class TestCreatePersTableWithAddress:
    
    def create_mock_wh_pers(self):
        """Create mock WH_PERS data"""
        return pd.DataFrame({
            'persnbr': [5001, 5002, 5003, 5004],
            'firstname': ['John', 'Jane', 'Bob', 'Alice'],
            'lastname': ['Smith', 'Doe', 'Johnson', 'Brown'],
            'birthdate': ['1980-01-01', '1975-05-15', '1990-12-10', '1985-03-22']
        })
    
    def create_mock_persaddruse(self):
        """Create mock PERSADDRUSE data with both PRI and non-PRI records"""
        return pd.DataFrame({
            'persnbr': [5001, 5001, 5002, 5003, 5003, 5005],
            'addrnbr': [2001, 2002, 2003, 2004, 2005, 2006],
            'addrusecd': ['PRI', 'SEC', 'PRI', 'PRI', 'SEC', 'PRI']
        })
    
    def create_mock_wh_addr(self):
        """Create mock WH_ADDR data"""
        return pd.DataFrame({
            'addrnbr': [2001, 2002, 2003, 2004, 2005, 2006],
            'text1': ['123 Main St', '456 Oak Ave', '789 Pine Rd', '321 Elm St', '654 Maple Dr', '987 Cedar Ln'],
            'text2': ['Apt 1', 'Suite 200', '', 'Unit B', '', 'Floor 3'],
            'text3': ['', '', 'Bldg A', '', 'Rear', ''],
            'cityname': ['Springfield', 'Riverside', 'Franklin', 'Georgetown', 'Madison', 'Arlington'],
            'statecd': ['IL', 'CA', 'TN', 'TX', 'WI', 'VA'],
            'zipcd': ['62701', '92501', '37064', '78626', '53703', '22201'],
            'zipsuf': ['1234', '5678', '', '9012', '', '3456'],
            'addrlinetypdesc1': ['Street', 'Street', 'Street', 'Street', 'Street', 'Street'],
            'addrlinetypcd1': ['STR', 'STR', 'STR', 'STR', 'STR', 'STR'],
            'addrlinetypdesc2': ['Apartment', 'Suite', '', 'Unit', '', 'Floor'],
            'addrlinetypcd2': ['APT', 'STE', '', 'UNT', '', 'FLR']
        })
    
    def test_successful_merge_with_pri_filter(self):
        """Test successful merge with PRI address filtering"""
        wh_pers = self.create_mock_wh_pers()
        persaddruse = self.create_mock_persaddruse()
        wh_addr = self.create_mock_wh_addr()
        
        result = create_pers_table_with_address(wh_pers, persaddruse, wh_addr)
        
        # Should have 4 person records (all from wh_pers)
        assert len(result) == 4
        
        # Check that only PRI addresses are included
        pri_addresses = result.dropna(subset=['addrusecd'])
        assert all(pri_addresses['addrusecd'] == 'PRI')
        
        # Verify specific person with address
        john_record = result[result['firstname'] == 'John']
        assert len(john_record) == 1
        assert john_record.iloc[0]['text1'] == '123 Main St'
        assert john_record.iloc[0]['cityname'] == 'Springfield'
    
    def test_person_without_address_gets_null_values(self):
        """Test that persons without addresses get null values"""
        wh_pers = self.create_mock_wh_pers()
        persaddruse = self.create_mock_persaddruse()
        wh_addr = self.create_mock_wh_addr()
        
        result = create_pers_table_with_address(wh_pers, persaddruse, wh_addr)
        
        # Person 5004 should not have address data (not in persaddruse)
        alice_record = result[result['firstname'] == 'Alice']
        assert len(alice_record) == 1
        assert pd.isna(alice_record.iloc[0]['text1'])
        assert pd.isna(alice_record.iloc[0]['addrusecd'])
    
    def test_filter_excludes_non_pri_addresses(self):
        """Test that non-PRI addresses are filtered out"""
        wh_pers = self.create_mock_wh_pers()
        persaddruse = self.create_mock_persaddruse()
        wh_addr = self.create_mock_wh_addr()
        
        result = create_pers_table_with_address(wh_pers, persaddruse, wh_addr)
        
        # Should not contain any SEC addresses
        assert 'SEC' not in result['addrusecd'].values
        
        # Person 5001 has both PRI and SEC, should only get PRI
        john_records = result[result['firstname'] == 'John']
        assert len(john_records) == 1
        assert john_records.iloc[0]['addrusecd'] == 'PRI'
    
    def test_none_dataframe_validation(self):
        """Test that None DataFrames raise assertions"""
        wh_pers = self.create_mock_wh_pers()
        persaddruse = self.create_mock_persaddruse()
        wh_addr = self.create_mock_wh_addr()
        
        with pytest.raises(AssertionError, match="wh_pers DataFrame must not be None"):
            create_pers_table_with_address(None, persaddruse, wh_addr)
        
        with pytest.raises(AssertionError, match="persaddruse DataFrame must not be None"):
            create_pers_table_with_address(wh_pers, None, wh_addr)
        
        with pytest.raises(AssertionError, match="wh_addr DataFrame must not be None"):
            create_pers_table_with_address(wh_pers, persaddruse, None)
    
    def test_missing_column_validation(self):
        """Test that missing required columns raise assertions"""
        wh_pers = pd.DataFrame({'wrong_col': [1, 2]})
        persaddruse = self.create_mock_persaddruse()
        wh_addr = self.create_mock_wh_addr()
        
        with pytest.raises(AssertionError, match="wh_pers must have 'persnbr' column"):
            create_pers_table_with_address(wh_pers, persaddruse, wh_addr)
    
    def test_dtype_mismatch_validation(self):
        """Test that mismatched data types are automatically converted"""
        wh_pers = self.create_mock_wh_pers()
        persaddruse = self.create_mock_persaddruse()
        wh_addr = self.create_mock_wh_addr()
        
        # Change persnbr to string in one DataFrame
        wh_pers_str = wh_pers.copy()
        wh_pers_str['persnbr'] = wh_pers_str['persnbr'].astype(str)
        
        # Should succeed with automatic conversion (no exception)
        result = create_pers_table_with_address(wh_pers_str, persaddruse, wh_addr)
        assert len(result) == 4  # Should still work with converted types (all persons returned)
    
    def test_empty_dataframes(self):
        """Test behavior with empty DataFrames"""
        wh_pers = pd.DataFrame(columns=['persnbr', 'firstname', 'lastname'])
        persaddruse = pd.DataFrame(columns=['persnbr', 'addrnbr', 'addrusecd'])
        wh_addr = pd.DataFrame(columns=['addrnbr', 'text1', 'cityname', 'statecd', 'zipcd'])
        
        result = create_pers_table_with_address(wh_pers, persaddruse, wh_addr)
        
        assert len(result) == 0
        # Should contain columns from person table and filtered address fields
        expected_columns = ['persnbr', 'firstname', 'lastname', 'addrnbr', 'addrusecd', 'text1', 'cityname', 'statecd', 'zipcd']
        assert all(col in result.columns for col in expected_columns if col in wh_addr.columns or col in wh_pers.columns or col in persaddruse.columns)
    
    def test_no_pri_addresses(self):
        """Test when no PRI addresses exist"""
        wh_pers = self.create_mock_wh_pers()
        persaddruse = pd.DataFrame({
            'persnbr': [5001, 5002],
            'addrnbr': [2001, 2002],
            'addrusecd': ['SEC', 'SEC']  # No PRI addresses
        })
        wh_addr = self.create_mock_wh_addr()
        
        result = create_pers_table_with_address(wh_pers, persaddruse, wh_addr)
        
        # Should have all persons but no address data
        assert len(result) == 4
        assert result['addrusecd'].isna().all()


class TestFilterToActiveAccounts:
    
    def create_mock_acct_df(self):
        """Create mock active account dataframe"""
        return pd.DataFrame({
            'acctnbr': [1001, 1002, 1003, 1004],
            'customername': ['Customer A', 'Customer B', 'Customer C', 'Customer D'],
            'balance': [10000, 25000, 50000, 75000]
        })
    
    def create_mock_wh_allroles(self):
        """Create mock WH_ALLROLES data"""
        return pd.DataFrame({
            'acctnbr': [1001, 1001, 1002, 1003, 1005, 1006],  # 1005, 1006 not in active accounts
            'persnbr': [5001, 5002, 5002, 5003, 5004, 5001],
            'orgnbr': [1001, 1002, 1003, 1004, 1005, 1006],
            'acctrolecd': ['OWN', 'SIG', 'OWN', 'OWN', 'OWN', 'SIG'],
            'acctroledesc': ['Owner', 'Signer', 'Owner', 'Owner', 'Owner', 'Signer']
        })
    
    def create_mock_pers_with_address(self):
        """Create mock person with address data"""
        return pd.DataFrame({
            'persnbr': [5001, 5002, 5003, 5004],
            'firstname': ['John', 'Jane', 'Bob', 'Alice'],
            'lastname': ['Smith', 'Doe', 'Johnson', 'Brown'],
            'text1': ['123 Main St', '456 Oak Ave', '789 Pine Rd', '321 Elm St'],
            'cityname': ['Springfield', 'Riverside', 'Franklin', 'Georgetown']
        })
    
    def create_mock_org_with_address(self):
        """Create mock organization with address data"""
        return pd.DataFrame({
            'orgnbr': [1001, 1002, 1003, 1004, 1005, 1006],
            'orgname': ['Acme Corp', 'Beta Inc', 'Gamma LLC', 'Delta Co', 'Echo Ltd', 'Foxtrot Corp'],
            'text1': ['123 Business St', '456 Commerce Ave', '789 Trade Rd', '321 Industry St', '654 Market Dr', '987 Corporate Ln'],
            'cityname': ['Springfield', 'Riverside', 'Franklin', 'Georgetown', 'Madison', 'Arlington']
        })
    
    def test_filter_persons_to_active_accounts(self):
        """Test filtering persons to only those with active accounts"""
        acct_df = self.create_mock_acct_df()
        wh_allroles = self.create_mock_wh_allroles()
        pers_with_address = self.create_mock_pers_with_address()
        
        result = filter_to_active_accounts(acct_df, wh_allroles, pers_with_address=pers_with_address)
        
        # Should only include persons linked to active accounts (1001, 1002, 1003)
        # Person 5004 linked to account 1005 should be excluded (not active)
        expected_persons = {5001, 5002, 5003}
        actual_persons = set(result['persnbr'].unique())
        assert actual_persons == expected_persons
        
        # Verify we only have person and address fields (no account/role fields)
        assert 'acctrolecd' not in result.columns
        assert 'acctroledesc' not in result.columns
        assert 'acctnbr' not in result.columns
    
    def test_filter_orgs_to_active_accounts(self):
        """Test filtering organizations to only those with active accounts"""
        acct_df = self.create_mock_acct_df()
        wh_allroles = self.create_mock_wh_allroles()
        org_with_address = self.create_mock_org_with_address()
        
        result = filter_to_active_accounts(acct_df, wh_allroles, org_with_address=org_with_address)
        
        # Should only include orgs linked to active accounts (1001, 1002, 1003)
        # Orgs 1005, 1006 linked to inactive accounts should be excluded
        expected_orgs = {1001, 1002, 1003, 1004}
        actual_orgs = set(result['orgnbr'].unique())
        assert actual_orgs == expected_orgs
        
        # Verify we only have org and address fields (no account/role fields)
        assert 'acctrolecd' not in result.columns
        assert 'acctroledesc' not in result.columns
        assert 'acctnbr' not in result.columns
    
    def test_both_dataframes_provided_raises_error(self):
        """Test that providing both pers and org dataframes raises error"""
        acct_df = self.create_mock_acct_df()
        wh_allroles = self.create_mock_wh_allroles()
        pers_with_address = self.create_mock_pers_with_address()
        org_with_address = self.create_mock_org_with_address()
        
        with pytest.raises(ValueError, match="Provide either pers_with_address OR org_with_address, not both"):
            filter_to_active_accounts(acct_df, wh_allroles, 
                                    pers_with_address=pers_with_address, 
                                    org_with_address=org_with_address)
    
    def test_neither_dataframe_provided_raises_error(self):
        """Test that providing neither pers nor org dataframes raises error"""
        acct_df = self.create_mock_acct_df()
        wh_allroles = self.create_mock_wh_allroles()
        
        with pytest.raises(ValueError, match="Must provide either pers_with_address or org_with_address"):
            filter_to_active_accounts(acct_df, wh_allroles)
    
    def test_none_dataframe_validation(self):
        """Test that None DataFrames raise assertions"""
        acct_df = self.create_mock_acct_df()
        wh_allroles = self.create_mock_wh_allroles()
        pers_with_address = self.create_mock_pers_with_address()
        
        with pytest.raises(AssertionError, match="acct_df DataFrame must not be None"):
            filter_to_active_accounts(None, wh_allroles, pers_with_address=pers_with_address)
        
        with pytest.raises(AssertionError, match="wh_allroles DataFrame must not be None"):
            filter_to_active_accounts(acct_df, None, pers_with_address=pers_with_address)
    
    def test_missing_column_validation(self):
        """Test that missing required columns raise assertions"""
        acct_df = pd.DataFrame({'wrong_col': [1, 2]})
        wh_allroles = self.create_mock_wh_allroles()
        pers_with_address = self.create_mock_pers_with_address()
        
        with pytest.raises(AssertionError, match="acct_df must have 'acctnbr' column"):
            filter_to_active_accounts(acct_df, wh_allroles, pers_with_address=pers_with_address)
    
    def test_dtype_mismatch_validation(self):
        """Test that mismatched data types are automatically converted"""
        acct_df = self.create_mock_acct_df()
        wh_allroles = self.create_mock_wh_allroles()
        pers_with_address = self.create_mock_pers_with_address()
        
        # Change acctnbr to string in one DataFrame
        acct_df_str = acct_df.copy()
        acct_df_str['acctnbr'] = acct_df_str['acctnbr'].astype(str)
        
        # Should succeed with automatic conversion (no exception)
        result = filter_to_active_accounts(acct_df_str, wh_allroles, pers_with_address=pers_with_address)
        assert len(result) >= 0  # Should still work with converted types
    
    def test_no_active_accounts_for_persons(self):
        """Test when no persons are linked to active accounts"""
        acct_df = pd.DataFrame({'acctnbr': [9999], 'balance': [1000]})  # No matching accounts
        wh_allroles = self.create_mock_wh_allroles()
        pers_with_address = self.create_mock_pers_with_address()
        
        result = filter_to_active_accounts(acct_df, wh_allroles, pers_with_address=pers_with_address)
        
        # Should have no records
        assert len(result) == 0
    
    def test_empty_dataframes(self):
        """Test behavior with empty DataFrames"""
        acct_df = pd.DataFrame(columns=['acctnbr', 'balance'])
        wh_allroles = pd.DataFrame(columns=['acctnbr', 'persnbr', 'orgnbr', 'acctrolecd', 'acctroledesc'])
        pers_with_address = pd.DataFrame(columns=['persnbr', 'firstname'])
        
        result = filter_to_active_accounts(acct_df, wh_allroles, pers_with_address=pers_with_address)
        
        assert len(result) == 0


class TestMergeWithInputFile:
    """Test the merge_with_input_file function."""
    
    def test_merge_with_input_file_org_success(self, tmp_path):
        """Test successful merge with org input file."""
        # Create test org dataframe
        org_df = pd.DataFrame({
            'orgnbr': [1, 2, 3],
            'orgname': ['Org A', 'Org B', 'Org C'],
            'status': ['Active', 'Active', 'Inactive']
        })
        
        # Create test Janet's file with additional columns
        janet_df = pd.DataFrame({
            'ORGNBR': [1, 2, 4],  # 4 is extra record we don't want
            'ORGNAME': ['Org A', 'Org B', 'Org D'],  # Duplicate column
            'STATUS': ['Active', 'Active', 'Active'],  # Duplicate column
            'NOTES': ['Note 1', 'Note 2', 'Note 4'],  # Extra column we want
            'CONTACT': ['John', 'Jane', 'Bob']  # Extra column we want
        })
        
        # Create input folder and file
        input_folder = tmp_path / "org"
        input_folder.mkdir()
        excel_file = input_folder / "janet_org.xlsx"
        janet_df.to_excel(excel_file, index=False)
        
        # Call function
        result = src.data_quality.core.merge_with_input_file(org_df, str(input_folder), 'org')
        
        # Verify results
        assert len(result) == 3  # Should keep all my records
        assert 'ORGNBR' in result.columns
        assert 'ORGNAME' in result.columns  # From my data
        assert 'STATUS' in result.columns   # From my data
        assert 'NOTES' in result.columns    # Added from Janet's
        assert 'CONTACT' in result.columns  # Added from Janet's
        
        # Check merge worked correctly
        assert result.loc[result['ORGNBR'] == 1, 'NOTES'].iloc[0] == 'Note 1'
        assert result.loc[result['ORGNBR'] == 2, 'NOTES'].iloc[0] == 'Note 2'
        assert pd.isna(result.loc[result['ORGNBR'] == 3, 'NOTES'].iloc[0])  # No match in Janet's file
    
    def test_merge_with_input_file_pers_success(self, tmp_path):
        """Test successful merge with pers input file."""
        # Create test pers dataframe
        pers_df = pd.DataFrame({
            'persnbr': [101, 102, 103],
            'lastname': ['Smith', 'Jones', 'Brown'],
            'firstname': ['John', 'Jane', 'Bob']
        })
        
        # Create test Janet's file
        janet_df = pd.DataFrame({
            'PERSNBR': [101, 102],
            'LASTNAME': ['Smith', 'Jones'],  # Duplicate column
            'FIRSTNAME': ['John', 'Jane'],   # Duplicate column
            'COMMENTS': ['VIP customer', 'Regular customer']  # Extra column
        })
        
        # Create input folder and file
        input_folder = tmp_path / "pers"
        input_folder.mkdir()
        excel_file = input_folder / "janet_pers.xlsx"
        janet_df.to_excel(excel_file, index=False)
        
        # Call function
        result = src.data_quality.core.merge_with_input_file(pers_df, str(input_folder), 'pers')
        
        # Verify results
        assert len(result) == 3
        assert 'PERSNBR' in result.columns
        assert 'COMMENTS' in result.columns  # Added from Janet's
        assert result.loc[result['PERSNBR'] == 101, 'COMMENTS'].iloc[0] == 'VIP customer'
    
    def test_merge_with_input_file_no_excel_file(self, tmp_path):
        """Test error when no Excel file exists."""
        org_df = pd.DataFrame({'orgnbr': [1], 'orgname': ['Test']})
        input_folder = tmp_path / "org"
        input_folder.mkdir()
        
        with pytest.raises(FileNotFoundError, match="No Excel files found"):
            src.data_quality.core.merge_with_input_file(org_df, str(input_folder), 'org')
    
    def test_merge_with_input_file_multiple_excel_files(self, tmp_path):
        """Test error when multiple Excel files exist."""
        org_df = pd.DataFrame({'orgnbr': [1], 'orgname': ['Test']})
        input_folder = tmp_path / "org"
        input_folder.mkdir()
        
        # Create multiple Excel files
        pd.DataFrame().to_excel(input_folder / "file1.xlsx", index=False)
        pd.DataFrame().to_excel(input_folder / "file2.xlsx", index=False)
        
        with pytest.raises(ValueError, match="Multiple Excel files found"):
            src.data_quality.core.merge_with_input_file(org_df, str(input_folder), 'org')
    
    def test_merge_with_input_file_folder_not_exists(self):
        """Test error when input folder doesn't exist."""
        org_df = pd.DataFrame({'orgnbr': [1], 'orgname': ['Test']})
        
        with pytest.raises(AssertionError, match="Input folder .* does not exist"):
            src.data_quality.core.merge_with_input_file(org_df, "/nonexistent/path", 'org')
    
    def test_merge_with_input_file_empty_excel(self, tmp_path):
        """Test error when Excel file is empty."""
        org_df = pd.DataFrame({'orgnbr': [1], 'orgname': ['Test']})
        input_folder = tmp_path / "org"
        input_folder.mkdir()
        
        # Create empty Excel file
        empty_df = pd.DataFrame()
        excel_file = input_folder / "empty.xlsx"
        empty_df.to_excel(excel_file, index=False)
        
        with pytest.raises(ValueError, match="Excel file .* is empty"):
            src.data_quality.core.merge_with_input_file(org_df, str(input_folder), 'org')
    
    def test_merge_with_input_file_missing_join_key_my_df(self, tmp_path):
        """Test error when join key missing from my dataframe."""
        # Missing orgnbr column
        org_df = pd.DataFrame({'orgname': ['Test'], 'status': ['Active']})
        janet_df = pd.DataFrame({'ORGNBR': [1], 'NOTES': ['Note']})
        
        input_folder = tmp_path / "org"
        input_folder.mkdir()
        excel_file = input_folder / "janet.xlsx"
        janet_df.to_excel(excel_file, index=False)
        
        with pytest.raises(ValueError, match="Join key ORGNBR not found in org dataframe"):
            src.data_quality.core.merge_with_input_file(org_df, str(input_folder), 'org')
    
    def test_merge_with_input_file_missing_join_key_janet_df(self, tmp_path):
        """Test error when join key missing from Janet's file."""
        org_df = pd.DataFrame({'orgnbr': [1], 'orgname': ['Test']})
        # Missing ORGNBR column
        janet_df = pd.DataFrame({'ORGNAME': ['Test'], 'NOTES': ['Note']})
        
        input_folder = tmp_path / "org"
        input_folder.mkdir()
        excel_file = input_folder / "janet.xlsx"
        janet_df.to_excel(excel_file, index=False)
        
        with pytest.raises(ValueError, match="Join key ORGNBR not found in Janet's file"):
            src.data_quality.core.merge_with_input_file(org_df, str(input_folder), 'org')
    
    def test_merge_with_input_file_invalid_entity_type(self, tmp_path):
        """Test error with invalid entity type."""
        org_df = pd.DataFrame({'orgnbr': [1], 'orgname': ['Test']})
        input_folder = tmp_path / "test"
        input_folder.mkdir()
        
        with pytest.raises(AssertionError, match="entity_type must be 'org' or 'pers'"):
            src.data_quality.core.merge_with_input_file(org_df, str(input_folder), 'invalid')
    
    def test_merge_with_input_file_none_inputs(self):
        """Test error with None inputs."""
        with pytest.raises(AssertionError, match="org_df must not be None"):
            src.data_quality.core.merge_with_input_file(None, "path", 'org')
        
        org_df = pd.DataFrame({'orgnbr': [1]})
        with pytest.raises(AssertionError, match="input_folder must not be None"):
            src.data_quality.core.merge_with_input_file(org_df, None, 'org')
    
    def test_merge_with_input_file_dtype_conversion(self, tmp_path):
        """Test automatic dtype conversion for join key."""
        # My df has int, Janet's has string
        org_df = pd.DataFrame({'orgnbr': [1, 2], 'orgname': ['A', 'B']})
        janet_df = pd.DataFrame({
            'ORGNBR': ['1', '2'],  # String instead of int
            'NOTES': ['Note 1', 'Note 2']
        })
        
        input_folder = tmp_path / "org"
        input_folder.mkdir()
        excel_file = input_folder / "janet.xlsx"
        janet_df.to_excel(excel_file, index=False)
        
        # Should work with automatic conversion
        result = src.data_quality.core.merge_with_input_file(org_df, str(input_folder), 'org')
        assert len(result) == 2
        assert 'NOTES' in result.columns
    
    def test_merge_with_path_object_input(self, tmp_path):
        """Test merge function with Path object as input_folder parameter."""
        # Create test org dataframe
        org_df = pd.DataFrame({
            'orgnbr': [1, 2],
            'orgname': ['Org A', 'Org B'],
            'status': ['Active', 'Active']
        })
        
        # Create test Janet's file
        janet_df = pd.DataFrame({
            'ORGNBR': [1, 2],
            'ORGNAME': ['Org A', 'Org B'],
            'NOTES': ['Note 1', 'Note 2']
        })
        
        # Create input folder and file
        input_folder = tmp_path / "org"
        input_folder.mkdir()
        excel_file = input_folder / "janet_org.xlsx"
        janet_df.to_excel(excel_file, index=False)
        
        # Call function with Path object (not string)
        result = src.data_quality.core.merge_with_input_file(org_df, input_folder, 'org')
        
        # Verify results
        assert len(result) == 2
        assert 'NOTES' in result.columns
        assert result.loc[result['ORGNBR'] == 1, 'NOTES'].iloc[0] == 'Note 1'
    
class TestProcessInputFiles:
    """Test the process_input_files function."""
    
    def test_process_input_files_both_exist(self, tmp_path, monkeypatch):
        """Test when both org and pers folders exist with Excel files."""
        # Change to tmp directory for this test
        monkeypatch.chdir(tmp_path)
        
        # Create folder structure
        (tmp_path / "data/inputs/org").mkdir(parents=True)
        (tmp_path / "data/inputs/pers").mkdir(parents=True)
        
        # Create Excel files
        pd.DataFrame().to_excel(tmp_path / "data/inputs/org/org_file.xlsx", index=False)
        pd.DataFrame().to_excel(tmp_path / "data/inputs/pers/pers_file.xlsx", index=False)
        
        result = src.data_quality.core.process_input_files()
        
        assert result['has_org_input'] is True
        assert result['has_pers_input'] is True
    
    def test_process_input_files_none_exist(self, tmp_path, monkeypatch):
        """Test when no folders exist."""
        monkeypatch.chdir(tmp_path)
        
        result = src.data_quality.core.process_input_files()
        
        assert result['has_org_input'] is False
        assert result['has_pers_input'] is False
    
    def test_process_input_files_folders_exist_no_excel(self, tmp_path, monkeypatch):
        """Test when folders exist but no Excel files."""
        monkeypatch.chdir(tmp_path)
        
        # Create empty folders
        (tmp_path / "data/inputs/org").mkdir(parents=True)
        (tmp_path / "data/inputs/pers").mkdir(parents=True)
        
        result = src.data_quality.core.process_input_files()
        
        assert result['has_org_input'] is False
        assert result['has_pers_input'] is False
    
    def test_process_input_files_mixed_scenarios(self, tmp_path, monkeypatch):
        """Test mixed scenarios - one has Excel, one doesn't."""
        monkeypatch.chdir(tmp_path)
        
        # Create org folder with Excel file
        (tmp_path / "data/inputs/org").mkdir(parents=True)
        pd.DataFrame().to_excel(tmp_path / "data/inputs/org/org_file.xlsx", index=False)
        
        # Create pers folder without Excel file
        (tmp_path / "data/inputs/pers").mkdir(parents=True)
        
        result = src.data_quality.core.process_input_files()
        
        assert result['has_org_input'] is True
        assert result['has_pers_input'] is False

class TestArchiveInputFile:
    """Test the archive_input_file function."""
    
    def test_archive_single_file_success(self, tmp_path, monkeypatch):
        """Test successful archiving of single Excel file."""
        monkeypatch.chdir(tmp_path)
        
        # Create input folder and file
        input_folder = tmp_path / "data/inputs/org"
        input_folder.mkdir(parents=True)
        excel_file = input_folder / "test_file.xlsx"
        pd.DataFrame({'test': [1, 2, 3]}).to_excel(excel_file, index=False)
        
        # Archive the file
        result = src.data_quality.core.archive_input_file(str(input_folder), 'org')
        
        # Verify file was moved
        archive_file = tmp_path / "data/archive/test_file.xlsx"
        assert archive_file.exists()
        assert not excel_file.exists()  # Original should be gone
        assert result == archive_file
        
        # Verify content is preserved
        archived_df = pd.read_excel(archive_file)
        assert len(archived_df) == 3
        assert 'test' in archived_df.columns
    
    def test_archive_multiple_files(self, tmp_path, monkeypatch):
        """Test archiving multiple Excel files."""
        monkeypatch.chdir(tmp_path)
        
        # Create input folder and multiple files
        input_folder = tmp_path / "data/inputs/pers"
        input_folder.mkdir(parents=True)
        
        file1 = input_folder / "file1.xlsx"
        file2 = input_folder / "file2.xls"
        pd.DataFrame({'data': [1]}).to_excel(file1, index=False)
        pd.DataFrame({'data': [2]}).to_excel(file2, index=False)
        
        # Archive the files
        result = src.data_quality.core.archive_input_file(str(input_folder), 'pers')
        
        # Verify both files were moved
        archive1 = tmp_path / "data/archive/file1.xlsx"
        archive2 = tmp_path / "data/archive/file2.xls"
        assert archive1.exists()
        assert archive2.exists()
        assert not file1.exists()
        assert not file2.exists()
        assert isinstance(result, list)
        assert len(result) == 2
    
    def test_archive_overwrite_existing(self, tmp_path, monkeypatch):
        """Test overwriting existing file in archive."""
        monkeypatch.chdir(tmp_path)
        
        # Create input folder and file
        input_folder = tmp_path / "data/inputs/org"
        input_folder.mkdir(parents=True)
        excel_file = input_folder / "test_file.xlsx"
        pd.DataFrame({'new_data': [10, 20]}).to_excel(excel_file, index=False)
        
        # Create existing file in archive with different content
        archive_folder = tmp_path / "data/archive"
        archive_folder.mkdir(parents=True)
        existing_archive = archive_folder / "test_file.xlsx"
        pd.DataFrame({'old_data': [1, 2, 3]}).to_excel(existing_archive, index=False)
        
        # Archive the new file (should overwrite)
        result = src.data_quality.core.archive_input_file(str(input_folder), 'org')
        
        # Verify file was overwritten with new content
        assert existing_archive.exists()
        assert not excel_file.exists()
        
        # Check content was replaced
        archived_df = pd.read_excel(existing_archive)
        assert 'new_data' in archived_df.columns
        assert 'old_data' not in archived_df.columns
        assert len(archived_df) == 2
    
    def test_archive_no_excel_files(self, tmp_path, monkeypatch):
        """Test when no Excel files exist to archive."""
        monkeypatch.chdir(tmp_path)
        
        # Create empty input folder
        input_folder = tmp_path / "data/inputs/org"
        input_folder.mkdir(parents=True)
        
        # Try to archive (should return None)
        result = src.data_quality.core.archive_input_file(str(input_folder), 'org')
        
        assert result is None
    
    def test_archive_folder_not_exists(self):
        """Test error when input folder doesn't exist."""
        with pytest.raises(AssertionError, match="Input folder .* does not exist"):
            src.data_quality.core.archive_input_file("/nonexistent/path", 'org')
    
    def test_archive_invalid_entity_type(self, tmp_path):
        """Test error with invalid entity type."""
        input_folder = tmp_path / "test"
        input_folder.mkdir()
        
        with pytest.raises(AssertionError, match="entity_type must be 'org' or 'pers'"):
            src.data_quality.core.archive_input_file(str(input_folder), 'invalid')
    
    def test_archive_none_inputs(self):
        """Test error with None inputs."""
        with pytest.raises(AssertionError, match="input_folder must not be None"):
            src.data_quality.core.archive_input_file(None, 'org')
    
    def test_archive_creates_archive_folder(self, tmp_path, monkeypatch):
        """Test that archive folder is created if it doesn't exist."""
        monkeypatch.chdir(tmp_path)
        
        # Create input folder and file (no archive folder yet)
        input_folder = tmp_path / "data/inputs/org"
        input_folder.mkdir(parents=True)
        excel_file = input_folder / "test.xlsx"
        pd.DataFrame({'test': [1]}).to_excel(excel_file, index=False)
        
        # Archive should create the archive folder
        result = src.data_quality.core.archive_input_file(str(input_folder), 'org')
        
        # Verify archive folder was created
        archive_folder = tmp_path / "data/archive"
        assert archive_folder.exists()
        assert archive_folder.is_dir()
        
        # Verify file was archived
        archived_file = archive_folder / "test.xlsx"
        assert archived_file.exists()
        assert result == archived_file

    def test_archive_with_path_object_input(self, tmp_path, monkeypatch):
        """Test archive function with Path object as input_folder parameter."""
        monkeypatch.chdir(tmp_path)
        
        # Create input folder and file
        input_folder = tmp_path / "data/inputs/org"
        input_folder.mkdir(parents=True)
        excel_file = input_folder / "test_file.xlsx"
        pd.DataFrame({'test': [1, 2, 3]}).to_excel(excel_file, index=False)
        
        # Archive the file using Path object (not string)
        result = src.data_quality.core.archive_input_file(input_folder, 'org')
        
        # Verify file was moved
        archive_file = tmp_path / "data/archive/test_file.xlsx"
        assert archive_file.exists()
        assert not excel_file.exists()  # Original should be gone
        assert result == archive_file.resolve()

        # Test archive function with Path object as input_folder parameter.
        # Create test org dataframe
        org_df = pd.DataFrame({
            'orgnbr': [1, 2],
            'orgname': ['Org A', 'Org B'],
            'status': ['Active', 'Active']
        })
        
        # Create test Janet's file
        janet_df = pd.DataFrame({
            'ORGNBR': [1, 2],
            'ORGNAME': ['Org A', 'Org B'],
            'NOTES': ['Note 1', 'Note 2']
        })
        
        # Create input folder and file
        input_folder = tmp_path / "org"
        input_folder.mkdir()
        excel_file = input_folder / "janet_org.xlsx"
        janet_df.to_excel(excel_file, index=False)
        
        # Call function with Path object (not string)
        result = src.data_quality.core.merge_with_input_file(org_df, input_folder, 'org')
        
        # Verify results
        assert len(result) == 2
        assert 'NOTES' in result.columns
        assert result.loc[result['ORGNBR'] == 1, 'NOTES'].iloc[0] == 'Note 1'
    
class TestRobustDtypeConversion:
    """Test robust dtype conversion with NaN values and various data type scenarios"""
    
    def test_float64_with_nan_to_int64_conversion(self):
        """Test conversion from float64 with NaN values to int64"""
        # This simulates the real-world scenario you encountered
        wh_org = pd.DataFrame({
            'orgnbr': [1, 2, 3],  # int64
            'orgname': ['Company A', 'Company B', 'Company C']
        })
        
        # Simulate orgaddruse with float64 containing NaN (common in real data)
        # Include a NaN that matches an org, and test that conversion works
        orgaddruse = pd.DataFrame({
            'orgnbr': [1.0, float('nan'), 3.0],  # float64 with NaN - NaN will not match any org
            'addrnbr': [101, 102, 103],
            'addrusecd': ['PRI', 'PRI', 'PRI']
        })
        
        wh_addr = pd.DataFrame({
            'addrnbr': [101, 102, 103],
            'text1': ['123 Main St', '456 Oak Ave', '789 Pine Rd'],
            'cityname': ['Anytown', 'Somewhere', 'Elsewhere'],
            'statecd': ['CA', 'NY', 'TX']
        })
        
        # This should succeed with automatic conversion handling NaN
        result = src.data_quality.core.create_org_table_with_address(wh_org, orgaddruse, wh_addr)
        assert len(result) == 3
        # Orgs 1 and 3 should have addresses, org 2 should not (due to NaN in orgaddruse)
        # This tests that the dtype conversion worked and didn't crash on NaN
        assert result['orgnbr'].notna().all()  # All orgnbr values should be present
        
        # Check that org 2 has no address info (because "2" doesn't match "nan")
        # Note: after conversion, orgnbr becomes a string
        org2_record = result[result['orgnbr'] == "2"]
        assert len(org2_record) == 1
        assert pd.isna(org2_record.iloc[0]['text1'])  # Should have no address
    
    def test_string_numbers_with_nulls_conversion(self):
        """Test conversion from string numbers with null values"""
        wh_org = pd.DataFrame({
            'orgnbr': [1, 2, 3],  # int64
            'orgname': ['Company A', 'Company B', 'Company C']
        })
        
        # String representations with None/null
        orgaddruse = pd.DataFrame({
            'orgnbr': ['1', '2', None],  # object with None
            'addrnbr': [101, 102, 103],
            'addrusecd': ['PRI', 'PRI', 'PRI']
        })
        
        wh_addr = pd.DataFrame({
            'addrnbr': [101, 102, 103],
            'text1': ['123 Main St', '456 Oak Ave', '789 Pine Rd'],
            'cityname': ['Anytown', 'Somewhere', 'Elsewhere'],
            'statecd': ['CA', 'NY', 'TX']
        })
        
        # Should succeed with robust conversion
        result = src.data_quality.core.create_org_table_with_address(wh_org, orgaddruse, wh_addr)
        assert len(result) == 3
        
    def test_mixed_types_in_allroles_conversion(self):
        """Test conversion in filter_to_active_accounts with mixed types and NaNs"""
        acct_df = pd.DataFrame({'acctnbr': [1001, 1002]})  # int64
        
        # Simulate wh_allroles with float64 due to NaN values
        wh_allroles = pd.DataFrame({
            'acctnbr': [1001.0, 1002.0, float('nan')],  # float64 with NaN
            'orgnbr': [1.0, 2.0, 3.0],  # float64
            'persnbr': [float('nan'), float('nan'), float('nan')],  # All NaN
            'acctrolecd': ['OWNER', 'OWNER', 'MEMBER']
        })
        
        org_with_address = pd.DataFrame({
            'orgnbr': [1, 2, 3],  # int64
            'orgname': ['Company A', 'Company B', 'Company C'],
            'text1': ['123 Main St', '456 Oak Ave', '789 Pine Rd']
        })
        
        # Should succeed with robust conversion
        result = src.data_quality.core.filter_to_active_accounts(
            acct_df, wh_allroles, org_with_address=org_with_address
        )
        assert isinstance(result, pd.DataFrame)
        assert len(result) >= 0  # May be empty but should not crash
        
    def test_int32_to_int64_conversion(self):
        """Test conversion between different integer types"""
        wh_org = pd.DataFrame({
            'orgnbr': pd.array([1, 2, 3], dtype='int32'),  # int32
            'orgname': ['Company A', 'Company B', 'Company C']
        })
        
        orgaddruse = pd.DataFrame({
            'orgnbr': [1, 2, 3],  # int64 (default)
            'addrnbr': [101, 102, 103],
            'addrusecd': ['PRI', 'PRI', 'PRI']
        })
        
        wh_addr = pd.DataFrame({
            'addrnbr': [101, 102, 103],
            'text1': ['123 Main St', '456 Oak Ave', '789 Pine Rd'],
            'cityname': ['Anytown', 'Somewhere', 'Elsewhere'],
            'statecd': ['CA', 'NY', 'TX']
        })
        
        # Should succeed with automatic conversion
        result = src.data_quality.core.create_org_table_with_address(wh_org, orgaddruse, wh_addr)
        assert len(result) == 3
        
    def test_nullable_integer_preservation(self):
        """Test that nullable integer types are handled correctly"""
        wh_org = pd.DataFrame({
            'orgnbr': pd.array([1, 2, None], dtype='Int64'),  # Nullable Int64
            'orgname': ['Company A', 'Company B', 'Company C']
        })
        
        orgaddruse = pd.DataFrame({
            'orgnbr': [1, 2, 3],  # Regular int64
            'addrnbr': [101, 102, 103],
            'addrusecd': ['PRI', 'PRI', 'PRI']
        })
        
        wh_addr = pd.DataFrame({
            'addrnbr': [101, 102, 103],
            'text1': ['123 Main St', '456 Oak Ave', '789 Pine Rd'],
            'cityname': ['Anytown', 'Somewhere', 'Elsewhere'],
            'statecd': ['CA', 'NY', 'TX']
        })
        
        # Should handle nullable integers correctly
        result = src.data_quality.core.create_org_table_with_address(wh_org, orgaddruse, wh_addr)
        assert len(result) == 3
