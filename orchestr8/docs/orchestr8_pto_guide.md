# Orchestr8 & PTO Guide
by Chad Doorley

## Launching Orchestr8
1. Find folder in Documents: 'Orchestr8'
2. Navigate to 'django_app'
3. Launch 'simplified_runner'

You are all set. Server & Worker are running on localhost:8000

## Endpoints
- You can access these endpoints through Google Chrome (recommended Private Browser/Incognito to avoid caching issues)

### localhost:8000/admin
- This is the admin panel. Please log in with username/password
- Click on Periodic Tasks
- Use the check boxes to the left of each 'task' (report) and use the 'Action' dropdown at the top to 'Run Selected Task(s)' and press Go
    - You may click on each item to read the description which has information on whether it is has distribution (auto-email) built in or if it needs to be emailed out to particular users.
    - I outline all of this below, so you do not need to necessarily look there, but it will be there if you like to reference it in another location

### localhost:8000/status_page
- This is the status page GUI where you can run status pages
- Users will send in requests to BusinessIntelligence@bcsbmail.com
    - They will need to include the household number in their request (or sometimes the name)
        - They may include additions/deletes as well
    - You'll want to use the account_segments.xlsx file @ Project_Management\Data_Analytics\R360_Dimensions and Segments\Development\output on DA-1 to cross reference and find out the portfolio_key
        - double check to make sure there aren't consistency issues and you can ask the requestor if they want to add/remove entities that differ in householdnbr/portfolio_key (edge cases)

## Reports to Run
### Guide
- Daily = Every Day (Business Days)
    - Run on 1st of the month as well
- Weekly = Monday
- Monthly = 1st of the Month (Thursday, May 1)

### Daily
Orchestr8:
- R360 Portfolio Key Run
    - Distribution: n/a
- Deposit Update
    - Distribution: n/a
- Indirect Recon Reserve
    - Distribution: n/a

### Weekly
Orchestr8:
- New Loan Report: Francine
    - Distribution: Built-in
        - Francine Ferguson
- New Loan Report LR/Credit
    - Distribution: Built-in
        - Paul Kocak
        - Linda Clark
- Household Report
    - Distribution: n/a

Credit Track:
- Covenant Action Report
    - Distribution: Manual
        - Eldora Moore
    - Skip this: I gave her a heads up that I'll just double up the following week

### Monthly
Orchestr8:
- Balance Tracker YTD
    - Distribution: Built-in
        - Tim Chaves
        - John Silva
        - Hasan Ali
        - Dawn Young
        - Chris Alves
        - Donna Oliveira
        - Nancy Pimentel
        - Michael Patacao
        - Jeffrey Pagliuca
        - Erin Riendeau
        - Donna Pavao 
- Delinquency
    - Distribution: Built-in
        - Brandon George
- Business Deposits YTD
    - Distribution: Built-in
        - Hasan Ali
        - Becky Velazquez
- New Business Checking
    - Distribution: n/a
        - Refreshes dashboard for Retail
- New Consumer Checking
    - Distribution: n/a
        - Refreshes dashboard for Retail
- Deposit Deep Dive
    - Distribution: Built-in
        - Eusebio Borges
- Trail Balance - Operations
    - Distribution: Built-in
        - Kelly Abernathy
        - Zachary Cabral
- Deposit Dash
    - Distribution: Built-in
        - Commercial Portfolio Managers (group mailbox)

Alteryx:
- **Note:** *If you have connection issues, feel free to update the connection issues and save over the workflow. I have a copy of it in 'archive'*
- WARR
    - Directory:
    ```bash
    \\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Credit_Loan_Review\WARR\Production\WARR_ME.yxmd
    ```
    - Distribution: Manual
        - Paul Kocak
        - Brandon George
    - Notes:
        - Go into Excel file and pretty up (Autofit rows, bold header row)
        - Send out 'WARR_Final.xlsx'
- Concentration of Credit
    - Directory:
    ```bash
    \\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Credit_Loan_Review\Concentration Reports\Credit\Production
    ```
    - Notes:
        - There are 2 workflows, run both. They will produce excel files in the same directory.
        - Autofit columns on all sheets and pretty up
        - It may throw an error with Run Command, but should still produce output just fine 
    - Distribution: Manual
        - 'COC_Report_Includes_Personal.xlsx'
            - Paul Kocak
            - Patrick Leddy
            - Sean Cartwright
        - 'COC_Report_CMLonly
            - Hasan Ali
- **I'll run the other report when I return**

    

