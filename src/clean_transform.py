import click
import pandas as pd

@click.command()
@click.option("--input",
              default="data/raw/iris_validated.csv",
              help="Path to validated raw dataset.")
@click.option("--output",
              default="data/processed/iris_processed.csv",
              help="Path to save cleaned dataset.")
def main(input, output):
    print("Loading validated data...")
    df = pd.read_csv(input)

    df.columns = df.columns.str.strip()

    df.to_csv(output, index=False)
    print(f"Processed dataset saved to: {output}")

if __name__ == "__main__":
    main()
