Objective:

To create a person mailing list to North raynham Branch Construction customers

Params:

Assigned to N Raynham
Transacted at N Raynham within 90 days
Address within a 5 mile radius of N. Raynham, Raynham Center, Main Office
Owns Safe Deposit Box @ N. Raynham
Exclusions (do we have standard exclusions for all mailings? Including common ones below)
Customers under 18 years of age
Deceased customers
Charged off accounts
 

Data fields:

First name
Last name
Address
City
State
Zip


# 2025-09-24
A couple things on this.
- don't forget that pers is the end goal, where we will be having persnbr as the centralized view here

active acct assigned to N raynham is easy
address within 5 mi radius, need some geocoding
    - or simple rule to just get town name
age is easy to filter out

I think safe deposit boxes would have a branch name right?

Businesses are included too.

# 2025-09-26

Will devote some time to working on this today. We will have a customer dimension table as the end goal, which will have certain critiera to show a person or a business.

O+orgnbr or P+persnbr will be the primary key here
- easy decoding and encoding to get at some of the other tables here.

Mapped out how this works:
customer dimension table created from wh_org, wh_pers, pers, org
    - has addrnbr and typical exclusion fields

append address

Separately, we handle account table
- create customer_id to match primary key of customer dim
- branch name will be a filter later on
- need calculated field from rtxn table (90 day#  window) to see if transacted at this particular branch
    - basically becomes a boolean on rtxn table that gets left joined to active account table

This gets joined back to the customer dim table
- filter down, exclusions

Ready to share.

# 2025-09-28
Minor issue. Pulled all orgs/pers and db looks like 100% of records have N for allow promo. So we don't allow promo for anything?

No way to peer into historical view of this. No db access on that.

Regardless, I can still build customer dim and create this, but I don't know if we can send things out. Someone must've done something because this wasn't historically what org and pers tables looked like.

# 2025-09-29
Not a major factor. Checked with Tom K and this is all set. No issues there.
- not used as an exclusion at all. This is just the state of the database.