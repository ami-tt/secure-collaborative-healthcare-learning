import pytest
from app.core.config import Settings
from pathlib import Path

def test_backend_env_loaded(tmp_path, monkeypatch):
    """Ensure Settings can load a custom .env file.

    The test creates a temporary .env with harmless values and
    verifies that Settings reads them correctly via the `SETTINGS_ENV_FILE`
    environment variable. This avoids reliance on the real project `.env`
    and ensures deterministic behavior.
    """
    # Prepare a temporary .env file
    env_content = """ENVIRONMENT=test\nFIRST_SUPERADMIN_PASSWORD=TemporaryTestPassword123!\n"""
    env_file = tmp_path / ".env"
    env_file.write_text(env_content)

    # Ensure no environment variables interfere
    monkeypatch.delenv('ENVIRONMENT', raising=False)
    monkeypatch.delenv('FIRST_SUPERADMIN_PASSWORD', raising=False)

    # Instantiate Settings with the temporary .env explicitly
    settings = Settings(_env_file=str(env_file))

    assert settings.ENVIRONMENT == "test"
    assert settings.FIRST_SUPERADMIN_PASSWORD == "TemporaryTestPassword123!"
