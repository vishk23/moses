"""
Line Utilization Testing module. 
"""
import pandas as pd # type: ignore
import numpy as np # type: ignore
from sqlalchemy import text # type: ignore

import src.cdutils.database.connect


def line_utilization_fetch(loan_data: pd.DataFrame):
    """
    This function gathers line utilization data over past 12 months for each item
    
    Args:
        db_handler: Database Connection abstraction for SQL query
        loan_data: loan_data is passed in for unique account numbers
        
    Returns:
        df1: Line Utilization
            - 2 column table with:
                - acctnbr
                - avg line utilization over trailing 12 months
            
        df2: 30 Day Cleanup Provision
            - 2 column table with:
                - acctnbr
                - cleanup (1=Fail, 0=Pass)
    Operations:
        - unique account numbers extracted from loan_data
        - current_date and year_ago_date are calculated from loan_data (effdate)
        - SQL Query:
            SELECT b.ACCTNBR, b.EFFDATE, b.BOOKBALANCE, c.CREDITLIMITAMT
            FROM COCCDM.WH_ACCTCOMMON b
            JOIN COCCDM.WH_ACCTLOAN c
            ON b.ACCTNBR = c.ACCTNBR AND b.EFFDATE = c.EFFDATE
            WHERE b.ACCTNBR IN ({acctnbr_placeholder})
            AND b.EFFDATE BETWEEN TO_DATE('{year_ago_date}', 'yyyy-mm-dd hh24:mi:ss') AND TO_DATE('{current_date}', 'yyyy-mm-dd hh24:mi:ss')
        - if creditlimitamt is null, replace with 0
        - Calculate line utilization:
            - ttm line utilization = bookbalance / creditlimit amount
            - fill na values with 0 (0/0) and inf with 100 (credit limit = 0, bookbalance > 0)
            - group by acctnbr and take average line utilization
        - Calculate 30 day cleanup provision:
            - sort by acctnbr and effdate in ascending order
            - create a rolling 30 day window and adjust slider through full date range for each
            acctnbr
            - return 0 if it was paid to 0 for at least 30 days in past year, else return 1 (fail)
    
    """
    acctnbrs = loan_data['acctnbr'].unique().tolist()
    acctnbr_placeholder = ', '.join([f"'{acct}'" for acct in acctnbrs])
    
    current_date = pd.to_datetime(loan_data['effdate'][0])
    temp_data = {
        'current_date': [current_date]
    }

    temp_df = pd.DataFrame(temp_data)

    temp_df['year_ago_date'] = temp_df['current_date'] - pd.DateOffset(years=1)

    current_date = temp_df['current_date'][0].strftime('%Y-%m-%d')+' 00:00:00'
    year_ago_date = temp_df['year_ago_date'][0].strftime('%Y-%m-%d')+' 00:00:00'
    
    # Query SQL
    query = text(f"""
        SELECT b.ACCTNBR, b.EFFDATE, b.BOOKBALANCE, c.CREDITLIMITAMT
        FROM COCCDM.WH_ACCTCOMMON b
        JOIN COCCDM.WH_ACCTLOAN c
        ON b.ACCTNBR = c.ACCTNBR AND b.EFFDATE = c.EFFDATE
        WHERE b.ACCTNBR IN ({acctnbr_placeholder})
        AND b.EFFDATE BETWEEN TO_DATE('{year_ago_date}', 'yyyy-mm-dd hh24:mi:ss') AND TO_DATE('{current_date}', 'yyyy-mm-dd hh24:mi:ss')
    """)

    queries = [
        {'key':'query', 'sql':query, 'engine':2},
        # {'key':'acctcommon', 'sql':acctcommon, 'engine':1},
        # {'key':'persaddruse', 'sql':persaddruse, 'engine':1},
        # {'key':'orgaddruse', 'sql':orgaddruse, 'engine':1},
        # {'key':'wh_addr', 'sql':wh_addr, 'engine':1},
        # {'key':'wh_allroles', 'sql':wh_allroles, 'engine':1},
    ]

    data = src.cdutils.database.connect.retrieve_data(queries)
    df = data['query'].copy()
    
    df['bookbalance'] = pd.to_numeric(df['bookbalance'], errors='coerce')
    df['creditlimitamt'] = pd.to_numeric(df['creditlimitamt'], errors='coerce')
    
    df['creditlimitamt'] = df['creditlimitamt'].fillna(0)
    
    df1 = df.copy()
    df1['ttm line utilization'] = df1['bookbalance'] / df1['creditlimitamt']
    df1['ttm line utilization'] = df1['ttm line utilization'].fillna(0)
    df1['ttm line utilization'] = df1['ttm line utilization'].replace([np.inf], 1.00)
    df1 = df1.groupby('acctnbr')['ttm line utilization'].mean().reset_index()
    
    df2 = df.copy()
    df2['effdate'] = pd.to_datetime(df2['effdate'])
    df2 = df2.sort_values(by=['acctnbr','effdate'])
    
    def check_30_day_cleanup(group):
        """
        Check if line of credit has been cleaned up for 30 days
        """
        group['rolling_zeros'] = group['bookbalance'].rolling(window=30).apply(lambda x: (x == 0).all(), raw=True)
        return 0 if (group['rolling_zeros'] == 1).any() else 1
    
    df2 = df2.groupby('acctnbr').apply(check_30_day_cleanup, include_groups=False).reset_index(name='cleanup_provision')
    
    return df1, df2


#################################
def append_line_utilization_data(loan_data, utilization_data, cleanup_data):
    """
    Appends line utilization data to loan_data
    
    Args:
        utilization_data: df with line utilization % over ttm
        cleanup_data : df with 30-day cleanup test (boolean)
        
    Returns:
        df: loan_data with additional tests
        
    Operations:
        - left merge with acctnbr & utilization data on acctnbr
        - left merge with acctnbr & cleanup_data on acctnbr
    """
    df = pd.merge(loan_data, utilization_data, on='acctnbr', how='left')
    df = pd.merge(df, cleanup_data, on='acctnbr', how='left')
    return df

