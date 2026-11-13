"""
Stratified train, validation, and test split.

Training: 70%
Validation: 15%
Testing: 15%

Scaler is fitted only on training data to prevent data leakage.
"""

from pathlib import Path

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DIR = PROJECT_ROOT / "ml" / "datasets" / "data" / "processed"
SPLITS_DIR = PROJECT_ROOT / "ml" / "datasets" / "data" / "splits"

PROCESSED_PATH = PROCESSED_DIR / "clean.csv"
SCALER_PATH = PROCESSED_DIR / "scaler.pkl"

SPLITS_DIR.mkdir(parents=True, exist_ok=True)

TARGET_COL = "cardio"
ID_COL = "id"

NUMERIC_COLS = [
    "age",
    "height",
    "weight",
    "ap_hi",
    "ap_lo",
]


def main():
    df = pd.read_csv(PROCESSED_PATH)

    X = df.drop(columns=[TARGET_COL])
    y = df[TARGET_COL]

    # Split test data (15%)
    X_temp, X_test, y_temp, y_test = train_test_split(
        X,
        y,
        test_size=0.15,
        stratify=y,
        random_state=42,
    )

    # Split validation data (15% of total)
    val_ratio = 0.15 / 0.85

    X_train, X_val, y_train, y_val = train_test_split(
        X_temp,
        y_temp,
        test_size=val_ratio,
        stratify=y_temp,
        random_state=42,
    )

    # Create independent copies and convert numeric columns to float
    X_train = X_train.copy()
    X_val = X_val.copy()
    X_test = X_test.copy()

    for dataset in (X_train, X_val, X_test):
        dataset[NUMERIC_COLS] = dataset[NUMERIC_COLS].astype("float64")

    # Fit scaler only on training data
    scaler = StandardScaler()

    X_train[NUMERIC_COLS] = scaler.fit_transform(
        X_train[NUMERIC_COLS]
    )

    X_val[NUMERIC_COLS] = scaler.transform(
        X_val[NUMERIC_COLS]
    )

    X_test[NUMERIC_COLS] = scaler.transform(
        X_test[NUMERIC_COLS]
    )

    # Save scaler
    joblib.dump(scaler, SCALER_PATH)

    # Reattach target
    train_df = pd.concat([X_train, y_train], axis=1)
    val_df = pd.concat([X_val, y_val], axis=1)
    test_df = pd.concat([X_test, y_test], axis=1)

    # Save datasets
    train_df.to_csv(SPLITS_DIR / "train.csv", index=False)
    val_df.to_csv(SPLITS_DIR / "val.csv", index=False)
    test_df.to_csv(SPLITS_DIR / "test.csv", index=False)

    print("\nDataset splitting and scaling completed.")
    print(f"Training records: {len(train_df)}")
    print(f"Validation records: {len(val_df)}")
    print(f"Testing records: {len(test_df)}")
    print(f"Scaler saved: {SCALER_PATH}")
    print(f"Splits saved: {SPLITS_DIR}")


if __name__ == "__main__":
    main()