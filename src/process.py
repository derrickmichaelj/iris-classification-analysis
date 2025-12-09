import click
import pandas as pd

from data_validation_iris import validate_iris_dataframe
from utils_data import strip_column_whitespace


@click.command()
@click.option(
    "--input",
    default="data/raw/iris.csv",
    help="Path to raw dataset."
)
@click.option(
    "--output",
    default="data/processed/iris_clean.csv",
    help="Path to save cleaned and validated dataset."
)
def main(input, output):
    """Load raw Iris data, validate it, clean column names, and save."""
    print("Loading raw data...")
    df = pd.read_csv(input)

    print("Running validation and cleaning...")
    df_clean = validate_iris_dataframe(df)

    # Use utility function to clean column names
    df_clean = strip_column_whitespace(df_clean)

    df_clean.to_csv(output, index=False)
    print(f"Cleaned dataset saved to: {output}")


if __name__ == "__main__":
    main()
