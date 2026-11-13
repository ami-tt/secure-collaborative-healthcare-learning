import pytest
from pydantic import ValidationError
from app.core.config import Settings


def test_missing_secret_key(monkeypatch):
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("FIRST_SUPERADMIN_PASSWORD", "StrongPass123!")
    # Provide valid production settings to isolate the missing secret key case
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pwd@localhost:5432/testdb")
    monkeypatch.setenv("BACKEND_CORS_ORIGINS", "https://test.example.com")
    with pytest.raises(ValidationError) as excinfo:
        Settings(_env_file=None)
    assert "SECRET_KEY" in str(excinfo.value)


def test_placeholder_secret_key(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "default-insecure-dev-key-change-me")
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("FIRST_SUPERADMIN_PASSWORD", "StrongPass123!")
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pwd@localhost:5432/testdb")
    monkeypatch.setenv("BACKEND_CORS_ORIGINS", "https://test.example.com")
    with pytest.raises(ValidationError) as excinfo:
        Settings(_env_file=None)
    msg = str(excinfo.value).lower()
    assert "placeholder" in msg or "secret_key" in msg


def test_debug_disabled_in_production(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "a" * 32)
    monkeypatch.setenv("FIRST_SUPERADMIN_PASSWORD", "StrongPass123!")
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pwd@localhost:5432/testdb")
    monkeypatch.setenv("BACKEND_CORS_ORIGINS", "https://test.example.com")
    s = Settings(_env_file=None)
    assert s.DEBUG is False


def test_sqlite_not_allowed_in_production(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "a" * 32)
    monkeypatch.setenv("FIRST_SUPERADMIN_PASSWORD", "StrongPass123!")
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./healthcare_fl.db")
    # CORS still required for validation path
    monkeypatch.setenv("BACKEND_CORS_ORIGINS", "https://test.example.com")
    with pytest.raises(ValidationError) as excinfo:
        Settings(_env_file=None)
    assert "postgresql" in str(excinfo.value).lower()


def test_missing_admin_password_when_provision(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "a" * 32)
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("PROVISION_SUPERADMIN", "true")
    monkeypatch.delenv("FIRST_SUPERADMIN_PASSWORD", raising=False)
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pwd@localhost:5432/testdb")
    monkeypatch.setenv("BACKEND_CORS_ORIGINS", "https://test.example.com")
    with pytest.raises(ValidationError) as excinfo:
        Settings(_env_file=None)
    assert "FIRST_SUPERADMIN_PASSWORD" in str(excinfo.value)


def test_admin_password_ignored_when_not_provision(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "a" * 32)
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("PROVISION_SUPERADMIN", "false")
    monkeypatch.delenv("FIRST_SUPERADMIN_PASSWORD", raising=False)
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pwd@localhost:5432/testdb")
    monkeypatch.setenv("BACKEND_CORS_ORIGINS", "https://test.example.com")
    s = Settings(_env_file=None)
    assert s.PROVISION_SUPERADMIN is False


def test_empty_cors_origins_in_production(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "a" * 32)
    monkeypatch.setenv("FIRST_SUPERADMIN_PASSWORD", "StrongPass123!")
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("BACKEND_CORS_ORIGINS", "")
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pwd@localhost:5432/testdb")
    with pytest.raises(ValidationError) as excinfo:
        Settings(_env_file=None)
    assert "cors" in str(excinfo.value).lower()


def test_wildcard_cors_origins_in_production(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "a" * 32)
    monkeypatch.setenv("FIRST_SUPERADMIN_PASSWORD", "StrongPass123!")
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("BACKEND_CORS_ORIGINS", "*")
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pwd@localhost:5432/testdb")
    with pytest.raises(ValidationError) as excinfo:
        Settings(_env_file=None)
    assert "wildcard" in str(excinfo.value).lower()


def test_valid_production_settings(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "a" * 32)
    monkeypatch.setenv("FIRST_SUPERADMIN_PASSWORD", "StrongPass123!")
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pwd@localhost:5432/dbname")
    monkeypatch.setenv("BACKEND_CORS_ORIGINS", "https://myapp.vercel.app")
    s = Settings(_env_file=None)
    assert s.SECRET_KEY == "a" * 32
    assert s.DEBUG is False
    assert s.DATABASE_URL.startswith("postgresql://")
    assert s.BACKEND_CORS_ORIGINS == ["https://myapp.vercel.app"]


def test_development_defaults(monkeypatch):
    # Remove any production overrides
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("BACKEND_CORS_ORIGINS", raising=False)
    s = Settings(_env_file=None)
    assert s.ENVIRONMENT == "development"
    assert s.DEBUG is True
    assert s.DATABASE_URL.startswith("sqlite")
    assert s.BACKEND_CORS_ORIGINS == ["http://localhost:3000", "http://localhost:5173"]
