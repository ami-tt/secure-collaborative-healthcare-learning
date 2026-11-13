"""
Integration tests for the Phase 3 ML pipeline.

Tests:
1. Data preprocessing.
2. Train/validation/test splitting.
3. Training-only scaler fitting.
4. Non-overlapping hospital client partitions.
5. MLP and Logistic Regression training.
6. Model checkpoints and evaluation metrics.
"""

import json
import subprocess
import sys

from pathlib import Path

import joblib
import pandas as pd
import pytest


BASE_DIR = Path(__file__).resolve().parents[2]

PROCESSED_DIR = BASE_DIR / "ml" / "datasets" / "data" / "processed"
SPLITS_DIR = BASE_DIR / "ml" / "datasets" / "data" / "splits"
CLIENTS_DIR = BASE_DIR / "ml" / "datasets" / "data" / "clients"
CHECKPOINT_DIR = BASE_DIR / "ml" / "models" / "checkpoints"

NUMERIC_COLS = ["age", "height", "weight", "ap_hi", "ap_lo"]


def run_module(module_path):

    result = subprocess.run(
        [sys.executable, "-m", module_path],
        capture_output=True,
        text=True,
        cwd=BASE_DIR,
        timeout=600,
    )

    assert result.returncode == 0, (
        f"{module_path} failed.\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )

    return result.stdout


def test_preprocess_runs():

    output = run_module("ml.datasets.preprocess")

    assert "Cleaned dataset saved" in output

    clean_path = PROCESSED_DIR / "clean.csv"

    assert clean_path.exists()

    df = pd.read_csv(clean_path)

    assert len(df) > 1000
    assert "cardio" in df.columns
    assert "id" in df.columns

    # Preprocessing should preserve original numeric units.
    assert df["age"].between(0, 30000).all()
    assert df["height"].between(120, 220).all()


def test_split_runs():

    output = run_module("ml.datasets.split")

    assert "Dataset splitting and scaling completed" in output

    for filename in ["train.csv", "val.csv", "test.csv"]:
        assert (SPLITS_DIR / filename).exists()

    train = pd.read_csv(SPLITS_DIR / "train.csv")
    val = pd.read_csv(SPLITS_DIR / "val.csv")
    test = pd.read_csv(SPLITS_DIR / "test.csv")

    assert list(train.columns) == list(val.columns)
    assert list(train.columns) == list(test.columns)

    assert len(train) > len(val)
    assert len(train) > len(test)

    assert len(train) + len(val) + len(test) > 0


def test_scaler_fitted_only_on_training_data():

    scaler_path = PROCESSED_DIR / "scaler.pkl"

    assert scaler_path.exists()

    scaler = joblib.load(scaler_path)

    clean = pd.read_csv(PROCESSED_DIR / "clean.csv")
    train = pd.read_csv(SPLITS_DIR / "train.csv")

    # Recover original training records using their IDs.
    train_original = (
        train[["id"]]
        .merge(clean[["id"] + NUMERIC_COLS], on="id", how="left")
    )

    assert not train_original[NUMERIC_COLS].isna().any().any()

    expected_means = train_original[NUMERIC_COLS].mean().values

    # Scaler means must match the original training data only.
    assert scaler.n_features_in_ == len(NUMERIC_COLS)

    assert scaler.feature_names_in_.tolist() == NUMERIC_COLS

    assert (abs(scaler.mean_ - expected_means) < 1e-6).all()


def test_client_partitioning():

    output = run_module("ml.datasets.partition_clients")

    assert "Client partitioning completed successfully" in output

    client_files = [
        CLIENTS_DIR / "client_1.csv",
        CLIENTS_DIR / "client_2.csv",
        CLIENTS_DIR / "client_3.csv",
    ]

    clients = []

    for path in client_files:

        assert path.exists()

        df = pd.read_csv(path)

        assert len(df) > 0

        clients.append(df)

    all_ids = pd.concat(
        [client["id"] for client in clients],
        ignore_index=True,
    )

    train = pd.read_csv(SPLITS_DIR / "train.csv")

    # Every training record must belong to exactly one client.
    assert len(all_ids) == len(train)
    assert all_ids.nunique() == len(train)
    assert set(all_ids) == set(train["id"])

    # Verify age-based partitioning.
    clean = pd.read_csv(PROCESSED_DIR / "clean.csv")
    age_lookup = clean.set_index("id")["age"] / 365.25

    client1_ages = clients[0]["id"].map(age_lookup)
    client2_ages = clients[1]["id"].map(age_lookup)
    client3_ages = clients[2]["id"].map(age_lookup)

    assert (client1_ages > 55).all()
    assert (client2_ages <= 55).all()
    assert (client3_ages <= 55).all()

    # Verify gender partitioning.
    assert (clients[1]["gender"] == 1).all()
    assert (clients[2]["gender"] == 2).all()


def test_training_scripts():

    output_mlp = run_module("ml.models.train_mlp")

    assert "Test Metrics" in output_mlp

    output_logreg = run_module("ml.models.train_logreg")

    assert "Test Metrics" in output_logreg


def test_model_checkpoints_exist():

    expected_files = [
        "tabular_mlp.pt",
        "logreg.joblib",
    ]

    for filename in expected_files:
        assert (CHECKPOINT_DIR / filename).exists()


def test_metric_files_exist_and_loadable():

    expected_metrics = [
        "mlp_test_metrics.json",
        "logreg_test_metrics.json",
    ]

    required_keys = [
        "accuracy",
        "precision",
        "recall",
        "f1",
        "roc_auc",
        "sensitivity",
        "specificity",
    ]

    for filename in expected_metrics:

        path = CHECKPOINT_DIR / filename

        assert path.exists()

        with open(path, encoding="utf-8") as file:
            metrics = json.load(file)

        for key in required_keys:

            assert key in metrics
            assert isinstance(metrics[key], (int, float))
            assert 0 <= metrics[key] <= 1


if __name__ == "__main__":

    pytest.main([str(Path(__file__).resolve()), "-v"])