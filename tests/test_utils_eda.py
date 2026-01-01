import pandas as pd
import sys
from pathlib import Path

# Ensure we can import from src/
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from utils_eda import compute_correlation_long

def test_compute_correlation_long_returns_expected_columns_and_shape():
    """Test compute_correlation_long with normal and edge cases."""

    # Normal case: small DataFrame
    df = pd.DataFrame({
        "sepal_length": [5.1, 4.9, 5.0],
        "sepal_width": [3.5, 3.0, 3.6],
        "petal_length": [1.4, 1.4, 1.5]
    })
    corr_long = compute_correlation_long(df)
    expected_cols = ["feature1", "feature2", "correlation"]
    assert list(corr_long.columns) == expected_cols
    assert len(corr_long) > 0

    # Normal case: DataFrame with perfectly correlated columns
    df2 = pd.DataFrame({
        "a": [1, 2, 3],
        "b": [2, 4, 6],
        "c": [5, 6, 7]
    })
    corr_long2 = compute_correlation_long(df2)
    assert list(corr_long2.columns) == expected_cols

    # Edge case: empty DataFrame
    df_empty = pd.DataFrame()
    corr_empty = compute_correlation_long(df_empty)
    assert corr_empty.empty
