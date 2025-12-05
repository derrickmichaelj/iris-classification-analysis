import click
import pandas as pd
from data_validation_iris import validate_iris_dataframe

@click.command()
@click.option("--output", default="data/raw/iris_validated.csv",
              help="Path to save validated raw dataset.")
def main(output):
    print("Downloading Iris dataset...")
    url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
    iris = pd.read_csv(url)

    print("Running validation checks...")
    iris = validate_iris_dataframe(iris)

    iris.to_csv(output, index=False)
    print(f"Validated dataset saved to: {output}")

if __name__ == "__main__":
    main()
