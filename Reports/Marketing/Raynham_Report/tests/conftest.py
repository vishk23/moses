import pytest
import pandas as pd

@pytest.fixture
def wh_org():
    # Define sample data for the wh_org DataFrame
    data = {
        "orgnbr": ["1", "2", "3"],  # Primary key, integers stored as strings
        "orgname": ["Org A", "Org B", "Org C"],
        "orgtypcd": ["T01", "T02", "T03"],
        "orgtypcddesc": ["Type A Desc", "Type B Desc", "Type C Desc"],
        "naicscd": ["N01", "N02", "N03"],
        "naicscddesc": ["NAICS A Desc", "NAICS B Desc", "NAICS C Desc"],
        "adddate": pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-03"]),
        "rundate": pd.to_datetime(["2023-01-10", "2023-01-11", "2023-01-12"])
    }
    df = pd.DataFrame(data)
    # Set orgnbr as index to simulate primary key behavior
    df.set_index("orgnbr", inplace=True)
    return df