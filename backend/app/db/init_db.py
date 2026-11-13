"""Database initialization and seeding utilities.

- In **development** (or any non‑production environment) the function creates the
  tables via ``Base.metadata.create_all`` and populates a set of demo records.
- In **production** the function never creates tables (migrations are expected to
  handle schema changes). It only provisions the super‑admin user if
  ``PROVISION_SUPERADMIN`` is true. All demo data is omitted.
- The implementation is idempotent: repeated calls never duplicate records.
"""

import os
import importlib
import sys
import secrets
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, ProgrammingError

from app.core.config import get_settings
from app.core import database
from app.core.security import get_password_hash
from app.models.base import generate_uuid


# Backward‑compatibility alias for tests expecting ``init_db.Base``
Base = database.Base

# Import models so that ``Base.metadata`` knows about all tables.
# ``models_pkg`` is used only for reloading in test environments where the
# metadata may have been cleared.
# Import model package to register all models.
from app import models as models_pkg
# Individual model imports are avoided to prevent duplicate registrations.

from app.models.dataset import Dataset, DatasetModality
from app.models.fl_project import FLProject
from app.models.institution import Institution, InstitutionStatus
from app.models.user import User, UserRole
from app.services.audit_service import AuditService


def _create_superadmin(db: Session) -> None:
    """Create the superadmin using the existing database schema."""

    cfg = get_settings()

    if cfg.ENVIRONMENT == "production":
        try:
            existing = (
                db.query(User)
                .filter(User.email == cfg.FIRST_SUPERADMIN_EMAIL)
                .first()
            )
        except (OperationalError, ProgrammingError) as exc:
            raise RuntimeError(
                "Database schema is not initialized. "
                "Run Alembic migrations before provisioning the superadmin."
            ) from exc

        if existing:
            return

        superadmin = User(
            email=cfg.FIRST_SUPERADMIN_EMAIL,
            password_hash=get_password_hash(cfg.FIRST_SUPERADMIN_PASSWORD),
            full_name=cfg.FIRST_SUPERADMIN_NAME,
            role=UserRole.ADMIN,
            is_active=True,
            is_verified=True,
        )

        db.add(superadmin)
        db.commit()
        db.refresh(superadmin)
        return

    # Development environment
    superadmin = (
        db.query(User)
        .filter(User.email == cfg.FIRST_SUPERADMIN_EMAIL)
        .first()
    )

    if not superadmin:
        superadmin = User(
            email=cfg.FIRST_SUPERADMIN_EMAIL,
            password_hash=get_password_hash(cfg.FIRST_SUPERADMIN_PASSWORD),
            full_name=cfg.FIRST_SUPERADMIN_NAME,
            role=UserRole.ADMIN,
            is_active=True,
            is_verified=True,
        )

        db.add(superadmin)
        db.commit()
        db.refresh(superadmin)

        AuditService.log(
            db,
            action="SYSTEM_INIT_SUPERADMIN_CREATED",
            resource_type="USER",
            resource_id=superadmin.id,
            user_id=superadmin.id,
            details={"email": superadmin.email, "role": superadmin.role.value},
            status="SUCCESS",
        )
    # No audit logging in production test path – tables may not exist.



