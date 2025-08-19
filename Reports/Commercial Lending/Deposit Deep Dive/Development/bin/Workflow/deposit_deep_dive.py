"""
= Project Name: Deposit Dash Report =
= Status: In-progress = 
v1.0.0
File_path:
\\10.161.85.66\Home\Share\Data & Analytics Initiatives\Project Management\Chad Projects\Monthly Reports\Deposit Deep Dive\



= Overview =
Goal: Assist one of the portfolio managers with understanding month over month deposit balances and trends for their team and lenders that they assist.
 
Key Stakeholder: Eusebio Borges

= Milestones =
- [x] Code in Python
- [ ] Recode to automated execution

= Notes =
"""



import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from sqlalchemy import create_engine, text
import os
import time
from win32com.client import Dispatch
from pathlib import Path


#################################
def retrieve_data():
    class DatabaseHandler:
        """
        Attributes:
        """
        def __init__(self, tns_admin_path, credentials_path_db1, credentials_path_db2):
            """
            Args:
                tns_admin_path (str): Oracle driver path
                credentials_path_db1 (str): Database 1 credentials path
                credentials_path_db1 (str): Databsae 2 credentials path
            """
            os.environ['TNS_ADMIN'] = tns_admin_path

            with open(credentials_path_db1) as config_file:
                config1 = json.load(config_file)

            self.username1 = config1['username']
            self.password1 = config1['password']
            self.dsn1 = config1['dsn']

            with open(credentials_path_db2) as config_file:
                config2 = json.load(config_file)

            self.username2 = config2['username']
            self.password2 = config2['password']
            self.dsn2 = config2['dsn']

            self.connection_string1 = f'oracle+oracledb://{self.username1}:{self.password1}@{self.dsn1}'
            self.connection_string2 = f'oracle+oracledb://{self.username2}:{self.password2}@{self.dsn2}'

            self.engine1 = create_engine(self.connection_string1, max_identifier_length=128)
            self.engine2 = create_engine(self.connection_string2, max_identifier_length=128)

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
    tns_admin_path = r'C:\Oracle2\instantclient_21_13\network\admin'
    credentials_path_db1 = r'\\10.161.85.66\Home\Share\Alteryx_Admin\Configuration\Connection\db_config_main.json'
    credentials_path_db2 = r'\\10.161.85.66\Home\Share\Alteryx_Admin\Configuration\Connection\db_config_datamart.json'
    db_handler = DatabaseHandler(tns_admin_path, credentials_path_db1, credentials_path_db2)

    with db_handler.engine2.connect() as connection:
    #     # For development only
    #     lookup_df = text("""
    #     SELECT 
    #         *
    #     FROM 
    #         sys.all_tab_columns col
    #     """)
    #     start_time = time.time()
    #     lookup_df = pd.read_sql(lookup_df, connection)
    #     print(f"lookup_df took {time.time() - start_time} seconds.")

        effdates = text("""
        SELECT DISTINCT
            a.EFFDATE
        FROM 
            COCCDM.WH_ACCTCOMMON a
        WHERE
            MONTHENDYN = 'Y'
        ORDER BY EFFDATE DESC

        """)
        effdates = pd.read_sql(effdates, connection)
        print("Loaded ME dataframe in")

        recent_me = effdates['effdate'][0]
        prior_me = effdates['effdate'][1]

        recent_acctcommon = text(f"""
        SELECT 
            a.ACCTNBR,
            a.OWNERNAME,
            a.PRODUCT,
            a.LOANOFFICER,
            a.ACCTOFFICER,
            a.EFFDATE, 
            a.MJACCTTYPCD, 
            a.CURRMIACCTTYPCD,
            a.NOTEBAL,
            a.BOOKBALANCE,
            a.NOTEINTRATE,
            a.CURRACCTSTATCD, 
            a.CONTRACTDATE,
            a.DATEMAT,
            a.TAXRPTFORORGNBR,
            a.TAXRPTFORPERSNBR
        FROM 
            COCCDM.WH_ACCTCOMMON a
        WHERE
            a.EFFDATE = TO_DATE('{recent_me}', 'yyyy-mm-dd hh24:mi:ss')
            AND a.CURRACCTSTATCD IN ('ACT','DORM')
            AND a.MJACCTTYPCD IN ('CK','SAV','TD')
        """)
        recent_acctcommon = pd.read_sql(recent_acctcommon, connection)
        print("Loaded Recent_ME in")

        prior_acctcommon = text(f"""
        SELECT 
            a.ACCTNBR,
            a.OWNERNAME,
            a.PRODUCT,
            a.LOANOFFICER,
            a.ACCTOFFICER,
            a.EFFDATE, 
            a.MJACCTTYPCD, 
            a.CURRMIACCTTYPCD,
            a.NOTEBAL,
            a.BOOKBALANCE,
            a.NOTEINTRATE,
            a.CURRACCTSTATCD, 
            a.CONTRACTDATE,
            a.DATEMAT,
            a.TAXRPTFORORGNBR,
            a.TAXRPTFORPERSNBR
        FROM 
            COCCDM.WH_ACCTCOMMON a
        WHERE
            a.EFFDATE = TO_DATE('{prior_me}', 'yyyy-mm-dd hh24:mi:ss')
            AND a.CURRACCTSTATCD IN ('ACT','DORM')
            AND a.MJACCTTYPCD IN ('CK','SAV','TD')
        """)
        prior_acctcommon = pd.read_sql(prior_acctcommon, connection)
        print("Loaded PRIOR_ME in")
    
    data = {
        'recent_acctcommon': recent_acctcommon,
        'prior_acctcommon': prior_acctcommon
    }
    
    return data



