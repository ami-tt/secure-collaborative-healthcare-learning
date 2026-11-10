from sqlalchemy import Column, String, Integer, BigInteger, Boolean, JSON, ForeignKey

from sqlalchemy.orm import relationship

from app.core.database import Base

from app.models.base import BaseModelMixin





class ModelCheckpoint(Base, BaseModelMixin):

    """

    Metadata for global PyTorch model weights serialized after each training round.

    """

    __tablename__ = "model_checkpoints"



    session_id = Column(String(36), ForeignKey("fl_sessions.id", ondelete="CASCADE"), nullable=False, index=True)

    round_number = Column(Integer, nullable=False)

    file_path = Column(String(500), nullable=False)

    file_size_bytes = Column(BigInteger, default=0, nullable=False)

    sha256_checksum = Column(String(64), nullable=False)

    is_best_model = Column(Boolean, default=False, nullable=False)

    metrics_summary = Column(JSON, default=dict, nullable=False)



    # Relationships

    session = relationship("FLSession", back_populates="checkpoints")
