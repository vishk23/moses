# **Data Catalog: BKM Marketing Campaign Suppression List**

#### **1. Overview**

1. BCSB provides BKM Marketing with a list of businesses that have at least 1 active account with the bank.
    - We may have organizations that may not be of interest, but an extensive list (including non-profits, munis, and other non-applicable types) is fine because they will be filtered out later on anyway
2. BKM Marketing has a list of prospects from their own research/data sources
    - They will exclude existing BCSB customers from the suppression list in step 1
3. BKM Marketing will handle distribution.
4. Repeat over the course of the period
    - If a new prospect has signed up for an account with the bank, they will now show up on the BCSB provided suppresion list in step 1. When completing step 2, that new customer won't be mailed because they are filtered out.

#### **2. Data Sources**

The process queries the internal relational database to construct the customer list.

#### **3. Workflow and Business Logic**

The suppression list is generated through the following automated steps:

1.  **Fetch Source Data**:
    *   Organization, Account, and Address level data is queried.

2.  **Filter and Refine Organizations**:
    *   The `WH_ORG` table is deduplicated by the unique organization number (`orgnbr`) to ensure one record per business.
    *   Internal entities are removed by filtering out organizations where `orgtypcd` is `'BRCH'` (Branch) or `'BANK'`. This ensures the list only contains external customers.
        * Note: There may be more organization types than needed (non-profits, religious, municipals included in this list, but these would all be excluded anyway from my understanding). A more full list of organizations is preferable than excluding specific organization types and then mailing a business that is already a customer.

3.  **Identify Active Customer Relationships**:
    *   The active account list is filtered to include only accounts tied to an organization (i.e., not tied to an individual person).
    *   Calculate the earliest account open date (`earliest_opendate`) for each organization, establishing the start of their customer relationship. The dataset provided can be filtered in descending order on this field to see customer that opened a new account (Loan or Deposit) at the top.

4.  **Process and Standardize Addresses**:
    *   A key function (`create_full_street_address`) is used to construct a single, complete address line from the multiple raw fields in `WH_ADDR`.
    *   **Address Logic**: The function correctly identifies and assembles various address components (street, suite, building number). It gives precedence to the physical street address. If a physical street address is not available, it populates the field with the Post Office Box number.
    *   The `ORGADDRUSE` table is used to select only the **Primary** (`'PRI'`) address for each organization.

5.  **Generate Final Suppression List**:
    *   The filtered organization data is joined with their earliest open date and their primary, standardized address.
    *   The final dataset is formatted with user-friendly column names and saved as `bkm_suppresion_list.parquet`. This file is delivered to BKM Marketing.

#### **4. Outside Scope: "Do Not Mail"**

*   **Source**: The `WH_ORG` table contains a field named `ALLOWPROMOYN`. This flag indicates an organization's preference regarding promotional contact.
*   Note: This is not used at all during this process, but the field exists in our database and has been updated in the past so this may be part of a separate process. This would apply to existing customers that opt out of our mailing lists.

#### **5. Output Data Dictionary**

**File**: `bkm_suppresion_list.parquet`

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `Organization Name` | `string` | The legal name of the business entity. |
| `Org Type` | `string` | The bank's classification for the organization type (e.g., 'Corporation'). |
| `Earliest Open Date` | `date` | The contract date of the first account the organization opened with the bank. |
| `Full Street Address` | `string` | The primary mailing address. This will be the PO Box if a street address is not present. |
| `City` | `string` | The city for the primary mailing address. |
| `State` | `string` | The state for the primary mailing address. |
| `Zip` | `string` | The zip code for the primary mailing address. |
