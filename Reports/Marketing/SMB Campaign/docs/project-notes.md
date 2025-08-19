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

Note: Some business addresses have their full street address listed as PO box, which shows up on the data that was sent over.

A second piece is the DO NOT MAIL piece, which falls out of the scope of the above section. We will need to maintain a list of business not to mail to and we have a field "ALLOWPROMOYN" (in WH_ORG table in engine 1 database).


---

# --- 1. Setup ---

# Define the set of type codes that should be part of a full street address.
# Using a set provides very fast lookups (e.g., `if 'street' in STREET_TYPES:`).
STREET_TYPES = {
    'street', 'apartment number', 'mobile home park name', 'rural route number',
    'building number', 'suite number', 'apartment complex name', 'room number'
}

# Sample data representing rows from your database table.
# This would typically come from a database query like `cursor.fetchall()`.
raw_address_data = [
    {
        'id': 101, 'city': 'Springfield', 'state': 'IL', 'zip': '62704',
        'text1': '123 Maple St', 'text1_type': 'street',
        'text2': 'Apt 4B', 'text2_type': 'apartment number',
        'text3': None, 'text3_type': None
    },
    {
        'id': 102, 'city': 'Metropolis', 'state': 'NY', 'zip': '10001',
        'text1': 'PO BOX 4567', 'text1_type': 'post office box number',
        'text2': 'ATTN: Accounts', 'text2_type': 'attention',
        'text3': None, 'text3_type': None
    },
    {
        'id': 103, 'city': 'Gotham', 'state': 'NJ', 'zip': '07001',
        'text1': '45 Ocean View Dr', 'text1_type': 'street',
        'text2': None, 'text2_type': None,
        'text3': 'Building C', 'text3_type': 'building number'
    },
    {
        'id': 104, 'city': 'Metropolis', 'state': 'NY', 'zip': '10001',
        'text1': 'PO BOX 1122', 'text1_type': 'post office box number',
        'text2': '555 Side Street', 'text2_type': 'street',
        'text3': None, 'text3_type': None
    },
    {
        'id': 105, 'city': 'Springfield', 'state': 'IL', 'zip': '62704',
        'text1': '789 Industrial Pkwy', 'text1_type': 'street',
        'text2': None, 'text2_type': None,
        'text3': None, 'text3_type': None
    }
]

# --- 2. The Cleaning Logic ---

def create_full_street_address(address_records):
    """
    Processes a list of raw address records and returns a cleaned list.
    """
    cleaned_data = []

    # Loop through each record (e.g., each row from the database)
    for record in address_records:
        street_parts = []

        # Check text1, text2, and text3 in order
        for i in [1, 2, 3]:
            text_value = record.get(f'text{i}')
            type_value = record.get(f'text{i}_type')

            # Ensure both text and type exist, and the type is a street component
            if text_value and type_value and type_value.lower() in STREET_TYPES:
                street_parts.append(text_value)

        # Join the collected parts with a space.
        # If street_parts is empty, this will correctly result in an empty string.
        full_address = ' '.join(street_parts)

        # Create a new, clean dictionary with the final address
        new_record = {
            'id': record['id'],
            'Full_Street_Address': full_address,
            'city': record['city'],
            'state': record['state'],
            'zip': record['zip']
        }
        cleaned_data.append(new_record)

    return cleaned_data

# --- 3. Execution and Output ---

# Run the cleaning function on our raw data
final_data_extract = create_full_street_address(raw_address_data)

# Print the results in a readable format
print("Resulting Cleaned Data:")
for item in final_data_extract:
    print(item)


---
import pandas as pd
import numpy as np

# --- 1. Setup ---

# Define the set of type codes that belong to a street address.
# Using a set is very fast. We'll compare against the lowercase version.
STREET_TYPES = {
    'street', 'apartment number', 'mobile home park name', 'rural route number',
    'building number', 'suite number', 'apartment complex name', 'room number'
}

# Create a sample DataFrame that matches your structure and column names.
# np.nan represents a NULL value from the database.
data = {
    'addrnbr': [101, 102, 103, 104, 105],
    'text1': ['123 Maple St', 'PO BOX 4567', '45 Ocean View Dr', 'PO BOX 1122', '789 Industrial Pkwy'],
    'addrlinetypdesc1': ['street', 'post office box number', 'street', 'post office box number', 'street'],
    'text2': ['Apt 4B', 'c/o John Doe', np.nan, '555 Side Street', np.nan],
    'addrlinetypdesc2': ['apartment number', 'attention', np.nan, 'street', np.nan],
    'text3': [np.nan, np.nan, 'Building C', np.nan, np.nan],
    'addrlinetypdesc3': [np.nan, np.nan, 'building number', np.nan, np.nan],
    'cityname': ['Springfield', 'Metropolis', 'Gotham', 'Metropolis', 'Springfield'],
    'statecd': ['IL', 'NY', 'NJ', 'NY', 'IL'],
    'zipcd': ['62704', '10001', '07001', '10001', '62704']
}
df = pd.DataFrame(data)

# --- 2. The Cleaning Logic ---

# We will create temporary 'parts' columns, just like in the SQL logic.

