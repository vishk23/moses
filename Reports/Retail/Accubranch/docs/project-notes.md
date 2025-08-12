(bcsb-prod) PS C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Retail\Accubranch> python -m src.main
Starting Accubranch Analysis
Version: v1.0.0-dev
Environment: dev
Business Line: Retail
Schedule: On-Demand
Owner: Francine Ferguson
Working directory: C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Retail\Accubranch
Output directory: C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Retail\Accubranch\output
--------------------------------------------------
Processing account data...
✓ Account data processing completed
Processing transaction data...
Fetching transaction data from 2024-06-30 to 2025-06-30...
Retrieved 100000 transaction records
Retrieved 946340 cashbox transaction records
Retrieved 16944 organization records
Fetching account data for merging...
Retrieved 89805 account records
Merging transaction and account data...
Adding branch information from WH_ORG...
Error during processing: "['orgnbr'] not in index"