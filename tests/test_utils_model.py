import pandas as pd
import sys
from pathlib import Path

# Ensure we can import from src/
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from utils_model import prepare_features_and_target, create_train_test_split


def test_prepare_features_and_target_splits_X_and_y():
    df = pd.DataFrame(
        {
            "sepal_length": [5.1, 4.9, 4.7],
            "sepal_width": [3.5, 3.0, 3.2],
            "species": ["setosa", "setosa", "versicolor"],
        }
    )

    X, y = prepare_features_and_target(df, target_col="species")

    # species column should be removed from X and present in y
    assert "species" not in X.columns
    assert len(X) == len(y) == 3
    assert y.iloc[0] == "setosa"


def test_create_train_test_split_respects_sizes():
    X = pd.DataFrame({"feature": [1, 2, 3, 4, 5]})
    y = pd.Series([0, 1, 0, 1, 0])

    X_train, X_test, y_train, y_test = create_train_test_split(
        X, y, test_size=0.4, random_state=522
    )

    # Sizes should add up correctly
    assert len(X_train) == len(y_train)
    assert len(X_test) == len(y_test)
    assert len(X_train) + len(X_test) == len(X)
