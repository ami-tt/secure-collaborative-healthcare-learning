import enum

from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, UniqueConstraint

from sqlalchemy.orm import relationship

from app.core.database import Base

from app.models.base import BaseModelMixin





class ClientStatus(str, enum.Enum):

    REGISTERED = "registered"

    CONNECTED = "connected"

    TRAINING = "training"

    SUBMITTING = "submitting"

    IDLE = "idle"

    DISCONNECTED = "disconnected"

    ERROR = "error"





class FLSessionParticipant(Base, BaseModelMixin):

    """

    Tracks hospital edge clients registered in a given FL session.

    """

    __tablename__ = "fl_session_participants"



    session_id = Column(String(36), ForeignKey("fl_sessions.id", ondelete="CASCADE"), nullable=False, index=True)

    institution_id = Column(String(36), ForeignKey("institutions.id", ondelete="CASCADE"), nullable=False, index=True)

    client_status = Column(

        Enum(ClientStatus, values_callable=lambda x: [e.value for e in x]),

        default=ClientStatus.REGISTERED,

        nullable=False

    )

    local_dataset_id = Column(String(36), ForeignKey("datasets.id", ondelete="SET NULL"), nullable=True)

    last_heartbeat = Column(DateTime(timezone=True), nullable=True)

    registered_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)



    __table_args__ = (

        UniqueConstraint("session_id", "institution_id", name="uq_session_institution"),

    )



    # Relationships

    session = relationship("FLSession", back_populates="participants")

    institution = relationship("Institution", back_populates="participations")
