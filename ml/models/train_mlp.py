"""ml/models/train_mlp.py



Train a simple feed‑forward neural network (TabularMLP) on the cleaned cardiovascular dataset.



The script expects the split CSV files produced by `ml/datasets/split.py`:

    - train.csv

    - val.csv

    - test.csv



Outputs:

    - Model checkpoint saved to `ml/models/checkpoints/tabular_mlp.pt`

    - Test metrics saved to `ml/models/checkpoints/mlp_test_metrics.json`

"""



import json

from pathlib import Path

import pandas as pd

import torch

import torch.nn as nn

from torch.utils.data import DataLoader, TensorDataset

from sklearn.metrics import (

    accuracy_score,

    precision_score,

    recall_score,

    f1_score,

    roc_auc_score,

    confusion_matrix,

)



# Import the model definition

from ml.models.tabular_mlp import TabularMLP, build_model



# ---------------------------------------------------------------------------

# Project layout constants – calculated relative to this file

# ---------------------------------------------------------------------------

# Two levels up from this file: ml/models/train_mlp.py -> ml -> project root

PROJECT_ROOT = Path(__file__).resolve().parents[2]



# Directories used by the pipeline

SPLITS_DIR = PROJECT_ROOT / "ml" / "datasets" / "data" / "splits"

CHECKPOINT_DIR = PROJECT_ROOT / "ml" / "models" / "checkpoints"

CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)



TARGET_COL = "cardio"

ID_COL = "id"





def load_split(split_name: str) -> tuple[pd.DataFrame, pd.Series]:

    """Load a CSV split and return features (X) and target (y)."""

    path = SPLITS_DIR / f"{split_name}.csv"

    df = pd.read_csv(path)

    X = df.drop(columns=[TARGET_COL, ID_COL])

    y = df[TARGET_COL]

    return X, y





def to_tensor_dataset(X: pd.DataFrame, y: pd.Series) -> TensorDataset:

    """Convert pandas data to a TensorDataset for PyTorch training."""

    X_tensor = torch.tensor(X.values, dtype=torch.float32)

    y_tensor = torch.tensor(y.values, dtype=torch.float32)

    return TensorDataset(X_tensor, y_tensor)





def full_metrics(model: nn.Module, loader: DataLoader) -> dict:

    """Compute a full set of metrics (including ROC‑AUC, sensitivity & specificity)."""

    model.eval()

    all_probs = []

    all_preds = []

    all_labels = []

    with torch.no_grad():

        for xb, yb in loader:

            logits = model(xb)

            probs = torch.sigmoid(logits)

            preds = (probs >= 0.5).int()

            all_probs.extend(probs.cpu().numpy())

            all_preds.extend(preds.cpu().numpy())

            all_labels.extend(yb.int().cpu().numpy())

    acc = accuracy_score(all_labels, all_preds)

    prec = precision_score(all_labels, all_preds, zero_division=0)

    rec = recall_score(all_labels, all_preds, zero_division=0)

    f1 = f1_score(all_labels, all_preds, zero_division=0)

    auc = roc_auc_score(all_labels, all_probs)

    tn, fp, fn, tp = confusion_matrix(all_labels, all_preds).ravel()

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

    # ---------------------------------------------------------------------

    # Load data splits

    # ---------------------------------------------------------------------

    X_train, y_train = load_split("train")

    X_val, y_val = load_split("val")

    X_test, y_test = load_split("test")



    train_ds = to_tensor_dataset(X_train, y_train)

    val_ds = to_tensor_dataset(X_val, y_val)

    test_ds = to_tensor_dataset(X_test, y_test)



    train_loader = DataLoader(train_ds, batch_size=64, shuffle=True)

    val_loader = DataLoader(val_ds, batch_size=256)

    test_loader = DataLoader(test_ds, batch_size=256)



    # ---------------------------------------------------------------------

    # Model setup

    # ---------------------------------------------------------------------

    input_dim = X_train.shape[1]

    model = build_model(input_dim)

    criterion = nn.BCEWithLogitsLoss()

    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)



    best_val_loss = float("inf")

    epochs = 30

    patience = 5

    patience_counter = 0



    # ---------------------------------------------------------------------

    # Training loop with early stopping

    # ---------------------------------------------------------------------

    for epoch in range(1, epochs + 1):

        model.train()

        epoch_losses = []

        for xb, yb in train_loader:

            optimizer.zero_grad()

            logits = model(xb)

            loss = criterion(logits, yb)

            loss.backward()

            optimizer.step()

            epoch_losses.append(loss.item())

        avg_train_loss = sum(epoch_losses) / len(epoch_losses)



        # Validation

        model.eval()

        val_losses = []

        all_val_probs = []

        all_val_labels = []

        with torch.no_grad():

            for xb, yb in val_loader:

                logits = model(xb)

                loss = criterion(logits, yb)

                val_losses.append(loss.item())

                probs = torch.sigmoid(logits)

                all_val_probs.extend(probs.cpu().numpy())

                all_val_labels.extend(yb.cpu().numpy())

        avg_val_loss = sum(val_losses) / len(val_losses)

        val_auc = roc_auc_score(all_val_labels, all_val_probs)



        print(

            f"Epoch {epoch:02d} – Train loss: {avg_train_loss:.4f}, "

            f"Val loss: {avg_val_loss:.4f}, Val AUC: {val_auc:.4f}"

        )



        # Early‑stopping check

        if avg_val_loss < best_val_loss:

            best_val_loss = avg_val_loss

            patience_counter = 0

            torch.save(model.state_dict(), CHECKPOINT_DIR / "tabular_mlp.pt")

        else:

            patience_counter += 1

            if patience_counter >= patience:

                print("Early stopping triggered.")

                break



    # ---------------------------------------------------------------------

    # Load best checkpoint for final evaluation

    # ---------------------------------------------------------------------

    model.load_state_dict(torch.load(CHECKPOINT_DIR / "tabular_mlp.pt"))

    model.eval()



    val_metrics = full_metrics(model, val_loader)

    test_metrics = full_metrics(model, test_loader)



    print("\n=== Validation Metrics ===")

    for k, v in val_metrics.items():

        print(f"{k}: {v:.4f}")



    print("\n=== Test Metrics ===")

    for k, v in test_metrics.items():

        print(f"{k}: {v:.4f}")



    # Save test metrics for the reporting script

    metrics_path = CHECKPOINT_DIR / "mlp_test_metrics.json"

    with open(metrics_path, "w") as f:

        json.dump(test_metrics, f, indent=2)

    print(f"Test metrics saved to {metrics_path}")





if __name__ == "__main__":

    main()
