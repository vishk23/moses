# 2025-08-08
Had to fix a small bug (related to outlook application on distribution)

Tried to convert to openpyxl, but remembered issues with the formatting of numbers and implications.
- before I used to have the numbers as strings and put in $ and %, but then the analysts go in to adjust numbers and they are stored as text and don't work for math.
  - orphaned this branch, but may come back to this later on.

There is some functionality within core transform that I can simplify so I'm not duplicating logic I've built in cdutils.

# 2025-10-01
Fixed face value amount
- still testing but I think I got it

New cdutils function that gets orig face amt
- earliest (min) effdate, query then for each account number.

Incurred a bit of tech debt with way I coded this, but will be more efficient for sure than embedding into pipeline.

Make run time faster. To be cleaned up later on.

Tim brought this to my attention, had to fix this.