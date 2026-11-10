"""ml/models/train_logreg.py



Train a scikit‑learn Logistic Regression baseline on the same pre‑processed data used for the

PyTorch MLP.  The script loads the train/validation/test CSVs, fits a ``LogisticRegression``

(with the same numeric scaling already applied during preprocessing), evaluates the model with

the full metric suite, prints results, and persists the trained model via ``joblib``.

"""



"""ml/models/train_logreg.py



Train a scikit‑learn Logistic Regression baseline on the same pre‑processed data used for the PyTorch MLP.



The script loads the train/validation/test CSVs, fits a LogisticRegression, evaluates, and saves the model and test metrics.

"""



from pathlib import Path

import pandas as pd

import joblib

import os

from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (

    accuracy_score,

    precision_score,

    recall_score,

    f1_score,

    roc_auc_score,

    confusion_matrix,

)



# Project root two levels up (ml/models/train_logreg.py -> ml -> project root)

PROJECT_ROOT = Path(__file__).resolve().parents[2]



SPLITS_DIR = PROJECT_ROOT / "ml" / "datasets" / "data" / "splits"

CHECKPOINT_DIR = PROJECT_ROOT / "ml" / "models" / "checkpoints"

CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)



TARGET_COL = "cardio"

ID_COL = "id"



def load_split(name: str) -> tuple[pd.DataFrame, pd.Series]:

    df = pd.read_csv(SPLITS_DIR / f"{name}.csv")

    X = df.drop(columns=[TARGET_COL, ID_COL])

    y = df[TARGET_COL]

    return X, y



def compute_metrics(model, X, y) -> dict:

    probs = model.predict_proba(X)[:, 1]

    preds = (probs >= 0.5).astype(int)

    acc = accuracy_score(y, preds)

    prec = precision_score(y, preds, zero_division=0)

    rec = recall_score(y, preds, zero_division=0)

    f1 = f1_score(y, preds, zero_division=0)

    auc = roc_auc_score(y, probs)

    tn, fp, fn, tp = confusion_matrix(y, preds).ravel()

    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0

    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0.0

    return {

        "accuracy": acc,

        "precision": prec,

        "recall": rec,

        "f1": f1,

        "roc_auc": auc,

        "sensitivity": sensitivity,

        "specificity": specificity,

    }



def main() -> None:

    X_train, y_train = load_split("train")

    X_val, y_val = load_split("val")

    X_test, y_test = load_split("test")



    clf = LogisticRegression(max_iter=1000, solver="lbfgs")

    clf.fit(X_train, y_train)



    # Validation metrics (optional display)

    val_metrics = compute_metrics(clf, X_val, y_val)

    print("\n=== Validation Metrics (LogReg) ===")

    for k, v in val_metrics.items():

        print(f"{k}: {v:.4f}")



    # Test metrics

    test_metrics = compute_metrics(clf, X_test, y_test)

    print("\n=== Test Metrics (LogReg) ===")

    for k, v in test_metrics.items():

        print(f"{k}: {v:.4f}")



    # Persist the model

    model_path = CHECKPOINT_DIR / "logreg.joblib"

    joblib.dump(clf, model_path)

    print(f"Logistic Regression model saved to {model_path}")



    # Save test metrics for the reporting script

    metrics_path = CHECKPOINT_DIR / "logreg_test_metrics.json"

    with open(metrics_path, "w") as f:

        import json

        json.dump(test_metrics, f, indent=2)

    print(f"Test metrics saved to {metrics_path}")



if __name__ == "__main__":

    main()





TARGET_COL = "cardio"

ID_COL = "id"



def load_split(name: str) -> tuple[pd.DataFrame, pd.Series]:

    df = pd.read_csv(os.path.join(SPLITS_DIR, f"{name}.csv"))

    X = df.drop(columns=[TARGET_COL, ID_COL])

    y = df[TARGET_COL]

    return X, y



def compute_metrics(model, X, y) -> dict:

    probs = model.predict_proba(X)[:, 1]

    preds = (probs >= 0.5).astype(int)

    acc = accuracy_score(y, preds)

    prec = precision_score(y, preds, zero_division=0)

    rec = recall_score(y, preds, zero_division=0)

    f1 = f1_score(y, preds, zero_division=0)

    auc = roc_auc_score(y, probs)

    tn, fp, fn, tp = confusion_matrix(y, preds).ravel()

    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0

    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0.0

    return {

        "accuracy": acc,

        "precision": prec,

        "recall": rec,

        "f1": f1,

        "roc_auc": auc,

        "sensitivity": sensitivity,

        "specificity": specificity,

    }



def main():

    X_train, y_train = load_split("train")

    X_val, y_val = load_split("val")

    X_test, y_test = load_split("test")



    # LogisticRegression expects no missing values and already‑scaled numeric features.

    # The preprocessing script already scaled them, so we can train directly.

    clf = LogisticRegression(max_iter=1000, solver="lbfgs")

    clf.fit(X_train, y_train)



    # Validation metrics (optional display)

    val_metrics = compute_metrics(clf, X_val, y_val)

    print("\n=== Validation Metrics (LogReg) ===")

    for k, v in val_metrics.items():

        print(f"{k}: {v:.4f}")



    # Test metrics

    test_metrics = compute_metrics(clf, X_test, y_test)

    print("\n=== Test Metrics (LogReg) ===")

    for k, v in test_metrics.items():

        print(f"{k}: {v:.4f}")



    # Persist the model

    model_path = os.path.join(CHECKPOINT_DIR, "logreg.joblib")

    joblib.dump(clf, model_path)

    print(f"Logistic Regression model saved to {model_path}")



    # Save test metrics for the reporting script

    metrics_path = os.path.join(CHECKPOINT_DIR, "logreg_test_metrics.json")

    with open(metrics_path, "w") as f:

        import json

        json.dump(test_metrics, f, indent=2)

    print(f"Test metrics saved to {metrics_path}")



if __name__ == "__main__":

    main()
