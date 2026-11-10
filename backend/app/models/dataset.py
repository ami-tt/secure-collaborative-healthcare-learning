import enum

from sqlalchemy import Column, String, Integer, Float, Boolean, JSON, ForeignKey, Enum

from sqlalchemy.orm import relationship

from app.core.database import Base

from app.models.base import BaseModelMixin





class DatasetModality(str, enum.Enum):

    TABULAR_EHR = "tabular_ehr"

    MEDICAL_IMAGING = "medical_imaging"

    CLINICAL_NOTES_NLP = "clinical_notes_nlp"





class Dataset(Base, BaseModelMixin):

    """

    Metadata representation of hospital-held datasets.

    Raw patient records stay strictly within hospital firewalls.

    """

    __tablename__ = "datasets"



    institution_id = Column(String(36), ForeignKey("institutions.id", ondelete="CASCADE"), nullable=False, index=True)

    name = Column(String(255), nullable=False)

    modality = Column(

        Enum(DatasetModality, values_callable=lambda x: [e.value for e in x]),

        default=DatasetModality.TABULAR_EHR,

        nullable=False

    )

    sample_count = Column(Integer, default=0, nullable=False)

    feature_schema = Column(JSON, default=dict, nullable=False)

    is_validated = Column(Boolean, default=False, nullable=False)

    privacy_budget_spent = Column(Float, default=0.0, nullable=False)



    # Relationships

    institution = relationship("Institution", back_populates="datasets")
