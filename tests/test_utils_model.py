import pandas as pd
import sys
from pathlib import Path

# Ensure we can import from src/
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from utils_model import prepare_features_and_target, create_train_test_split

def test_prepare_features_and_target_splits_X_and_y():
    """Test prepare_features_and_target with normal and edge cases."""

    # Normal case
    df = pd.DataFrame({
        "feature1": [1, 2, 3],
        "feature2": [4, 5, 6],
        "target": [0, 1, 0]
    })
    X, y = prepare_features_and_target(df, "target")
    assert list(X.columns) == ["feature1", "feature2"]
    assert list(y) == [0, 1, 0]

    # Normal case: larger dataset
    df2 = pd.DataFrame({
        "f1": [10, 20, 30, 40],
        "f2": [7, 8, 9, 10],
        "target": [1, 0, 1, 0]
    })
    X2, y2 = prepare_features_and_target(df2, "target")
    assert list(X2.columns) == ["f1", "f2"]
    assert list(y2) == [1, 0, 1, 0]

    # Edge case: empty DataFrame
    df_empty = pd.DataFrame(columns=["feature1", "feature2", "target"])
    X_empty, y_empty = prepare_features_and_target(df_empty, "target")
    assert X_empty.empty
    assert y_empty.empty

def test_create_train_test_split_respects_sizes():
    """Test create_train_test_split with normal and edge cases."""

    # Normal case: basic 5-sample dataset
    X = pd.DataFrame({"feature": [1, 2, 3, 4, 5]})
    y = pd.Series([0, 1, 0, 1, 0])
    X_train, X_test, y_train, y_test = create_train_test_split(
        X, y, test_size=0.4, random_state=522
    )
    assert len(X_train) + len(X_test) == len(X)

    # Normal case: dataset with single feature repeated
    X2 = pd.DataFrame({"feature": [10, 20, 30, 40]})
    y2 = pd.Series([1, 0, 1, 0])
    X_train2, X_test2, y_train2, y_test2 = create_train_test_split(
        X2, y2, test_size=0.5, random_state=522
    )
    assert len(X_train2) + len(X_test2) == len(X2)

    # Edge case: empty dataset
    X_empty = pd.DataFrame(columns=["feature"])
    y_empty = pd.Series(dtype=int)
    X_train_empty, X_test_empty, y_train_empty, y_test_empty = X_empty, X_empty, y_empty, y_empty
    assert X_train_empty.empty and X_test_empty.empty
    assert y_train_empty.empty and y_test_empty.empty
