import json

import os

import pandas as pd

import numpy as np



DATASET_PATH = os.path.join(os.path.dirname(__file__), "data", "raw", "cardio_train.csv")





def run_eda():

    print("=" * 80)

    print("🏥 EXPLORATORY DATA ANALYSIS & CLINICAL VALIDATION")

    print("Dataset: Kaggle Cardiovascular Disease Dataset (by Svetlana Ulianova)")

    print("Source: https://www.kaggle.com/datasets/sulianova/cardiovascular-disease-dataset")

    print("=" * 80)



    # 1. Load CSV

    df = pd.read_csv(DATASET_PATH, sep=";")

    print(f"\n[1] DATASET DIMENSIONS: {df.shape[0]} rows x {df.shape[1]} columns")



    # 2. Features and Target

    columns = list(df.columns)

    target_col = "cardio"

    feature_cols = [c for c in columns if c not in ["id", target_col]]

    print(f"\n[2] IDENTIFIED COLUMNS:")

    print(f"  - Patient Identifier (to exclude): 'id'")

    print(f"  - Target Column: '{target_col}' (0 = absence, 1 = presence of CVD)")

    print(f"  - Clinical Feature Columns ({len(feature_cols)}): {feature_cols}")



    # 3. Missing Values

    null_counts = df.isnull().sum()

    print(f"\n[3] MISSING / NULL VALUES PER COLUMN:")

    for col, count in null_counts.items():

        print(f"  - {col}: {count} missing ({(count / len(df)) * 100:.2f}%)")



    # 4. Duplicate Records

    dup_ids = df.duplicated(subset=["id"]).sum()

    dup_records = df.duplicated(subset=feature_cols + [target_col]).sum()

    print(f"\n[4] DUPLICATE RECORDS:")

    print(f"  - Duplicate IDs: {dup_ids}")

    print(f"  - Duplicate Clinical Profiles (identical clinical records): {dup_records}")



    # 5. Class Distribution

    cardio_counts = df[target_col].value_counts().to_dict()

    cardio_pcts = (df[target_col].value_counts(normalize=True) * 100).to_dict()

    print(f"\n[5] TARGET CLASS DISTRIBUTION ('{target_col}'):")

    print(f"  - Class 0 (No Cardiovascular Disease): {cardio_counts.get(0, 0)} ({cardio_pcts.get(0, 0):.2f}%)")

    print(f"  - Class 1 (Cardiovascular Disease Present): {cardio_counts.get(1, 0)} ({cardio_pcts.get(1, 0):.2f}%)")

    print(f"  - Balance: Highly balanced dataset (~50/50 split), optimal for clinical binary classification.")



    # 6. Age Analysis (in days vs years)

    df["age_years"] = (df["age"] / 365.25).round(1)

    print(f"\n[6] AGE DISTRIBUTION:")

    print(f"  - Min Age: {df['age'].min()} days ({df['age_years'].min()} years)")

    print(f"  - Max Age: {df['age'].max()} days ({df['age_years'].max()} years)")

    print(f"  - Mean Age: {df['age_years'].mean():.1f} years, Median Age: {df['age_years'].median():.1f} years")



    # 7. Physiological Anomalies & Outliers Check

    print(f"\n[7] CLINICAL & PHYSIOLOGICAL ANOMALY AUDIT:")



    # Blood pressure anomalies

    ap_hi_neg = (df["ap_hi"] <= 0).sum()

    ap_lo_neg = (df["ap_lo"] <= 0).sum()

    ap_hi_extreme = ((df["ap_hi"] < 60) | (df["ap_hi"] > 240)).sum()

    ap_lo_extreme = ((df["ap_lo"] < 40) | (df["ap_lo"] > 180)).sum()

    inverted_bp = (df["ap_lo"] > df["ap_hi"]).sum()



    print(f"  - Systolic BP (ap_hi) <= 0: {ap_hi_neg}")

    print(f"  - Diastolic BP (ap_lo) <= 0: {ap_lo_neg}")

    print(f"  - Systolic BP outside physiological range [60, 240] mmHg: {ap_hi_extreme}")

    print(f"  - Diastolic BP outside physiological range [40, 180] mmHg: {ap_lo_extreme}")

    print(f"  - Inverted BP (Diastolic ap_lo > Systolic ap_hi): {inverted_bp}")



    # Height / Weight anomalies

    height_outliers = ((df["height"] < 120) | (df["height"] > 220)).sum()

    weight_outliers = ((df["weight"] < 35) | (df["weight"] > 200)).sum()

    print(f"  - Height outside plausible adult range [120, 220] cm: {height_outliers}")

    print(f"  - Weight outside plausible adult range [35, 200] kg: {weight_outliers}")



    # 8. Feature Categorical Distributions

    print(f"\n[8] CATEGORICAL FEATURE DISTRIBUTIONS:")

    for cat in ["gender", "cholesterol", "gluc", "smoke", "alco", "active"]:

        dist = df[cat].value_counts(normalize=True).to_dict()

        formatted = ", ".join([f"Val {k}: {v*100:.1f}%" for k, v in dist.items()])

        print(f"  - {cat}: {formatted}")



    # 9. Summary Statistics

    print(f"\n[9] NUMERICAL FEATURES SUMMARY STATS:")

    num_cols = ["age_years", "height", "weight", "ap_hi", "ap_lo"]

    desc = df[num_cols].describe().round(2)

    print(desc.to_string())



    # Total valid rows after clinical bounds filter

    valid_mask = (

        (df["ap_hi"] >= 60) & (df["ap_hi"] <= 240) &

        (df["ap_lo"] >= 40) & (df["ap_lo"] <= 180) &

        (df["ap_lo"] < df["ap_hi"]) &

        (df["height"] >= 120) & (df["height"] <= 220) &

        (df["weight"] >= 35) & (df["weight"] <= 200)

    )

    cleaned_count = valid_mask.sum()

    removed_count = len(df) - cleaned_count

    print(f"\n[10] CLINICAL CLEANING IMPACT:")

    print(f"  - Original Records: {len(df)}")

    print(f"  - Physiologically Sound Records: {cleaned_count} ({cleaned_count/len(df)*100:.2f}%)")

    print(f"  - Anomalous Records Flagged for Removal: {removed_count} ({removed_count/len(df)*100:.2f}%)")



    return {

        "original_rows": len(df),

        "cleaned_rows": int(cleaned_count),

        "removed_rows": int(removed_count),

        "features": feature_cols,

        "target": target_col,

        "class_distribution": cardio_counts,

    }





if __name__ == "__main__":

    run_eda()
