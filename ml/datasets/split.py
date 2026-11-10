"""ml/datasets/split.py



Stratified split of the cleaned cardiovascular dataset into train, validation, and test sets.



The script expects the cleaned CSV produced by `preprocess.py` at

`ml/datasets/data/processed/clean.csv`.



Outputs:

- `train.csv` (70%)

- `val.csv`   (15%)

- `test.csv`  (15%)



All files are saved under `ml/datasets/data/splits/`.

"""



'''ml/datasets/split.py



Stratified split of the cleaned cardiovascular dataset into train, validation, and test sets.



The script expects the cleaned CSV produced by `preprocess.py` at:

    ml/datasets/data/processed/clean.csv



Outputs are saved under:

    ml/datasets/data/splits/train.csv

    ml/datasets/data/splits/val.csv

    ml/datasets/data/splits/test.csv

'''



from pathlib import Path

import pandas as pd

from sklearn.model_selection import train_test_split



# Project root two levels up from this file (ml/datasets/split.py -> ml -> project root)

PROJECT_ROOT = Path(__file__).resolve().parents[2]



PROCESSED_PATH = PROJECT_ROOT / "ml" / "datasets" / "data" / "processed" / "clean.csv"

SPLITS_DIR = PROJECT_ROOT / "ml" / "datasets" / "data" / "splits"

SPLITS_DIR.mkdir(parents=True, exist_ok=True)



TARGET_COL = "cardio"



def main() -> None:

    df = pd.read_csv(PROCESSED_PATH)

    X = df.drop(columns=[TARGET_COL])

    y = df[TARGET_COL]



    # First split off test (15%)

    X_temp, X_test, y_temp, y_test = train_test_split(

        X, y, test_size=0.15, stratify=y, random_state=42

    )

    # Split remaining into train (≈70%) and validation (≈15%)

    val_ratio = 0.15 / (1 - 0.15)  # proportion of remaining to be validation

    X_train, X_val, y_train, y_val = train_test_split(

        X_temp, y_temp, test_size=val_ratio, stratify=y_temp, random_state=42

    )



    train_df = pd.concat([X_train, y_train], axis=1)

    val_df = pd.concat([X_val, y_val], axis=1)

    test_df = pd.concat([X_test, y_test], axis=1)



    train_df.to_csv(SPLITS_DIR / "train.csv", index=False)

    val_df.to_csv(SPLITS_DIR / "val.csv", index=False)

    test_df.to_csv(SPLITS_DIR / "test.csv", index=False)



    print(f"Train size: {train_df.shape[0]}")

    print(f"Validation size: {val_df.shape[0]}")

    print(f"Test size: {test_df.shape[0]}")



if __name__ == "__main__":

    main()
