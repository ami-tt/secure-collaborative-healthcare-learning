'''Configuration constants for the federated learning package.



All paths are constructed relative to the project root using ``pathlib.Path``.

The same ``PROJECT_ROOT`` constant is used throughout the federated codebase to

avoid the duplicated ``ml/ml`` path problem that caused earlier test failures.

'''



from pathlib import Path

import os



# ---------------------------------------------------------------------------

# Project root – two levels up from this file (federated/common/config.py)

#   C:/Users/amt97/New folder (2)/

# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]



# Directories used by both Phase‑3 and Phase‑4 code

DATA_DIR = PROJECT_ROOT / "ml" / "datasets" / "data"

CHECKPOINT_DIR = PROJECT_ROOT / "ml" / "models" / "checkpoints"



# Client CSV filenames (located under ml/datasets/data/clients/)

CLIENT_FILES = [

    "client_1.csv",

    "client_2.csv",

    "client_3.csv",

]



# Pre‑computed scaler (saved by Phase‑3 preprocessing)

SCALER_PATH = DATA_DIR / "processed" / "scaler.joblib"



# Hyper‑parameters (feel free to override via environment variables)

DEVICE = "cuda" if ("CUDA_VISIBLE_DEVICES" in os.environ and torch.cuda.is_available()) else "cpu"

BATCH_SIZE = int(os.getenv("FED_BATCH_SIZE", "64"))

LR = float(os.getenv("FED_LR", "1e-3"))

EPOCHS_LOCAL = int(os.getenv("FED_EPOCHS_LOCAL", "2"))

FED_ROUNDS = int(os.getenv("FED_ROUNDS", "3"))



# Ensure checkpoint directory exists at import time

CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
