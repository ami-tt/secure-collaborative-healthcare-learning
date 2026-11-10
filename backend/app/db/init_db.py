import secrets

from sqlalchemy.orm import Session

from app.core.config import settings

from app.core.database import Base, engine, SessionLocal

from app.core.security import get_password_hash

from app.models.institution import Institution, InstitutionStatus

from app.models.user import User, UserRole

from app.models.dataset import Dataset, DatasetModality

from app.models.fl_project import FLProject

from app.services.audit_service import AuditService





def init_db(db: Session) -> None:

    """

    Initialize database tables and seed baseline records (Admin, Sample Hospitals, Researchers).

    """

    # Create all tables defined in models

    Base.metadata.create_all(bind=engine)



    # 1. Seed Initial Super Admin

    superadmin = db.query(User).filter(User.email == settings.FIRST_SUPERADMIN_EMAIL).first()

    if not superadmin:

        superadmin = User(

            email=settings.FIRST_SUPERADMIN_EMAIL,

            password_hash=get_password_hash(settings.FIRST_SUPERADMIN_PASSWORD),

            full_name=settings.FIRST_SUPERADMIN_NAME,

            role=UserRole.ADMIN,

            is_active=True,

            is_verified=True

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

            status="SUCCESS"

        )



    # 2. Seed Sample Partner Institutions

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

            status=InstitutionStatus.ACTIVE

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

            status=InstitutionStatus.ACTIVE

        )

        db.add(hosp_beta)

        db.commit()

        db.refresh(hosp_beta)



    # 3. Seed Hospital Administrator for Hospital Alpha

    hosp_admin = db.query(User).filter(User.email == "hospadmin@hospital-alpha.org").first()

    if not hosp_admin:

        hosp_admin = User(

            email="hospadmin@hospital-alpha.org",

            password_hash=get_password_hash("HospAdmin123!"),

            full_name="Dr. Marcus Vance (Hospital Alpha)",

            role=UserRole.HOSPITAL_ADMIN,

            institution_id=hosp_alpha.id,

            is_active=True,

            is_verified=True

        )

        db.add(hosp_admin)

        db.commit()



    # 4. Seed Clinical Researcher

    researcher = db.query(User).filter(User.email == "researcher@fl-research.org").first()

    if not researcher:

        researcher = User(

            email="researcher@fl-research.org",

            password_hash=get_password_hash("Researcher123!"),

            full_name="Dr. Elena Rostova",

            role=UserRole.RESEARCHER,

            institution_id=None,

            is_active=True,

            is_verified=True

        )

        db.add(researcher)

        db.commit()

        db.refresh(researcher)



    # 5. Seed Baseline EHR Dataset Schema for Hospital Alpha

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

                "target_type": "binary"

            },

            is_validated=True,

            privacy_budget_spent=0.0

        )

        db.add(alpha_dataset)

        db.commit()



    # 6. Seed Baseline Clinical FL Project

    project = db.query(FLProject).filter(FLProject.title == "Federated Cardiovascular Risk Prediction").first()

    if not project:

        project = FLProject(

            title="Federated Cardiovascular Risk Prediction",

            description="Collaborative predictive modeling of 5-year cardiovascular event risk across hospital inpatient cohorts without raw EHR exchange.",

            target_condition="Cardiovascular Risk",

            model_architecture="TabularMLP",

            modality=DatasetModality.TABULAR_EHR,

            created_by=researcher.id

        )

        db.add(project)

        db.commit()





if __name__ == "__main__":

    db = SessionLocal()

    try:

        init_db(db)

        print("Database initialized and seeded successfully.")

    finally:

        db.close()
