"""
Train and evaluate a Logistic Regression baseline.

Uses the same corrected train, validation, and test splits
as the PyTorch MLP.
"""

import json
from pathlib import Path

import joblib
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SPLITS_DIR = (
    PROJECT_ROOT / "ml" / "datasets" / "data" / "splits"
)

CHECKPOINT_DIR = (
    PROJECT_ROOT / "ml" / "models" / "checkpoints"
)

CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)

TARGET_COL = "cardio"
ID_COL = "id"


def load_split(name):

    df = pd.read_csv(SPLITS_DIR / f"{name}.csv")

    X = df.drop(columns=[TARGET_COL, ID_COL])
    y = df[TARGET_COL]

    return X, y


def compute_metrics(model, X, y):

    probabilities = model.predict_proba(X)[:, 1]
    predictions = (probabilities >= 0.5).astype(int)

    tn, fp, fn, tp = confusion_matrix(
        y, predictions, labels=[0, 1]
    ).ravel()

    return {
        "accuracy": float(
            accuracy_score(y, predictions)
        ),
        "precision": float(
            precision_score(y, predictions, zero_division=0)
        ),
        "recall": float(
            recall_score(y, predictions, zero_division=0)
        ),
        "f1": float(
            f1_score(y, predictions, zero_division=0)
        ),
        "roc_auc": float(
            roc_auc_score(y, probabilities)
        ),
        "sensitivity": float(
            tp / (tp + fn) if (tp + fn) else 0.0
        ),
        "specificity": float(
            tn / (tn + fp) if (tn + fp) else 0.0
        ),
    }


def main():

    X_train, y_train = load_split("train")
    X_val, y_val = load_split("val")
    X_test, y_test = load_split("test")

    model = LogisticRegression(
        max_iter=1000,
        solver="lbfgs",
        random_state=42,
    )

    model.fit(X_train, y_train)

    val_metrics = compute_metrics(
        model, X_val, y_val
    )

    test_metrics = compute_metrics(
        model, X_test, y_test
    )

    print("\n=== Validation Metrics (Logistic Regression) ===")

    for metric, value in val_metrics.items():
        print(f"{metric}: {value:.4f}")

    print("\n=== Test Metrics (Logistic Regression) ===")

    for metric, value in test_metrics.items():
        print(f"{metric}: {value:.4f}")

    model_path = CHECKPOINT_DIR / "logreg.joblib"
    metrics_path = CHECKPOINT_DIR / "logreg_test_metrics.json"

    joblib.dump(model, model_path)

    with open(metrics_path, "w") as file:
        json.dump(test_metrics, file, indent=2)

    print(f"\nModel saved: {model_path}")
    print(f"Metrics saved: {metrics_path}")


if __name__ == "__main__":
    main()