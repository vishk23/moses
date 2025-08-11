import pytest
import pandas as pd
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
from lxml import html
import sys
import os
# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from ingest import (
    extract_standardized_report_data,
    extract_table_data,
    process_xls_files
)
class TestExtractStandardizedReportData:
    """Test cases for extract_standardized_report_data function."""
    
    def test_extract_with_valid_html_data(self):
        """Test extraction with valid HTML containing report data."""
        html_content = """
        <html>
            <body>
                <span class="date">Report Creation Date : 01/15/2024 10:30:00</span>
                <tr>
                    <td>
                        <span class="SummaryTitle clientnameSmall">Customer Name : Test Customer 1</span>
                        <table class="uk-table uk-table-striped">
                            <tr>
                                <th>Covenant Name</th>
                                <th>Required Value</th>
                                <th>Actual Value</th>
                                <th>Period Date</th>
                                <th>Due Date</th>
                                <th>Days Past Due</th>
                                <th>Comments</th>
                            </tr>
                            <tr>
                                <td>Debt Service Coverage</td>
                                <td>1.25</td>
                                <td>1.30</td>
                                <td>12/31/2023</td>
                                <td>01/30/2024</td>
                                <td>0</td>
                                <td>In compliance</td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </body>
        </html>
        """
        
        tree = html.fromstring(html_content)
        result = extract_standardized_report_data(tree, "Test Report")
        
        assert result is not None
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        
        # Check standardized columns exist
        expected_columns = [
            'customer_name', 'item_name', 'required_value', 'actual_value',
            'period_date', 'due_date', 'days_past_due', 'interval', 'comments',
            'report_type', 'report_date'
        ]
        for col in expected_columns:
            assert col in result.columns
        
        # Check data values
        row = result.iloc[0]
        assert row['customer_name'] == 'Test Customer 1'
        assert row['item_name'] == 'Debt Service Coverage'
        assert row['required_value'] == '1.25'
        assert row['actual_value'] == '1.30'
        assert row['period_date'] == '12/31/2023'
        assert row['due_date'] == '01/30/2024'
        assert row['days_past_due'] == '0'
        assert row['comments'] == 'In compliance'
        assert row['report_type'] == 'Test Report'
        assert row['report_date'] == '01/15/2024'
    
    def test_extract_multiple_customers(self):
        """Test extraction with multiple customers."""
        html_content = """
        <html>
            <body>
                <span class="date">Report Creation Date : 02/01/2024 09:00:00</span>
                <tr>
                    <td>
                        <span class="SummaryTitle clientnameSmall">Customer Name : Customer A</span>
                        <table class="uk-table uk-table-striped">
                            <tr><th>Covenant Name</th><th>Required Value</th></tr>
                            <tr><td>Ratio 1</td><td>2.0</td></tr>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="SummaryTitle clientnameSmall">Customer Name : Customer B</span>
                        <table class="uk-table uk-table-striped">
                            <tr><th>Covenant Name</th><th>Required Value</th></tr>
                            <tr><td>Ratio 2</td><td>1.5</td></tr>
                        </table>
                    </td>
                </tr>
            </body>
        </html>
        """
        
        tree = html.fromstring(html_content)
        result = extract_standardized_report_data(tree, "Multi Customer Report")
        
        assert result is not None
        assert len(result) == 2
        assert 'Customer A' in result['customer_name'].values
        assert 'Customer B' in result['customer_name'].values
        assert len(result['customer_name'].unique()) == 2
    
    def test_extract_no_date_element(self):
        """Test extraction when no date element is present."""
        html_content = """
        <html>
            <body>
                <tr>
                    <td>
                        <span class="SummaryTitle clientnameSmall">Customer Name : Test Customer</span>
                        <table class="uk-table uk-table-striped">
                            <tr><th>Covenant Name</th></tr>
                            <tr><td>Test Covenant</td></tr>
                        </table>
                    </td>
                </tr>
            </body>
        </html>
        """
        
        tree = html.fromstring(html_content)
        result = extract_standardized_report_data(tree, "No Date Report")
        
        assert result is not None
        assert result.iloc[0]['report_date'] is None
    
    def test_extract_no_covenant_data(self):
        """Test extraction when no covenant data is found."""
        html_content = """
        <html>
            <body>
                <span class="date">Report Creation Date : 01/15/2024 10:30:00</span>
                <p>No covenant data available</p>
            </body>
        </html>
        """
        
        tree = html.fromstring(html_content)
        result = extract_standardized_report_data(tree, "Empty Report")
        
        assert result is None
    
    def test_extract_empty_rows_skipped(self):
        """Test that empty rows are properly skipped."""
        html_content = """
        <html>
            <body>
                <tr>
                    <td>
                        <span class="SummaryTitle clientnameSmall">Customer Name : Test Customer</span>
                        <table class="uk-table uk-table-striped">
                            <tr><th>Covenant Name</th><th>Required Value</th></tr>
                            <tr><td>Valid Covenant</td><td>1.0</td></tr>
                            <tr><td></td><td></td></tr>
                            <tr><td>   </td><td>   </td></tr>
                        </table>
                    </td>
                </tr>
            </body>
        </html>
        """
        
        tree = html.fromstring(html_content)
        result = extract_standardized_report_data(tree, "Test Report")
        
        assert result is not None
        assert len(result) == 1  # Only one valid row
        assert result.iloc[0]['item_name'] == 'Valid Covenant'
    
    def test_extract_header_mapping(self):
        """Test that different header variations are properly mapped."""
        html_content = """
        <html>
            <body>
                <tr>
                    <td>
                        <span class="SummaryTitle clientnameSmall">Customer Name : Test Customer</span>
                        <table class="uk-table uk-table-striped">
                            <tr>
                                <th>Covenant Item</th>
                                <th>Required</th>
                                <th>Actual</th>
                                <th>Item Date</th>
                                <th>Interval</th>
                                <th>Comment</th>
                            </tr>
                            <tr>
                                <td>Test Item</td>
                                <td>2.0</td>
                                <td>2.1</td>
                                <td>12/31/2023</td>
                                <td>Quarterly</td>
                                <td>Good</td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </body>
        </html>
        """
        
        tree = html.fromstring(html_content)
        result = extract_standardized_report_data(tree, "Header Test")
        
        assert result is not None
        row = result.iloc[0]
        assert row['item_name'] == 'Test Item'
        assert row['required_value'] == '2.0'
        assert row['actual_value'] == '2.1'
        assert row['period_date'] == '12/31/2023'
        assert row['interval'] == 'Quarterly'
        assert row['comments'] == 'Good'
    
    def test_extract_exception_handling(self):
        """Test that exceptions are properly handled."""
        # Create an invalid tree object that will cause an exception
        with patch('builtins.print') as mock_print:
            result = extract_standardized_report_data(None, "Error Test")
            assert result is None
            mock_print.assert_called_with("Error extracting standardized report data: 'NoneType' object has no attribute 'xpath'")
