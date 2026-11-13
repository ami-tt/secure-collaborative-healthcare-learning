import pytest
import os
from app.core.config import Settings, clear_settings_cache
from pydantic import ValidationError

@pytest.fixture(autouse=True)
def clear_env(monkeypatch):
    # Remove any settings-related env vars before each test
    for var in ["ENVIRONMENT", "DEBUG", "SECRET_KEY", "DATABASE_URL", "BACKEND_CORS_ORIGINS", "PROVISION_SUPERADMIN", "FIRST_SUPERADMIN_PASSWORD"]:
        monkeypatch.delenv(var, raising=False)
    yield

def test_cors_wildcard_not_allowed_in_production(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("SECRET_KEY", "a"*32)
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@host/db")
    monkeypatch.setenv("BACKEND_CORS_ORIGINS", "*")
    with pytest.raises(ValueError, match="Wildcard '\*' is not allowed"):
        clear_settings_cache()
        Settings(_env_file=None)

def test_cors_http_non_localhost_not_allowed(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("SECRET_KEY", "b"*32)
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@host/db")
    monkeypatch.setenv("BACKEND_CORS_ORIGINS", "http://example.com")
    with pytest.raises(ValueError, match="HTTP origin .* is only allowed for localhost"):
        clear_settings_cache()
        Settings(_env_file=None)

def test_cors_https_with_path_not_allowed(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("SECRET_KEY", "c"*32)
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@host/db")
    monkeypatch.setenv("BACKEND_CORS_ORIGINS", "https://example.com/somepath")
    with pytest.raises(ValueError, match="must not contain a path"):
        clear_settings_cache()
        Settings(_env_file=None)

def test_cors_https_with_query_not_allowed(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("SECRET_KEY", "d"*32)
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@host/db")
    monkeypatch.setenv("BACKEND_CORS_ORIGINS", "https://example.com?query=1")
    with pytest.raises(ValueError, match="must not contain query"):
        clear_settings_cache()
        Settings(_env_file=None)

def test_cors_https_with_credentials_not_allowed(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("SECRET_KEY", "e"*32)
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@host/db")
    # user:pass@ in URL
    monkeypatch.setenv("BACKEND_CORS_ORIGINS", "https://user:pass@example.com")
    with pytest.raises(ValueError, match="must not contain credentials"):
        clear_settings_cache()
        Settings(_env_file=None)

def test_cors_valid_https_origin_allowed(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("SECRET_KEY", "f"*32)
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@host/db")
    monkeypatch.setenv("BACKEND_CORS_ORIGINS", "https://example.com")
    s = Settings()
    assert "https://example.com" in s.BACKEND_CORS_ORIGINS

def test_database_sqlite_not_allowed_in_production(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("SECRET_KEY", "g"*32)
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./test.db")
    monkeypatch.setenv("BACKEND_CORS_ORIGINS", "https://example.com")
    with pytest.raises(ValidationError, match="must be a PostgreSQL URL"):
        clear_settings_cache()
        Settings(_env_file=None)

def test_database_postgres_allowed_in_production(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("SECRET_KEY", "h"*32)
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@host/db")
    monkeypatch.setenv("BACKEND_CORS_ORIGINS", "https://example.com")
    s = Settings()
    assert s.DATABASE_URL.startswith("postgresql://")
