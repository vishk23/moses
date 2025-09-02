"""
Main Entry Point
"""
from datetime import date
from dateutil.relativedelta import relativedelta
from pathlib import Path

import pandas as pd # type: ignore

import src.fetch_data
import src.core_transform
import cdutils.distribution # type: ignore
import src.output_to_excel
from src._version import __version__

def main(production_flag: bool=False):
    if production_flag:
        BASE_PATH = Path(r'\\00-DA1\Home\Share\Line of Business_Shared Services\Operations\Trial Balance Ops')
        assert "prod" in __version__, (f"Cannot run in production mode without 'prod' in the __version__")
    else:
        BASE_PATH = Path('.')
    data = src.fetch_data.fetch_data()

    # Core transformations
    raw_data_single = src.core_transform.main_pipeline(data)
    raw_data_multiple = src.core_transform.main_pipeline_multiple_prop(data)

    current_date = (date.today() + relativedelta(day=1) - relativedelta(days=1)).strftime('%Y%m%d')

    # Output to excel (raw data)
    OUTPUT_PATH_SINGLE = BASE_PATH / Path(f'./output/CML_Trial_Balance_Ops_{current_date}.xlsx')
    raw_data_single.to_excel(OUTPUT_PATH_SINGLE, sheet_name='Sheet1', index=False)

    # Output to excel (raw data)
    OUTPUT_PATH_MULTIPLE = BASE_PATH / Path(f'./output/CML_Trial_Balance_Ops_MultipleProperties_{current_date}.xlsx')
    raw_data_multiple.to_excel(OUTPUT_PATH_MULTIPLE, sheet_name='Sheet1', index=False)

    # Format excel
    src.output_to_excel.format_excel_file(OUTPUT_PATH_SINGLE)
    src.output_to_excel.format_excel_file(OUTPUT_PATH_MULTIPLE)

    # Distribution
    recipients = [
        # "chad.doorley@bcsbmail.com"
        "kelly.abernathy@bcsbmail.com",
        "Zachary.Cabral@bcsbmail.com",
        "kelly.masefield@bcsbmail.com"
    ]
    bcc_recipients = [
        "chad.doorley@bcsbmail.com",
        "businessintelligence@bcsbmail.com"
    ]
    attachment_paths = [
        OUTPUT_PATH_SINGLE,
        OUTPUT_PATH_MULTIPLE
    ]
    subject=f"Trial Balance ME Reports - {current_date}"
    body = "Hi all, \n\nAttached are the Trial Balance reports. If you have any questions, please reach out to BusinessIntelligence@bcsbmail.com\n\n There is a new version of this coming soon with an expanded list of fields. That will be in place for future runs."

    cdutils.distribution.email_out(
        recipients = recipients, 
        bcc_recipients = bcc_recipients, 
        subject = subject, 
        body = body, 
        attachment_paths = attachment_paths
        )


if __name__ == '__main__':
    print(f"Starting [{__version__}]")
    # main(production_flag=True)
    main()
    print("Complete!")

