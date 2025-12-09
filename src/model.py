import os
import pickle

import click
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import loguniform
from sklearn.compose import make_column_transformer
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.model_selection import RandomizedSearchCV, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from utils_model import prepare_features_and_target, create_train_test_split


@click.command()
@click.option(
    "--input",
    default="data/processed/iris_clean.csv",
    help="Path to cleaned dataset."
)
@click.option(
    "--output-dir",
    default="results/metrics",
    help="Directory to save model artifacts (figures, metrics, model)."
)
def main(input, output_dir):
    """Train baseline and logistic regression models and save artifacts."""
    os.makedirs(output_dir, exist_ok=True)

    # Load processed data
    df = pd.read_csv(input)

    # Use utility function to split features & target
    X, y = prepare_features_and_target(df, target_col="species")

    # Use utility function to create train/test splits
    X_train, X_test, y_train, y_test = create_train_test_split(
        X, y, test_size=0.2, random_state=522
    )

    # Dummy classifier baseline
    dummy = DummyClassifier(strategy="most_frequent")
    cv_dummy = cross_validate(dummy, X_train, y_train, cv=5, return_train_score=True)
    pd.DataFrame(cv_dummy).to_csv(
        os.path.join(output_dir, "dummy_cv_results.csv"), index=False
    )

    # Pipeline with standard scaling and logistic regression
    features = X_train.columns.tolist()
    preprocessor = make_column_transformer(
        (StandardScaler(), features)
    )
    pipeline = Pipeline(
        [
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression()),
        ]
    )

    # Hyperparameter tuning
    param_grid = {"classifier__C": loguniform(1e-6, 1e6)}
    rand_search = RandomizedSearchCV(
        pipeline,
        param_grid,
        n_iter=50,
        cv=5,
        n_jobs=-1,
        random_state=522,
    )
    rand_search.fit(X_train, y_train)

    # Save CV results
    results = (
        pd.DataFrame(rand_search.cv_results_)
        .sort_values(by="mean_test_score", ascending=False)
    )
    results.to_csv(os.path.join(output_dir, "cv_results.csv"), index=False)

    # Best model
    best_model = rand_search.best_estimator_
    print("Train accuracy:", best_model.score(X_train, y_train))
    print("Test accuracy:", best_model.score(X_test, y_test))

    # Save confusion matrix figure
    disp = ConfusionMatrixDisplay.from_estimator(best_model, X_test, y_test)
    plt.title("Confusion Matrix — Iris Logistic Regression")
    cm_path = os.path.join(output_dir, "confusion_matrix.png")
    plt.savefig(cm_path)
    plt.close()
    print(f"Confusion matrix saved to: {cm_path}")

    # Save trained model as pickle
    model_path = os.path.join(output_dir, "logreg_model.pickle")
    with open(model_path, "wb") as f:
        pickle.dump(best_model, f)
    print(f"Trained model saved to: {model_path}")


if __name__ == "__main__":
    main()
