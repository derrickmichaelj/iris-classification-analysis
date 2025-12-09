import pandas as pd
import sys
from pathlib import Path

# Ensure we can import from src/
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from utils_data import strip_column_whitespace


def test_strip_column_whitespace_trims_spaces():
    df = pd.DataFrame([[1, 2]], columns=[" sepal_length ", "petal_width  "])

    cleaned = strip_column_whitespace(df)

    # Column names should have no leading/trailing spaces
    assert list(cleaned.columns) == ["sepal_length", "petal_width"]
