# Weekly Loan Report - 45 day lookback
# Developed by CD
# v1.5.0

# %%
import os
from io import StringIO
from datetime import datetime, timedelta, date
from sqlalchemy import create_engine, text
import pandas as pd
import time
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import win32com.client as win32


# %%
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
    with db_handler.engine2.connect() as connection:
#         For development only
        wh_acctcommon = text("""
        SELECT 
            a.ACCTNBR,
            a.LOANOFFICER,
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
            COCCDM.WH_ACCTCOMMON_TEMP a
        """)
        start_time = time.time()
        wh_acctcommon = pd.read_sql(wh_acctcommon, connection)
        print(f"acctcommon took {time.time() - start_time} seconds.")

        # COCCDM -> WH_LOANS_TEMP
        wh_loans = text("""
        SELECT
            a.ACCTNBR,
            a.ORIGDATE,
            a.ORIGBAL,
            a.FDICCATDESC,
            a.RUNDATE
        FROM
            COCCDM.WH_LOANS_TEMP a
        """)
        start_time = time.time()
        wh_loans = pd.read_sql(wh_loans, connection)
        print(f"wh_loans took {time.time() - start_time} seconds.")

        # COCCDM -> WH_ACCTLOAN_TEMP
        wh_acctloan = text("""
        SELECT
            a.ACCTNBR,
            a.MININTRATE,
            a.FDICCATCD,
            a.PROPNBR
        FROM
            COCCDM.WH_ACCTLOAN_TEMP a
        """)
        start_time = time.time()
        wh_acctloan = pd.read_sql(wh_acctloan, connection)
        print(f"wh_acctloan took {time.time() - start_time} seconds.")

        # COCCDM -> WH_ORG
        wh_org = text("""
        SELECT
            a.ORGNBR,
            a.NAICSCD,
            a.NAICSCDDESC
        FROM
            COCCDM.WH_ORG a
        """)
        start_time = time.time()
        wh_org = pd.read_sql(wh_org, connection)
        print(f"wh_org took {time.time() - start_time} seconds.")

        # # COCCDM -> WH_PERS
        # wh_pers = text("""
        # SELECT
        #     a.PERSNBR,
        #     a.NAICSCD,
        #     a.NAICSDESC
        # FROM
        #     COCCDM.WH_PERS a
        # """)
        # start_time = time.time()
        # wh_pers = pd.read_sql(wh_pers, connection)
        # print(f"wh_pers took {time.time() - start_time} seconds.")

        # OSIBANK -> HOUSEHLDACCT
        # Skipping for now because I don't have connection that database

        # COCCDM -> WH_PROP
        wh_prop = text("""
        SELECT
            a.ACCTNBR,
            a.PROPNBR,
            a.APRSVALUEAMT,
            a.APRSDATE,
            a.PROPADDR1,
            a.PROPADDR2,
            a.PROPADDR3,
            a.PROPCITY,
            a.PROPSTATE,
            a.PROPZIP,
            a.PROPTYPECD
        FROM
            COCCDM.WH_PROP a
        """)
        start_time = time.time()
        wh_prop = pd.read_sql(wh_prop, connection)
        print(f"wh_prop took {time.time() - start_time} seconds.")

        # COCCDM -> WH_PROP2
        wh_prop2 = text("""
        SELECT
            a.ACCTNBR,
            a.PROPNBR,
            a.PROPDESC
        FROM
            COCCDM.WH_PROP2 a
        """)
        start_time = time.time()
        wh_prop2 = pd.read_sql(wh_prop2, connection)
        print(f"wh_prop2 took {time.time() - start_time} seconds.")

        # # COCCDM -> ORGADDRUSE
        # orgaddruse = text("""
        # SELECT
        #     a.ORGNBR,
        #     a.ADDRUSECD,
        #     a.ADDRNBR
        # FROM
        #     COCCDM.ORGADDRUSE a
        # """)
        # start_time = time.time()
        # orgaddruse = pd.read_sql(orgaddruse, connection)
        # print(f"orgaddruse took {time.time() - start_time} seconds.")

        # # COCCDM -> PERSADDRUSE
        # persaddruse = text("""
        # SELECT
        #     a.PERSNBR,
        #     a.ADDRUSECD,
        #     a.ADDRNBR
        # FROM
        #     COCCDM.PERSADDRUSE a
        # """)
        # start_time = time.time()
        # persaddruse = pd.read_sql(persaddruse, connection)
        # print(f"persaddruse took {time.time() - start_time} seconds.")
        
        # # COCCDM -> WH_ADDR
        # wh_addr = text("""
        # SELECT
        #     a.ADDRNBR,
        #     a.TEXT1,
        #     a.TEXT2,
        #     a.TEXT3,
        #     a.CITYNAME,
        #     a.STATECD,
        #     a.ZIPCD
        # FROM
        #     COCCDM.WH_ADDR a
        # """)
        # start_time = time.time()
        # wh_addr = pd.read_sql(wh_addr, connection)
        # print(f"wh_addr took {time.time() - start_time} seconds.")


    data = {
        'wh_acctcommon': wh_acctcommon,
        'wh_loans': wh_loans,
        'wh_acctloan': wh_acctloan,
        'wh_org': wh_org,
        # 'wh_pers': wh_pers,
        'wh_prop': wh_prop,
        'wh_prop2': wh_prop2,
        # 'orgaddruse': orgaddruse,
        # 'persaddruse': persaddruse,
        # 'wh_addr': wh_addr
    }
    return data

