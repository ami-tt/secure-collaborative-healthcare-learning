from pathlib import Path
import sys

import joblib
import numpy as np
import pandas as pd
import torch


# ============================================================
# PROJECT PATH CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Add project root to Python path so backend can import ml package
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ml.models.tabular_mlp import TabularMLP


# ============================================================
# MODEL AND SCALER PATHS
# ============================================================

MODEL_PATH = (
    PROJECT_ROOT
    / "ml"
    / "models"
    / "checkpoints"
    / "tabular_mlp.pt"
)

SCALER_PATH = (
    PROJECT_ROOT
    / "ml"
    / "datasets"
    / "data"
    / "processed"
    / "scaler.pkl"
)


# ============================================================
# FEATURE CONFIGURATION
# ============================================================

FEATURE_ORDER = [
    "age",
    "gender",
    "height",
    "weight",
    "ap_hi",
    "ap_lo",
    "cholesterol",
    "gluc",
    "smoke",
    "alco",
    "active",
]

NUMERIC_FEATURES = [
    "age",
    "height",
    "weight",
    "ap_hi",
    "ap_lo",
]


# ============================================================
# PREDICTION SERVICE
# ============================================================

class PredictionService:

    def __init__(self):
        self.device = torch.device("cpu")
        self.model = None
        self.scaler = None

    # --------------------------------------------------------
    # LOAD TRAINED MODEL AND SCALER
    # --------------------------------------------------------

    def load_artifacts(self):

        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Model checkpoint not found: {MODEL_PATH}"
            )

        if not SCALER_PATH.exists():
            raise FileNotFoundError(
                f"Scaler file not found: {SCALER_PATH}"
            )

        # Load preprocessing scaler
        self.scaler = joblib.load(SCALER_PATH)

        # Create model architecture
        self.model = TabularMLP(
            input_dim=len(FEATURE_ORDER)
        )

        # Load trained model weights
        state_dict = torch.load(
            MODEL_PATH,
            map_location=self.device,
            weights_only=True
        )

        self.model.load_state_dict(state_dict)

        self.model.to(self.device)
        self.model.eval()

    # --------------------------------------------------------
    # GENERATE PREDICTION
    # --------------------------------------------------------

    def predict(self, patient_data: dict):

        # Load model and scaler if not already loaded
        if self.model is None or self.scaler is None:
            self.load_artifacts()

        # Arrange input features in training order
        features = {
            name: float(patient_data[name])
            for name in FEATURE_ORDER
        }

        # Create DataFrame with original column names
        numeric_values = pd.DataFrame(
            [[features[name] for name in NUMERIC_FEATURES]],
            columns=NUMERIC_FEATURES
        )

        # Apply the scaler fitted on training data
        scaled_values = self.scaler.transform(
            numeric_values
        )[0]

        # Replace numerical features with scaled values
        for index, name in enumerate(NUMERIC_FEATURES):
            features[name] = float(scaled_values[index])

        # Prepare all 11 model input features
        input_values = np.array(
            [
                [features[name] for name in FEATURE_ORDER]
            ],
            dtype=np.float32
        )

        # Convert input into PyTorch tensor
        input_tensor = torch.tensor(
            input_values,
            dtype=torch.float32,
            device=self.device
        )

        # Generate prediction
        with torch.no_grad():

            logits = self.model(input_tensor)

            probability = torch.sigmoid(
                logits
            ).item()

        # Classification threshold
        predicted_class = int(probability >= 0.5)

        # Return prediction response
        return {
            "risk_probability": round(probability, 4),
            "predicted_class": predicted_class,
            "model_name": "TabularMLP",
            "disclaimer": (
                "This is an educational research prototype. "
                "It is not a medical diagnosis or a substitute "
                "for professional medical advice."
            )
        }


# ============================================================
# SHARED PREDICTION SERVICE INSTANCE
# ============================================================

prediction_service = PredictionService()