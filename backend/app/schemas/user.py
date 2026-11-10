from typing import Optional

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict

from app.models.user import UserRole

from app.schemas.institution import InstitutionResponse





class UserBase(BaseModel):

    email: EmailStr = Field(..., json_schema_extra={"example": "sarah.chen@hospital-alpha.org"})

    full_name: str = Field(..., min_length=2, max_length=255, json_schema_extra={"example": "Dr. Sarah Chen"})

    role: UserRole = Field(default=UserRole.RESEARCHER, json_schema_extra={"example": "researcher"})

    institution_id: Optional[str] = Field(None, json_schema_extra={"example": "550e8400-e29b-41d4-a716-446655440000"})





class UserCreate(UserBase):

    password: str = Field(..., min_length=8, max_length=128, json_schema_extra={"example": "StrongP@ssw0rd!"})





class UserUpdate(BaseModel):

    full_name: Optional[str] = None

    email: Optional[EmailStr] = None

    role: Optional[UserRole] = None

    is_active: Optional[bool] = None

    is_verified: Optional[bool] = None

    institution_id: Optional[str] = None





class UserResponse(UserBase):

    id: str

    is_active: bool

    is_verified: bool

    last_login: Optional[datetime] = None

    created_at: datetime

    updated_at: datetime



    model_config = ConfigDict(from_attributes=True)





class UserDetailResponse(UserResponse):

    institution: Optional[InstitutionResponse] = None



    model_config = ConfigDict(from_attributes=True)
