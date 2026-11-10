from sqlalchemy import Column, String, Integer, Float, ForeignKey, UniqueConstraint

from sqlalchemy.orm import relationship

from app.core.database import Base

from app.models.base import BaseModelMixin





class FLRoundMetric(Base, BaseModelMixin):

    """

    Global federated learning performance recorded per training round.

    """

    __tablename__ = "fl_round_metrics"



    session_id = Column(String(36), ForeignKey("fl_sessions.id", ondelete="CASCADE"), nullable=False, index=True)

    round_number = Column(Integer, nullable=False)

    global_loss = Column(Float, nullable=False)

    global_accuracy = Column(Float, nullable=False)

    global_auc = Column(Float, nullable=True)

    global_f1_score = Column(Float, nullable=True)

    global_precision = Column(Float, nullable=True)

    global_recall = Column(Float, nullable=True)

    participating_clients_count = Column(Integer, nullable=False)

    round_duration_seconds = Column(Float, nullable=True)



    __table_args__ = (

        UniqueConstraint("session_id", "round_number", name="uq_session_round"),

    )



    # Relationships

    session = relationship("FLSession", back_populates="round_metrics")

    client_metrics = relationship("FLClientRoundMetric", back_populates="round_metric", cascade="all, delete-orphan")





class FLClientRoundMetric(Base, BaseModelMixin):

    """

    Individual hospital client performance reported for a round.

    """

    __tablename__ = "fl_client_round_metrics"



    round_metric_id = Column(String(36), ForeignKey("fl_round_metrics.id", ondelete="CASCADE"), nullable=False, index=True)

    institution_id = Column(String(36), ForeignKey("institutions.id", ondelete="CASCADE"), nullable=False, index=True)

    local_loss = Column(Float, nullable=False)

    local_accuracy = Column(Float, nullable=False)

    local_samples_trained = Column(Integer, nullable=False)

    local_training_duration_seconds = Column(Float, nullable=True)



    # Relationships

    round_metric = relationship("FLRoundMetric", back_populates="client_metrics")

    institution = relationship("Institution")
