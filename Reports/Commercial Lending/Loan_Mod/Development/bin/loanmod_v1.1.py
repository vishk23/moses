#################################
"""
= Loan Modification Report =
= Status: Complete =
v1.1.0
File Path:
\\10.161.85.66\Home\Share\Data & Analytics Initiatives\Project Management\Chad Projects\Ad Hoc Reports\Loan_Mod\

Key Stakeholder(s): Hasan Ali, Kelly Abernathy
= Overview = 
This covers loan modifications on act/npfm loans in CML portfolio

= Milestones =
- [x] Develop report

"""

import pandas as pd
from pandas.tseries.offsets import MonthEnd
import numpy as np
import time
from openpyxl import load_workbook
from openpyxl.styles import Font, Border, Side, Alignment, NamedStyle
from openpyxl.styles.numbers import NumberFormat
import os
from datetime import datetime, timedelta, date
import json
from sqlalchemy import create_engine, text
from pydantic import BaseModel, Field
from typing import List


#################################
def retrieve_data():
    """
    Retrieve data from COCC database
    """
    class DatabaseHandler:
        """
        This class abstracts the connection to the database and allows a clean
        interface for the developer to use.

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

    #Last business day
    with db_handler.engine1.connect() as connection:
        # Acctcommon
        acctcommon = text("""
        SELECT 
            a.ACCTNBR,
            a.OWNERNAME,
            a.LOANOFFICER,
            a.EFFDATE, 
            a.MJACCTTYPCD, 
            a.PRODUCT, 
            a.CURRMIACCTTYPCD, 
            a.BOOKBALANCE,
            a.NOTEBAL,
            a.NOTEOPENAMT,
            a.CURRACCTSTATCD, 
            a.CONTRACTDATE,
            a.DATEMAT 
        FROM
            OSIBANK.WH_ACCTCOMMON a
        WHERE 
            a.CURRACCTSTATCD IN ('ACT','NPFM')
            AND a.MJACCTTYPCD IN ('CML')
        """)
        start_time = time.time()
        acctcommon = pd.read_sql(acctcommon, connection)
        print(f"ACCTCOMMON took {time.time() - start_time} seconds.")
        
        # AcctSubAcct
        acctsubacct = text("""
        SELECT 
            *
        FROM 
            OSIBANK.ACCTSUBACCT a
        WHERE
            a.BALCATCD = 'CMDF'
            AND BALTYPCD = 'FEE'
        """)
        start_time = time.time()
        acctsubacct = pd.read_sql(acctsubacct, connection)
        print(f"acctsubacct took {time.time() - start_time} seconds.")
        
        # AcctLoanModHist
        acctloanmodhist = text("""
        SELECT
            *
        FROM
            OSIBANK.ACCTLOANMODHIST a
        """)
        start_time = time.time()
        acctloanmodhist = pd.read_sql(acctloanmodhist, connection)
        print(f"ACCTLOANMODHIST took {time.time() - start_time} seconds.")
        
        # AcctLoanReason
        loanmodreason = text("""
        SELECT
            *
        FROM
            OSIBANK.LOANMODREASON a
        """)
        start_time = time.time()
        loanmodreason = pd.read_sql(loanmodreason, connection)
        print(f"LOANMODREASON took {time.time() - start_time} seconds.")
        
        
        # Package up data object
        data = {
            'acctcommon': acctcommon,
            'acctsubacct': acctsubacct,
            'acctloanmodhist': acctloanmodhist,
            'loanmodreason': loanmodreason
        }

        return data




#################################
# Execution
data = retrieve_data()


#################################
acctcommon = data['acctcommon']
acctsubacct = data['acctsubacct']
acctloanmodhist = data['acctloanmodhist']
loanmodreason = data['loanmodreason']


#################################
#################################
# def create_validation_model(df):
#     """
#     Here we explicitly validate all data types and fields that will be used in this report.
#     """
#     class LoanModReport(BaseModel):
#         acctnbr: int
#         ownername: str
#         loanofficer: str
#         contractdate: date
#         datemat: date
#         bookbalance: float
#         notebal: float
#         noteopenamt: float
#         product: str
#         curracctstatcd: str
#         loanmodnbr: int
#         postdate: date
#         loanmodreasoncd: str
#         loanmodreasondesc: str
#         apprpersnbr: int
#         loanmodbalamt: float
#         canceldate: date
#         loanmodtypcd: str
#         effdate: date
        
    
#     class LoanModDataFrame(BaseModel):
#         data: List[LoanModReport]
    
