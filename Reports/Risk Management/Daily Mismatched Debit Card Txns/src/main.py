"""
Main Entry Point
"""
from pathlib import Path
from typing import List
from datetime import datetime
from collections import deque
from openpyxl import load_workbook

import os
import shutil
from src._version import __version__
from src.config import BASE_PATH


def main():

    ASSETS_PATH = BASE_PATH / Path('./assets')
    INPUT_PATH = BASE_PATH / Path('./input')
    OUTPUT_PATH = BASE_PATH / Path('./output')

    # ensure there is only one txt file in specified location
    txt_files = [file.name for file in INPUT_PATH.glob("*.txt")]
    assert len(txt_files) == 1, ("There should only be one file .txt file in " +
                            str(INPUT_PATH))
    file_to_move = txt_files[0]
    output_date_str = file_to_move.split()[1]

    # read in txt file
    src_path = INPUT_PATH / Path(file_to_move)
    with open(src_path, "r") as txt_file:
        # txt_file = open(src_path, "r")
        content = txt_file.read()

        split_content = content.split()
        split_content = deque(split_content)

        # position head after first delimiter
        while '----' not in split_content[0]:
            split_content.popleft()
        split_content.popleft() # popping first delimiter

        acctnbrs = []
        amount = []
        merchants = []
        deb_or_cred = [] # dep = credit, wth = withdrawal
        initial_nums = []


        while split_content[0] != 'Credits':
            initial_nums.append(split_content[0])
            amount.append(split_content[1])
            if split_content[2] == 'DEP':
                deb_or_cred.append("Credit")
            else:
                deb_or_cred.append("Debit")
            acctnbrs.append(split_content[3])
            # i = 13
            # currMerchant = []
            # # covers edge case of multi-word merchant names
            # while '----' not in split_content[i]:
            #     currMerchant.append(split_content[i])
            #     i += 1
            # merchant = " ".join(currMerchant[:-1])
            # merchant += f" ({split_content[0][-4:]})"
            # merchants.append(merchant)
            # repositioning head at next section
            while '----' not in split_content[0]:
                split_content.popleft()
            split_content.popleft()
        
        # get merchants using this way due to inconsistensies in length of words for locations
        split_on_delim = content.split('----------------------------------------------------------------------------------------------')
        for section in split_on_delim[1:-1:]:
            merchants.append(' '.join(section[198:len(section):].split()[:-1:]))
        for i in range(len(merchants)):
            merchants[i] = merchants[i] + f" ({initial_nums[i][-4:]})"

    # move txt file to archive
    input_archive_path = INPUT_PATH / Path('./archive') / Path(file_to_move)
    shutil.move(src_path, input_archive_path)
    print(f"Moved {file_to_move} to input/archive directory.")


    # filling in template
    wb = load_workbook(ASSETS_PATH / Path("txtparser_template.xlsx"))
    ws = wb.active

    for i, value in enumerate(deb_or_cred):
        ws.cell(row=8+2*i, column=1, value=value)
    for i, value in enumerate(acctnbrs):
        ws.cell(row=8+2*i, column=3, value=value)
    for i, value in enumerate(amount):
        ws.cell(row=8+2*i, column=5, value=value)
    for i, value in enumerate(merchants):
        ws.cell(row=8+2*i, column=7, value=value)


    os.makedirs(OUTPUT_PATH, exist_ok=True)
    today = datetime.today()
    # output_date_str = f"{today.month}.{today.day:02}.{today.year % 100:02}"
    # date_str = f"{today.month}/{today.day:02}/{today.year % 100:02}"
    filename = "Daily Posting Sheet " + output_date_str + ".xlsx"
    output_file = os.path.join(OUTPUT_PATH,filename)

    ws['C3'] = f"{output_date_str}"

    # before saving, move everything in output folder to output/archive
    for file in OUTPUT_PATH.glob("*.xlsx"):
        file_to_move = file.name
        src_path = OUTPUT_PATH / Path(file_to_move)
        output_archive_path = OUTPUT_PATH / Path('./archive') / Path(file_to_move)
        shutil.move(src_path, output_archive_path)
        print(f"Moved {file_to_move} to output/archive directory.")

    # save spreadsheet to output directory
    wb.save(output_file)
    print(f"Report saved to {output_file}")



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

