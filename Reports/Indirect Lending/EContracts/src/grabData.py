from datetime import datetime
import os
import re
import pandas as pd
from src.config import INPUT_DIR

"""
Grabs daily reports and book to look and preps in "K:\E Contract Summary Report\Production\Input"
and preps them for merging.
"""
def grabData():
    
    # daily funding reports
    today = datetime.today()

    # finding the month and year of report we should be making

    current_year = today.year
    current_month = today.month

    if current_month == 1:
        previous_month = 12
        year_of_previous_month = current_year - 1
    else:
        previous_month = current_month - 1
        year_of_previous_month = current_year

    previous_month = datetime(year_of_previous_month, previous_month, 1).strftime("%B")
    
    pattern = re.compile(rf'^{previous_month}.*{year_of_previous_month}\.xls[x]?$')

    dataframes = []

    # looping through each file in directory
    for filename in os.listdir(INPUT_DIR):
        if pattern.match(filename):
            file_path = os.path.join(INPUT_DIR, filename)
            try:
                xls = pd.ExcelFile(file_path)
                for sheet_name in xls.sheet_names:
                    if 'folder' in sheet_name.lower():
                        funding_report = xls.parse(sheet_name=sheet_name)
                        
                        funding_report['source_file'] = filename
                        funding_report['source_sheet'] = sheet_name

                        filename_no_commas = filename.replace(",", "")
                        filename_no_commas = filename.replace(".", "")

                        date_obj = datetime.strptime(filename_no_commas[:-5], "%B %d %Y")
                        formatted_date = date_obj.strftime("%m/%d/%Y")

                        funding_report['Funded Date'] = formatted_date
                        
                        dataframes.append(funding_report)
                        print("Reading file: " + filename)
                        # if (filename == "March 13, 2025.xlsx"):
                        #     print(funding_report)
                if not any('folder' in sheetname.lower() for sheetname in xls.sheet_names):
                    print(f"Naming of sheets: {file_path} is inconsistent with expected naming convention."
                            + " This file may be in the wrong place.")
            except Exception as e:
                print(f"error reading {file_path}: {e}")

    # Concatenating all daily funding reports into one big dataframe
    if dataframes:
        combined_funding_reports = pd.concat(dataframes, ignore_index=True)
    else:
        print("No matching Excel files found.")

    
    

    
    # book to look
    curr_year_and_month = str(year_of_previous_month) + " " + previous_month
    # folder_path = "K:\E Contract Summary Report\Production\Input"

    pattern = re.compile(rf'^{curr_year_and_month}.*xls[x]?$')

    # finding relevant book to look in folder
    for filename in os.listdir(INPUT_DIR):
        if pattern.match(filename):
            print(filename)
            file_path = os.path.join(INPUT_DIR, filename)
            try:
                book_to_look = pd.read_excel(file_path)
            except Exception as e:
                print(f"error reading {file_path}: {e}")
    
    
    
    
    
    # cleaning up funding reports
    combined_funding_reports = combined_funding_reports.drop(combined_funding_reports.iloc[:, 15::].columns, axis=1)
    combined_funding_reports.columns = combined_funding_reports.iloc[1]

    combined_funding_reports.columns.values[14] = 'Funding Date'
    combined_funding_reports = combined_funding_reports.iloc[2:]
    # Normalizing dealer name column since we are joining on it later
    combined_funding_reports['Dealer Name'] = combined_funding_reports['Dealer Name'].str.strip().str.upper()
    combined_funding_reports.dropna(subset=['Dealer Name'], inplace=True)
    combined_funding_reports = combined_funding_reports[combined_funding_reports['Dealer Name'] != 'DEALER NAME']
    
    
    

    # cleaning up book to look
    book_to_look.columns = book_to_look.iloc[1]
    book_to_look = book_to_look.iloc[2:]
    book_to_look = book_to_look.rename(columns={'Dealer': 'Dealer Name'})
    # Normalizing dealer name column since we are joining on it later
    book_to_look['Dealer Name'] = book_to_look['Dealer Name'].str.strip().str.upper()
    book_to_look.dropna(subset=['Dealer Name'], inplace=True)
    
    return combined_funding_reports, book_to_look
