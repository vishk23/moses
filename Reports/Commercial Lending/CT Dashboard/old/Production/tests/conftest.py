
import pytest
import shutil
import tempfile
from pathlib import Path
@pytest.fixture
def temp_assets_dir():
    """Create a temporary directory with test fixtures for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        assets_dir = Path(temp_dir) / "assets"
        assets_dir.mkdir()
        
        # Copy test fixtures to temporary assets directory
        fixtures_dir = Path(__file__).parent / "fixtures"
        for fixture_file in fixtures_dir.glob("*.xls"):
            shutil.copy(fixture_file, assets_dir)
        
        yield assets_dir
@pytest.fixture
def empty_assets_dir():
    """Create an empty temporary assets directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        assets_dir = Path(temp_dir) / "assets"
        assets_dir.mkdir()
        yield assets_dir
@pytest.fixture
def single_file_assets_dir():
    """Create a temporary assets directory with only one test file."""
    with tempfile.TemporaryDirectory() as temp_dir:
        assets_dir = Path(temp_dir) / "assets"
        assets_dir.mkdir()
        
        # Copy only one fixture file
        fixtures_dir = Path(__file__).parent / "fixtures"
        fixture_file = fixtures_dir / "covenant_coming_due_test_data_no_pii.xls"
        shutil.copy(fixture_file, assets_dir)
        
        yield assets_dir
