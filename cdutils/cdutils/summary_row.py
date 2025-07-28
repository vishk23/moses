# add a summary row to a df

import pandas as pd
from typing import List, Optional, Any
def append_summary_row(
    df: pd.DataFrame,
    sum_cols:        Optional[List[str]] = None,
    avg_cols:        Optional[List[str]] = None,
    label_col:       Optional[str]       = None,
    label:           Any                 = "Total"
) -> pd.DataFrame:
    """
    Return a new DataFrame with one extra “footer” row that:
       - Sums each column in `sum_cols`
       - Averages each column in `avg_cols`
       - (Optionally) writes `label` into `label_col`
    All other columns in that row are empty strings.
    Parameters
    ----------
    df : pd.DataFrame
        Your data.
    sum_cols : list of str, optional
        Columns to sum.  Default: none.
    avg_cols : list of str, optional
        Columns to average.  Default: none.
    label_col : str, optional
        Column in which to place `label`.  Default: no label.
    label : any
        What to write into `label_col` in the footer.  Default: "Total".
    Returns
    -------
    pd.DataFrame
        The original `df` plus one summary row at the bottom.
    """
    if df.empty:
        return df

    # --- VALIDATION ---
    assert isinstance(df, pd.DataFrame),                    "df must be a pandas DataFrame"
    sum_cols = sum_cols or []
    avg_cols = avg_cols or []
    assert all(isinstance(c, str) for c in sum_cols),       "sum_cols must be list of strings"
    assert all(isinstance(c, str) for c in avg_cols),       "avg_cols must be list of strings"
    missing = set(sum_cols + avg_cols) - set(df.columns)
    assert not missing, f"These columns are missing from df: {missing}"
    if label_col is not None:
        assert isinstance(label_col, str),                   "label_col must be a string"
        assert label_col in df.columns,                     f"label_col '{label_col}' not in df"
    # --- AGGREGATE ---
    sums = df[sum_cols].sum() if sum_cols else pd.Series(dtype=float)
    avgs = df[avg_cols].mean() if avg_cols else pd.Series(dtype=float)
    # --- BUILD FOOTER ---
    footer = {col: "" for col in df.columns}
    for col, val in sums.items():
        footer[col] = val
    for col, val in avgs.items():
        footer[col] = val
    if label_col:
        footer[label_col] = label
    footer_df = pd.DataFrame([footer], columns=df.columns)
    # --- CONCAT & RETURN ---
    return pd.concat([df, footer_df], ignore_index=True)