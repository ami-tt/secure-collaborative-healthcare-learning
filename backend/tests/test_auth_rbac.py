import os

import sys

import uuid

import pytest

from fastapi.testclient import TestClient



# Ensure backend root is on Python path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))



from app.main import app

from app.core.config import get_settings



# client fixture will be provided by pytest





def test_01_root_and_health(client):

    """Verify service root and health check endpoints."""

    # Test Root

    res_root = client.get("/")

    assert res_root.status_code == 200, res_root.text

    data_root = res_root.json()

    assert data_root["status"] == "online"

    assert "documentation" in data_root



    # Test Health Check

    res_health = client.get("/health")

    assert res_health.status_code == 200, res_health.text

    data_health = res_health.json()

    assert data_health["status"] == "healthy"

    assert data_health["database"] == "healthy"





def test_02_superadmin_login(client):

    """Verify seeded superadmin can authenticate and receive JWT token."""

    login_payload = {

        "email": get_settings().FIRST_SUPERADMIN_EMAIL,

        "password": get_settings().FIRST_SUPERADMIN_PASSWORD

    }

    from app.core.database import SessionLocal
    from app.core.security import verify_password
    from app.models.user import User

    db = SessionLocal()

    test_user = db.query(User).filter(
        User.email == login_payload["email"]
    ).first()

    print("\n--- PYTEST LOGIN DIAGNOSTICS ---")
    print("Email:", login_payload["email"])
    print("Superadmin exists:", test_user is not None)

    if test_user:
        print(
            "Password matches:",
            verify_password(
                login_payload["password"],
                test_user.password_hash
            )
        )

    print("Database URL:", db.get_bind().url)
    db.close()

    response = client.post("/api/v1/auth/login", json=login_payload)

    assert response.status_code == 200, response.text

    data = response.json()

    assert "access_token" in data

    assert data["token_type"] == "bearer"

    assert data["role"] == "admin"

    assert data["email"] == get_settings().FIRST_SUPERADMIN_EMAIL





def test_03_invalid_login(client):

    """Verify that invalid credentials yield 401 Unauthorized."""

    response = client.post("/api/v1/auth/login", json={

        "email": get_settings().FIRST_SUPERADMIN_EMAIL,

        "password": "WrongPassword999!"

    })

    assert response.status_code == 401

    assert "Incorrect email or password" in response.json()["detail"]





def test_04_unauthenticated_request_rejected(client):

    """Verify protected endpoints reject requests without a Bearer token."""

    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401





def test_05_user_registration_and_login(client):

    """Verify new user registration and subsequent authentication with repeatable unique email."""

    uid = uuid.uuid4().hex[:8]

    new_user = {

        "email": f"dr.watson.{uid}@clinical-fl.org",

        "password": "WatsonSecurePassword123!",

        "full_name": f"Dr. John Watson {uid}",

        "role": "researcher"

    }

    # Register

    reg_res = client.post("/api/v1/auth/register", json=new_user)

    assert reg_res.status_code == 201, reg_res.text

    reg_data = reg_res.json()

    assert reg_data["email"] == new_user["email"]

    assert reg_data["role"] == "researcher"

    assert "id" in reg_data



    # Duplicate registration should return 409 Conflict

    dup_res = client.post("/api/v1/auth/register", json=new_user)

    assert dup_res.status_code == 409



    # Login with new credentials

    login_res = client.post("/api/v1/auth/login", json={

        "email": new_user["email"],

        "password": new_user["password"]

    })

    assert login_res.status_code == 200

    token_data = login_res.json()

    assert token_data["role"] == "researcher"



    # Profile lookup

    headers = {"Authorization": f"Bearer {token_data['access_token']}"}

    me_res = client.get("/api/v1/auth/me", headers=headers)

    assert me_res.status_code == 200

    assert me_res.json()["email"] == new_user["email"]





def test_06_rbac_enforcement_admin_endpoints(client):

    """Verify RBAC enforces admin-only restrictions against non-admin roles."""

    # 1. Login as Admin

    admin_login = client.post("/api/v1/auth/login", json={

        "email": get_settings().FIRST_SUPERADMIN_EMAIL,

        "password": get_settings().FIRST_SUPERADMIN_PASSWORD

    }).json()

    admin_headers = {"Authorization": f"Bearer {admin_login['access_token']}"}



    # 2. Login as Researcher

    res_login = client.post("/api/v1/auth/login", json={

        "email": "researcher@fl-research.org",

        "password": "Researcher123!"

    }).json()

    res_headers = {"Authorization": f"Bearer {res_login['access_token']}"}



    # 3. Login as Hospital Admin

    hosp_login = client.post("/api/v1/auth/login", json={

        "email": "hospadmin@hospital-alpha.org",

        "password": "HospAdmin123!"

    }).json()

    hosp_headers = {"Authorization": f"Bearer {hosp_login['access_token']}"}



    # Admin accesses /api/v1/users/ -> Allowed (200)

    users_admin = client.get("/api/v1/users/", headers=admin_headers)

    assert users_admin.status_code == 200

    assert len(users_admin.json()) >= 3



    # Researcher accesses /api/v1/users/ -> Forbidden (403)

    users_res = client.get("/api/v1/users/", headers=res_headers)

    assert users_res.status_code == 403

    assert "Access denied" in users_res.json()["detail"]



    # Hospital Admin accesses /api/v1/users/ -> Forbidden (403)

    users_hosp = client.get("/api/v1/users/", headers=hosp_headers)

    assert users_hosp.status_code == 403



    # Admin accesses /api/v1/audit/ -> Allowed (200)

    audit_admin = client.get("/api/v1/audit/", headers=admin_headers)

    assert audit_admin.status_code == 200

    assert len(audit_admin.json()) > 0



    # Researcher accesses /api/v1/audit/ -> Forbidden (403)

    audit_res = client.get("/api/v1/audit/", headers=res_headers)

    assert audit_res.status_code == 403