# %%
# data = retrieve_data()

# %%
# wh_acctcommon = data['wh_acctcommon'].copy()
# wh_loans = data['wh_loans'].copy()
# wh_acctloan = data['wh_acctloan'].copy()
# wh_org = data['wh_org'].copy()
# wh_pers = data['wh_pers'].copy()
# wh_prop = data['wh_prop'].copy()
# wh_prop2 = data['wh_prop2'].copy()
# orgaddruse = data['orgaddruse'].copy()
# persaddruse = data['persaddruse'].copy()
# wh_addr = data['wh_addr'].copy()

# %%
def filter_acctcommon(df):
    """
    Filter acctcommon table

    Args:
        df: acctcommon table from COCC

    Returns:
        result_df: dataframe after filters are applied
    
    Operations:
    [MJACCTTYPCD] IN ("CML", "CNS", "MTG", "MLN") 
    AND 
    [CURRMIACCTTYPCD] != "CI07"
    If [MJACCTTYPCD] IN "CNS", [CURRMIACCTTYPCD] IN ("IL02", "IL11", "IL12", "IL13", "IL14") 
    AND 
    !IsNull([TAXRPTFORORGNBR])
    """
    df = df[df['mjaccttypcd'].isin(['CML', 'CNS', 'MTG', 'MLN'])]
    df = df[df['currmiaccttypcd'] != 'CI07']
    df = df[(df['mjaccttypcd'] == 'CNS') &
            (df['currmiaccttypcd'].isin(['IL02', 'IL11', 'IL12', 'IL13', 'IL14'])) &
            (~df['taxrptfororgnbr'].isnull()) | 
            (df['mjaccttypcd'] != 'CNS')]
    return df

# %%
def filter_wh_loans(df):
    """
    Filter wh_loans

    Args:
        df: WH_LOANS_TEMP from COCCDM db table
    
    Returns:
        result_df: filtered dataframe of wh_loans

    Operations:
    - Create a day difference between 
    """
    df['day diff'] = (df['rundate'] - df['origdate']).dt.days + 1
    result_df = df[df['day diff'] <= 45]
    return result_df
    


# %%
# filtered_wh_loans = filter_wh_loans(wh_loans)

