from typing import Optional

from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from app.models.fl_session import SessionStatus

from app.models.dataset import DatasetModality





class FLProjectCreate(BaseModel):

    title: str = Field(..., min_length=3, max_length=255, json_schema_extra={"example": "Diabetic Nephropathy Risk Federated Study"})

    description: Optional[str] = Field(None, json_schema_extra={"example": "Multi-institutional collaborative model training without raw EHR sharing."})

    target_condition: str = Field(..., json_schema_extra={"example": "Diabetes Nephropathy"})

    model_architecture: str = Field(default="TabularMLP", json_schema_extra={"example": "TabularMLP"})

    modality: DatasetModality = Field(default=DatasetModality.TABULAR_EHR)





class FLProjectResponse(FLProjectCreate):

    id: str

    created_by: str

    created_at: datetime

    updated_at: datetime



    model_config = ConfigDict(from_attributes=True)





class FLSessionCreate(BaseModel):

    project_id: str

    session_name: str = Field(..., min_length=3, max_length=255, json_schema_extra={"example": "Run-01-Baseline-FedAvg"})

    total_rounds: int = Field(default=10, ge=1, le=100)

    min_participating_clients: int = Field(default=2, ge=1)

    aggregation_strategy: str = Field(default="FedAvg")

    dp_enabled: bool = Field(default=True)

    dp_epsilon: float = Field(default=1.5, gt=0)

    dp_delta: float = Field(default=1e-5, gt=0)

    dp_max_grad_norm: float = Field(default=1.0, gt=0)

    learning_rate: float = Field(default=0.001, gt=0)

    local_epochs: int = Field(default=3, ge=1)

    batch_size: int = Field(default=32, ge=1)





class FLSessionResponse(FLSessionCreate):

    id: str

    current_round: int

    status: SessionStatus

    started_at: Optional[datetime] = None

    finished_at: Optional[datetime] = None

    created_at: datetime

    updated_at: datetime



    model_config = ConfigDict(from_attributes=True)
