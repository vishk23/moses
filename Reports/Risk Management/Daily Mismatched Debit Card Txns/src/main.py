"""
Main Entry Point
"""
import pandas as pd
import numpy as np

from pathlib import Path
from openpyxl import load_workbook

import os
import shutil
from src._version import __version__
from src.config import BASE_PATH, INPUT_DIR, OUTPUT_DIR
from src.daily_mismatch_txns.api_call import (
    kwyk_search_first_pkid,
    download_document,
)


def main():
    ASSETS_PATH = BASE_PATH / Path('./assets')
    # Ensure assets folder exists and fetch latest CO_VSUS file into it
    ASSETS_PATH.mkdir(parents=True, exist_ok=True)
    try:
        pkid, _results = kwyk_search_first_pkid("CO_VSUS", results_limit=100)
        if pkid:
            dest_file = ASSETS_PATH / f"CO_VSUS_{pkid}.prn"
            download_document(pkid, dest_file, storage_type_id=1)
            print(f"Downloaded CO_VSUS document to: {dest_file}")
        else:
            print("No CO_VSUS documents found via API search.")
    except Exception as e:
        # Non-fatal: continue with local processing even if API fetch fails
        print(f"Warning: API fetch skipped/failed: {e}")
    
    # ensure there is only one txt file in specified location
    txt_files = [file.name for file in INPUT_DIR.glob("*.txt")]
    assert len(txt_files) == 1, ("There should only be one file .txt file in " +
                            str(INPUT_DIR))
    file_to_move = txt_files[0]
    input_src_path = INPUT_DIR / Path(file_to_move)


    column_names = [
        "Card Nbr",
        "Acct Nbr",
        "Trans Amt",
        "RTXN Typ",
        "RetRefNbr",
        "Comment",
        "Merchant"
    ]

    column_widths = [16, 20, 18, 18, 12, 35, 40]

    df = pd.read_fwf(
        input_src_path,
        widths=column_widths,
        names=column_names,
        encoding='latin1'
    )

    input1 = df.copy()
    input2 = df.copy()

    input1 = input1[input1['Card Nbr'].str.contains('5', na=False)]
    input1['Card and Acct and Tran Amt'] = input1['Card Nbr'] + input1['Acct Nbr'] + input1['Trans Amt']

    summary_df = (
    input1.groupby('Card and Acct and Tran Amt')
    .size()
    .reset_index(name="Count")
)

    summary_df = summary_df[summary_df['Count'].isin([1, 3, 5, 7, 9])]

    merged_df = pd.merge(summary_df, input1, on="Card and Acct and Tran Amt", how="inner")
    merged_df = merged_df[['Card Nbr', 'Acct Nbr', 'Trans Amt', 'RTXN Typ', 'RetRefNbr', 'Merchant']]

    field_widths = [120, 10]
    field_names = ['Not Needed', 'Date']
    input2 = pd.read_fwf(
        input_src_path,
        widths=field_widths,
        names=field_names,
        encoding='latin1'
    )
    input2['RecordID'] = pd.Series(range(1, len(input2) + 1), dtype='int32')
    
    date_str = input2.at[1, 'Date']
    merged_df['Date'] = date_str
    merged_df['Source'] = "co_vsus re-run"
    
    merged_df['Trans Amt'] = pd.to_numeric(merged_df['Trans Amt'], errors="coerce")
    merged_df['Trans Amt'] = np.where(merged_df['RTXN Typ'] == "PWTH", 0 - merged_df['Trans Amt'], merged_df['Trans Amt'])

    merged_df = merged_df[['Card Nbr', 'Date', 'Source', 'Trans Amt', 'Acct Nbr', 'RTXN Typ', 'RetRefNbr', 'Merchant']]


    cardnbrs = list(merged_df['Card Nbr'])
    acctnbrs = list(merged_df['Acct Nbr'])
    amount = list(merged_df['Trans Amt'])
    deb_or_cred = []
    merchants = list(merged_df['Merchant'])

    for i in range(len(merged_df)):

        # left padding acctnbrs with 0s
        while len(acctnbrs[i]) < 12:
            acctnbrs[i] = '0' + acctnbrs[i]

        # determining if debit or credit based on sign of Trans Amt
        if amount[i] < 0:
            deb_or_cred.append("Debit")
            amount[i] = amount[i] * -1  # making all amounts positive
        elif amount[i] > 0:
            deb_or_cred.append("Credit")
        else:
            raise ValueError("Transaction amount of 0")
        
        # appending last 4 digits of card number to the merchant

        merchants[i] += f" ({cardnbrs[i][-4:]})"


    # move txt file to archive
    input_archive_path = INPUT_DIR / Path('./archive') / Path(file_to_move)
    shutil.move(input_src_path, input_archive_path)
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


    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # output_date_str = f"{today.month}.{today.day:02}.{today.year % 100:02}"
    # date_str = f"{today.month}/{today.day:02}/{today.year % 100:02}"
    filename = "Daily Posting Sheet " + date_str + ".xlsx"
    output_file = os.path.join(OUTPUT_DIR,filename)

    ws['C3'] = f"{date_str}"

    # before saving, move everything in output folder to output/archive
    for file in OUTPUT_DIR.glob("*.xlsx"):
        file_to_move = file.name
        src_path = OUTPUT_DIR / Path(file_to_move)
        output_archive_path = OUTPUT_DIR / Path('./archive') / Path(file_to_move)
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

