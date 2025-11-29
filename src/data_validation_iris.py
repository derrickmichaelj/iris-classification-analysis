import pandas as pd
import pandera.pandas as pa
from pandera.pandas import Column, DataFrameSchema, Check
import numpy as np

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

    # Outlier and anomalies value checks
    numeric_cols = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    z_scores = ((df_validated[numeric_cols] - df_validated[numeric_cols].mean()) /
                df_validated[numeric_cols].std())

    if (z_scores.abs() > 4).any().any():
        raise ValueError("Outlier values detected in numeric columns.")
    print("Outlier check passed.")

    #Correct Category levels
    expected_species = {"setosa", "versicolor", "virginica"}
    actual_species = set(df_validated["species"].unique())

    unknown_species = actual_species - expected_species

    if unknown_species:
        print(f"Warning: Unknown species values found and removed: {unknown_species}")
        df_validated = df_validated[df_validated["species"].isin(expected_species)]

    print("Species category level check passed (unknown categories removed if present).")

    #Target response  (Iris is totally balanced but allow a tolerance of 10)

    species_count = df_validated["species"].value_counts()
    if not species_count.between(40,60).all():
        raise ValueError("Species distribution outside expected range.")
    print("Target Distribution check passed")

    #No anomalous correlations between target and features

    grouped_means = df_validated.groupby("species")[numeric_cols].mean()

    if (grouped_means.nunique() == 1).any():
        raise ValueError("No variation in feature means across species.")
    print("Correlation check (features vs target) passed.")

    #No anomalous correlations between features

    corr_matrix = df_validated[numeric_cols].corr().abs()

    upper = corr_matrix.where(
        np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
    )

    high_corr_pairs = []
    threshold = 0.95

    for col_i in numeric_cols:
        for col_j in numeric_cols:
            if col_i == col_j:
                continue
            corr_val = upper.loc[col_i, col_j]
            if pd.notna(corr_val) and corr_val > threshold:
                high_corr_pairs.append((col_i, col_j, corr_val))

    if high_corr_pairs:
        msg_lines = [
            f"[WARNING] High correlations between features detected (|corr| > {threshold}):"
        ]
        for col_i, col_j, corr_val in sorted(high_corr_pairs, key=lambda x: -x[2]):
            msg_lines.append(f"  - {col_i} & {col_j}: corr = {corr_val:.3f}")

        msg_lines.append(
            "This is a warning only — continuing the analysis (no error raised)."
        )

        print("\n".join(msg_lines))

    else:
        print("Correlation check (feature vs feature) passed.")


    print("=== IRIS DATA VALIDATION — ALL CHECKS PASSED ===\n")


    return df_validated


