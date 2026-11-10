from sqlalchemy import Column, String, Text, Enum

from sqlalchemy.orm import relationship

import enum

from app.core.database import Base

from app.models.base import BaseModelMixin





class InstitutionStatus(str, enum.Enum):

    PENDING_VERIFICATION = "pending_verification"

    ACTIVE = "active"

    SUSPENDED = "suspended"

    DECOMMISSIONED = "decommissioned"





class Institution(Base, BaseModelMixin):

    __tablename__ = "institutions"



    name = Column(String(255), nullable=False)

    institution_code = Column(String(50), unique=True, index=True, nullable=False)

    contact_email = Column(String(255), nullable=False)

    phone = Column(String(50), nullable=True)

    address = Column(Text, nullable=True)

    api_key_hash = Column(String(255), nullable=False)

    status = Column(

        Enum(InstitutionStatus, values_callable=lambda x: [e.value for e in x]),

        default=InstitutionStatus.PENDING_VERIFICATION,

        nullable=False

    )



    # Relationships

    users = relationship("User", back_populates="institution", cascade="all, delete-orphan")

    datasets = relationship("Dataset", back_populates="institution", cascade="all, delete-orphan")

    participations = relationship("FLSessionParticipant", back_populates="institution")
