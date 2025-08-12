
"""
Main Entry Point for CT Dashboard (Covenant & Tickler tracking)
"""
import pandas as pd  # type: ignore
import numpy as np

import src.config
from src._version import __version__
from src.ct_dashboard import core


def main():
    """
    Main processing pipeline for CT Dashboard.
    
    Reads HTML export files from assets/, enriches with officer data,
    and outputs Excel tracking files for covenants and ticklers.
    """
    print(f"Starting CT Dashboard [{__version__}]")
    print(f"Report: {src.config.REPORT_NAME}")
    print(f"Business Line: {src.config.BUSINESS_LINE}")
    print(f"Owner: {src.config.OWNER}")
    print(f"Output Directory: {src.config.OUTPUT_DIR}")
    
    # Ensure output directory exists
    src.config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Run main business logic
    core.process_ct_dashboard()
    
    print("CT Dashboard processing complete!")


if __name__ == '__main__':
    main()