def test_07_institution_registration_and_status_update(client):

    """Verify hospital registration and administrative approval flow."""

    admin_login = client.post("/api/v1/auth/login", json={

        "email": get_settings().FIRST_SUPERADMIN_EMAIL,

        "password": get_settings().FIRST_SUPERADMIN_PASSWORD

    }).json()

    admin_headers = {"Authorization": f"Bearer {admin_login['access_token']}"}



    uid = uuid.uuid4().hex[:6].upper()

    new_inst = {

        "name": f"St. Jude Research Lab {uid}",

        "institution_code": f"HOSP-SJ-{uid}",

        "contact_email": f"contact.{uid.lower()}@stjude-research.org",

        "phone": "+1-555-019-3344",

        "address": "333 Health Park Ave"

    }

    create_res = client.post("/api/v1/institutions/", json=new_inst, headers=admin_headers)

    assert create_res.status_code == 201, create_res.text

    inst_data = create_res.json()

    assert inst_data["institution_code"] == new_inst["institution_code"]



    # Admin updates status to active

    patch_res = client.patch(

        f"/api/v1/institutions/{inst_data['id']}/status?new_status=active",

        headers=admin_headers

    )

    assert patch_res.status_code == 200

    assert patch_res.json()["status"] == "active"





def test_08_dataset_metadata_registration(client):

    """Verify Hospital Admin can register dataset metadata for their institution."""

    hosp_login = client.post("/api/v1/auth/login", json={

        "email": "hospadmin@hospital-alpha.org",

        "password": "HospAdmin123!"

    }).json()

    hosp_headers = {"Authorization": f"Bearer {hosp_login['access_token']}"}



    uid = uuid.uuid4().hex[:6]

    dataset_payload = {

        "name": f"Cardiovascular ICU Cohort {uid}",

        "modality": "tabular_ehr",

        "sample_count": 850,

        "feature_schema": {

            "features": ["age", "gender", "troponin_i", "creatinine", "mean_arterial_pressure"],

            "target": "myocardial_infarction_risk"

        }

    }



    create_res = client.post("/api/v1/datasets/", json=dataset_payload, headers=hosp_headers)

    assert create_res.status_code == 201, create_res.text

    ds_data = create_res.json()

    assert ds_data["name"] == dataset_payload["name"]

    assert ds_data["sample_count"] == 850

    assert ds_data["is_validated"] is True





def test_09_researcher_project_and_session_creation(client):

    """Verify Researcher can create FL projects and configure training sessions."""

    res_login = client.post("/api/v1/auth/login", json={

        "email": "researcher@fl-research.org",

        "password": "Researcher123!"

    }).json()

    res_headers = {"Authorization": f"Bearer {res_login['access_token']}"}



    uid = uuid.uuid4().hex[:6]

    # 1. Create Project

    project_payload = {

        "title": f"Collaborative Sepsis Early Detection Study {uid}",

        "description": "Federated model training across ICU EHR data with differential privacy.",

        "target_condition": "Septic Shock",

        "model_architecture": "TabularMLP",

        "modality": "tabular_ehr"

    }

    proj_res = client.post("/api/v1/fl/projects", json=project_payload, headers=res_headers)

    assert proj_res.status_code == 201, proj_res.text

    proj_data = proj_res.json()

    assert proj_data["title"] == project_payload["title"]



    # 2. Configure Session

    session_payload = {

        "project_id": proj_data["id"],

        "session_name": f"Sepsis-FedAvg-Exp-{uid}",

        "total_rounds": 15,

        "min_participating_clients": 2,

        "aggregation_strategy": "FedAvg",

        "dp_enabled": True,

        "dp_epsilon": 1.25,

        "dp_delta": 1e-5,

        "dp_max_grad_norm": 1.0,

        "learning_rate": 0.001,

        "local_epochs": 2,

        "batch_size": 32

    }

    sess_res = client.post("/api/v1/fl/sessions", json=session_payload, headers=res_headers)

    assert sess_res.status_code == 201, sess_res.text

    sess_data = sess_res.json()

    assert sess_data["session_name"] == session_payload["session_name"]

    assert sess_data["total_rounds"] == 15

    assert sess_data["dp_epsilon"] == 1.25

    assert sess_data["status"] == "created"





def test_10_audit_trail_recorded(client):

    """Verify HIPAA audit trail has recorded entries for all sensitive operations."""

    admin_login = client.post("/api/v1/auth/login", json={

        "email": get_settings().FIRST_SUPERADMIN_EMAIL,

        "password": get_settings().FIRST_SUPERADMIN_PASSWORD

    }).json()

    admin_headers = {"Authorization": f"Bearer {admin_login['access_token']}"}



    audit_res = client.get("/api/v1/audit/", headers=admin_headers)

    assert audit_res.status_code == 200

    logs = audit_res.json()

    assert len(logs) >= 5



    actions = [log["action"] for log in logs]

    assert "AUTH_LOGIN_SUCCESS" in actions

    assert "AUTH_REGISTER_SUCCESS" in actions
