"""
Create three non-overlapping simulated hospital datasets.

Client 1: Older patients (>55 years).
Client 2: Younger patients (<=55 years), gender 1.
Client 3: Younger patients (<=55 years), gender 2.

All clients are created exclusively from the training split.
Original age values are recovered using patient IDs.
"""

from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CLEAN_PATH = (
    PROJECT_ROOT / "ml" / "datasets" / "data"
    / "processed" / "clean.csv"
)

TRAIN_PATH = (
    PROJECT_ROOT / "ml" / "datasets" / "data"
    / "splits" / "train.csv"
)

CLIENTS_DIR = (
    PROJECT_ROOT / "ml" / "datasets" / "data" / "clients"
)

CLIENTS_DIR.mkdir(parents=True, exist_ok=True)

ID_COL = "id"


def main():

    clean_df = pd.read_csv(CLEAN_PATH)
    train_df = pd.read_csv(TRAIN_PATH)

    # Recover original age values using patient IDs.
    age_lookup = clean_df.set_index(ID_COL)["age"]

    train_df = train_df.copy()

    train_df["original_age_days"] = train_df[ID_COL].map(
        age_lookup
    )

    if train_df["original_age_days"].isna().any():
        raise ValueError("Missing original age values detected.")

    train_df["age_years"] = (
        train_df["original_age_days"] / 365.25
    )

    # Client 1: Older patients.
    client1 = train_df[
        train_df["age_years"] > 55
    ].copy()

    # Younger patient pool.
    younger = train_df[
        train_df["age_years"] <= 55
    ].copy()

    # Client 2: Younger patients with gender 1.
    client2 = younger[
        younger["gender"] == 1
    ].copy()

    # Client 3: Younger patients with gender 2.
    client3 = younger[
        younger["gender"] == 2
    ].copy()

    clients = {
        "client_1.csv": client1,
        "client_2.csv": client2,
        "client_3.csv": client3,
    }

    # Remove temporary columns and save.
    for filename, client_df in clients.items():

        client_df = client_df.drop(
            columns=["original_age_days", "age_years"]
        )

        client_df.to_csv(
            CLIENTS_DIR / filename,
            index=False
        )

        print(f"{filename}: {len(client_df)} records")

    # Verify that all clients contain records.
    if any(df.empty for df in clients.values()):
        raise ValueError(
            "At least one client is empty. Check gender distribution."
        )

    # Verify no patient appears in multiple clients.
    all_ids = pd.concat(
        [df[ID_COL] for df in clients.values()],
        ignore_index=True
    )

    if all_ids.duplicated().any():
        raise ValueError(
            "Duplicate patient IDs found across clients."
        )

    # Verify all training records are assigned.
    if len(all_ids) != len(train_df):
        raise ValueError(
            "Some training records were not assigned to clients."
        )

    print("\nClient partitioning completed successfully.")
    print(f"Total training records: {len(train_df)}")
    print(f"Total client records: {len(all_ids)}")
    print("Duplicate patient IDs: 0")


if __name__ == "__main__":
    main()