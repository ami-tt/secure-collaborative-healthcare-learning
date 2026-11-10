"""ml/reporting/evaluation_report.py



Load the saved test‑metrics JSON files from the two training scripts and print a side‑by‑side comparison table.

Also prints a short discussion of dataset limitations and the non‑IID client setup.

"""



import os

import json

from tabulate import tabulate



BASE_DIR = os.path.dirname(__file__)

CHECKPOINT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "models", "checkpoints"))



def load_metrics(fname: str) -> dict:

    path = os.path.join(CHECKPOINT_DIR, fname)

    with open(path, "r") as f:

        return json.load(f)



def main():

    mlp_metrics = load_metrics("mlp_test_metrics.json")

    logreg_metrics = load_metrics("logreg_test_metrics.json")



    headers = ["Metric", "Tabular MLP", "Logistic Regression"]

    rows = []

    for metric in ["accuracy", "precision", "recall", "f1", "roc_auc", "sensitivity", "specificity"]:

        rows.append([metric, f"{mlp_metrics.get(metric, 0):.4f}", f"{logreg_metrics.get(metric, 0):.4f}"])



    table = tabulate(rows, headers=headers, tablefmt="github")

    print("\n=== Model Comparison on Test Set ===")

    print(table)



    # Brief discussion (static text, can be expanded later)

    discussion = (

        "\nDataset Limitations & Observations:\n"

        "- The Kaggle Cardiovascular Disease dataset is based on a Czech population (≈70k records) and may not generalize to other ethnic groups.\n"

        "- All features are self‑reported or measured once; no longitudinal data.\n"

        "- Class balance is near 50/50, which is unusual for real‑world prevalence and may inflate performance metrics.\n"

        "- Age is recorded in days; we converted to years for client partitioning.\n"

        "- Non‑IID simulation: client 1 (older), client 2 (younger), client 3 (female‑skewed). This creates demographic drift that can affect federated averaging later.\n"

    )

    print(discussion)



if __name__ == "__main__":

    main()
