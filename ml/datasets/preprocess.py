"""
Preprocess the raw Cardiovascular Disease dataset.

Operations:
1. Load raw CSV data.
2. Apply clinical validity filters.
3. Remove duplicate clinical records.
4. Preserve categorical variables as integers.
5. Save cleaned, unscaled data.

Scaling is intentionally performed later in split.py,
using training data only, to prevent data leakage.
"""

from pathlib import Path
import pandas as pd

# Paths
BASE_DIR = Path(__file__).resolve().parent

RAW_PATH = BASE_DIR / "data" / "raw" / "cardio_train.csv"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

CLEAN_PATH = PROCESSED_DIR / "clean.csv"

TARGET_COL = "cardio"
ID_COL = "id"


def load_raw() -> pd.DataFrame:
    """Load the original semicolon-separated CSV."""
    return pd.read_csv(RAW_PATH, sep=";")


def clinical_filter(df: pd.DataFrame) -> pd.DataFrame:
    """Remove clinically implausible records."""

    mask = (
        (df["ap_hi"] >= 60)
        & (df["ap_hi"] <= 240)
        & (df["ap_lo"] >= 40)
        & (df["ap_lo"] <= 180)
        & (df["ap_lo"] < df["ap_hi"])
        & (df["height"] >= 120)
        & (df["height"] <= 220)
        & (df["weight"] >= 35)
        & (df["weight"] <= 200)
    )

    return df.loc[mask].reset_index(drop=True)


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate clinical records."""

    feature_cols = [
        col for col in df.columns
        if col not in [ID_COL, TARGET_COL]
    ]

    return df.drop_duplicates(
        subset=feature_cols + [TARGET_COL]
    ).reset_index(drop=True)


def encode_categoricals(df: pd.DataFrame) -> pd.DataFrame:
    """
    The original dataset already stores categorical
    variables as integers. No additional encoding is needed.
    """
    return df.copy()


def main():
    raw = load_raw()

    print(
        f"Loaded raw dataset: "
        f"{raw.shape[0]} rows, {raw.shape[1]} columns"
    )

    filtered = clinical_filter(raw)

    print(
        f"After clinical filtering: "
        f"{filtered.shape[0]} rows"
    )

    deduped = remove_duplicates(filtered)

    print(
        f"After duplicate removal: "
        f"{deduped.shape[0]} rows"
    )

    cleaned = encode_categoricals(deduped)

    # Save cleaned data WITHOUT scaling.
    cleaned.to_csv(CLEAN_PATH, index=False)

    print(f"Cleaned dataset saved to: {CLEAN_PATH}")
    print(f"Final dataset shape: {cleaned.shape}")
    print("Preprocessing completed successfully.")
    print("Note: Numeric scaling will be performed in split.py.")


if __name__ == "__main__":
    main()