# Async Connector
# Developed by CD
# v2.0.1-prod

from io import StringIO
import time
import numpy as np
import os
from datetime import datetime, timedelta, date
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from typing import List
from collections import defaultdict, Counter
import pandas as pd
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from io import StringIO
from pathlib import Path
import asyncio
import nest_asyncio
import sys
from typing import Dict, Union, List
nest_asyncio.apply()

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def retrieve_data(queries: List[Dict[str, Union[str, pd.DataFrame, int]]]) -> Dict[str, pd.DataFrame]:
    """
   Retrieve data from Oracle Database (COCC)

    Args:
        queries (List): pass list of queries in specific format
            - List[Dict[str, Union[str, pd.DataFrame, int]]]
    
    Returns:
        data (Dict): Returns a dictionary with df name and the df attached as key/value pair.  
    
    """
    class DatabaseHandler:
        """
        This class abstracts the connection to the database and allows a clean
        interface for the developer to use.

        This connector can handle async queries

        """
        def __init__(self, tns_admin_path):
            """
            Args:
                tns_admin_path (str): Oracle driver path
                credentials_path_db1 (str): Database 1 credentials path
                credentials_path_db1 (str): Databsae 2 credentials path
            """
            os.environ['TNS_ADMIN'] = tns_admin_path

            project_root = os.getcwd()
            
            # Load private key
            key_key_path = 'src\cdutils\database\env_admin\key.key'
            with open(key_key_path, "rb") as key_file:
                key = key_file.read()

            cipher = Fernet(key)
            
            # Load encrypted data
            encoded_env_path = r'src\cdutils\database\env_admin\.env.enc'
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

            self.engine1 = create_async_engine(self.connection_string1, max_identifier_length=128, echo=False, future=True)
            self.engine1.dialect.hide_parameters = True
            self.engine2 = create_async_engine(self.connection_string2, max_identifier_length=128, echo=False, future=True)
            self.engine1.dialect.hide_parameters = True


        async def query(self, sql_query, engine=1):
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

            async with selected_engine.connect() as connection:
                result = await connection.execute(sql_query)
                rows = result.fetchall()
                if not rows:
                    return pd.DataFrame()
                df = pd.DataFrame(rows, columns=result.keys())
            return df

        async def close(self):
            if self.engine1:
                await self.engine1.dispose()
            if self.engine2:
                await self.engine2.dispose()


    # Database Connection Configuration
    tns_admin_path = r'src\cdutils\database\env_admin\tns_admin'
    db_handler = DatabaseHandler(tns_admin_path)

    async def fetch_data(queries):
        try:
            tasks = {query['key']: asyncio.create_task(db_handler.query(query['sql'], query['engine'])) for query in queries}
            results = await asyncio.gather(*tasks.values())
            return {key: df for key, df in zip(tasks.keys(), results)}
        except Exception as e:
            print(f"Error")
            raise
        finally:
            await db_handler.close()

    def run_sql_queries(queries):

        async def run_queries():
            return await fetch_data(queries)
        
        loop = asyncio.get_event_loop()
        if loop.is_running():
            return loop.run_until_complete(run_queries())
        else:
            return asyncio.run(run_queries())
        
    data = run_sql_queries(queries)
    
    return data