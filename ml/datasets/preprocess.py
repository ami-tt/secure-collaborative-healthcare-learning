"""ml/datasets/preprocess.py



Preprocess the raw Cardiovascular Disease dataset.



- Applies clinical validity filters (blood pressure, height, weight).

- Removes duplicate clinical records (including target column).

- Splits identifier column.

- Encodes categorical variables as integers (kept as‑is for now).

- Standardizes numeric features using `StandardScaler`.

- Saves the cleaned dataframe and the fitted scaler for later stages.



The script can be executed directly:



    python -m ml.datasets.preprocess



"""



import os

import pandas as pd

import numpy as np

from sklearn.preprocessing import StandardScaler

import joblib



# Paths

BASE_DIR = os.path.dirname(__file__)

RAW_PATH = os.path.join(BASE_DIR, "data", "raw", "cardio_train.csv")

PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

os.makedirs(PROCESSED_DIR, exist_ok=True)

CLEAN_PATH = os.path.join(PROCESSED_DIR, "clean.csv")

SCALER_PATH = os.path.join(PROCESSED_DIR, "scaler.pkl")



TARGET_COL = "cardio"

ID_COL = "id"



def load_raw() -> pd.DataFrame:

    """Load the original CSV (semicolon separated)."""

    df = pd.read_csv(RAW_PATH, sep=";")

    return df



def clinical_filter(df: pd.DataFrame) -> pd.DataFrame:

    """Apply realistic clinical bounds and keep only physiologically plausible rows.



    Bounds (based on the EDA script):

        - systolic BP (ap_hi): 60‑240 mmHg

        - diastolic BP (ap_lo): 40‑180 mmHg

        - diastolic < systolic

        - height: 120‑220 cm

        - weight: 35‑200 kg

    """

    mask = (

        (df["ap_hi"] >= 60) & (df["ap_hi"] <= 240) &

        (df["ap_lo"] >= 40) & (df["ap_lo"] <= 180) &

        (df["ap_lo"] < df["ap_hi"]) &

        (df["height"] >= 120) & (df["height"] <= 220) &

        (df["weight"] >= 35) & (df["weight"] <= 200)

    )

    return df[mask].reset_index(drop=True)



def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:

    """Drop duplicate clinical records (including target)."""

    feature_cols = [c for c in df.columns if c not in [ID_COL, TARGET_COL]]

    # Drop rows that are identical in all feature columns + target

    df_nodup = df.drop_duplicates(subset=feature_cols + [TARGET_COL])

    return df_nodup.reset_index(drop=True)



def encode_categoricals(df: pd.DataFrame) -> pd.DataFrame:

    """Current dataset already encodes categoricals as integers (0/1/2/3).

    No transformation is needed for the baseline models, but the function is kept

    for future extensibility.

    """

    return df



def scale_numeric(df: pd.DataFrame, scaler: StandardScaler = None):

    """Scale numeric columns using StandardScaler.



    Returns the transformed dataframe and the fitted scaler (if a scaler was not

    provided).

    """

    numeric_cols = ["age", "height", "weight", "ap_hi", "ap_lo"]

    if scaler is None:

        scaler = StandardScaler()

        df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    else:

        df[numeric_cols] = scaler.transform(df[numeric_cols])

    return df, scaler



def main():

    raw = load_raw()

    print(f"Loaded raw dataset with {raw.shape[0]} rows and {raw.shape[1]} columns")



    filtered = clinical_filter(raw)

    print(f"After clinical filter: {filtered.shape[0]} rows remain")



    deduped = remove_duplicates(filtered)

    print(f"After duplicate removal: {deduped.shape[0]} rows remain")



    encoded = encode_categoricals(deduped)



    # Separate features and target (the scaler should be fit on features only)

    features = encoded.drop(columns=[ID_COL, TARGET_COL])

    target = encoded[TARGET_COL]



    # Fit scaler on numeric columns

    features_scaled, scaler = scale_numeric(features)



    # Re‑attach id and target for downstream pipelines that expect them.

    cleaned = pd.concat([encoded[[ID_COL]], features_scaled, target], axis=1)



    cleaned.to_csv(CLEAN_PATH, index=False)

    joblib.dump(scaler, SCALER_PATH)

    print(f"Saved cleaned data to {CLEAN_PATH}")

    print(f"Saved scaler to {SCALER_PATH}")



if __name__ == "__main__":

    main()
