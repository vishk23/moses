import pandas as pd
import shutil
from pathlib import Path
from lxml import html
import re

import src.config
def extract_standardized_report_data(tree, report_title):
    """
    Creates a consistent DataFrame structure regardless of the source report type:
    - customer_name: Name of the customer
    - item_name: Name/description of the item (covenant or tickler)
    - required_value: Required value for the item
    - actual_value: Actual value (if available)
    - period_date: Period/item date
    - due_date: Due date
    - days_past_due: Days past due (if available)
    - interval: Reporting interval (if available)
    - comments: Comments field
    - report_type: Type of source report
    - report_date: Date the report was created
    
    Args:
        tree: lxml HTML tree object
        report_title: Title of the report for context
        
    Returns:
        pandas.DataFrame or None if no data found
    """
    try:
        # Extract report creation date
        report_date = None
        date_elements = tree.xpath("//span[@class='date']")
        if date_elements:
            date_text = date_elements[0].text_content()
            # Extract date from "Report Creation Date : MM/DD/YYYY HH:MM:SS"
            date_match = re.search(r'(\d{2}/\d{2}/\d{4})', date_text)
            if date_match:
                report_date = date_match.group(1)
        
        # Find customer sections - each customer has their own table
        customer_sections = tree.xpath("//tr[contains(@class, '') or not(@class)]//span[contains(@class, 'SummaryTitle clientnameSmall') and contains(text(), 'Customer Name')]")
        
        all_report_data = []
        
        for customer_span in customer_sections:
            # Extract customer name
            customer_text = customer_span.text_content()
            customer_name = customer_text.replace('Customer Name :', '').strip()
            
            # Find the covenant table for this customer
            # Look for the uk-table uk-table-striped table that follows this customer name
            customer_row = customer_span
            current_element = customer_span
            
            # Traverse up to find the containing TD, then look for the table
            while current_element is not None:
                if current_element.tag == 'td':
                    break
                current_element = current_element.getparent()
            
            if current_element is not None:
                covenant_tables = current_element.xpath(".//table[@class='uk-table uk-table-striped']")
                
                for table in covenant_tables:
                    # Extract table data
                    rows = table.xpath(".//tr")
                    if len(rows) < 2:  # Need at least header + 1 data row
                        continue
                    
                    # Get headers
                    headers = []
                    header_row = rows[0]
                    for th in header_row.xpath(".//th"):
                        headers.append(th.text_content().strip())
                    
                    # Process data rows
                    for row in rows[1:]:
                        cells = row.xpath(".//td")
                        if not cells:
                            continue
                        
                        row_data = []
                        for cell in cells:
                            cell_text = cell.text_content().strip()
                            row_data.append(cell_text)
                        
                        if not any(cell.strip() for cell in row_data):  # Skip empty rows
                            continue
                        
                        # Create standardized record
                        item_record = {
                            'customer_name': customer_name,
                            'item_name': '',
                            'required_value': '',
                            'actual_value': '',
                            'period_date': '',
                            'due_date': '',
                            'days_past_due': '',
                            'interval': '',
                            'comments': '',
                            'report_type': report_title,
                            'report_date': report_date
                        }
                        
                        # Map fields based on headers and available data
                        for i, header in enumerate(headers):
                            if i < len(row_data):
                                value = row_data[i]
                                header_lower = header.lower()
                                
                                if ('covenant' in header_lower or 'tickler' in header_lower) and ('name' in header_lower or 'item' in header_lower):
                                    item_record['item_name'] = value
                                elif 'required' in header_lower:
                                    item_record['required_value'] = value
                                elif 'actual' in header_lower:
                                    item_record['actual_value'] = value
                                elif 'period' in header_lower or 'item date' in header_lower:
                                    item_record['period_date'] = value
                                elif 'due date' in header_lower:
                                    item_record['due_date'] = value
                                elif 'days past due' in header_lower:
                                    item_record['days_past_due'] = value
                                elif 'interval' in header_lower:
                                    item_record['interval'] = value
                                elif 'comment' in header_lower:
                                    item_record['comments'] = value
                        
                        all_report_data.append(item_record)
        
        if not all_report_data:
            print(f"No report data found for: {report_title}")
            return None
        
        # Create DataFrame
        df = pd.DataFrame(all_report_data)
        print(f"Extracted {len(df)} records for {len(df['customer_name'].unique())} customers")
        return df
        
    except Exception as e:
        print(f"Error extracting standardized report data: {str(e)}")
        return None
