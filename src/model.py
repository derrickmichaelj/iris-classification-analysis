import click
import pandas as pd
import matplotlib.pyplot as plt
import os
import pickle

from sklearn.compose import make_column_transformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import train_test_split, cross_validate, RandomizedSearchCV
from sklearn.metrics import ConfusionMatrixDisplay
from scipy.stats import loguniform

@click.command()
@click.option("--input",
              default="data/processed/iris_clean.csv",
              help="Path to cleaned dataset.")
@click.option("--output-dir",
              default="results/metrics",
              help="Directory to save model artifacts (figures, metrics, model).")
def main(input, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # Load processed data
    df = pd.read_csv(input)
    X = df.drop(columns=['species'])
    y = df['species']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=522)

    # Dummy classifier baseline
    dummy = DummyClassifier(strategy="most_frequent")
    cv_dummy = cross_validate(dummy, X_train, y_train, cv=5, return_train_score=True)
    pd.DataFrame(cv_dummy).to_csv(os.path.join(output_dir, "dummy_cv_results.csv"), index=False)

    # Pipeline with standard scaling and logistic regression
    features = X_train.columns.tolist()
    preprocessor = make_column_transformer((StandardScaler(), features))
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression())
    ])

    # Hyperparameter tuning
    param_grid = {"classifier__C": loguniform(1e-6, 1e6)}
    rand_search = RandomizedSearchCV(pipeline, param_grid, n_iter=50, cv=5, n_jobs=-1, random_state=522)
    rand_search.fit(X_train, y_train)

    # Save CV results
    results = pd.DataFrame(rand_search.cv_results_).sort_values(by='mean_test_score', ascending=False)
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
