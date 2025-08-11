import pandas as pd
import shutil
from pathlib import Path
from lxml import html
import re


def extract_standardized_report_data(tree, report_title):
    """
    Extract report data from HTML tree and convert to standardized pandas DataFrame.

    Standard columns:
    - customer_name, item_name, required_value, actual_value,
      period_date, due_date, days_past_due, interval, comments,
      report_type, report_date
    """
    try:
        # Extract report creation date
        report_date = None
        date_elements = tree.xpath("//span[@class='date']")
        if date_elements:
            date_text = date_elements[0].text_content()
            date_match = re.search(r'(\d{2}/\d{2}/\d{4})', date_text)
            if date_match:
                report_date = date_match.group(1)

        # Find customer sections
        customer_sections = tree.xpath("//tr[contains(@class, '') or not(@class)]//span[contains(@class, 'SummaryTitle clientnameSmall') and contains(text(), 'Customer Name')]")

        all_report_data = []
        for customer_span in customer_sections:
            customer_text = customer_span.text_content()
            customer_name = customer_text.replace('Customer Name :', '').strip()

            # Ascend to containing TD and find associated tables
            current_element = customer_span
            while current_element is not None:
                if current_element.tag == 'td':
                    break
                current_element = current_element.getparent()

            if current_element is not None:
                covenant_tables = current_element.xpath(".//table[@class='uk-table uk-table-striped']")

                for table in covenant_tables:
                    rows = table.xpath(".//tr")
                    if len(rows) < 2:
                        continue

                    # Headers
                    headers = [th.text_content().strip() for th in rows[0].xpath(".//th")]

                    # Data rows
                    for row in rows[1:]:
                        cells = row.xpath(".//td")
                        if not cells:
                            continue
                        row_data = [cell.text_content().strip() for cell in cells]
                        if not any(cell.strip() for cell in row_data):
                            continue

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

                        for i, header in enumerate(headers):
                            if i >= len(row_data):
                                break
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
            return None

        return pd.DataFrame(all_report_data)

    except Exception:
        return None


def process_xls_files():
    """
    Process up to 5 HTML files (saved with .xls extension) from ./assets.
    Returns a dict of standardized DataFrames keyed by report type.
    """
    assets_folder = Path('./assets')
    archive_folder = assets_folder / 'archive'
    assets_folder.mkdir(exist_ok=True)
    archive_folder.mkdir(exist_ok=True)

    excel_files = list(assets_folder.glob('*.xls'))
    assert len(excel_files) <= 5, f"Found {len(excel_files)} .xls files, maximum is 5"
    all_files = [f for f in assets_folder.iterdir() if f.is_file() and not f.name.startswith('.')]
    non_excel = [f for f in all_files if not f.name.endswith('.xls')]
    assert len(non_excel) == 0, f"Found non-.xls files: {[f.name for f in non_excel]}"

    df_mappings = {
        'covenants coming due within the next 365 days': 'covenants_coming_due_365',
        'covenants 1 or more days past due': 'covenants_past_due',
        'covenants 1 or more days in default': 'covenants_in_default',
        'ticklers coming due within 365 days': 'ticklers_coming_due_365',
        'ticklers 1 or more days past due': 'ticklers_past_due',
    }

    dataframes = {}

    for html_file in excel_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            tree = html.fromstring(html_content)

            title_elements = tree.xpath("//span[@class='clientnameheading']")
            if title_elements:
                report_title = title_elements[0].text_content().lower().strip()
                df_key = None
                for pattern, key in df_mappings.items():
                    if pattern in report_title:
                        df_key = key
                        break
                if df_key:
                    df = extract_standardized_report_data(tree, report_title)
                    if df is not None:
                        dataframes[df_key] = df
        finally:
            archive_dest = archive_folder / html_file.name
            shutil.move(str(html_file), str(archive_dest))

    return dataframes
