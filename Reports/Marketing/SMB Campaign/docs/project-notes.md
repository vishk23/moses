# 2025-08-18


list of org types
array(['ASSN', 'TRST', 'CORP', 'REIT', 'MUNI', 'COMP', 'REL', 'LTD',
       'DBA', 'EST', 'LLC', 'LLP', 'PROP', 'NP', None, 'INSR', 'FOVE',
       'TAXR', 'GOV', 'BUS', 'INV', 'PC', 'DEA', 'REAG', 'BRCH', 'PART',
       'LAW', 'OTHR', 'EDUC', 'LEG', 'COMM', 'BANK', 'TAXS', 'CRPT',
       'COOP', 'FLDV', 'CBUR', 'FHLB', 'CU', 'REGN', 'SCHL', 'PROS',
       'INSA'], dtype=object)

I will just exclude BRCH (these are bscb branches)
- other is kind of weird, but might include some valid customers



Here is how I understand the suppression assignment:

1. BCSB provides BKM Marketing with a list of businesses that have at least 1 active account with the bank.
    - We may have organizations that may not be of interest, but an extensive list (including non-profits, munis, and other non-applicable types) is fine because they will be filtered out later on anyway
2. BKM Marketing has a list of prospects from their own research/data sources
    - They will exclude existing BCSB customers from the suppression list in step 1
3. BKM Marketing will handle distribution
4. Repeat over the course of the period
    - If a new prospect has signed up for an account with the bank, they will now show up on the BCSB provided suppresion list in step 1. When completing step 2, that new customer won't be mailed because they are filtered out.


A second piece is the DO NOT MAIL piece, which falls out of the scope of the above section. We will need to maintain a list of business not to mail to and we have a field "ALLOWPROMOYN" (in WH_ORG table in engine 1 database).

