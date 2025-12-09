import pandas as pd


def strip_column_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return a copy of `df` where leading and trailing whitespace
    has been removed from all column names.

    This is useful to ensure column names are clean and consistent
    before downstream processing and modeling.
    """
    df_copy = df.copy()
    df_copy.columns = df_copy.columns.str.strip()
    return df_copy
