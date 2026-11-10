from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from sqlalchemy.orm import Session



from app.core.database import get_db

from app.models.audit import AuditLog

from app.models.user import User, UserRole

from app.schemas.audit import AuditLogResponse

from app.api.deps import require_roles



router = APIRouter()





@router.get(

    "/",

    response_model=List[AuditLogResponse],

    summary="Query compliance audit trail (Admin only)"

)

def get_audit_logs(

    skip: int = Query(0, ge=0),

    limit: int = Query(50, ge=1, le=100),

    action: Optional[str] = None,

    resource_type: Optional[str] = None,

    user_id: Optional[str] = None,

    current_user: User = Depends(require_roles([UserRole.ADMIN])),

    db: Session = Depends(get_db)

):

    """

    Retrieve system security and access logs for HIPAA / regulatory compliance.

    """

    query = db.query(AuditLog)

    if action:

        query = query.filter(AuditLog.action == action)

    if resource_type:

        query = query.filter(AuditLog.resource_type == resource_type)

    if user_id:

        query = query.filter(AuditLog.user_id == user_id)



    return query.order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit).all()
