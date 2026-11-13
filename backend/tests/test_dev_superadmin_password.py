import pytest
from pydantic import ValidationError
from app.core.config import Settings

def test_development_password_default(monkeypatch):
    # Ensure no env overrides for superadmin password or environment
    monkeypatch.delenv('ENVIRONMENT', raising=False)
    monkeypatch.delenv('FIRST_SUPERADMIN_PASSWORD', raising=False)
    s = Settings(_env_file=None)
    assert s.FIRST_SUPERADMIN_PASSWORD == "DevSuperAdminPass123!"
    assert s.ENVIRONMENT == "development"

def test_production_no_dev_fallback(monkeypatch):
    # Production environment without provisioning should not get dev fallback
    monkeypatch.setenv('ENVIRONMENT', 'production')
    monkeypatch.delenv('FIRST_SUPERADMIN_PASSWORD', raising=False)
    monkeypatch.setenv('SECRET_KEY', 'a' * 32)
    monkeypatch.setenv('PROVISION_SUPERADMIN', 'false')
    monkeypatch.setenv('DATABASE_URL', 'postgresql://user:pwd@localhost:5432/testdb')
    monkeypatch.setenv('BACKEND_CORS_ORIGINS', 'https://test.example.com')
    s = Settings(_env_file=None)
    assert s.FIRST_SUPERADMIN_PASSWORD is None
    assert s.PROVISION_SUPERADMIN is False
