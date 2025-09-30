import pandas as pd
from sqlalchemy import create_engine

# Step 1: Load data
engine = create_engine('postgresql://username:password@host:port/database')
df_org = pd.read_sql("SELECT orgnbr, orgname, org_status FROM wh_org", engine)
df_pers = pd.read_sql("SELECT persnbr, persname, pers_status FROM wh_pers", engine)

# Step 2: Transform
df_org['customer_id'] = 'O' + df_org['orgnbr'].astype(str)
df_org['customer_name'] = df_org['orgname']
df_org['customer_type'] = 'Organization'
df_org['entity_status'] = df_org['org_status']
df_org = df_org[['customer_id', 'customer_name', 'customer_type', 'entity_status']]

df_pers['customer_id'] = 'P' + df_pers['persnbr'].astype(str)
df_pers['customer_name'] = df_pers['persname']
df_pers['customer_type'] = 'Person'
df_pers['entity_status'] = df_pers['pers_status']
df_pers = df_pers[['customer_id', 'customer_name', 'customer_type', 'entity_status']]

# Step 3: Combine
customer_dim = pd.concat([df_org, df_pers], ignore_index=True)
duplicates = customer_dim['customer_id'].duplicated().sum()
if duplicates > 0:
    customer_dim = customer_dim.drop_duplicates(subset=['customer_id'], keep='first')
customer_dim = customer_dim.sort_values('customer_id').reset_index(drop=True)

# Step 4: Save
customer_dim.to_csv('customer_dim.csv', index=False)
print("Done! Shape:", customer_dim.shape)
print(customer_dim.head())