"""
Example unit test for the main module.

This demonstrates how to import from the src/ directory using pathlib
and write basic unit tests with pytest.
"""

import sys
from pathlib import Path
from unittest.mock import patch
import pytest

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Now we can import from src/
import main
import config
import _version


class TestMain:
    """Test cases for the main module."""
    
    def test_version_import(self):
        """Test that version can be imported and has expected format."""
        assert hasattr(_version, '__version__')
        assert isinstance(_version.__version__, str)
        assert _version.__version__.startswith('v')
    
    def test_config_import(self):
        """Test that config can be imported and has required attributes."""
        required_attrs = ['REPORT_NAME', 'BUSINESS_LINE', 'SCHEDULE', 'OWNER', 'ENV', 'OUTPUT_DIR']
        for attr in required_attrs:
            assert hasattr(config, attr), f"Config missing required attribute: {attr}"
    
    @patch('builtins.print')
    def test_main_function_prints_version(self, mock_print):
        """Test that main function prints version information."""
        main.main()
        
        # Check that print was called with version information
        print_calls = [call.args[0] for call in mock_print.call_args_list]
        version_printed = any(_version.__version__ in call for call in print_calls)
        assert version_printed, "Version information not printed in main()"
    
    @patch('builtins.print')
    def test_main_function_prints_config(self, mock_print):
        """Test that main function prints configuration information."""
        main.main()
        
        # Check that key config values are printed
        print_calls = [call.args[0] for call in mock_print.call_args_list]
        config_items = [config.REPORT_NAME, config.BUSINESS_LINE, config.SCHEDULE, config.OWNER]
        
        for item in config_items:
            item_printed = any(str(item) in call for call in print_calls)
            assert item_printed, f"Config item '{item}' not printed in main()"


if __name__ == "__main__":
    pytest.main([__file__])