# %%
def consolidate_prop_data(wh_prop, wh_prop2):
    """
    Consolidate property data between the two property tables in COCC

    Args:
        wh_prop
        wh_prop2

    Returns:
        consolidated_prop_data

    Operations:
    - merge the tables
    - rename columns
    - keep only the property with the highest appraised value
    - fill null values in aprsvalueamt field

    """
    consolidated_prop_data = pd.merge(wh_prop, wh_prop2, how='inner', on='propnbr')
    consolidated_prop_data['acctnbr'] = consolidated_prop_data['acctnbr_x'].combine_first(consolidated_prop_data['acctnbr_y'])
    consolidated_prop_data = consolidated_prop_data.drop(columns=['acctnbr_x','acctnbr_y'])
    consolidated_prop_data['aprsvalueamt'] = consolidated_prop_data['aprsvalueamt'].fillna(0)
    consolidated_prop_data = (consolidated_prop_data.sort_values('aprsvalueamt', ascending=False).groupby('acctnbr', as_index=False).first())
    consolidated_prop_data = consolidated_prop_data.reset_index(drop=True)
    return consolidated_prop_data

# %%
# consolidated_prop_data = consolidate_prop_data(wh_prop, wh_prop2)

# %%
def merge_data(filtered_acctcommon, filtered_wh_loans, wh_acctloan, consolidated_prop_data, wh_org):
    """
    Merging dataframes together
    
    Args:
        dfs: all dataframes
    
    Returns:
        merged_df: merged data
    """
    merged_df = pd.merge(filtered_acctcommon, filtered_wh_loans, on='acctnbr', how='inner')
    merged_df = pd.merge(merged_df, wh_acctloan, on='acctnbr', how='left')
    merged_df = pd.merge(merged_df, consolidated_prop_data, on='acctnbr', how='left')
    merged_df = merged_df.drop(columns=['propnbr_y'])
    merged_df = merged_df.rename(columns={'propnbr_x':'propnbr'})
    merged_df = pd.merge(merged_df, wh_org, left_on='taxrptfororgnbr', right_on='orgnbr', how='left').sort_values(by='origdate', ascending=False)
    return merged_df


# %%
# merged_df = merge_data(filtered_acctcommon, filtered_wh_loans, wh_acctloan, consolidated_prop_data, wh_org)

# %%
def main():
    data = retrieve_data()

    wh_acctcommon = data['wh_acctcommon'].copy()
    wh_loans = data['wh_loans'].copy()
    wh_acctloan = data['wh_acctloan'].copy()
    wh_org = data['wh_org'].copy()
    wh_prop = data['wh_prop'].copy()
    wh_prop2 = data['wh_prop2'].copy()

    filtered_acctcommon = filter_acctcommon(wh_acctcommon)
    filtered_wh_loans = filter_wh_loans(wh_loans)
    consolidated_prop_data = consolidate_prop_data(wh_prop, wh_prop2)
    merged_df = merge_data(filtered_acctcommon, filtered_wh_loans, wh_acctloan, consolidated_prop_data, wh_org)
    
    # Output to excel
    current_date = datetime.now().strftime('%Y%m/%d')
    file_path = r'\\10.161.85.66\Home\Share\Data & Analytics Initiatives\Project Management\Chad Projects\Weekly Reports\NewLoanReport_LR_Credit\Production\Output'
    file_name = f'Loan_Report_45_day_lookback_{current_date}.xlsx'
    full_path = os.path.join(file_path, file_name)
    merged_df.to_excel(full_path, sheet_name='Sheet1', engine='openpyxl', index=False)

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

    date_columns = ["I","L","O","R","X"]

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

    # Email
    recipients = [
        # "commercial.portfolio.managers@bcsbmail.com",
        "chad.doorley@bcsbmail.com"
    ]
    bcc_recipients = [
        "chad.doorley@bcsbmail.com"
    ]
    outlook = win32.Dispatch("Outlook.Application")
    message = outlook.CreateItem(0)
    # message.Display()
    message.To = ";".join(recipients)
    message.BCC = ";".join(bcc_recipients)
    message.Subject = f"Weekly Loan Report - {datetime.now().strftime('%m/%d%Y')}"
    message.Body = "Hi all, \n\nAttached is the Weekly Loan Report with a 45 day lookback. Please let me know if you have any questions."
    message.Attachments.Add(str(full_path))
    message.Send()
    print("Email sent!")


# %%
if __name__ == '__main__':
    main()

# %%



