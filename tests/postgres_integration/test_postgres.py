import os

import pytest

from fastapi.testclient import TestClient



# Try to import the testcontainers PostgreSQL helper. If unavailable, mark the whole module as skipped.

try:

    from testcontainers.postgres import PostgresContainer

    _HAS_DOCKER = True

except Exception:  # pragma: no cover

    _HAS_DOCKER = False



if not _HAS_DOCKER:

    pytestmark = pytest.mark.skip(reason="Docker / testcontainers not available – PostgreSQL integration tests are pending.")



# ---------------------------------------------------------------------------

# Fixtures

# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")

def postgres_url():

    """Start a temporary PostgreSQL container and expose its connection URL.

    The container is automatically stopped when the fixture goes out of scope.

    """

    with PostgresContainer("postgres:15-alpine") as pg:

        url = pg.get_connection_url()

        # Export the URL so the FastAPI app picks it up via Settings(DATABASE_URL)

        os.environ["DATABASE_URL"] = url

        yield url



@pytest.fixture(scope="session")

def client(postgres_url):

    """Create a FastAPI TestClient that uses the temporary DB.

    The backend imports Settings at import time, so we must set the env var

    before importing the app.

    """

    # Import the app **after** the env var is set.

    from backend.app.main import app

    return TestClient(app)



# ---------------------------------------------------------------------------

# Alembic migration test

# ---------------------------------------------------------------------------

def test_alembic_migration(postgres_url):

    """Run Alembic ``upgrade head`` against the temporary PostgreSQL instance.

    Verify that at least one table was created.

    """

    from alembic import command as alembic_command

    from alembic.config import Config as AlembicConfig



    cfg = AlembicConfig("alembic.ini")

    cfg.set_main_option("sqlalchemy.url", postgres_url)

    # Apply all migrations

    alembic_command.upgrade(cfg, "head")



    # Simple sanity check – query information_schema for any tables in the public schema.

    from sqlalchemy import create_engine, text

    engine = create_engine(postgres_url)

    with engine.connect() as conn:

        result = conn.execute(text("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public'"))

        count = result.scalar()

        assert count > 0, "No tables were created by Alembic migration"



# ---------------------------------------------------------------------------

# API integration tests (authentication, RBAC, dataset, audit)

# ---------------------------------------------------------------------------

def test_user_registration_and_authentication(client):

    """Register a new hospital admin, log in, and access a protected endpoint.

    The endpoints used are the ones already defined in the backend.

    """

    # 1. Register a user (the route exists at /api/v1/auth/register)

    register_payload = {

        "email": "hospital_admin@test.org",

        "password": "StrongPass!23",

        "full_name": "Test Admin",

        "role": "hospital_admin",

    }

    resp = client.post("/api/v1/auth/register", json=register_payload)

    assert resp.status_code == 201, f"Registration failed: {resp.text}"



    # 2. Log in to obtain JWT

    login_payload = {

        "username": "hospital_admin@test.org",

        "password": "StrongPass!23",

    }

    resp = client.post("/api/v1/auth/login", data=login_payload)

    assert resp.status_code == 200, f"Login failed: {resp.text}"

    token = resp.json().get("access_token")

    assert token, "No access token returned"

    auth_headers = {"Authorization": f"Bearer {token}"}



    # 3. Access a protected endpoint – create a simple dataset metadata entry

    dataset_payload = {

        "name": "test_dataset",

        "description": "Integration test dataset",

    }

    resp = client.post("/api/v1/datasets/", json=dataset_payload, headers=auth_headers)

    assert resp.status_code == 201, f"Dataset creation failed: {resp.text}"

    dataset_id = resp.json().get("id")

    assert dataset_id, "Dataset response missing id"



    # 4. Verify audit log entry was created (the endpoint exists at /api/v1/audit/)

    # The audit endpoint is read‑only; we just fetch the latest entries.

    resp = client.get("/api/v1/audit/", headers=auth_headers)

    assert resp.status_code == 200, f"Audit fetch failed: {resp.text}"

    audit_entries = resp.json()

    # At least one entry should reference the dataset creation action.

    assert any(entry.get("action") == "create_dataset" for entry in audit_entries), "No audit entry for dataset creation"
