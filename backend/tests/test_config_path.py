import pytest
from pathlib import Path
from app.core import config

def test_default_env_path_points_to_backend_env():
    # The DEFAULT_ENV_PATH should resolve to the project-root/backend/.env relative to this config file.
    config_path = Path(config.__file__).resolve()
    expected = config_path.parents[2] / ".env"
    assert config.Settings.DEFAULT_ENV_PATH == expected
