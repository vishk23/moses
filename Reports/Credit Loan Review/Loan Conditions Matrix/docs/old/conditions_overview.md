Loan Conditions
===

Notes
---
### 2025-05-24
Example output from survey
Requirements Summary

Appraisal
─────────
• An appraisal is required and should not be dated more than 12 months prior to loan closing. Appraisal dated in excess of 12 months are considered Policy Exceptions. Note, per policy loan to value is calculated based on the lesser of the properties purchase price or appraised value.
• Secured property is subject to a bank ordered appraisal showing a maximum loan to value not to exceed XX%

Environmental
─────────────
• A Phase 1 assessment is required.

Flood
─────
• The following conditions are required: Customer was informed 10 days prior to closing, The flood insurance been reviewed by compliance, Sufficient flood insurance has been obtained

Financial Statements
────────────────────
• Please list the loan type:: Special loan
• Corporate guarantor requirements: FYE Statements within 120 days of FYE or 30 days of filing, Interims, if required, Any supporting statements/reports, if required, Projections if applicable or required

### 2025-05-22
Loan conditions matrix/waterfall:
- for appraisals, add in a note at the top without the option to select it


Is this a CRE Secured loan, other than 1-4 family residential property or real estate taken as an abundance if caution
- Yes
    - Please select one of the 6 options? 
        - Checkbox option 1
        - Checkbox option 2
        - Checkbox option 3
        - Checkbox option 4
        - Checkbox option 5
        - Checkbox option 6
    - Is further action required?
        - Yes
            - Please fill in the box below with details?
                - Open ended box where people fill this in
        - No
- No


Loan Option 6 Selected
- look at this on the loan to individual section

Copies of any mortgage loan statements
- SBLC loan, should be on a second line


# Flood
Is the loan secured by real estate?
- Yes
    - Has flood certificate been generated? 
        - Yes
            - Did the certificate indicate that the property is in a flood zone (AE/V)?
                - Yes
                    - %The following conditions are required:
                        - The customer was informed 10 days prior to closing
                        - The flood insurance been reviewed by compliance
                        - Sufficient flood insurance has been obtained
                - No
                    - %No further action required
        - No
            - Flood cert must be generated
- No
    - Is the loan a guaranteed SBA loan secured by building contents ?
        - Yes
            - Did the certificate indicate that the property is in a flood zone (AE/V)?
                - Yes
                    - %The following conditions are required:
                        - The customer was informed 10 days prior to closing
                        - The flood insurance been reviewed by compliance
                        - Sufficient flood insurance has been obtained
                - No
                    - %No further action required
        - No
            - %No Further Action is required

Build out the SWAP/ hold on the ARC

SWAP section:
Is this a Swap Loan? 
    - Yes
        - Has Swap Checklist been Completed and all pre-closing documents been received?
            - Yes
                    -%No further action needed
                - No
                    - %Please complete the SWAP Checklist
    - No
        - %No further action needed



### 2025-02-11
Met with Eldora & Paul. Going to build a sample of this, hopefully before next week's meeting (but it is a busy week so I'll do my best)
- First approach was with excel, but that will be too clunky for a process like this where the users are answering questions and different questions are popping up based on how they answer those questions.

Modular approach:
- they are splitting the conditions into sections
Right now it is:
- Appraisal
- Environmental
- Financial Statements

These are listed in increasing complexity (nested questions)

Tech stack for this: vanilla HTML/CSS/JS and users can run this in their browser
- We could explore hosting this for internal users, but we can just put .html in a shared location or bookmark for people so they can access this.
- at least for first iterations, we'll do this approach


### 2025-02-25 [v1.0.0-dev]
Completed this demo. 
Includes the 3 sections that paul & Eldora outline in the excel form

condition_matrix.html