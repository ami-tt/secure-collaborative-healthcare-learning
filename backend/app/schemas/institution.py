from typing import Optional

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict

from app.models.institution import InstitutionStatus





class InstitutionBase(BaseModel):

    name: str = Field(..., min_length=2, max_length=255, json_schema_extra={"example": "Apollo Health Institute"})

    institution_code: str = Field(..., min_length=2, max_length=50, json_schema_extra={"example": "HOSP-APOLLO-01"})

    contact_email: EmailStr = Field(..., json_schema_extra={"example": "contact@apollohealth.org"})

    phone: Optional[str] = Field(None, json_schema_extra={"example": "+1-555-019-2831"})

    address: Optional[str] = Field(None, json_schema_extra={"example": "100 Medical Center Blvd, Suite 400"})





class InstitutionCreate(InstitutionBase):

    pass





class InstitutionUpdate(BaseModel):

    name: Optional[str] = None

    contact_email: Optional[EmailStr] = None

    phone: Optional[str] = None

    address: Optional[str] = None

    status: Optional[InstitutionStatus] = None





class InstitutionResponse(InstitutionBase):

    id: str

    status: InstitutionStatus

    created_at: datetime

    updated_at: datetime



    model_config = ConfigDict(from_attributes=True)
