CoStar
===

Meta Information
---
- Developed by CD
- v2.0.0-dev
- Overview:
    - An extract of CRE related CML loans is provided to CoStar on a monthly basis to update the CoStar Lender Platform
    - CoStar has redesigned their input files and this initiative will be the a remapping of all the same existing fields, but in a different format that integrates with their system in a smoother fashion

Milestones
---
- TODO Remap Extract File

Notes
---

### 2025-01-23
- Initializing this project today.
- Work will not on this until wrapping up a few other projects
- Met with Max today over a call:
    - Described new input features
        - Redesigned templates which needs to be remapped to
        - There are 2 templates now: one for the full list of loans and the other as a balance update (or updating other fields)
            - Need to build a process for charged off loans + closed loans (early paydowns) where I would be setting the maturity date to 1 (for prior month)
                - He explained this with an example, but I will need to get in there and play with this.