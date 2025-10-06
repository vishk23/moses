Links:
https://clientexperience.getbuilt.com/project-updates

# 2025-09-04

Kickoff meeting with everyone


From hasan
```
FYI, just so we are on the same page – Tim and I discussed not having all construction loans roll into BUILT.  We will set thresholds for loan that exceed a certain dollar figure.  It could be $1MM or $2MM – I need to review the construction loan portfolio.  We don’t want smaller less complex loans in Built and eat up our CUCV (amount we can put into Built for free).  When the time comes to provide the loan data, I just want to make sure we don’t give them all construction loans.
```


# 2025-09-18

Resi:
2 residential minors
- 

we sell - disbursement of repairs
- set up schedules for disbursements


Savngs 

Escrow Reserve Holdback
- field

Chris to send me logic on resi side.


Met with Hasan/kelly a/Deva to review cml side and process
- sent through


# 2025-10-04
Need to have extract done by Mon Oct 6

Will get done. Mapped out a bunch of this in my head already, just need to build.

CML
- hard code 12 acctnbrs
    - later userfield to specify built
MTG
- chris gave me specific instructions on logic

Package into a single file
loan_type: commercial/resi

Separate pipelines but same schema (mostly), concat together

# 2025-10-05

Action plan:
1. new core.py
2. cml first
    - hard code acctnbrs
    - acct user field to specify later on
3. get all fields to match extract from silver layer (bronze if needed or source)
4. mtg data
    - look at chris logic he sent me
    - create separately with same schema
5. concat together
6. schedule send first thing in morning
    - explain I'm on PTO but will be back EOD to send to them via mimecast.
    - please send me thoughts/revisions/questions if necessary


Question for Hasan:
- once these are no longer construction and switch to PERM, they no longer are managed in BUILT correct?
    - They would just come off the extract in view

Please correct me if I'm wrong.

Need clarification on closedate whether that's contractdate or origdate
- making executive decision that it's orgidate

# 2025-10-06

FIELDS:
Loan Number

Line Of Credit Account Number
Project Reference ID
Project Type
Loan Amount

Draw Funded to Date
Close Date
Maturity Date
Interest Rate
Cost Center
Account/ GL Number 
Is Builder
Additional Reference ID

Line Of Credit Account Number
Loan Amount
Term (Months)
Revolving
Loan Maturity Date
Line of Credit Type

Product Type (Residential)

Asset Class

Renovation Product
Purpose
Retainage Percentage

Construction Start Date
Construction End Date
Appraisal Date
Appraised Value
Owner Occupied
Purpose Code
Notes

Property Address
Property City
Property State or Property Province
Property Zip or Postal Code
Property Lot Number
Property Subdivision Name
Property Type
NAICS Code
Parcel Number
Square Feet

Borrower Company Name
Borrower Admin First Name
Borrower Admin Last Name
Borrower Address
Borrower City
Borrower State or Borrower Province
Borrower Zip Code or Postal Code
Borrower Admin Email
Borrower Admin Home Phone Number
Borrower Admin Mobile Phone Number
Borrower Admin Office Phone Number

Builder Company Name
Builder Admin First Name
Builder Admin Last Name
Builder Address
Builder City
Builder State or Province
Builder Zip Code or Postal Code
Builder Admin Email
Builder Admin Home Phone Number
Builder Admin Mobile Phone Number
Builder Admin Office Phone Number

Equity Type
Equity Amount
Equity Amount Remaining
Equity Source Type
Equity Disbursement Rule

Disbursement Method
Disbursement Account Number
Disbursement Aba Number
Disbursement Payee Address
Disbursement Payee City
Disbursement Payee State
Disbursement Payee Zip Code
Disbursement Payee Bank Name
Disbursement Payee Bank Address
Disbursement Payee Bank City
Disbursement Payee Bank State
Disbursement Payee Bank Zip

Loan Administrator Email
Relationship Manager Email
Inspector Email

Title Company Company Name
Title Company Admin First Name
Title Company Admin Last Name
Title Company Address
Title Company City
Title Company State
Title Company Zip Code
Title Company Admin Office Phone Number
Title Company Admin Mobile Phone Number
Title Company Admin Home Phone Number
Title Company Admin Email
