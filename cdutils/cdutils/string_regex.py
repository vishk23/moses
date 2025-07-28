""" 
String Regex 
"""

import re

def normalize_to_alnum_underscore(s: str) -> str:
    """
    Force uppercase and replace non-alphanumeric with underscore
    """

    s = s.upper()
    s = re.sub(r'[^A-Z0-9]+', '_', s)
    return s.strip('_')