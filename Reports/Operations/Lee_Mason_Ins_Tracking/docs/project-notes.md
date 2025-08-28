# 2025-08-20

Picking this back up.

Real estate loans for ins tracking is the goal.

Resi, commercial, HE loans in a flood zone

---

I need Kelly to walk through filters and a few examples to get me to exactly where I need to get to on this.

---


Thank you. It also needs to only home equity loans that are in a flood zone. We will have a blanket policy for HE and will not need to track them unless they are in a flood zone.


# 2025-08-22

I was supposed to meet with Kelly, but I think things got busy on her end.

I'll work on this next week to bring to natural conclusion.
- there are assumptions and filters that I need her to check on. Sometimes, I don't know where things are in our uncataloged database.


# 2025-08-22

Most of the data is from account
- some accounts will have collateral
- some collateral will have insurance attached.
    - I think this is the link, but not sure


Account:
- acctnbr
- ownersortname
- Borrower_name_2 ?
    - NonTax Signator
- primary address (cleaned from BKM)
- primary city
- primary state
- primary zip
- notebal 
    - or bookbal
- creditlimitamt
- total exposure?
Collateral:
- Cleaned PropType
- proptypdesc
- Collateral type:
    - Real Esate/Auto/Misc?
- Prop street
- prop city
- prop state
- prop zip
Insurance:
- insurable value
- replacement cost
- flood zone
- coverage type
    - Hazard, flood, BPP, Auto
- premium escrowed
    - Yes/No
- loan type
    - Resi/Commercial
    - major or some form of product mapping
- building type?
    - residential/commercial/condo/mobile home/land
    - isn't this collateral type
        - proptypdesc



----
# 2025-08-28

Questions for Kelly

On account table, do we only want accounts where there is an active insurance policy?

Commercial (CML/MLN)
Resi (MTG)
- HE only in flood zone?
    - These are a subset of MTG


Chad Business
- 123
    

L&M track every property end goal

4 types of home equity

Doesn't need PMI

If there is no property, don't include loan

coverageamt is the same for insurable value + replacement cost

