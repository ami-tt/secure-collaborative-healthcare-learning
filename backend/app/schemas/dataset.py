from typing import Optional, Dict, Any

from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from app.models.dataset import DatasetModality





class DatasetBase(BaseModel):

    name: str = Field(..., min_length=2, max_length=255, json_schema_extra={"example": "Cardiovascular Risk Cohort"})

    modality: DatasetModality = Field(default=DatasetModality.TABULAR_EHR)

    sample_count: int = Field(default=0, ge=0, json_schema_extra={"example": 1500})

    feature_schema: Dict[str, Any] = Field(

        default_factory=dict,

        json_schema_extra={"example": {"features": ["age", "bmi", "blood_pressure", "cholesterol", "glucose"], "target": "cardiovascular_event"}}

    )





class DatasetCreate(DatasetBase):

    institution_id: Optional[str] = None





class DatasetResponse(DatasetBase):

    id: str

    institution_id: str

    is_validated: bool

    privacy_budget_spent: float

    created_at: datetime

    updated_at: datetime



    model_config = ConfigDict(from_attributes=True)
