import logging

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user, require_roles
from app.models.user import User, UserRole
from app.schemas.prediction import (
    PredictionRequest,
    PredictionResponse,
)
from app.services.prediction_service import prediction_service


logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/predict",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Predict cardiovascular risk",
    description=(
        "Generate an educational cardiovascular risk prediction "
        "using the trained TabularMLP model."
    ),
)
def predict_cardiovascular_risk(
    patient_data: PredictionRequest,
    current_user: User = Depends(
        require_roles([
            UserRole.ADMIN,
            UserRole.HOSPITAL_ADMIN,
            UserRole.RESEARCHER,
        ])
    ),
):
    """
    Generate a cardiovascular risk prediction.

    Requires an authenticated and active user.
    Patient input is processed in memory and is not stored
    by this endpoint.
    """

    try:
        result = prediction_service.predict(
            patient_data.model_dump()
        )

        return PredictionResponse(**result)

    except (FileNotFoundError, RuntimeError, OSError, ValueError):
        logger.exception(
            "Cardiovascular prediction service failed."
        )

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Prediction service is temporarily unavailable.",
        )