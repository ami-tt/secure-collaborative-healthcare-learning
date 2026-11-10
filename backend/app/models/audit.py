from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime, JSON, ForeignKey

from sqlalchemy.orm import relationship

from app.core.database import Base

from app.models.base import BaseModelMixin





class AuditLog(Base, BaseModelMixin):

    """

    Immutable compliance log record for tracking platform security events.

    """

    __tablename__ = "audit_logs"



    user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)

    institution_id = Column(String(36), ForeignKey("institutions.id", ondelete="SET NULL"), nullable=True, index=True)

    action = Column(String(100), nullable=False, index=True)

    resource_type = Column(String(100), nullable=False)

    resource_id = Column(String(255), nullable=True)

    ip_address = Column(String(45), nullable=True)

    user_agent = Column(String(500), nullable=True)

    details = Column(JSON, default=dict, nullable=False)

    status = Column(String(50), default="SUCCESS", nullable=False)

    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)



    # Relationships

    user = relationship("User", back_populates="audit_logs")

    institution = relationship("Institution")
