import os
import pytest
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core import config as cfg
from app.core import database as db_mod
import app.models
from app.db.init_db import init_db

Base = db_mod.Base


# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def row_exists(session: Session, table: str, condition: str, params=None) -> bool:
    params = params or {}

    result = session.execute(
        text(f"SELECT 1 FROM {table} WHERE {condition}"),
        params
    ).fetchone()

    return result is not None


def count_rows(session: Session, table: str) -> int:
    result = session.execute(
        text(f"SELECT COUNT(*) FROM {table}")
    )

    return result.scalar_one()


def create_test_database(monkeypatch, db_path, environment="development"):
    """Create an isolated SQLite database for an individual test."""

    monkeypatch.setenv("ENVIRONMENT", environment)
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    monkeypatch.setenv("SECRET_KEY", "a" * 32)

    cfg.clear_settings_cache()
    settings = cfg.get_settings()

    db_mod.reset_engine(settings)

    db_mod.Base.metadata.create_all(bind=db_mod.engine)

    return db_mod.SessionLocal()


def restore_default_test_database():
    """Restore the shared SQLite database configured by conftest.py."""

    db_mod.engine.dispose()

    os.environ["ENVIRONMENT"] = "development"
    os.environ["DATABASE_URL"] = "sqlite:///test.db"
    os.environ["SECRET_KEY"] = "a" * 32
    os.environ["FIRST_SUPERADMIN_PASSWORD"] = "TestSuperPass123!"

    cfg.clear_settings_cache()

    settings = cfg.get_settings()
    cfg.settings = settings

    db_mod.reset_engine(settings)


# --------------------------------------------------
# Development database fixture
# --------------------------------------------------

@pytest.fixture
def fresh_db(tmp_path, monkeypatch):
    db = create_test_database(
        monkeypatch,
        tmp_path / "development.db",
        "development"
    )

    try:
        yield db
    finally:
        db.close()
        restore_default_test_database()


# --------------------------------------------------
# Development initialization tests
# --------------------------------------------------

def test_development_initialization_creates_demo_data(fresh_db):
    init_db(fresh_db)

    admin_email = cfg.get_settings().FIRST_SUPERADMIN_EMAIL

    assert row_exists(
        fresh_db,
        "users",
        "email = :email",
        {"email": admin_email}
    )

    assert row_exists(
        fresh_db,
        "institutions",
        "institution_code = 'HOSP-ALPHA-01'"
    )

    assert row_exists(
        fresh_db,
        "institutions",
        "institution_code = 'HOSP-BETA-02'"
    )

    assert row_exists(
        fresh_db,
        "users",
        "email = 'hospadmin@hospital-alpha.org'"
    )

    assert row_exists(
        fresh_db,
        "users",
        "email = 'researcher@fl-research.org'"
    )

    assert count_rows(fresh_db, "datasets") > 0
    assert count_rows(fresh_db, "fl_projects") > 0


def test_development_initialization_idempotent(fresh_db):
    init_db(fresh_db)

    counts_first = {
        "users": count_rows(fresh_db, "users"),
        "institutions": count_rows(fresh_db, "institutions"),
        "datasets": count_rows(fresh_db, "datasets"),
        "projects": count_rows(fresh_db, "fl_projects"),
    }

    init_db(fresh_db)

    counts_second = {
        "users": count_rows(fresh_db, "users"),
        "institutions": count_rows(fresh_db, "institutions"),
        "datasets": count_rows(fresh_db, "datasets"),
        "projects": count_rows(fresh_db, "fl_projects"),
    }

    assert counts_first == counts_second


# --------------------------------------------------
# Production initialization tests
# --------------------------------------------------

def test_production_no_demo_data(monkeypatch, tmp_path):
    monkeypatch.setenv("PROVISION_SUPERADMIN", "false")

    db = create_test_database(
        monkeypatch,
        tmp_path / "production.db",
        "production"
    )

    called = {"create_all": False}

    def fake_create_all(*args, **kwargs):
        called["create_all"] = True
        raise RuntimeError(
            "create_all should not be called in production"
        )

    monkeypatch.setattr(
        Base.metadata,
        "create_all",
        fake_create_all
    )

    try:
        init_db(db)

        admin_email = cfg.get_settings().FIRST_SUPERADMIN_EMAIL

        assert not row_exists(
            db,
            "users",
            "email = :email",
            {"email": admin_email}
        )

        assert count_rows(db, "institutions") == 0
        assert not called["create_all"]

    finally:
        db.close()
        restore_default_test_database()


def test_production_provision_superadmin(monkeypatch, tmp_path):
    monkeypatch.setenv("PROVISION_SUPERADMIN", "true")
    monkeypatch.setenv(
        "FIRST_SUPERADMIN_PASSWORD",
        "ProdSuperPass123!"
    )

    db = create_test_database(
        monkeypatch,
        tmp_path / "production_admin.db",
        "production"
    )

    monkeypatch.setattr(
        Base.metadata,
        "create_all",
        lambda *args, **kwargs: (
            _ for _ in ()
        ).throw(RuntimeError("Production must not create tables"))
    )

    try:
        init_db(db)

        admin_email = cfg.get_settings().FIRST_SUPERADMIN_EMAIL

        assert row_exists(
            db,
            "users",
            "email = :email",
            {"email": admin_email}
        )

        from app.core.security import verify_password

        result = db.execute(
            text(
                "SELECT password_hash FROM users "
                "WHERE email = :email"
            ),
            {"email": admin_email}
        ).fetchone()

        assert result is not None
        assert verify_password("ProdSuperPass123!", result[0])

    finally:
        db.close()
        restore_default_test_database()


def test_production_superadmin_not_overwritten(monkeypatch, tmp_path):
    monkeypatch.setenv("PROVISION_SUPERADMIN", "true")
    monkeypatch.setenv(
        "FIRST_SUPERADMIN_PASSWORD",
        "InitialPass123!"
    )

    db = create_test_database(
        monkeypatch,
        tmp_path / "production_existing_admin.db",
        "production"
    )

    try:
        init_db(db)

        admin_email = cfg.get_settings().FIRST_SUPERADMIN_EMAIL

        monkeypatch.setenv(
            "FIRST_SUPERADMIN_PASSWORD",
            "NewPassShouldNotOverwrite"
        )

        cfg.clear_settings_cache()

        init_db(db)

        from app.core.security import verify_password

        result = db.execute(
            text(
                "SELECT password_hash FROM users "
                "WHERE email = :email"
            ),
            {"email": admin_email}
        ).fetchone()

        assert result is not None
        assert verify_password("InitialPass123!", result[0])
        assert not verify_password(
            "NewPassShouldNotOverwrite",
            result[0]
        )

    finally:
        db.close()
        restore_default_test_database()