for i in [1, 2, 3]:
    # Define the columns for this iteration
    text_col = f'text{i}'
    type_col = f'addrlinetypdesc{i}'
    part_col = f'street_part{i}' # The new temporary column

    # Create the condition: True if the type is a non-null street type
    # .str.lower() makes the check case-insensitive.
    # .isin() checks against our set of STREET_TYPES.
    # .fillna(False) handles cases where the type description is null.
    is_street_part = df[type_col].str.lower().isin(STREET_TYPES).fillna(False)

    # Use the .where() method to get the text value if the condition is True,
    # otherwise, it will be NaN (which is exactly what we want).
    df[part_col] = df[text_col].where(is_street_part)

# Now, combine the parts into the final address column
street_part_columns = ['street_part1', 'street_part2', 'street_part3']

# The .apply() method lets us run a function on each row.
# We join the non-null values from our street parts.
df['Full_Street_Address'] = df[street_part_columns].apply(
    lambda row: ' '.join(row.dropna().astype(str)),
    axis=1
)


# --- 3. Finalizing the Extract ---

# Create the final, clean DataFrame with user-friendly column names
df_clean = df[[
    'addrnbr',
    'Full_Street_Address',
    'cityname',
    'statecd',
    'zipcd'
]].rename(columns={
    'addrnbr': 'id',
    'cityname': 'city',
    'statecd': 'state',
    'zipcd': 'zip'
})


print("Final Cleaned DataFrame:")
print(df_clean)


---

import pandas as pd
import numpy as np

# --- 1. Setup ---

# Define the TYPE sets for clarity.
STREET_TYPES = {
    'street', 'apartment number', 'mobile home park name', 'rural route number',
    'building number', 'suite number', 'apartment complex name', 'room number'
}
POBOX_TYPE = 'post office box number' # It's a single value

# Create a sample DataFrame that can test the new logic
# - ID 101: Street + Unit (Street should win)
# - ID 102: PO Box only (PO Box should be used)
# - ID 104: PO Box and Street (Street should win)
data = {
    'addrnbr': [101, 102, 103, 104, 105],
    'text1': ['123 Maple St', 'PO BOX 4567', '45 Ocean View Dr', 'PO BOX 1122', '789 Industrial Pkwy'],
    'addrlinetypdesc1': ['street', 'post office box number', 'street', 'post office box number', 'street'],
    'text2': ['Apt 4B', 'c/o John Doe', np.nan, '555 Side Street', np.nan],
    'addrlinetypdesc2': ['apartment number', 'attention', np.nan, 'street', np.nan],
    'text3': [np.nan, np.nan, 'Building C', np.nan, np.nan],
    'addrlinetypdesc3': [np.nan, np.nan, 'building number', np.nan, np.nan],
    'cityname': ['Springfield', 'Metropolis', 'Gotham', 'Metropolis', 'Springfield'],
    'statecd': ['IL', 'NY', 'NJ', 'NY', 'IL'],
    'zipcd': ['62704', '10001', '07001', '10001', '62704']
}
df = pd.DataFrame(data)

# --- 2. The Enhanced Cleaning Logic ---

# Step A: Extract both street parts AND po box parts into temporary columns
for i in [1, 2, 3]:
    text_col = f'text{i}'
    type_col = f'addrlinetypdesc{i}'
    
    # Condition for street parts
    is_street_part = df[type_col].str.lower().isin(STREET_TYPES).fillna(False)
    df[f'street_part{i}'] = df[text_col].where(is_street_part)
    
    # Condition for PO Box parts
    is_pobox_part = (df[type_col].str.lower() == POBOX_TYPE).fillna(False)
    df[f'pobox_part{i}'] = df[text_col].where(is_pobox_part)


# Step B: Combine the parts into two separate, complete address strings
street_parts = ['street_part1', 'street_part2', 'street_part3']
pobox_parts = ['pobox_part1', 'pobox_part2', 'pobox_part3']

df['combined_street'] = df[street_parts].apply(
    lambda row: ' '.join(row.dropna().astype(str)), axis=1
)
df['combined_pobox'] = df[pobox_parts].apply(
    lambda row: ' '.join(row.dropna().astype(str)), axis=1
)

# Step C: Apply the final rule: Use Street, but if it's empty, use PO Box.
# First, replace empty strings '' in the street column with NaN so .fillna() works
df['combined_street'].replace('', np.nan, inplace=True)

# Now, use .fillna() to populate empty street addresses with the po box value
df['Full_Street_Address'] = df['combined_street'].fillna(df['combined_pobox'])


# --- 3. Finalizing the Extract ---

# Create the final, clean DataFrame with user-friendly column names
df_clean = df[[
    'addrnbr',
    'Full_Street_Address',
    'cityname',
    'statecd',
    'zipcd'
]].rename(columns={
    'addrnbr': 'id',
    'cityname': 'city',
    'statecd': 'state',
    'zipcd': 'zip'
})


print("Final Cleaned DataFrame:")
print(df_clean)

---

FutureWarning: A value is trying to be set on a copy of a DataFrame or Series through chained assignment using an inplace method.
The behavior will change in pandas 3.0. This inplace method will never work because the intermediate object on which we are setting values always behaves as a copy.

For example, when doing 'df[col].method(value, inplace=True)', try using 'df.method({col: value}, inplace=True)' or df[col] = df[col].method(value) instead, to perform the operation inplace on the original object.


  df['combined_street'].replace('', np.nan, inplace=True)