## Slice: Merging XAA data with exisiting concentration of deposits data

## TODO
- [x] Create development branch to work on this and set up environment
- [x] Build I/O system for XAA
- [x] Merge to concetration report
- [x] Developer Validation/Testing
- [x] Re-do I/O system with updated template (different fields) | 2025-07-07
- [x] Add account officer mode
- [x] Re-do I/O system again with update template (Steve sent me csv directly as it comes off of XAA) | 2025-07-09
- [x] Add officer to summary sheet
- [x] Create new sheet for relationship summary
- [x] Adjust columns for hasan
- [ ] User Testing
- [ ] Set up on scheduler system
    - Cadence: Monthly (on the 10th/11th of every month when Steve supplies me XAA data)


### 2025-06-29 (Chad Doorley)
- Working on this. Need to have out to end users prior to July 10 so they have time to test.
    

### 2025-06-30 (Chad Doorley)
```text
Please see the attached report with the added data from XAA.

The way it works is I have this workflow assets folder and you can throw any report directly off of XAA into this folder and when I run this report, it'll aggregate the total fees over whatever period was supplied on XAA report.



On the attached version, it just had May 2025, so you'll see in total fees column the total for any specific account and on the Summary sheet (Sheet1), it'll sum these up per relationship, but usually we have one operating account per relationship anyway that all the fees get applied to.

Take a look at this and let me know your thoughts.

Hasan, per your last comment, we could aggregate in different ways, such as pulling a last month file of XAA and then one over the trailing period, but I wanted to get this out to you guys so you can have a look and give me some feedback. Some like this (and the XAA 2025-05 file would go in recent month in this example)
```

### 2025-07-02 (Chad Doorley)
I guess the template that was provided to me off XAA was incorrect, so I will have to adjust this to work off the new templates

### 2025-07-07 (Chad Doorley)
Rebuilt the XAA ingestion and did last month vs TTM. I can extend this later on if necessary.

One thing to note, it looks like there are duplicates on the XAA report
Looking at SRU Inc (#)
We can see there are two records for Cycle Date 2/28/2025
I thought it was supposed to be unique records per account number for a particular month (and then I can aggregate over trailing 12 months or take latest month), but it could be double counting.

Look at the screenshot


### 2025-07-09 (Chad Doorley)
Having to fix this again because I was provided a new template. 

Made several fixes listed above and this is a ready to go branch. Still waiting on additional feedback from Steve/Hasan so I'll just wait there. 

Created new sheet based on how hasan had created it.

they are going to meet to mock up the output and advise me on how they want the columns foratted.


### 2025-07-11 (Chad Doorley)
Chad - here are the clean up items to make this more approachable.  See highlights in attached for areas to update and below notes.  Grey = eliminate / Yellow = updates.  I made highlights on Tab 2 but it should apply to both tabs.

Tab 2 – add account officer and cash management officer to the summary total line (currently blank)
Eliminate columns E, F, J, Q, & R – grey colored
Eliminate column Y for Trailing 12M Avg ECR – grey colored.  Don’t think there is much benefit here…just takes up space
Eliminate column Z for Treasury Officer – grey colored.  I don’t think this is needed since we have cash management officer listed and neither Sara or Taylor is listed as a treasury officer in XAA at this point.
Move column Cash Management Officer column to be right after the Account Officer column
Remove underscores in all account headers and just leave a space in between (if that is possible)
Rename the following headers:
Acctnbr – change to Acct No.
ownersortname – change to Borrower Name
notebal – change to Current Balance
noteintrate – change to Interest Rate
acctofficer = change to Account Officer
contractdate – change to Acct Open Date
Lastest_Month_Analyzed_Charges – change to Current Mo Analyzed Fees (Pre-ECR)
Latest_Month_Combined_Results – change to Current Mo Net Analyzed Fees (Post-ECR)
Trailing_12M_Analyzed_Charges – change to TTM Analyzed Fees (Pre-ECR)
Trailing_12M_Combined_Results – change to TTM Net Analyzed Fees (Post-ECR)
Latest_Month_ECR – change to Current ECR
 