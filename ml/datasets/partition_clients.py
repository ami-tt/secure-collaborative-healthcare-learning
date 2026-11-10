"""ml/datasets/partition_clients.py



Create three simulated hospital client datasets from the training split with controlled non‑IID distributions.



Clients:

- **client_1.csv** – Older patients (age > 55 years).

- **client_2.csv** – Younger patients (age ≤ 55 years).

- **client_3.csv** – Balanced age but skewed gender ratio (more females).



All files are saved under `ml/datasets/data/clients/`.

"""



import os

import pandas as pd

from sklearn.model_selection import train_test_split



BASE_DIR = os.path.dirname(__file__)

SPLITS_PATH = os.path.join(BASE_DIR, "data", "splits", "train.csv")

CLIENTS_DIR = os.path.join(BASE_DIR, "data", "clients")

os.makedirs(CLIENTS_DIR, exist_ok=True)



TARGET_COL = "cardio"

ID_COL = "id"



def load_train():

    return pd.read_csv(SPLITS_PATH)



def client_old(df: pd.DataFrame):

    # Age column is in days; convert to years for the threshold

    df = df.copy()

    df["age_years"] = df["age"] / 365.25

    mask = df["age_years"] > 55

    return df[mask]



def client_young(df: pd.DataFrame):

    df = df.copy()

    df["age_years"] = df["age"] / 365.25

    mask = df["age_years"] <= 55

    return df[mask]



def client_gender_skew(df: pd.DataFrame):

    # Aim for approx 70% female (gender 2) and 30% male (gender 1)

    df = df.copy()

    # gender encoded as 1 = male, 2 = female in the original dataset

    female = df[df["gender"] == 2]

    male = df[df["gender"] == 1]

    # Down‑sample males to achieve 30% proportion

    target_female_ratio = 0.7

    total_needed = len(df)

    female_needed = int(total_needed * target_female_ratio)

    male_needed = total_needed - female_needed

    female_sample = female.sample(n=min(female_needed, len(female)), random_state=42)

    male_sample = male.sample(n=min(male_needed, len(male)), random_state=42)

    return pd.concat([female_sample, male_sample])



def main():

    train = load_train()

    # Drop the temporary age_years column if present

    if "age_years" in train.columns:

        train = train.drop(columns=["age_years"])  # safety



    client1 = client_old(train)

    client2 = client_young(train)

    client3 = client_gender_skew(train)



    # Ensure roughly equal sizes – if any client is too small, fallback to stratified split

    sizes = [len(client1), len(client2), len(client3)]

    print("Client sizes before balancing:", sizes)



    # To keep the total training data size unchanged we will sample from the original

    # training set to create three partitions of equal size (≈ 1/3 each).

    total = len(train)

    per_client = total // 3

    # Helper to down‑sample to per_client rows while preserving class distribution

    def stratified_downsample(df, n):

        if len(df) <= n:

            return df

        return df.groupby(TARGET_COL, group_keys=False).apply(

            lambda x: x.sample(int(n * len(x) / len(df)), random_state=42)

        )

    client1 = stratified_downsample(client1, per_client)

    client2 = stratified_downsample(client2, per_client)

    client3 = stratified_downsample(client3, per_client)



    # Save

    client1.to_csv(os.path.join(CLIENTS_DIR, "client_1.csv"), index=False)

    client2.to_csv(os.path.join(CLIENTS_DIR, "client_2.csv"), index=False)

    client3.to_csv(os.path.join(CLIENTS_DIR, "client_3.csv"), index=False)

    print("Clients saved:", [os.path.join(CLIENTS_DIR, f"client_{i}.csv") for i in range(1,4)])



if __name__ == "__main__":

    main()
