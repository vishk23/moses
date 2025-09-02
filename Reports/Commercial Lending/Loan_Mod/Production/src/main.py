import pandas as pd
from pathlib import Path
import cdutils.distribution # type: ignore
from src._version import __version__ # type: ignore
import src.output_to_excel

import src.fetch_data

def main():
    #################################
    # Execution
    data = src.fetch_data.fetch_data()


    #################################
    acctcommon = data['acctcommon'].copy()
    acctsubacct = data['acctsubacct'].copy()
    acctloanmodhist = data['acctloanmodhist'].copy()
    loanmodreason = data['loanmodreason'].copy()


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


    #################################
    # Writing base report for Hasan
    BASE_PATH = Path(".")
    BASE_PATH.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH = BASE_PATH / "loan_mod.xlsx"
    df.to_excel(OUTPUT_PATH, index=False)

    # Format excel
    src.output_to_excel.format_excel_file(OUTPUT_PATH)

    # Distribution
    recipients = [
        "Hasan.Ali@bcsbmail.com",
        "Kelly.Abernathy@bcsbmail.com"
    ]
    bcc_recipients = [
        "chad.doorley@bcsbmail.com",
        "businessintelligence@bcsbmail.com"
    ]
    subject = f"Monthly Loan Mod" 
    body = "Hi, \n\nAttached is the Monthly Loan Mod Report. If you have any questions, please reach out to BusinessIntelligence@bcsbmail.com \n\nThanks!"
    attachment_paths = [OUTPUT_PATH]
    cdutils.distribution.email_out(recipients=recipients, bcc_recipients=bcc_recipients, subject=subject, body=body, attachment_paths=attachment_paths)

if __name__ == '__main__':
    print(f"Starting [{__version__}]")
    # main(production_flag=True)
    main()
    print("Complete!")

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