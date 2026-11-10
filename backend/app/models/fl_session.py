import enum

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Enum

from sqlalchemy.orm import relationship

from app.core.database import Base

from app.models.base import BaseModelMixin





class SessionStatus(str, enum.Enum):

    CREATED = "created"

    WAITING_FOR_CLIENTS = "waiting_for_clients"

    IN_PROGRESS = "in_progress"

    CONVERGED = "converged"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"





class FLSession(Base, BaseModelMixin):

    """

    Represents an active or completed Federated Training session.

    """

    __tablename__ = "fl_sessions"



    project_id = Column(String(36), ForeignKey("fl_projects.id", ondelete="CASCADE"), nullable=False, index=True)

    session_name = Column(String(255), nullable=False)

    total_rounds = Column(Integer, default=10, nullable=False)

    current_round = Column(Integer, default=0, nullable=False)

    min_participating_clients = Column(Integer, default=2, nullable=False)

    aggregation_strategy = Column(String(50), default="FedAvg", nullable=False)



    # Differential Privacy parameters

    dp_enabled = Column(Boolean, default=True, nullable=False)

    dp_epsilon = Column(Float, default=1.5, nullable=False)

    dp_delta = Column(Float, default=1e-5, nullable=False)

    dp_max_grad_norm = Column(Float, default=1.0, nullable=False)



    # Local training hyperparameters

    learning_rate = Column(Float, default=0.001, nullable=False)

    local_epochs = Column(Integer, default=3, nullable=False)

    batch_size = Column(Integer, default=32, nullable=False)



    status = Column(

        Enum(SessionStatus, values_callable=lambda x: [e.value for e in x]),

        default=SessionStatus.CREATED,

        nullable=False,

        index=True

    )

    started_at = Column(DateTime(timezone=True), nullable=True)

    finished_at = Column(DateTime(timezone=True), nullable=True)



    # Relationships

    project = relationship("FLProject", back_populates="sessions")

    participants = relationship("FLSessionParticipant", back_populates="session", cascade="all, delete-orphan")

    round_metrics = relationship("FLRoundMetric", back_populates="session", cascade="all, delete-orphan")

    checkpoints = relationship("ModelCheckpoint", back_populates="session", cascade="all, delete-orphan")
