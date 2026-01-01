import pandas as pd
import sys
from pathlib import Path

# Ensure we can import from src/
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from utils_data import strip_column_whitespace

def test_strip_column_whitespace_trims_spaces():
    """Test strip_column_whitespace with normal and edge cases."""
    
    # Normal case: columns with leading/trailing spaces
    df = pd.DataFrame([[1, 2]], columns=[" sepal_length ", "petal_width  "])
    cleaned = strip_column_whitespace(df)
    assert list(cleaned.columns) == ["sepal_length", "petal_width"]
    
    # Normal case: columns already clean
    df_clean = pd.DataFrame([[1, 2]], columns=["sepal_length", "petal_width"])
    cleaned2 = strip_column_whitespace(df_clean)
    assert list(cleaned2.columns) == ["sepal_length", "petal_width"]
    
    # Edge case: empty DataFrame (no columns)
    df_empty = pd.DataFrame()
    cleaned3 = strip_column_whitespace(df_empty)
    assert list(cleaned3.columns) == []

    # Edge case: columns are non-string type (RangeIndex)
    df_range = pd.DataFrame([[1,2],[3,4]])
    cleaned4 = strip_column_whitespace(df_range)
    # Columns should remain as RangeIndex
    assert list(cleaned4.columns) == [0, 1]