= Loan Report with 45 lookback =
Status: In-progress
v.1.0.0
\\10.161.85.66\Home\Share\Data & Analytics Initiatives\Project Management\Chad Projects\Weekly Reports\NewLoanReport_LR_Credit


Key Stakeholder: Paul Kocak

This is a modification of an existing report to assist Loan Review in ensuring all the new loans are booked correctly
and to keep tabs on all the new loans that are being originated with a 45 day lookback.

Milestones:
- [x] Gather fields necessary
- [x] Code out report
- [ ] Automate formatting
- [ ] Streamline distribution


= Notes =
Filters:
[MJACCTTYPCD] IN ("CML", "CNS", "MTG", "MLN") 
AND 
[CURRMIACCTTYPCD] != "CI07"

If [MJACCTTYPCD] IN "CNS", [CURRMIACCTTYPCD] IN ("IL02", "IL11", "IL12", "IL13", "IL14") 
AND 
!IsNull([TAXRPTFORORGNBR])
