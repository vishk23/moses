## Grant vs Growth (Overview)
- Created by Chad Doorley
- 09/15/2025

### 1. Pulling Account Information

The script starts by gathering a snapshot of all customer accounts for year end dates from 2020-2024.
It then groups these into two main categories:

* Loans (mortgages, personal loans, etc.)
* Deposits (checking, savings, time deposits)

---

### 2. Linking Properties and Addresses

Each account may be tied to a property. The script looks up those properties, keeps the highest-value property for each account, and then adds in address details like ZIP codes.

Zip code of collateral is the primary determinant of where something gets coded, with borrower primary address as the default if there is no collateral attached to an account.

---

### 3. Assigning Regions

Using the ZIP codes, the script assigns each account to a region. The regions are:

* Rhode Island
* South Coast – Southern Bristol County (Fall River, New Bedford, Dartmouth, etc.)
* Attleboro/Taunton – Northern Bristol County
* Other – if it doesn’t fall into the above areas (Boston, Cape Cod, etc.)

---

### 4. Creating the Summary

Finally, the script adds everything together and creates a summary report. It shows the total amount of money in loans and deposits, broken down by region. This feeds directly into the visuals.

---

## Impact

This helps BCSB understand the impact and trends of Foundation grants across different regions and seeing how that relates to growths on loans/deposits.


