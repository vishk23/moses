"""
Main Entry Point
"""
from pathlib import Path
from typing import List
from datetime import datetime

import os
import shutil

import pandas as pd # type: ignore

import src.fetch_data # type: ignore
import src.core_transform # type: ignore
import cdutils.pkey_sqlite # type: ignore
import cdutils.hhnbr # type: ignore
import src.output_to_excel
import cdutils.loans.calculations # type: ignore
# import cdutils.selo # type: ignore
from src._version import __version__
from src.config import BASE_PATH


def main():

    data = src.fetch_data.fetch_data()
    raw_data = data['wh_acctcommon']


    filename = 'staging_data.xlsx'

    
    OUTPUT_PATH = BASE_PATH / Path('./assets/staged_data') / Path(filename)
    
    directory = BASE_PATH / Path('./assets')
    files = [file.name for file in directory.glob("*.xlsx")]

    assert len(files) == 1, ("There should only be one file .xlsx file in " +
                            "\\00-DA1\Home\Share\\Data & Analytics Initiatives\\Project Management\\Operations\\LoanPayoffQuotes\\Production\\assets")
    
    # appending currmiacctypcd to staging data
    file_to_move = files[0]
    src_path = BASE_PATH / Path('./assets/') / Path(file_to_move)
    given_data = pd.read_excel(src_path)
    raw_data = raw_data.rename(columns={'acctnbr': 'ACCTNBR',
                                        'currmiaccttypcd': 'CURRMIACCTTYPCD'})
    given_data['ACCTNBR'] = given_data['ACCTNBR'].astype(int)
    raw_data['ACCTNBR'] = raw_data['ACCTNBR'].astype(int)
    
    staging_data = pd.merge(given_data, raw_data, on='ACCTNBR', how='left')

    # moving given file to archive
    dest_path = BASE_PATH / Path('./assets/archive') / Path(file_to_move)
    shutil.move(src_path, dest_path)
    print(f"Moved {file_to_move} to archive directory.")

    # outputting and formatting staging data to staged_data directory
    staging_data.to_excel(OUTPUT_PATH, sheet_name='Sheet1', index=False)
    src.output_to_excel.format_excel_file(OUTPUT_PATH)


    # Distribution
    # recipients = [
    #     # "chad.doorley@bcsbmail.com",
    # ]
    # bcc_recipients = [
    #     "chad.doorley@bcsbmail.com",
    #     "businessintelligence@bcsbmail.com"
    # ]
    # subject = f"File Name" 
    # body = "Hi, \n\nAttached is your requested report. If you have any questions, please reach out to BusinessIntelligence@bcsbmail.com \n\nThanks!"
    # attachment_paths = [OUTPUT_PATH]
    # cdutils.distribution.email_out(recipients, bcc_recipients, subject, body, attachment_paths)


if __name__ == '__main__':
    print(f"Starting [{__version__}]")
    main()
    print("Complete!")