def _seed_development_data(db: Session) -> None:
    """Seed all demo entities for development environments.

    The function is safe to call repeatedly – each lookup uses ``first()`` and
    only inserts when the record is missing.
    """
    # Ensure tables exist before seeding (defensive for test environments)
    engine = db.get_bind() if hasattr(db, "get_bind") else database.engine
    database.Base.metadata.create_all(bind=engine)
    # Ensure super‑admin exists (and sync password if needed)
    _create_superadmin(db)

    # Sample partner institutions
    hosp_alpha = db.query(Institution).filter(Institution.institution_code == "HOSP-ALPHA-01").first()
    if not hosp_alpha:
        raw_key_alpha = f"fl_inst_{secrets.token_urlsafe(32)}"
        hosp_alpha = Institution(
            name="Alpha Health Cardiology Center",
            institution_code="HOSP-ALPHA-01",
            contact_email="admin@hospital-alpha.org",
            phone="+1-555-010-0001",
            address="101 Heart & Vascular Way, Suite 100",
            api_key_hash=get_password_hash(raw_key_alpha),
            status=InstitutionStatus.ACTIVE,
        )
        db.add(hosp_alpha)
        db.commit()
        db.refresh(hosp_alpha)

    hosp_beta = db.query(Institution).filter(Institution.institution_code == "HOSP-BETA-02").first()
    if not hosp_beta:
        raw_key_beta = f"fl_inst_{secrets.token_urlsafe(32)}"
        hosp_beta = Institution(
            name="Beta Memorial Clinical Institute",
            institution_code="HOSP-BETA-02",
            contact_email="admin@hospital-beta.org",
            phone="+1-555-010-0002",
            address="202 Clinical Research Blvd",
            api_key_hash=get_password_hash(raw_key_beta),
            status=InstitutionStatus.ACTIVE,
        )
        db.add(hosp_beta)
        db.commit()
        db.refresh(hosp_beta)

    # Hospital administrator for Alpha
    hosp_admin = db.query(User).filter(User.email == "hospadmin@hospital-alpha.org").first()
    if not hosp_admin:
        hosp_admin = User(
            email="hospadmin@hospital-alpha.org",
            password_hash=get_password_hash("HospAdmin123!"),
            full_name="Dr. Marcus Vance (Hospital Alpha)",
            role=UserRole.HOSPITAL_ADMIN,
            institution_id=hosp_alpha.id,
            is_active=True,
            is_verified=True,
        )
        db.add(hosp_admin)
        db.commit()
        db.refresh(hosp_admin)

    # Clinical researcher
    researcher = db.query(User).filter(User.email == "researcher@fl-research.org").first()
    if not researcher:
        researcher = User(
            email="researcher@fl-research.org",
            password_hash=get_password_hash("Researcher123!"),
            full_name="Dr. Elena Rostova",
            role=UserRole.RESEARCHER,
            institution_id=None,
            is_active=True,
            is_verified=True,
        )
        db.add(researcher)
        db.commit()
        db.refresh(researcher)

    # Baseline EHR dataset for Alpha
    alpha_dataset = db.query(Dataset).filter(Dataset.institution_id == hosp_alpha.id).first()
    if not alpha_dataset:
        alpha_dataset = Dataset(
            institution_id=hosp_alpha.id,
            name="Cardiovascular Inpatient Cohort A",
            modality=DatasetModality.TABULAR_EHR,
            sample_count=1200,
            feature_schema={
                "features": ["age", "bmi", "systolic_bp", "diastolic_bp", "fasting_glucose", "cholesterol", "smoker"],
                "target": "cardiovascular_event_risk",
                "target_type": "binary",
            },
            is_validated=True,
            privacy_budget_spent=0.0,
        )
        db.add(alpha_dataset)
        db.commit()
        db.refresh(alpha_dataset)

    # Baseline FL project
    project = db.query(FLProject).filter(FLProject.title == "Federated Cardiovascular Risk Prediction").first()
    if not project:
        project = FLProject(
            title="Federated Cardiovascular Risk Prediction",
            description="Collaborative predictive modeling of 5-year cardiovascular event risk across hospital inpatient cohorts without raw EHR exchange.",
            target_condition="Cardiovascular Risk",
            model_architecture="TabularMLP",
            modality=DatasetModality.TABULAR_EHR,
            created_by=researcher.id,
        )
        db.add(project)
        db.commit()
        db.refresh(project)


def init_db(db: Session) -> None:
    """Initialize the database.

    Development: create tables and seed demo data.
    Production: never create tables; optionally provision superadmin.
    """

    env = os.getenv("ENVIRONMENT", "development")

    if env != "production":
        engine = db.get_bind()
        database.Base.metadata.create_all(bind=engine)
        _seed_development_data(db)

    else:
        cfg = get_settings()

        if cfg.PROVISION_SUPERADMIN:
            _create_superadmin(db)
