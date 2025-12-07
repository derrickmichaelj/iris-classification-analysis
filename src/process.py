import click
import pandas as pd
from data_validation_iris import validate_iris_dataframe

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
    print("Loading raw data...")
    df = pd.read_csv(input)

    print("Running validation and cleaning...")
    df_clean = validate_iris_dataframe(df)

    # Additional processing if needed
    df_clean.columns = df_clean.columns.str.strip()

    df_clean.to_csv(output, index=False)
    print(f"Cleaned dataset saved to: {output}")

if __name__ == "__main__":
    main()
