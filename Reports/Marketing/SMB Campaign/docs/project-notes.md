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
