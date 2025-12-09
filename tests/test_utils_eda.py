import pandas as pd
import sys
from pathlib import Path

# Ensure we can import from src/
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from utils_eda import compute_correlation_long


def test_compute_correlation_long_returns_expected_columns_and_shape():
    df = pd.DataFrame(
        {
            "sepal_length": [5.1, 4.9, 4.7],
            "sepal_width": [3.5, 3.0, 3.2],
            "petal_length": [1.4, 1.4, 1.3],
            "species": ["setosa", "setosa", "versicolor"],
        }
    )

    corr_long = compute_correlation_long(df, drop_col="species")

    # Column names
    assert set(corr_long.columns) == {"feature1", "feature2", "correlation"}

    # There are 3 numeric features => 3x3 correlation matrix => 9 rows after stack
    assert corr_long.shape[0] == 9
