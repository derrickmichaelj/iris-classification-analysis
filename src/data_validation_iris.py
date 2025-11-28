import pandas as pd
import pandera.pandas as pa
from pandera.pandas import Column, DataFrameSchema, Check


iris_schema = DataFrameSchema(
    {
        "sepal_length": Column(float, nullable=False, checks=Check.greater_than(0)),
        "sepal_width": Column(float, nullable=False, checks=Check.greater_than(0)),
        "petal_length": Column(float, nullable=False, checks=Check.greater_than(0)),
        "petal_width": Column(float, nullable=False, checks=Check.greater_than(0)),
        "species": Column(object, nullable=False),
    },
    strict=True,
    coerce=True,
)


def validate_iris_dataframe(df: pd.DataFrame):
    """
    Validate the Iris dataset.
    """

    print("\n=== RUNNING IRIS DATA VALIDATION CHECKS ===")

    # Correct data file format
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Data is not a pandas DataFrame.")
    print("Data loaded as pandas DataFrame.")

    # Duplicate observations — remove them
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        df = df.drop_duplicates()
    print("Duplicate check passed (duplicates removed if present).")

    # Schema validation (columns, types, missingness, empty rows)
    try:
        df_validated = iris_schema.validate(df)
        print("Schema validation passed.")
    except pa.errors.SchemaError as e:
        raise ValueError(f"Pandera schema validation failed:\n{e}")

    print("=== IRIS DATA VALIDATION — ALL CHECKS PASSED ===\n")

    return df_validated
