import pytest
import pandas as pd
from src.built.core import generate_inactive_df


def test_generate_inactive_df():
    # Sample input data with acctnbr and inactivedate
    data = {
        'acctnbr': ['A1', 'A1', 'A1', 'A2', 'A2', 'A3'],
        'inactivedate': [
            pd.to_datetime('2023-01-01'),
            pd.to_datetime('2023-02-01'),
            None,
            pd.to_datetime('2023-01-01'),
            pd.to_datetime('2023-01-01'),
            pd.to_datetime('2023-03-01')
        ]
    }
    input_df = pd.DataFrame(data)

    # Expected output: acctnbr, num_extensions, orig_inactive_date
    expected_data = {
        'acctnbr': ['A1', 'A2', 'A3'],
        'num_extensions': [1, 0, 0],
        'orig_inactive_date': [
            pd.to_datetime('2023-01-01'),
            pd.to_datetime('2023-01-01'),
            pd.to_datetime('2023-03-01')
        ]
    }
    expected = pd.DataFrame(expected_data)
    expected['acctnbr'] = expected['acctnbr'].astype(pd.StringDtype())

    result = generate_inactive_df(input_df)
    pd.testing.assert_frame_equal(result, expected)