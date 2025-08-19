# %%
# Household Report
# Developed by CD
# v2.0.0

import os
from io import StringIO
from datetime import datetime, timedelta, date
from sqlalchemy import create_engine, text
import pandas as pd
import time
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import win32com.client as win32
import shutil
import stat




def retrieve_data():
    """
    Retrieve data from COCC database
    """
    class DatabaseHandler:
        """
        This class abstracts the connection to the database and allows a clean
        interface for the developer to use.

        """
        def __init__(self, tns_admin_path):
            """
            Args:
                tns_admin_path (str): Oracle driver path
                credentials_path_db1 (str): Database 1 credentials path
                credentials_path_db1 (str): Databsae 2 credentials path
            """
            os.environ['TNS_ADMIN'] = tns_admin_path
            
            # Load private key
            key_key_path = r'C:\Users\w322800\Documents\coding3\env_admin\key.key'
            with open(key_key_path, "rb") as key_file:
                key = key_file.read()

            cipher = Fernet(key)
            
            # Load encrypted data
            encoded_env_path = r'C:\Users\w322800\Documents\coding3\env_admin\.env.enc'
            with open(encoded_env_path, "rb") as encrypted_file:
                encrypted_data = encrypted_file.read()

            decrypted_data = cipher.decrypt(encrypted_data).decode()

            env_file = StringIO(decrypted_data)
            load_dotenv(stream=env_file)

            self.username1 = os.getenv('main_username')
            self.password1 = os.getenv('main_password')
            self.dsn1 = os.getenv('main_dsn')

            self.username2 = os.getenv('datamart_username')
            self.password2 = os.getenv('datamart_password')
            self.dsn2 = os.getenv('datamart_dsn')

            self.connection_string1 = f'oracle+oracledb://{self.username1}:{self.password1}@{self.dsn1}'
            self.connection_string2 = f'oracle+oracledb://{self.username2}:{self.password2}@{self.dsn2}'

            self.engine1 = create_engine(self.connection_string1, max_identifier_length=128, echo=False, future=True)
            self.engine1.dialect.hide_parameters = True
            self.engine2 = create_engine(self.connection_string2, max_identifier_length=128, echo=False, future=True)
            self.engine1.dialect.hide_parameters = True


        def query(self, sql_query, engine=1):
            """
            This allows abstraction of the connection and the class
            so the developer can query a single table as a dataframe

            Args:
                sql_query (str): The query to SQL database is passed as a string
                engine (int): This selects the database. There are two engines:
                    1 -> R1625
                    2 -> COCC DataMart

            Returns:
                df: The SQL query is returned as a pandas DataFrame

            Usage:
                df = db_handler.query("SELECT * FROM DB.TABLE", engine=1)

                In this example, db_handler = DatabaseHandler(args)
            """
            if engine == 1:
                selected_engine = self.engine1
            elif engine == 2:
                selected_engine = self.engine2
            else:
                raise ValueError("Engine must be 1 or 2")

            with selected_engine.connect() as connection:
                df = pd.read_sql(sql_query, connection)
            return df

    # Database Connection Configuration
    tns_admin_path = r'C:\Users\w322800\Documents\coding3\env_admin\tns_admin'
    db_handler = DatabaseHandler(tns_admin_path)

    #Last business day
    with db_handler.engine1.connect() as connection:
        wh_acctcommon = text("""
        SELECT 
            a.ACCTNBR,
            a.LOANOFFICER,
            a.ACCTOFFICER,
            a.OWNERSORTNAME,
            a.PRODUCT,
            a.CURRACCTSTATCD,
            a.NOTEBAL,
            a.BOOKBALANCE,
            a.NOTEINTRATE,
            a.DATEMAT,
            a.TAXRPTFORORGNBR,
            a.TAXRPTFORPERSNBR,
            a.CONTRACTDATE,
            a.MJACCTTYPCD,
            a.CURRMIACCTTYPCD
        FROM 
            OSIBANK.WH_ACCTCOMMON a
        """)
        start_time = time.time()
        wh_acctcommon = pd.read_sql(wh_acctcommon, connection)
        print(f"acctcommon took {time.time() - start_time} seconds.")

        househldacct = text("""
        SELECT 
            a.ACCTNBR,
            a.HOUSEHOLDNBR
        FROM 
            OSIEXTN.HOUSEHLDACCT a
        """)
        start_time = time.time()
        househldacct = pd.read_sql(househldacct, connection)
        print(f"househldacct took {time.time() - start_time} seconds.")
        
    data = {
        'wh_acctcommon': wh_acctcommon,
        'househldacct': househldacct
    }
    return data


def acctcommon_cleaning(wh_acctcommon):
    """
    Filtering to only active, non-performing or dormant accounts
    """
    wh_acctcommon = wh_acctcommon[wh_acctcommon['curracctstatcd'].isin(['ACT','NPFM','DORM'])].copy()
    return wh_acctcommon



# %%
def merge_dfs(wh_acctcommon, househldacct):
    """
    Mergine acctcommon & household dataframes
    """
    merged_df = pd.merge(wh_acctcommon, househldacct, on='acctnbr', how='left')
    return merged_df




# %%

# %%
# Output to excel

def main():
    data = retrieve_data()
    wh_acctcommon = data['wh_acctcommon'].copy()
    househldacct = data['househldacct'].copy()
    
    wh_acctcommon = acctcommon_cleaning(wh_acctcommon)

    df = merge_dfs(wh_acctcommon, househldacct)

    df = df[['acctnbr','householdnbr','ownersortname','product','loanofficer','acctofficer','bookbalance','noteintrate','mjaccttypcd','contractdate','datemat']].copy()

    current_date = datetime.now().strftime('%Y%m%d')
    file_path = r'\\10.161.85.66\Home\Share\Data & Analytics Initiatives\Project Management\Chad Projects\Weekly Reports\Household_Report\Production\Output'
    file_name = f'Household_Report_{current_date}.xlsx'
    full_path = os.path.join(file_path, file_name)
    df.to_excel(full_path, sheet_name='Sheet1', engine='openpyxl', index=False)


    excel = win32.gencache.EnsureDispatch("Excel.Application")
    excel.Visible = False
    workbook = excel.Workbooks.Open(full_path)
    sheet = workbook.Worksheets("Sheet1")

    sheet.Columns.AutoFit()

    # Bold top row
    top_row = sheet.Rows(1)
    top_row.Font.Bold = True

    # Add bottom border to header row
    bottom_border = top_row.Borders(9)
    bottom_border.LineStyle = 1
    bottom_border.Weight = 2

    date_columns = ["J","K"]

    for col in date_columns:
        col_index = ord(col.upper()) - 64
        sheet.Columns(col_index).NumberFormat = "mm/dd/yyyy"

    # Freeze top row
    sheet.Application.ActiveWindow.SplitRow = 1
    sheet.Application.ActiveWindow.FreezePanes = True

    workbook.Save()
    workbook.Close()
    excel.Quit()

    print(f"Excel file saved with autofit at {file_path}")

    # Move to CLO_Share folder and make read-only
    destination_path = r'\\00-berlin\CLO_Share\Data Analytics\Household Report\Household Report.xlsx'
    try:
        if os.path.exists(destination_path):
            os.chmod(destination_path, stat.S_IWRITE)
        shutil.copy(full_path, destination_path)
        os.chmod(destination_path, stat.S_IREAD)
        print("Complete!")
    except Exception as e:
        print("Error occured: {e}")

if __name__ == '__main__':
    main()


