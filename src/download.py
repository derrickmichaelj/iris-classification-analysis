import click
import pandas as pd

@click.command()
@click.option(
    "--output",
    default="data/raw/iris.csv",
    help="Path to save raw dataset."
)
def main(output):
    print("Downloading Iris dataset...")
    url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
    iris = pd.read_csv(url)

    iris.to_csv(output, index=False)
    print(f"Raw dataset saved to: {output}")

if __name__ == "__main__":
    main()
