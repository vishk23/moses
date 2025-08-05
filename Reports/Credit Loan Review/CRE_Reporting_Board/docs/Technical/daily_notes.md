Daily Notes: Project Name
===
### 2025-02-12
- The board presentation will be 2025-02-25 (Tuesday)?

Two main areas where I need to assist:
- Visuals for CRE & interest rates
- Balance tracker updated so it works
    - Progress on this project is tracked in another directory

For the visuals on CRE, we validate against Call Report and COCC numbers should be exactly the same as reported.

### 2025-02-14
- CML indirect get classified as CIUS, while indirect is normally (AUTO) from the CNS major.
    - Get clarification on this
- Need to redo the interest rate graphs.

From linda:
```
Thank you so much for working on this presentation.

 

Here is my work in process.  I think we need a new slide 3 (ICRE Production), slide 8 (NOO Growth), slide 9 (Total Commercial Portfolio), slide 10 (Investment CRE Portfolio), slides 11-14 and slide 18.  I will finish the market data stuff today.  Does that make sense to you?  I can review the draft with Tim next week and hopefully he will not want to see a lot of changes except to the slides that I create/created.


Thanks again.  Much appreciated.  Have a great weekend!


```


Going through the call report vs the single_per_loan data dump I gave to Linda with 12/31/24 numbers.
Almost perfect, but need to adjust the tax exempt bond rule. Since 100% participated, not sure why they had net balance.
Oh wait, do they have net balance?
- It's possible the fed call report is missing this. Mine should stay.

Going to build a fully automated call report report reconciliation.
- I am looking at only commercial stuff, but call report numbers have MTG and AUTO and all other majors in there. Outside the scope of the presentation for Tim.

This is good that I'm doing this before the balance tracker, because they are kind of the same in the sense that it's just reconciling with this call report.

Listed a couple of accts that have no fed call code for someone to take a look at.

This took several hours.

Keep in mind, we can do the top 5 easily in the future by creating a table and just filtering. I deleted this.

Need to pull out items from the next rate change where next rate change >= maturity date


### 2025-02-15 [v2.0.0-prod]
Need to do the few remaining slides Linda had asked me for
- Plus fix the next rate change
- This should be a new custom report rather than the Tom K alteryx WF so all inputs come from here

Created icre_production.py file to do this for 3 years, will expand to more years if necessary, but I think 3 is good. Using noteopenamt

Created both icre_production and icre_balances from the same script as it's mostly the same pipeline but using balance vs noteopenamt
- Ties back to cre_loader, which is key because that ties to Call Report

Finally, sent this out to Linda for review. We'll see about feedback and tweaks. 

### 2025-03-05
Went through and created technical documentation for this.
- took inventory of the process and it is much cleaner than before

Something to be aware is any filters that may be applied from mid-analysis on PowerBI. Next time around, we will make a note to review any filters that are applied and it probably makes sense to have a fresh copy of the dashboard and then a working copy. The working copy can be where I do the analysis, looking at the data in different ways and looking at filters. That way, i'm not touching the vanilla dashboard.

Significantly easier to produce this going forward, now that we took the time to reorganize everything and do the reconciliation to the call report. 

### 2025-03-12
Went in today to address the item that Linda had brought up with my CML Var filter not working properly. She was correct that it wasn't working and we had the same customers showing up on both graphs. This is because one was a Date and the other was a Datetime and it wasn't working correctly in Alteryx. I cut alteryx out of this and just built this in with the rest of my script.

The loan types to exclude from the Interest Rate changes slide are:
- 1 Month CME Term SOFR
- BCSB corporate base rate
- the loan default
- WSJ prime

On that slide, we want Customer, Product, Next Rate Change, Net Balance
- need to apply the VAR to the ratetypcd

On the other slide for CML maturities, do we want to see 
Not Redbrook or EGMP 825 N Main

[FUTURE TODO]
Also, need to revisit the property type grouping when I get the 1 property type to append. It should actually a groupby property typ, sum it up and then take that as the property type.
- instead of max appraisal value amt getting appended, I can do an intermediate calculation here. I'll need to think about this for a small amount, but I'll get to it.
- won't need an update on this until the next time this report is run, which will be mid-summer.