class TestExtractTableData:
    """Test cases for extract_table_data function."""
    
    def test_extract_with_valid_table(self):
        """Test extraction with valid table data."""
        html_content = """
        <html>
            <body>
                <table class="uk-table uk-table-striped">
                    <tr>
                        <th>Column 1</th>
                        <th>Column 2</th>
                        <th>Column 3</th>
                    </tr>
                    <tr>
                        <td>Value 1</td>
                        <td>Value 2</td>
                        <td>Value 3</td>
                    </tr>
                    <tr>
                        <td>Value 4</td>
                        <td>Value 5</td>
                        <td>Value 6</td>
                    </tr>
                </table>
            </body>
        </html>
        """
        
        tree = html.fromstring(html_content)
        result = extract_table_data(tree, "Test Report")
        
        assert result is not None
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert len(result.columns) == 3
        assert list(result.columns) == ['Column 1', 'Column 2', 'Column 3']
        assert result.iloc[0]['Column 1'] == 'Value 1'
        assert result.iloc[1]['Column 3'] == 'Value 6'
    
    def test_extract_no_table_found(self):
        """Test when no table with the expected class is found."""
        html_content = """
        <html>
            <body>
                <table class="other-table">
                    <tr><th>Header</th></tr>
                    <tr><td>Data</td></tr>
                </table>
            </body>
        </html>
        """
        
        tree = html.fromstring(html_content)
        result = extract_table_data(tree, "No Table Report")
        
        assert result is None
    
    def test_extract_no_data_rows(self):
        """Test when table has headers but no data rows."""
        html_content = """
        <html>
            <body>
                <table class="uk-table uk-table-striped">
                    <tr>
                        <th>Header 1</th>
                        <th>Header 2</th>
                    </tr>
                </table>
            </body>
        </html>
        """
        
        tree = html.fromstring(html_content)
        result = extract_table_data(tree, "Empty Table Report")
        
        assert result is None
    
    def test_extract_mismatched_columns(self):
        """Test when data rows have different number of columns than headers."""
        html_content = """
        <html>
            <body>
                <table class="uk-table uk-table-striped">
                    <tr>
                        <th>Col 1</th>
                        <th>Col 2</th>
                        <th>Col 3</th>
                    </tr>
                    <tr>
                        <td>Val 1</td>
                        <td>Val 2</td>
                    </tr>
                    <tr>
                        <td>Val 3</td>
                        <td>Val 4</td>
                        <td>Val 5</td>
                        <td>Val 6</td>
                    </tr>
                </table>
            </body>
        </html>
        """
        
        tree = html.fromstring(html_content)
        result = extract_table_data(tree, "Mismatched Columns")
        
        assert result is not None
        assert len(result.columns) == 3
        assert len(result) == 2
        # First row should be padded with empty string
        assert result.iloc[0]['Col 3'] == ''
        # Second row should be truncated
        assert result.iloc[1]['Col 3'] == 'Val 5'

    def test_extract_no_headers_fallback(self):
        """Test fallback when no headers are found."""
        html_content = """
        <html>
            <body>
                <table class="uk-table uk-table-striped">
                    <tr>
                        <td>Data 1</td>
                        <td>Data 2</td>
                    </tr>
                    <tr>
                        <td>Data 3</td>
                        <td>Data 4</td>
                    </tr>
                </table>
            </body>
        </html>
        """
        
        tree = html.fromstring(html_content)
        result = extract_table_data(tree, "No Headers")
        
        assert result is not None
        assert len(result) == 1  # First row is treated as header when no <th> elements exist
        assert len(result.columns) == 2
        # Should have default column names (0, 1) or use first row as headers
        assert result.iloc[0][0] == 'Data 3' or result.iloc[0]['Data 1'] == 'Data 3'
    
    def test_extract_skip_empty_rows(self):
        """Test that empty rows are properly skipped."""
        html_content = """
        <html>
            <body>
                <table class="uk-table uk-table-striped">
                    <tr>
                        <th>Header</th>
                    </tr>
                    <tr>
                        <td>Valid Data</td>
                    </tr>
                    <tr>
                        <td></td>
                    </tr>
                    <tr>
                        <td>   </td>
                    </tr>
                    <tr>
                        <td>More Valid Data</td>
                    </tr>
                </table>
            </body>
        </html>
        """
        
        tree = html.fromstring(html_content)
        result = extract_table_data(tree, "Skip Empty Rows")
        
        assert result is not None
        assert len(result) == 2  # Only non-empty rows
        assert result.iloc[0]['Header'] == 'Valid Data'
        assert result.iloc[1]['Header'] == 'More Valid Data'
