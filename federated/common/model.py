"""Utilities for creating the shared model used in federated training.



The central model is the same `TabularMLP` defined for Phase 3.  The helper

`get_model` returns a fresh instance with the correct input dimension.  The

model architecture itself is unchanged – we only provide a thin wrapper so

that client and server code can import a single symbol.

"""



from pathlib import Path

import torch

from ml.models.tabular_mlp import TabularMLP



# Project‑root is two levels up from this file (federated/common/model.py)

PROJECT_ROOT = Path(__file__).resolve().parents[2]



# Path to the cleaned data – we can infer the feature count from the CSV header

CLEAN_DATA_PATH = PROJECT_ROOT / "ml" / "datasets" / "data" / "processed" / "clean.csv"





def _infer_input_dim() -> int:

    """Read the first line of `clean.csv` to determine the number of feature columns.



    The CSV contains the columns ``id, <features...>, cardio``.  The model expects

    all columns **except** ``id`` and the target ``cardio``.

    """

    with open(CLEAN_DATA_PATH, "r", encoding="utf-8") as f:

        header = f.readline().strip()

    cols = header.split(",")

    # Exclude id and target column

    feature_cols = [c for c in cols if c not in {"id", "cardio"}]

    return len(feature_cols)





def get_model() -> TabularMLP:

    """Factory returning a fresh TabularMLP with the correct input dimension.



    The function is used by both the server (to build the initial global model)

    and by each client (to initialise its local copy).

    """

    input_dim = _infer_input_dim()

    return TabularMLP(input_dim)
