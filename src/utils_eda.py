import pandas as pd


def compute_correlation_long(df: pd.DataFrame, drop_col: str = "species") -> pd.DataFrame:
    """
    Compute a long-form correlation table between numeric features.

    This is a small abstraction of the correlation computation used
    for the Altair heatmap in src/eda.py.

    Parameters
    ----------
    df : pandas.DataFrame
        Input data.
    drop_col : str, optional
        Column to drop before computing correlations (e.g., target column),
        by default "species".

    Returns
    -------
    pandas.DataFrame
        DataFrame with columns ['feature1', 'feature2', 'correlation'].
    """
    if drop_col in df.columns:
        features_df = df.drop(columns=drop_col)
    else:
        features_df = df.copy()

    corr = features_df.corr().stack().reset_index()
    corr.columns = ["feature1", "feature2", "correlation"]
    return corr
