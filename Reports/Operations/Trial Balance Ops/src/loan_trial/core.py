# Core logic specific to project/report

import src.config
import pandas as pd
from deltalake import DeltaTable
from pathlib import Path

def main_pipeline():
    # Main loan data, silver table
    TABLE_PATH = src.config.SILVER / "account"
    accounts = DeltaTable(TABLE_PATH).to_pandas()

    # filter to 
    # acctnbr
    # ownersortname
    # mjaccttypcd
    # currmiaccttypcd
    # curracctstatcd
    # noteintrate
    # notebal
    # bookbalance
    # branchname
    # loanofficer
    # contractdate
    # datemat
    # notenextratechange (WH_ACCTCOMMON)
    # noteratechangecalpercd (WH_ACCTCOMMON)