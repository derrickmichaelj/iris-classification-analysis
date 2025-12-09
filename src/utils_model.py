from typing import Tuple

import pandas as pd
from sklearn.model_selection import train_test_split


def prepare_features_and_target(
    df: pd.DataFrame, target_col: str = "species"
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Split a DataFrame into feature matrix X and target vector y.

    Parameters
    ----------
    df : pandas.DataFrame
        The full dataset containing features and the target column.
    target_col : str, optional
        Name of the target column, by default "species".

    Returns
    -------
    X : pandas.DataFrame
        Features with the target column removed.
    y : pandas.Series
        Target variable.
    """
    if target_col not in df.columns:
        raise KeyError(f"Target column '{target_col}' not found in DataFrame.")

    X = df.drop(columns=[target_col])
    y = df[target_col]
    return X, y


def create_train_test_split(
    X, y, test_size: float = 0.2, random_state: int = 522
):
    """
    Wrapper around sklearn.model_selection.train_test_split to create
    training and test splits for features and target.

    Parameters
    ----------
    X : array-like or pandas.DataFrame
        Features.
    y : array-like or pandas.Series
        Target.
    test_size : float, optional
        Proportion of the dataset to include in the test split.
    random_state : int, optional
        Random seed for reproducibility.

    Returns
    -------
    X_train, X_test, y_train, y_test
    """
    return train_test_split(X, y, test_size=test_size, random_state=random_state)
