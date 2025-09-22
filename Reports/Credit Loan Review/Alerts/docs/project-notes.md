Usage:
- cd to Production/ within repo
- python -m src.main
- for guarantor, utilize notebooks/permission_recon1 (fails) and permission_recon_pass (passes) for building extract to Xactus



# 2025-09-19

Alerts Q4 meeting coming up.

For permission db, everything is local, dev mode. No Project management folder on da1. Will do a refactor, but want to keep everything in the same place for this run.
- easier to manage

Pulled out equip line of credit per Linda's request. There was only 1 that came through. Not sure about the other 2 she mentioned that were coded as regular lines of credit.

Make a note about persnbr
421
1027703

Employee relationship not included in system, or should be included in system. What is more compliant?

# 2025-09-22
Can definitely create a calculated field for permission
- EBL loans are automatically in

We are all set for this run because we hand reviewed it, but can be part of the logic

The Employee YN question remains

I build this all in permission_recon_pass.ipynb to build xactus extract and we can go from there
- semi-manual to put all of this together.

I'll need to load back in via regular methods. Inspect code to see what's going on there.

This will receive a refactor, but running up against deadline so will get it working as regular and make modifications for next cycle.