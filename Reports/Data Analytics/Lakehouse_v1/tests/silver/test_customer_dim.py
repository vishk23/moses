import pytest
import pandas as pd
import cdutils.input_cleansing # type: ignore
import cdutils.customer_dim # type: ignore
from datetime import datetime

def test_input_cleansing():
    """
    Testing that the validation and data type casting worked.

    We'll use 
    """
    wh_org = pd.DataFrame({
        'orgnbr': [100, 100, 101],
        'orgname': ['Org A', 'Org A', 'Org C']
    })    

    schema_wh_org = {
        'orgnbr': 'str',
        'orgname': 'str'
    }

    wh_org = cdutils.input_cleansing.cast_columns(wh_org, schema_wh_org)

    assert wh_org['orgnbr'].dtype == 'string'

class TestPersify:
    def test_persify_missing_column(self):
        """
        Testing imported persify function from cdutils
        """

        wh_pers = pd.DataFrame({
            'other_col': [100,101,102]
        })
        with pytest.raises(ValueError):
            cdutils.customer_dim.persify(wh_pers, 'persnbr')

    def test_persify_creates_customer_id(self):
        """
        Testing imported persify function from cdutils
        """

        wh_pers = pd.DataFrame({
            'persnbr': [100,101,102]
        })

        expected = pd.DataFrame({
            'customer_id':['P100','P101','P102']
        })
        # Set equivalent types to mimic actual output, string instead of object
        expected_schema = {
            'customer_id': 'str'
        }
        expected = cdutils.input_cleansing.cast_columns(expected, expected_schema)

        result = cdutils.customer_dim.persify(wh_pers, 'persnbr')
        pd.testing.assert_frame_equal(result, expected)
