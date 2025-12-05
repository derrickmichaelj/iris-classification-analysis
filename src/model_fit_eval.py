import click
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.compose import make_column_transformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_validate, RandomizedSearchCV
from sklearn.dummy import DummyClassifier
from sklearn.metrics import ConfusionMatrixDisplay
from scipy.stats import loguniform

@click.command()
@click.option("--input",
              default="data/processed/iris_processed.csv",
              help="Path to cleaned dataset.")
@click.option("--output-dir",
              default="results/metrics",
              help="Directory to save metrics and plots.")
def main(input, output_dir):

    df = pd.read_csv(input)
    X = df.drop("species", axis=1)
    y = df["species"]

    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=522
    )

    print("Running baseline dummy classifier...")
    dummy = DummyClassifier(strategy="most_frequent")
    dummy_scores = cross_validate(dummy, X_train, y_train, cv=5)

    baseline = pd.DataFrame(dummy_scores)
    baseline.to_csv(f"{output_dir}/dummy_baseline_cv.csv", index=False)

    print("Building pipeline...")
    preprocessor = make_column_transformer((StandardScaler(), X.columns))
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression())
    ])

    print("Running RandomizedSearchCV...")
    param_grid = {"classifier__C": loguniform(1e-6, 1e6)}
    search = RandomizedSearchCV(
        pipeline, param_grid, n_iter=50, cv=5, n_jobs=-1, random_state=522
    )

    search.fit(X_train, y_train)

    results = pd.DataFrame(search.cv_results_)
    results.to_csv(f"{output_dir}/cv_results.csv", index=False)

    best_model = search.best_estimator_

    print("Training accuracy:", best_model.score(X_train, y_train))
    print("Test accuracy:", best_model.score(X_test, y_test))

    print("Saving confusion matrix...")
    disp = ConfusionMatrixDisplay.from_estimator(
        best_model, X_test, y_test
    )
    plt.title("Confusion Matrix — Iris Dataset Logistic Regression")
    plt.savefig(f"{output_dir}/confusion_matrix.png")
    plt.close()

    print("Model evaluation complete.")

if __name__ == "__main__":
    main()
