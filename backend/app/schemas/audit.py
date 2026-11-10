from typing import Optional, Dict, Any

from datetime import datetime

from pydantic import BaseModel, ConfigDict





class AuditLogCreate(BaseModel):

    user_id: Optional[str] = None

    institution_id: Optional[str] = None

    action: str

    resource_type: str

    resource_id: Optional[str] = None

    ip_address: Optional[str] = None

    user_agent: Optional[str] = None

    details: Dict[str, Any] = {}

    status: str = "SUCCESS"





class AuditLogResponse(AuditLogCreate):

    id: str

    timestamp: datetime



    model_config = ConfigDict(from_attributes=True)
