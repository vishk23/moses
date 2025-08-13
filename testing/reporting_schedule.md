# Reporting Procedures

## Daily
1. Open bcsb-prod repository
2. python testing/run_reports --list
3. $env:REPORT_ENV="prod"
    - Run things in production mode
4. Paste into terminal to run 4 morning reports
python testing/run_reports.py --name "R360"; python testing/run_reports.py --name "Daily Deposit Update"; python testing/run_reports.py --name "Dealer Reserve Recon"; python testing/run_reports.py --name "Daily Mismatched Debit Card Txns"
5. Done, terminal will output success/fail and updates as well as log everything to prod_execution.log