#     data_dicts = df[[
#         'acctnbr',
#     # need to input here
#     ]].to_dict('records')
    
#     pydantic_model = LoanModDataFrame(data=[LoanModReport(**row) for row in data_dicts])
    
#     return pydantic_model


#################################
# Execution
# validation_model = create_validation_model(df)


#################################
# def unpack_validation_model(x):
#     """
#     Post-validation, ready to unpack the model and use data to generate report
#     """
#     temp_dict = x.model_dump()
#     df = pd.DataFrame(temp_dict['data'])
#     return df


#################################
# with db_handler.engine2.connect() as connection:
#     # For development only
#     lookup_df2 = text("""
#     SELECT 
#         *
#     FROM 
#         sys.all_tab_columns col
#     """)
#     start_time = time.time()
#     lookup_df2 = pd.read_sql(lookup_df2, connection)
#     print(f"lookup_df2 took {time.time() - start_time} seconds.")


#################################
# output_path = r'H:\Chad\Resources\Knowledge Base\lookup_df.csv'
# lookup_df.to_csv(output_path, index=False)


#################################
# with db_handler.engine1.connect() as connection:
#     # For development only
#     acctsubacct = text("""
#     SELECT 
#         *
#     FROM 
#         OSIBANK.ACCTBALHIST a
#     WHERE
#         a.BALCATCD = 'CMDF'
#         AND BALTYPCD = 'FEE'
#     """)
#     start_time = time.time()
#     acctsubacct = pd.read_sql(acctsubacct, connection)
#     print(f"acctsubacct took {time.time() - start_time} seconds.")


#################################
merged_df = pd.merge(acctcommon, acctloanmodhist, on='acctnbr', how='inner', indicator=True)


#################################
df = merged_df
duplicates = df[df.duplicated(subset=['acctnbr'], keep=False)]

if duplicates.empty:
    print("no duplicates")
else:
    print("duplicates")


#################################
loanmodreason = loanmodreason[['loanmodreasoncd','loanmodreasondesc']]
duplicates = loanmodreason[loanmodreason.duplicated(subset=['loanmodreasoncd'], keep=False)]

if duplicates.empty:
    print("no duplicates")
else:
    print("unfortunately... duplicates")
df = pd.merge(df, loanmodreason, on='loanmodreasoncd', how='left')
df = df[['acctnbr','ownername','loanofficer','contractdate','datemat','bookbalance','notebal','noteopenamt','product','curracctstatcd','loanmodnbr','postdate','loanmodreasoncd','loanmodreasondesc','apprpersnbr','loanmodbalamt','canceldate','loanmodtypcd','effdate_x']]
df = df.rename(columns={'effdate_x': 'effdate'})


#################################
df = df.reset_index(drop=True)


#################################
df = df.sort_values(by=['acctnbr','loanmodnbr'])
df


#################################
# Writing base report for Hasan
file_path = r'\\10.161.85.66\Home\Share\Data & Analytics Initiatives\Project Management\Chad Projects\Ad Hoc Reports\Loan_Mod\Production\Output\loanmod_standard.csv'
df.to_csv(file_path, index=False)


# #################################
# acctcommon = data['acctcommon']
# acctsubacct = data['acctsubacct']
# acctloanmodhist = data['acctloanmodhist']
# loanmodreason = data['loanmodreason']


# #################################
# df = pd.merge(acctcommon, acctsubacct, on='acctnbr', how='inner')


# #################################
# df


# #################################
# # Check duplicates
# duplicates = df[df.duplicated(subset=['acctnbr'], keep=False)]

# if duplicates.empty:
#     print("no duplicates")
# else:
#     print("duplicates")


# #################################
# # df[df['acctnbr'] == 151053693]


# #################################
# acctsubacct[acctsubacct['acctnbr'] == 151053693]


# #################################
# df = pd.merge(df, acctsubacct, on='acctnbr', how='left')


# #################################
# df


# #################################
# # Need to bring in processing person to subacct
# # Output both to excel (different sheets)