def extract_table_data(tree, report_title):
    """
    Legacy function - Extract table data from HTML tree and convert to pandas DataFrame.
    
    Args:
        tree: lxml HTML tree object
        report_title: Title of the report for context
        
    Returns:
        pandas.DataFrame or None if no data found
    """
    try:
        # Look for the main data table - typically has class "uk-table uk-table-striped"
        main_tables = tree.xpath("//table[@class='uk-table uk-table-striped']")
        
        if not main_tables:
            print(f"No main data table found for: {report_title}")
            return None
        
        main_table = main_tables[0]
        
        # Extract headers
        headers = []
        header_rows = main_table.xpath(".//tr[1]")
        if header_rows:
            for th in header_rows[0].xpath(".//th"):
                headers.append(th.text_content().strip())
        
        # Extract data rows
        data_rows = []
        all_rows = main_table.xpath(".//tr")[1:]  # Skip header row
        
        for row in all_rows:
            row_data = []
            for td in row.xpath(".//td"):
                # Extract text content from td
                cell_text = td.text_content().strip()
                row_data.append(cell_text)
            
            if row_data and any(cell.strip() for cell in row_data):  # Only add non-empty rows
                data_rows.append(row_data)
        
        if not data_rows:
            print(f"No data rows found for: {report_title}")
            return None
        
        # Create DataFrame
        if headers and len(headers) > 0:
            # Ensure all rows have the same number of columns as headers
            max_cols = len(headers)
            normalized_rows = []
            for row in data_rows:
                # Pad or truncate row to match header length
                normalized_row = row[:max_cols] + [''] * (max_cols - len(row))
                normalized_rows.append(normalized_row)
            
            df = pd.DataFrame(normalized_rows, columns=headers)
        else:
            # Fallback: create DataFrame without headers
            df = pd.DataFrame(data_rows)
        
        print(f"Extracted {len(df)} rows with {len(df.columns)} columns")
        return df
        
    except Exception as e:
        print(f"Error extracting table data: {str(e)}")
        return None
def process_xls_files():
    """
    Process up to 5 HTML files (saved as .xls) from input folder and return dict of standardized dataframes.
    
    Returns:
        dict: Dictionary with dataframe names as keys and standardized pandas DataFrames as values
              All DataFrames have consistent columns regardless of source report type
    """
    # Use config paths for input folder
    input_folder = src.config.INPUT_DIR
    archive_folder = input_folder / "archive"
    
    # Create folders if they don't exist
    input_folder.mkdir(exist_ok=True)
    archive_folder.mkdir(exist_ok=True)
    
    # Find all .xls files (which are actually HTML files)
    excel_files = list(input_folder.glob('*.xls'))
    
    # Validate file count and types
    assert len(excel_files) <= 3, f"Found {len(excel_files)} .xls files, maximum is 3"
    all_files = [f for f in input_folder.iterdir() if f.is_file() and not f.name.startswith('.')]
    non_excel = [f for f in all_files if not f.name.endswith('.xls')]
    assert len(non_excel) == 0, f"Found non-.xls files: {[f.name for f in non_excel]}"
    
    # Mapping of report title patterns to dataframe keys
    df_mappings = {
        'covenants 1 or more days past due': 'covenants_past_due',
        'covenants 1 or more days in default': 'covenants_in_default',
        'ticklers 1 or more days past due': 'ticklers_past_due',
    }
    
    dataframes = {}
    
    # Process each HTML file (saved as .xls)
    for html_file in excel_files:
        print(f"Processing: {html_file.name}")
        
        try:
            # Read HTML content
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Parse HTML with lxml
            tree = html.fromstring(html_content)
            
            # Extract report title from the clientnameheading class
            title_elements = tree.xpath("//span[@class='clientnameheading']")
            if title_elements:
                report_title = title_elements[0].text_content().lower().strip()
                print(f"Report title: '{report_title}'")
                
                # Find matching dataframe key
                df_key = None
                for pattern, key in df_mappings.items():
                    if pattern.lower() in report_title:
                        df_key = key
                        break
                
                if df_key:
                    # Extract standardized report data
                    df = extract_standardized_report_data(tree, report_title)
                    if df is not None:
                        dataframes[df_key] = df
                        print(f"Mapped to: {df_key}")
                    else:
                        print(f"No report data found for: {report_title}")
                else:
                    print(f"No mapping found for report title: '{report_title}'")
            else:
                print(f"No report title found in: {html_file.name}")
        
        except Exception as e:
            print(f"Error processing {html_file.name}: {str(e)}")
        
        # Move to archive
        archive_dest = archive_folder / html_file.name
        shutil.move(str(html_file), str(archive_dest))
        print(f"Moved to archive: {html_file.name}")
    
    print(f"Processed {len(dataframes)} dataframes: {list(dataframes.keys())}")
    return dataframes
# Usage example:
# files = process_xls_files()
# 
# # Access individual report DataFrames (each with standardized columns)
# if 'covenants_past_due' in files:
#     df_covenants_pd = files['covenants_past_due'].copy()
# if 'covenants_in_default' in files:
#     df_covenants_default = files['covenants_in_default'].copy()
# if 'ticklers_past_due' in files:
#     df_ticklers_past_due = files['ticklers_past_due'].copy()
#     
#     # Example queries on standardized data:
#     # Get all items for a specific customer
#     customer_items = df_covenants_pd[df_covenants_pd['customer_name'] == "customer name"]
#     
#     # Get all past due items
#     past_due = df_covenants_pd[df_covenants_pd['days_past_due'] != '']
#     
#     # Get items by report type
#     in_default_covenants = df_covenants_default[df_covenants_default['report_type'].str.contains('in default', case=False, na=False)]

