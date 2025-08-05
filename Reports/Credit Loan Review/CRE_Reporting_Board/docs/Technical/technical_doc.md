Project Technical Documentation: Dealer Recon Reserve
===

## Usage
```bash
> Navigate to the Project Home directory
> cd Production
> python -m src.main
    - this creates the 'cre_loader.xlsx' file that all of this is based upon
> python -m src.icre_production
    - this refreshes:
        - 'icre_balances.xlsx'
        - 'icre_production.xlsx'
> Open grouping_call_codes.ipynb (Jupyter Notebook)
    - Press 'Run All'
    - this refreshes:
        - 'total_cml.xlsx'
        - 'icre.xlsx'
        - 'construction.xlsx'
```

Only item that is Alteryx is CML Var that Tom K wrote:
PowerBI reads from here: "H:\FinishedReports\CML VAR\OUTPUT\CML VAR with Rate Change Date.xlsx"

Once all excel files are updated, open PowerBI and refresh the data.

Validation:
- storing the worksheet from accounting in the assets folder
    - this can be manually reconciled
    - totals will match up when you filter on CML

Cadence of Execution:
This is ran semi-annually (upon request from Tim/Linda)


## Filters & Calculations
- fdic_recon.py
    - ACT/NPFM loans
    - mjaccttypcd (major): CML,MLN
    - you have to set the date manually (effdate)
        - For example: I set to 12/31/2024 to match the call report numbers
    - calculated fields
        bookbalance -> if currmiaccttypcd == 'CM45', use notebal, else bookbalance
            - Tax Exempt bonds always have $0 as book balance so adjustment is made
        net balance == bookbalance - cobal
            - BCSB balance - Charged off amount (COBAL)
        net available == available balance amount * (1 - total pct sold)
        net collateral reserve == collateral reserve * (1 - total pct sold)
        total exposure == net balance + net available + net collateral reserve
    - exclude ach manager products
    - exclude CML indirect loans 
    - Tax exempt bonds as CRE Other (OTAL)

- grouping_call_codes.ipynb
    - fdic_groups = 
        {
        '1-4 Fam Construction': ['CNFM'],
        'Construction': ['OTCN','LAND','LNDV','RECN'],
        '1-4 Family': ['REFI','REOE','REJU'],
        'OwnerOcc': ['REOW'],
        'I-CRE': ['RENO','REMU'],
        'C&I': ['CIUS'],
        'Other': ['OTAL','AGPR','REFM']
        }
    - prop_groups = 
        {
        'Autobody/Gas Station': ['Autobody/Gas Station','Gas Station and Convenience St','Auto-Truck Repair'],
        'Other': ['Other','Commercial - Other'],
        'Retail': ['Retail - Big Box Store','Shopping Plaza','Strip Plaza','Dry Cleaner/Laundromat','General Retail'],
        'Hospitality': ['Hotel/Motel','Hospitality/Event Space'],
        'Recreation': ['Outdoor Recreation','Indoor Recreational'],
        'Industrial': ['Manufacturing','Warehouse'],
        'Land': ['Land - Unimproved','Land - Improved'],
        'Mixed Use': ['Mixed Use (Retail/Office)','Mixed Use (Retail/Residential)','Mixed Use (Office/Residential)'],
        'Multi Family': ['Apartment Building'],
        'General Office': ['Office - Professional','Office- General'],
        'Medical Office': ['Office - Medical'],
        'Restaurant': ['Restaurant']
        }
    
- icre_production.py
    - same pipeline as the fdic_recon, we just run over different date ranges (prior 3 years)
    - extract net balance and noteopenamt (production) separately

- CML Var
    - CML loans that are active and have a variable interest rate
    - filtered to certain range when they are maturing and have next interest rate change.

## Changelog
[v2.0.1-prod] 2025-02-15
- Found an issue with the CML Var workflow and eliminated the need for that.
- Built in the CML Var filters directly into the src.main script which creates the cre_loader.xlsx
    - this is now used to power the interest rate visualizations & maturity rate
    - there is a new flag that is 1 if the rate change is before datemat, otherwise 0
- Updated paths post-drive conversion

[v2.0.0-prod] 2025-02-15
- Big overhaul of this, re-doing the pipeline, making it easier for the future

