# 2025-08-08
Had to fix a small bug (related to outlook application on distribution)

Tried to convert to openpyxl, but remembered issues with the formatting of numbers and implications.
- before I used to have the numbers as strings and put in $ and %, but then the analysts go in to adjust numbers and they are stored as text and don't work for math.
  - orphaned this branch, but may come back to this later on.

There is some functionality within core transform that I can simplify so I'm not duplicating logic I've built in cdutils.