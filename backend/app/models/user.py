import enum

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Enum

from sqlalchemy.orm import relationship

from app.core.database import Base

from app.models.base import BaseModelMixin





class UserRole(str, enum.Enum):

    ADMIN = "admin"

    HOSPITAL_ADMIN = "hospital_admin"

    RESEARCHER = "researcher"





class User(Base, BaseModelMixin):

    __tablename__ = "users"



    institution_id = Column(String(36), ForeignKey("institutions.id", ondelete="SET NULL"), nullable=True, index=True)

    email = Column(String(255), unique=True, index=True, nullable=False)

    password_hash = Column(String(255), nullable=False)

    full_name = Column(String(255), nullable=False)

    role = Column(

        Enum(UserRole, values_callable=lambda x: [e.value for e in x]),

        nullable=False,

        default=UserRole.RESEARCHER,

        index=True

    )

    is_active = Column(Boolean, default=True, nullable=False)

    is_verified = Column(Boolean, default=False, nullable=False)

    last_login = Column(DateTime(timezone=True), nullable=True)



    # Relationships

    institution = relationship("Institution", back_populates="users")

    fl_projects_created = relationship("FLProject", back_populates="creator")

    audit_logs = relationship("AuditLog", back_populates="user")
