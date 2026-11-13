from pydantic import BaseModel, Field, ConfigDict, model_validator


class PredictionRequest(BaseModel):
    """
    Patient features for cardiovascular risk prediction.

    Age must be provided in days, matching the original dataset.
    """

    age: float = Field(..., gt=0, le=150000, description="Age in days")
    gender: int = Field(..., ge=1, le=2, description="1 or 2")
    height: float = Field(..., ge=120, le=220, description="Height in cm")
    weight: float = Field(..., ge=35, le=200, description="Weight in kg")
    ap_hi: float = Field(..., ge=60, le=240, description="Systolic blood pressure")
    ap_lo: float = Field(..., ge=40, le=180, description="Diastolic blood pressure")
    cholesterol: int = Field(..., ge=1, le=3)
    gluc: int = Field(..., ge=1, le=3)
    smoke: int = Field(..., ge=0, le=1)
    alco: int = Field(..., ge=0, le=1)
    active: int = Field(..., ge=0, le=1)

    @model_validator(mode="after")
    def validate_blood_pressure(self):
        if self.ap_hi <= self.ap_lo:
            raise ValueError(
                "Systolic blood pressure must be greater than "
                "diastolic blood pressure."
            )
        return self

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "age": 18393,
                "gender": 2,
                "height": 168,
                "weight": 62.0,
                "ap_hi": 110,
                "ap_lo": 80,
                "cholesterol": 1,
                "gluc": 1,
                "smoke": 0,
                "alco": 0,
                "active": 1
            }
        }
    )


class PredictionResponse(BaseModel):
    risk_probability: float
    predicted_class: int
    model_name: str
    disclaimer: str