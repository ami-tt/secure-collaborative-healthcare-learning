from typing import Optional, Dict, Any

from sqlalchemy.orm import Session

from app.models.audit import AuditLog





class AuditService:

    @staticmethod

    def log(

        db: Session,

        action: str,

        resource_type: str,

        resource_id: Optional[str] = None,

        user_id: Optional[str] = None,

        institution_id: Optional[str] = None,

        ip_address: Optional[str] = None,

        user_agent: Optional[str] = None,

        details: Optional[Dict[str, Any]] = None,

        status: str = "SUCCESS"

    ) -> AuditLog:

        """

        Record an immutable audit log entry into the database.

        """

        audit_entry = AuditLog(

            action=action,

            resource_type=resource_type,

            resource_id=str(resource_id) if resource_id else None,

            user_id=str(user_id) if user_id else None,

            institution_id=str(institution_id) if institution_id else None,

            ip_address=ip_address,

            user_agent=user_agent,

            details=details or {},

            status=status

        )

        db.add(audit_entry)

        try:

            db.commit()

            db.refresh(audit_entry)

        except Exception:

            db.rollback()

        return audit_entry
