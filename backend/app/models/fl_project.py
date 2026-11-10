from sqlalchemy import Column, String, Text, ForeignKey, Enum

from sqlalchemy.orm import relationship

from app.core.database import Base

from app.models.base import BaseModelMixin

from app.models.dataset import DatasetModality





class FLProject(Base, BaseModelMixin):

    """

    Defines a collaborative clinical research initiative.

    """

    __tablename__ = "fl_projects"



    title = Column(String(255), nullable=False)

    description = Column(Text, nullable=True)

    target_condition = Column(String(255), nullable=False)

    model_architecture = Column(String(100), nullable=False, default="TabularMLP")

    modality = Column(

        Enum(DatasetModality, values_callable=lambda x: [e.value for e in x]),

        default=DatasetModality.TABULAR_EHR,

        nullable=False

    )

    created_by = Column(String(36), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)



    # Relationships

    creator = relationship("User", back_populates="fl_projects_created")

    sessions = relationship("FLSession", back_populates="project", cascade="all, delete-orphan")
