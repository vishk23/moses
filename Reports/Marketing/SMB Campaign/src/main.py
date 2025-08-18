"""
Main entry point for your project.

Replace this docstring with a description of your project's purpose and logic.
"""

import src.config
import src._version
import src.smb_campaing.core

def main():
    print(f"Running {src._version.__version__}")
    print(f"Running {src.config.REPORT_NAME} for {src.config.BUSINESS_LINE}")
    print(f"Schedule: {src.config.SCHEDULE}")
    print(f"Owner: {src.config.OWNER}")
    print(f"Environment: {src.config.ENV}")
    print(f"Output directory: {src.config.OUTPUT_DIR}")
    # Add your main project logic here

    df = src.smb_campaign.core.main_pipeline()

    # Add output path here
    # # %%
    # OUTPUT_PATH = Path("./output/bkm_suppresion_list.parquet")
    # merged_final.to_parquet(OUTPUT_PATH, index=False)


if __name__ == "__main__":
    main()