import pandas as pd
from datetime import datetime
import os
import re
import win32com.client as win32 # type: ignore
from pathlib import Path
from dateutil.relativedelta import relativedelta

from src._version import __version__
import src.grabData as grabData
import src.buildReport as buildReport
import src.exportReport as exportReport


def main() -> None:
    
    combined_funding_reports, book_to_look = grabData.grabData()

    merged_df = pd.merge(combined_funding_reports, book_to_look, on='Dealer Name')

    # changing Contract Type column to 0s and 1s to make later calculations easier
    merged_df['Contract Type'] = merged_df['Contract Type'] == 'E Contract'
    merged_df['Contract Type'] = merged_df['Contract Type'].astype(int)

    # if there is a mismatch in the number of rows from the merged dataframe and the combined funding reports, there is probably a mistake in the input data
    unmatched_combined_funding_reports = combined_funding_reports[~combined_funding_reports['Dealer Name'].isin(merged_df['Dealer Name'])]
    unmatched_combined_funding_reports
    error_msg = "Rows were dropped in the merging process.There are Dealer Names in either the funding Reports or the Book to Look that don't exist in the other."
    assert len(combined_funding_reports) == len(merged_df), error_msg

    # use merged dataframe to build final report
    final_df = buildReport.buildReport(merged_df)

    # appending book to look recon
    none_row = pd.DataFrame([{
        'Dealer Name': None
    }])
    btlHeader = pd.DataFrame([{
        'Dealer Name': "Book to Look Recon",
    }])
    final_df = pd.concat([final_df, none_row, none_row, btlHeader], ignore_index=True)
    btl_last_row = book_to_look.iloc[-1].tolist()
    btl_columns = book_to_look.columns.tolist()
    btl_columns.pop(0)
    btl_last_row.pop(0)
    padded_values = btl_last_row + [None] * (len(final_df.columns) - len(btl_last_row))
    padded_columns = btl_columns + [None] * (len(final_df.columns) - len(btl_columns))
    final_df.loc[len(final_df)] = padded_columns
    final_df.loc[len(final_df)] = padded_values

    exportReport.exportReport(final_df)


if __name__ == '__main__':
    print(f"Starting [{__version__}]")
    main()
    print("Complete!")