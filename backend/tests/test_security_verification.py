import os

import sys

import uuid

from datetime import timedelta

import pytest

from fastapi.testclient import TestClient

from jose import jwt



# Ensure backend root is on Python path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))



from app.main import app

from app.core.config import settings

from app.core.database import SessionLocal

from app.core.security import create_access_token

from app.models.user import User, UserRole

from app.models.institution import Institution



client = TestClient(app)





def test_sql_injection_resilience():

    """Verify that SQL injection strings in login parameters are safely handled."""

    sql_injection_payloads = [

        "' OR '1'='1",

        "admin@securefl.health' --",

        "' UNION SELECT * FROM users --",

        "'; DROP TABLE users; --"

    ]

    for injection in sql_injection_payloads:

        res = client.post("/api/v1/auth/login", json={

            "email": injection,

            "password": "random_password"

        })

        # Should be rejected with 422 (email validation) or 401 (invalid credentials), never 500

        assert res.status_code in [401, 422], f"Failed on payload: {injection}"





def test_tampered_and_invalid_jwt_rejection():

    """Verify that forged, tampered, or improperly signed JWT tokens are rejected."""

    # 1. Token signed with wrong secret key

    forged_token = jwt.encode(

        {"sub": "fake-admin-id", "role": "admin"},

        "wrong-secret-key-12345",

        algorithm="HS256"

    )

    headers = {"Authorization": f"Bearer {forged_token}"}

    res_forged = client.get("/api/v1/users/", headers=headers)

    assert res_forged.status_code == 401

    assert "Invalid or expired authentication token" in res_forged.json()["detail"]



    # 2. Expired token

    expired_token = create_access_token(

        subject="fake-user-id",

        role="admin",

        expires_delta=timedelta(seconds=-10)

    )

    headers_exp = {"Authorization": f"Bearer {expired_token}"}

    res_exp = client.get("/api/v1/users/", headers=headers_exp)

    assert res_exp.status_code == 401



    # 3. Malformed garbage token

    headers_bad = {"Authorization": "Bearer not.a.valid.jwt"}

    res_bad = client.get("/api/v1/users/", headers=headers_bad)

    assert res_bad.status_code == 401





def test_privilege_escalation_prevented():

    """Verify that regular researchers cannot escalate privileges to Admin via user update API."""

    # Register researcher

    uid = uuid.uuid4().hex[:6]

    res_creds = {

        "email": f"hacker.test.{uid}@research.org",

        "password": "Password123!",

        "full_name": "Test User",

        "role": "researcher"

    }

    reg_res = client.post("/api/v1/auth/register", json=res_creds)

    assert reg_res.status_code == 201

    user_id = reg_res.json()["id"]



    # Login

    login_res = client.post("/api/v1/auth/login", json={

        "email": res_creds["email"],

        "password": res_creds["password"]

    })

    token = login_res.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}



    # Attempt to escalate role to 'admin'

    escalate_res = client.patch(

        f"/api/v1/users/{user_id}",

        json={"role": "admin"},

        headers=headers

    )

    # Must be rejected with 403 Forbidden

    assert escalate_res.status_code == 403

    assert "Administrative privileges are required" in escalate_res.json()["detail"]





def test_cross_institution_data_isolation():

    """Verify Hospital Admin cannot register dataset schema for another institution."""

    db = SessionLocal()

    hosp_beta = db.query(Institution).filter(Institution.institution_code == "HOSP-BETA-02").first()

    db.close()

    assert hosp_beta is not None



    # Login as Hospital Admin of Hospital Alpha

    alpha_login = client.post("/api/v1/auth/login", json={

        "email": "hospadmin@hospital-alpha.org",

        "password": "HospAdmin123!"

    }).json()

    alpha_headers = {"Authorization": f"Bearer {alpha_login['access_token']}"}



    # Attempt to register dataset for Hospital Beta

    tamper_payload = {

        "institution_id": hosp_beta.id,

        "name": "Tampered Beta Records",

        "modality": "tabular_ehr",

        "sample_count": 500,

        "feature_schema": {"features": ["age"]}

    }

    res = client.post("/api/v1/datasets/", json=tamper_payload, headers=alpha_headers)

    assert res.status_code == 403

    assert "affiliated institution" in res.json()["detail"]





def test_deactivated_account_blocked():

    """Verify that deactivated users are blocked from both login and protected API calls."""

    db = SessionLocal()

    uid = uuid.uuid4().hex[:6]

    test_user = User(

        email=f"deactivated.{uid}@hospital.org",

        password_hash="$2b$12$somehashforsecuritytestsonly0000000000000000000000000",

        full_name="Deactivated User",

        role=UserRole.RESEARCHER,

        is_active=False

    )

    db.add(test_user)

    db.commit()

    db.refresh(test_user)

    user_id = test_user.id

    db.close()



    # Create token for this user

    token = create_access_token(subject=user_id, role="researcher")

    headers = {"Authorization": f"Bearer {token}"}



    # Calling protected endpoint with token of deactivated user must yield 403

    res = client.get("/api/v1/auth/me", headers=headers)

    assert res.status_code == 403

    assert "deactivated" in res.json()["detail"]





def test_strict_pydantic_input_validation():

    """Verify input validation handles invalid email and short password properly."""

    # 1. Invalid email

    res1 = client.post("/api/v1/auth/register", json={

        "email": "not-an-email",

        "password": "ValidPassword123!",

        "full_name": "Test",

        "role": "researcher"

    })

    assert res1.status_code == 422



    # 2. Password too short (<8 chars for register)

    res2 = client.post("/api/v1/auth/register", json={

        "email": "valid@email.com",

        "password": "short",

        "full_name": "Test",

        "role": "researcher"

    })

    assert res2.status_code == 422



    # 3. Invalid role enum

    res3 = client.post("/api/v1/auth/register", json={

        "email": "valid2@email.com",

        "password": "ValidPassword123!",

        "full_name": "Test",

        "role": "super_hacker_role"

    })

    assert res3.status_code == 422
