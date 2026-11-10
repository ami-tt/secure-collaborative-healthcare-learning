from typing import Optional

from pydantic import BaseModel, EmailStr, Field





class LoginRequest(BaseModel):

    email: EmailStr = Field(..., json_schema_extra={"example": "researcher@hospital-alpha.org"})

    password: str = Field(..., min_length=6, json_schema_extra={"example": "SecureP@ssword123"})





class Token(BaseModel):

    access_token: str

    token_type: str = "bearer"

    role: str

    user_id: str

    email: str

    full_name: str

    institution_id: Optional[str] = None





class TokenPayload(BaseModel):

    sub: Optional[str] = None

    role: Optional[str] = None

    institution_id: Optional[str] = None

    exp: Optional[int] = None