#################################
def main():
    data = retrieve_data()

    comparison_df = pd.merge(data['recent_acctcommon'], 
                         data['prior_acctcommon'], 
                         on=['acctofficer','acctnbr'], 
                         how='outer',
                         suffixes=('_recent', '_prior'))






    #################################
    comparison_df.info()


    #################################
    comparison_df['bookbalance_recent'] = comparison_df['bookbalance_recent'].fillna(0)
    comparison_df['bookbalance_prior'] = comparison_df['bookbalance_prior'].fillna(0)
    comparison_df['bookbalance_change'] = comparison_df['bookbalance_recent'] - comparison_df['bookbalance_prior']


    #################################
    comparison_df['bookbalance_change'] = comparison_df['bookbalance_change'].fillna(0)


    #################################
    # file_path = r'H:\FinishedReports\DepositDash\DeepDives\Production\Output\data.csv'
    # comparison_df.to_csv(file_path, index=False)


    #################################
    # officers = comparison_df['acctofficer'].unique().tolist()


    #################################
    # officers


    #################################
    my_list = ['ANDREW K. SPRINGER',
            'ANDREW RODRIGUES',
            'JEFFREY P. PAGLIUCA',
            'JOSHUA A. CAMARA',
            'WILLITTS S. MENDONCA',
            'ROGER A. CABRAL',
            'LAURA A. STACK']


    #################################
    # Most recent month end
    today = datetime.today()
    if today.day == 1:
        most_recent_month_end = today - timedelta(days=1)
    else:
        most_recent_month_end = today.replace(day=1) - timedelta(days=1)
    # most_recent_month_end_str = most_recent_month_end.strftime("%m/%d/%y")
    me_date_no_slash = most_recent_month_end.strftime("%m%d%y") # Month End date to append to file name

    file_path = Path(r'\\10.161.85.66\Home\Share\Data & Analytics Initiatives\Project Management\Chad Projects\Monthly Reports\Deposit Deep Dive\Production\Output')
    file_name = f"deposit_deep_dive_{me_date_no_slash}.xlsx"
    full_path = file_path / file_name

    with pd.ExcelWriter(full_path, engine='openpyxl') as writer:
        
        summary_df = comparison_df[comparison_df['acctofficer'].isin(my_list)].groupby('acctofficer').agg({
            'bookbalance_recent':'sum',
            'bookbalance_prior':'sum',
            'bookbalance_change': 'sum'
        }).reset_index()
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        for officer in my_list:
            officer_df = comparison_df[comparison_df['acctofficer'] == officer]
            officer_df.to_excel(writer, sheet_name=officer, index=False)
            
        
        
    print("Complete!")

    # Email
    recipients = [
        # "eusebio.borges@bcsbmail.com",
        "chad.doorley@bcsbmail.com"
    ]
    bcc_recipients = [
        "chad.doorley@bcsbmail.com"
    ]
    outlook = Dispatch("Outlook.Application")
    message = outlook.CreateItem(0)
    # message.Display()
    message.To = ";".join(recipients)
    message.BCC = ";".join(bcc_recipients)
    message.Subject = f"Deposit Deep Dive"
    message.Body = "Hi Eddie, \n\nAttached is the monthly deposit deep dive report. Please let me know if you have any questions"
    message.Attachments.Add(str(full_path))
    message.Send()
    print("Email sent!")


#################################
