"""
Main entry point for your project.

Replace this docstring with a description of your project's purpose and logic.
"""

import src.config
import src._version
import src.deposit_dash_prototype.core
from deltalake import DeltaTable, write_deltalake
from src.utils.parquet_io import add_load_timestamp

def main():
    print(f"Running {src._version.__version__}")
    print(f"Running {src.config.REPORT_NAME} for {src.config.BUSINESS_LINE}")
    print(f"Schedule: {src.config.SCHEDULE}")
    print(f"Owner: {src.config.OWNER}")
    print(f"Environment: {src.config.ENV}")
    print(f"Output directory: {src.config.OUTPUT_DIR}")

    dim_account, fact_balances, portfolio = src.deposit_dash_prototype.core.main_pipeline()
    dim_account = add_load_timestamp(dim_account)
    fact_balances = add_load_timestamp(fact_balances)
    portfolio = add_load_timestamp(portfolio)

    # DeltaTable written and loaded into PowerBI
    # local C: Drive
    # PowerBI will point to this

    DIM_ACCOUNT_PATH = src.config.OUTPUT_DIR / "dim_account"
    DIM_ACCOUNT_PATH.parent.mkdir(parents=True, exist_ok=True)
    write_deltalake(DIM_ACCOUNT_PATH, dim_account, mode='overwrite', schema_mode='merge')

    FACT_BALANCES_PATH = src.config.OUTPUT_DIR / "fact_balances"
    FACT_BALANCES_PATH.parent.mkdir(parents=True, exist_ok=True)
    write_deltalake(FACT_BALANCES_PATH, fact_balances, mode='overwrite', schema_mode='merge')

    PORTFOLIO_PATH = src.config.OUTPUT_DIR / "portfolio_deriv"
    PORTFOLIO_PATH.parent.mkdir(parents=True, exist_ok=True)
    write_deltalake(PORTFOLIO_PATH, portfolio, mode='overwrite', schema_mode='merge')

if __name__ == "__main__":
    main()
