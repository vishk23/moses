Objective:
Extract loan and deposit growth in different regions and plot against our grants/Foundation 

Usage:
- notebook only for now.

# 2025-09-12
I think this is historically about 10% of NI.
- or operating profits, not sure exactly

Ideally 1 graph
All loans/deposits (Year end figures)
- break out by the regions that CPG uses

----

Roadmap:
- Pull in full data
    - For different year ends
    - Bounce off of balance tracker and other things for accuracy
- Apply region mapping
    - Need to categorize all branches to region
- Get annual totals (group by)
- Consolidate df with giving data (years as columns should match)
- Plot this
    - figure out optimal way to show this all on one graph


I was thinking matplotlib, but might as well do powerBI. Maybe I start with matplotlib.

df should be year end dates as the rows. The columns would be the regions and loans/deposits (and there should be a total too), like a double column index in a pivot table. This should be whatever is going to load cleanly into both matplotlib and PowerBI

Idea for graph is time on X axis