class TestProcessXlsFiles:
    """Test cases for process_xls_files function."""
    
    def test_process_with_valid_files(self, temp_assets_dir):
        """Test processing with valid test files."""
        # Change to temp directory for testing
        original_cwd = os.getcwd()
        temp_dir = temp_assets_dir.parent
        
        try:
            os.chdir(temp_dir)
            
            # Mock the HTML content reading and parsing
            with patch('builtins.open', mock_open(read_data='<html><body><span class="clientnameheading">Covenants Coming Due Within the Next 365 Days</span></body></html>')):
                with patch('ingest.extract_standardized_report_data') as mock_extract:
                    # Mock successful extraction
                    mock_df = pd.DataFrame([{
                        'customer_name': 'Test Customer',
                        'item_name': 'Test Covenant',
                        'required_value': '1.0',
                        'actual_value': '1.1',
                        'period_date': '12/31/2023',
                        'due_date': '01/31/2024',
                        'days_past_due': '0',
                        'interval': 'Monthly',
                        'comments': 'Test',
                        'report_type': 'covenants coming due within the next 365 days',
                        'report_date': '01/15/2024'
                    }])
                    mock_extract.return_value = mock_df
                    
                    result = process_xls_files()
                    
                    assert isinstance(result, dict)
                    assert 'covenants_coming_due_365' in result
                    assert isinstance(result['covenants_coming_due_365'], pd.DataFrame)
        
        finally:
            os.chdir(original_cwd)
    
    def test_process_empty_directory(self, empty_assets_dir):
        """Test processing with empty assets directory."""
        original_cwd = os.getcwd()
        temp_dir = empty_assets_dir.parent
        
        try:
            os.chdir(temp_dir)
            result = process_xls_files()
            
            assert isinstance(result, dict)
            assert len(result) == 0
        
        finally:
            os.chdir(original_cwd)
    
    def test_process_file_limit_validation(self, temp_assets_dir):
        """Test that file count validation works."""
        original_cwd = os.getcwd()
        temp_dir = temp_assets_dir.parent
        
        try:
            os.chdir(temp_dir)
            
            # Create 3 more .xls files to exceed the limit (temp_assets_dir already has 3)
            for i in range(3):
                (temp_assets_dir / f"extra_file_{i}.xls").touch()
            
            # Should have 6 files total now, exceeding the limit of 5
            with pytest.raises(AssertionError, match="Found .* .xls files, maximum is 5"):
                process_xls_files()
        
        finally:
            os.chdir(original_cwd)
    
    def test_process_non_xls_files_validation(self, temp_assets_dir):
        """Test that non-.xls files are rejected."""
        original_cwd = os.getcwd()
        temp_dir = temp_assets_dir.parent
        
        try:
            os.chdir(temp_dir)
            
            # Create a non-.xls file
            (temp_assets_dir / "invalid.txt").touch()
            
            with pytest.raises(AssertionError, match="Found non-.xls files"):
                process_xls_files()
        
        finally:
            os.chdir(original_cwd)
    
    def test_process_unknown_report_title(self, single_file_assets_dir):
        """Test processing file with unknown report title."""
        original_cwd = os.getcwd()
        temp_dir = single_file_assets_dir.parent
        
        try:
            os.chdir(temp_dir)
            
            with patch('builtins.open', mock_open(read_data='<html><body><span class="clientnameheading">Unknown Report Type</span></body></html>')):
                with patch('ingest.extract_standardized_report_data') as mock_extract:
                    mock_extract.return_value = None
                    
                    result = process_xls_files()
                    
                    assert isinstance(result, dict)
                    # Should not create any dataframes for unknown report types
                    assert len(result) == 0
        
        finally:
            os.chdir(original_cwd)
    
    def test_process_file_without_title(self, single_file_assets_dir):
        """Test processing file without report title."""
        original_cwd = os.getcwd()
        temp_dir = single_file_assets_dir.parent
        
        try:
            os.chdir(temp_dir)
            
            with patch('builtins.open', mock_open(read_data='<html><body><p>No title here</p></body></html>')):
                result = process_xls_files()
                
                assert isinstance(result, dict)
                # Should not create any dataframes without title
                assert len(result) == 0
        
        finally:
            os.chdir(original_cwd)
    
    def test_process_archive_functionality(self, single_file_assets_dir):
        """Test that files are properly moved to archive."""
        original_cwd = os.getcwd()
        temp_dir = single_file_assets_dir.parent
        
        try:
            os.chdir(temp_dir)
            
            # Get the original file
            original_files = list(single_file_assets_dir.glob('*.xls'))
            assert len(original_files) == 1
            original_file = original_files[0]
            
            with patch('builtins.open', mock_open(read_data='<html><body><span class="clientnameheading">Test Report</span></body></html>')):
                process_xls_files()
            
            # Check file was moved to archive
            assert not original_file.exists()
            archive_folder = single_file_assets_dir / 'archive'
            assert archive_folder.exists()
            archived_files = list(archive_folder.glob('*.xls'))
            assert len(archived_files) == 1
            assert archived_files[0].name == original_file.name
        
        finally:
            os.chdir(original_cwd)
    
    def test_process_new_report_mappings(self, empty_assets_dir):
        """Test that new report types are properly mapped."""
        original_cwd = os.getcwd()
        temp_dir = empty_assets_dir.parent
        
        try:
            os.chdir(temp_dir)
            
            test_cases = [
                ('Covenants 1 or More Days Past Due', 'covenants_past_due'),
                ('Covenants 1 or More Days in Default', 'covenants_in_default'),
                ('Ticklers Coming Due Within 365 Days', 'ticklers_coming_due_365'),
            ]
            
            for report_title, expected_key in test_cases:
                # Create a temporary file for this test case
                test_file = empty_assets_dir / f"test_{expected_key}.xls"
                test_file.touch()
                
                with patch('builtins.open', mock_open(read_data=f'<html><body><span class="clientnameheading">{report_title}</span></body></html>')):
                    with patch('ingest.extract_standardized_report_data') as mock_extract:
                        mock_df = pd.DataFrame([{'customer_name': 'Test', 'item_name': 'Test Item'}])
                        mock_extract.return_value = mock_df
                        
                        result = process_xls_files()
                        
                        assert expected_key in result
                        assert isinstance(result[expected_key], pd.DataFrame)
                
                # Clean up for next iteration
                if test_file.exists():
                    test_file.unlink()
        
        finally:
            os.chdir(original_cwd)
    
    @patch('ingest.shutil.move')
    @patch('builtins.open')
    def test_process_file_read_error_handling(self, mock_open_func, mock_move, single_file_assets_dir):
        """Test error handling when file reading fails."""
        original_cwd = os.getcwd()
        temp_dir = single_file_assets_dir.parent
        
        try:
            os.chdir(temp_dir)
            
            # Mock file reading to raise an exception
            mock_open_func.side_effect = IOError("File read error")
            
            result = process_xls_files()
            
            # Should still return a dict even with errors
            assert isinstance(result, dict)
            # Files should still be moved to archive despite errors
            assert mock_move.called
        
        finally:
            os.chdir(original_cwd)
