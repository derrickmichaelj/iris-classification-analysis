# download.py
# Author: Sidharth Malik
# Date: 2025-12-10
#
# This script downloads the Iris dataset from scikit-learn and saves it as a CSV file.
#
# Usage:
# python src/download.py --output data/raw/iris.csv

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
