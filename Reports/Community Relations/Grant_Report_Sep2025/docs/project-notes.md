Objective:

Provide community relations dept with list of loan totals & deposit totals for organizations that are requesting grants. They provide a list of taxid numbers so I match against the COCC data to get the current account information broken down like this

Structure:
Folder/input: where the uploaded file by business lines goes
Folder/output: where the cleaned report is going to get written to

# 2025-09-09
Starting this report. Can turn around relatively quickly from silver layer account data

Overall process is to read in input data

ACCT_DATA = src.config.SILVER / "account"
DeltaTable(ACCT_DATA).to_pandas

The data can be filtered to
- effdate
- acctnbr
- ownersortname
- mjaccttypcd
- currmiaccttypcd

PERS_DATA = src.config.SILVER / "pers_dim"
- pernsbr
- perssortname

ORG_DATA = src.config.SILVER / "org_dim"
- orgnbr
- orgsortname
- taxid (not masked)

Filter down orgs to only ones that match taxid number on their provided list
- join input data + org cleaned dimension table, inner join
    - only ones that show up on provided input data make it through

Create loan/deposit field on specific majors, null out other ones
- Group by taxrptfororgnbr and get column for loan nunique and Net Balance + for deposits

Left join provided grant org data with accounts

That gives you solid output answering business need.