class TestIntegration:
    """Integration tests using real test fixtures."""
    
    def test_real_fixture_files(self):
        """Test with actual fixture files to ensure they can be parsed."""
        fixtures_dir = Path(__file__).parent / "fixtures"
        
        for fixture_file in fixtures_dir.glob("*.xls"):
            try:
                with open(fixture_file, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                tree = html.fromstring(html_content)
                
                # Test both extraction functions
                result1 = extract_standardized_report_data(tree, f"Test - {fixture_file.name}")
                result2 = extract_table_data(tree, f"Test - {fixture_file.name}")
                
                # At least one should work or both should handle gracefully
                if result1 is not None:
                    assert isinstance(result1, pd.DataFrame)
                    # Check that standardized columns exist
                    expected_columns = [
                        'customer_name', 'item_name', 'required_value', 'actual_value',
                        'period_date', 'due_date', 'days_past_due', 'interval', 'comments',
                        'report_type', 'report_date'
                    ]
                    for col in expected_columns:
                        assert col in result1.columns
                
                if result2 is not None:
                    assert isinstance(result2, pd.DataFrame)
                    assert len(result2.columns) > 0
                
            except Exception as e:
                pytest.fail(f"Failed to process fixture {fixture_file.name}: {str(e)}")
    
    def test_dataframe_mappings_coverage(self):
        """Test that the dataframe mappings in process_xls_files cover expected report types."""
        # Get the function's source to check mappings
        import inspect
        source = inspect.getsource(process_xls_files)
        
        # Verify key mappings exist
        assert 'covenants coming due within the next 365 days' in source
        assert 'covenants_coming_due_365' in source
        assert 'covenants 1 or more days past due' in source
        assert 'covenants_past_due' in source
        assert 'covenants 1 or more days in default' in source
        assert 'covenants_in_default' in source
        assert 'ticklers coming due within 365 days' in source
        assert 'ticklers_coming_due_365' in source
if __name__ == "__main__":
    # Run tests with: python -m pytest tests/test_ingest.py -v
    pytest.main([__file__])