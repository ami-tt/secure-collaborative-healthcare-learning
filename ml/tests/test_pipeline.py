"""ml/tests/test_pipeline.py



Basic sanity tests for the ML pipeline.

These tests verify that:

- The preprocessing script runs and produces a cleaned CSV.

- The train/val/test split script creates three CSVs with matching columns.

- Training scripts execute without raising exceptions.

- Saved metric JSON files can be loaded.

"""



import os

import subprocess

import json

import pandas as pd

from pathlib import Path





BASE_DIR = Path(__file__).resolve().parents[2]





def run_module(module_path: str):

    """Execute a Python module via subprocess and raise on non‑zero exit."""

    result = subprocess.run(["python", "-m", module_path], capture_output=True, text=True)

    assert result.returncode == 0, f"{module_path} failed: {result.stderr}"

    return result.stdout



def test_preprocess_runs():

    # Run the preprocessing script

    out = run_module("ml.datasets.preprocess")

    assert "Saved cleaned data" in out

    clean_path = os.path.join(BASE_DIR, "ml", "datasets", "data", "processed", "clean.csv")

    assert os.path.exists(clean_path)

    df = pd.read_csv(clean_path)

    # Expect at least a few thousand rows after cleaning

    assert len(df) > 1000



def test_split_runs():

    out = run_module("ml.datasets.split")

    assert "Train size" in out

    split_dir = os.path.join(BASE_DIR, "ml", "datasets", "data", "splits")

    for split in ["train.csv", "val.csv", "test.csv"]:

        assert os.path.exists(os.path.join(split_dir, split))

    # Ensure columns match across splits

    train = pd.read_csv(os.path.join(split_dir, "train.csv"))

    val = pd.read_csv(os.path.join(split_dir, "val.csv"))

    test = pd.read_csv(os.path.join(split_dir, "test.csv"))

    assert list(train.columns) == list(val.columns) == list(test.columns)



def test_training_scripts():

    # MLP training

    out_mlp = run_module("ml.models.train_mlp")

    assert "Test Metrics" in out_mlp

    # Logistic Regression training

    out_log = run_module("ml.models.train_logreg")

    assert "Test Metrics" in out_log



def test_metric_files_exist_and_loadable():

    ckpt_dir = os.path.join(BASE_DIR, "ml", "models", "checkpoints")

    for fname in ["mlp_test_metrics.json", "logreg_test_metrics.json"]:

        path = os.path.join(ckpt_dir, fname)

        assert os.path.exists(path)

        with open(path) as f:

            data = json.load(f)

        # Check a couple of expected keys

        for key in ["accuracy", "roc_auc"]:

            assert key in data

            assert isinstance(data[key], float)



if __name__ == "__main__":

    # When run directly, invoke pytest programmatically

    pytest.main([os.path.abspath(__file__)])
