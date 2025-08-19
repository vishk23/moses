Portfolio Alerts
===

Meta Information
---
Developed by CD

v2.1.1-prod

Key Stakeholder(s): Linda Sternfelt, Tim Chaves, Hasan Ali

File Path: \\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Chad Projects\Alerts

TTI: ~30 hours

## Overview 

This is an automated system that tests a specific subset of the loan portfolio across dimensions that may indicate a derioration in credit quality. It aggregates data across several sources (COCC, Xactus, soon to be D&B)

Current Parameters for Products Tested:
- Lines of Credit under $500M & under $1MM in total relationship exposure

### Red Flags
- TTM Past Due >= 3
- TTM Past Due 30 Days >= 1
- TTM Overdrafts >= 5
- Deposit Change <= -%30
    - Relationship needs have to have $250,000 in deposits to be test on this flag
    - Will be trailing 3 months vs trailing 12 months
- Utilization Limit >= 60%

Project Tracking
---

### TODO
- Integrate portfolio key
- Update PowerBI Dashboard based on latest call (2024-12-12)
    - Update the parameters above after adjusting these
- Build a process around the credit scores to integrate with the system

### DONE
- Develop prototype in Alteryx
- Develop more robust system (version 2) connected to COCC Data and programmed in Python
- PowerBI Dashboard developed
- Develop Xactus extract
    - We have credit scores to integrate now

### FUTURE WORK
- Connect to D&B data
- Refactor code and make more modular

Notes
---
### 2024-12-06

Meetings
- Dec 12
- 14:30-15:30
- Myles Standish conference room

Prior to the meeting, need to resync workflow to the environment and refresh the data

Xactus template should be ready to go and should have a streamlined way to inferface with quarterly credit score update
- This gets updated to COCC


### 2024-12-12
Update NOTEBAL to Deposit Balance

Daley & orton

EBL reviews
- Different handling (outside of system) 

Increase TTM line utilization (70%)

3mo vs TTM for deposits

Roll it up on the relationship level.
- Supplement with a separate full summary

60 days - 30-45 day SLA

Inactive date - 60 

Test all of them 1 quarter out or the ones that fail 3 or more

Judgements & Liens
Y/N

### 2025-01-15
- Built extract file
    - Cross-validated with Colin's PFS check. Only about 30 didn't pass the check and can go back and get those later
- Permission DB created
    - just CSV file, but saves permission ('Y') for soft pull, so we won't need a thorough review from intern in the future.
    - Colin had performed a check through this twice
    - The critieria is they have a PFS on file or loan officer is 'EBL PROGRAM ADMIN', as EBL loans have permission verbiage embedded in the application.
- David Piesco Putnam came through all the way, but no address
    - Xactus said they would exclude everything that wasn't complete anyway

### 2025-01-25
- We have the data as of this week.
- It is on my list to get to so I can deliver and close out this Project
    - Aside from ongoing maintenance

### 2025-01-31
From my email recapping 2025-12-12 meeting (to-do):
```
I'll make some adjustments/tweaks to the model & output based on the feedback.
Aggregate the testing to the whole relationship and any fails on individual products will trigger the flag
Increase line utilization flag to 70%
Adjust logic for deposit testing to rolling 3 months vs trailing 12 months. 
Build additional summary screen
We will perform backtesting & validation to provide transparency into the model for audit and regulators.
Business Intelligence, Loan Review & Credit resources.
```

### 2025-02-04
- Delivering and closing out this project in a week
- Codebase cleanup and modularize
- Attach credit scores system with easy I/O and updates
- Starting v2.1.0-dev
- almost adjusted loans to include NPFM, but I remember John telling me we wouldn't want them included for this system, because they are already being monitored.

I need to find out what the Score_Derogatory flag is
- appears to be if there are any derogatory marks for that person affecting their credit score

- Need to implement type hinting for static analysis
    - will be secondary to getting this all refactored and running with credit score component.

- I forgot that the daily deposit file was being used here as well.

Made good progress in the morning focus block on restructuring v2.1.0-dev, will continue this afternoon.

Wrapped up v2.1.0-prod. Major changes to the code base, not in terms of things it is doing, but API improvement and making this easier for future modifications and maintenance.

Successful run, no errors.

Tomorrow, I'll start implementing the changes on Hasan/John's list from the earlier meeting.

### 2025-02-07
- Shipping this by EOD, or at leasts to have the tweaks factored in.

High level, we have end to end system. Tweaks are to:
- adjust line utilization level
    - done
- engineer a new daily deposit data file
    - 3 month rolling balance
    - done
- roll this up on the portfolio level
- integrate the credit scores

v2.1.1-dev

Didn't get to all of it today, but will wrap this up tomorrow. Top of the list and needs to get done.

### 2025-02-08
- Additionally, need to update the PDF that gets sent out to everyone ahead of wednesday meeting with the parameters and overview.
- Deposits can use portfolio key or household key interchangeably
- A thing to consider is how we want to roll this up to the household level
        - end data is on the acctnbr level
        - the deposit data is on the household level (or portfolio level, interchangeable)
        - If we had 2 products in the same relationship that are being tested by alerts, we wouldn't want to add the total household statistics, those stay separate.
    - Ideally create something like a separate deposit detail sheet

Going to create several sheets as output, as more data is better than less in terms of visibility into the system and for auditability
    - Will have PDF print version for each snapshot. Example will be in Output folder as I wrap up this project
The credit score piece is pretty straightforward
- tying back via ALLROLES table and SSN as primary identifier, as firstname lastname concat had a couple mismatches

### 2025-02-09
CREDITSCORECONSINFOCD on Acctloan and Pers tables are interesting
- Connect credit scores to main file and create a criteria flag for it
- Add credit score to summary/own page on PBI
- Create additional page on PBI for my parameters
- Update markdown document overview to send out
- Review and update project management documentation

Link to distribute:
https://app.powerbi.com/links/b6Lv3llm2o?ctid=b269c861-cff0-4856-8634-20b246d56976&pbi_source=linkShare


### 2025-02-12
Working group meeting to go over procedures for business line to use this
- Will share my development accomplishments

cleanup provision only if $100,000

SBA authorization date
Orig date
- in regard to SBA

2nd tuesday of April

PFS delta extract to send out the loan offerings

Good meeting, a couple extra things to do:
- Additional screen for all those that had at least 1 fail in the quarter on the PBI
    - already exists, we just apply a filter to the master table for passed due flag.

### 2025-03-15 [v2.1.8-prod]
Revisiting code and documenting components. I found the daily deposit piece was using cached data, so I fixed this. The caching data is really a development only feature and needs to be disabled for Production.

Second guessing the logic that is programmed for the daily deposit section. I need to check how the 3 month and 12 month averages are being calculated. This daily deposit file will be recreated and most of it is already done here. Have to go through it line by line and ensure it's creating exactly what we want to create.
- Verified it is correct, go me! I had isolated to month end dates ahead of time, so I'm capturing exactly what it is supposed to.

However, there is a new error that is popping up that I need to solve. 
- during the deposit file part, they were coming through as integers and I needed them to be float to handle the division.
- fixed.
