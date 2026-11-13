import os
import sys
import importlib
from pathlib import Path

# Regular tests always use SQLite.
os.environ["ENVIRONMENT"] = "development"
os.environ["DATABASE_URL"] = "sqlite:///test.db"
os.environ["FIRST_SUPERADMIN_PASSWORD"] = "TestSuperPass123!"

# Add backend directory to Python path.
BACKEND_ROOT = Path(__file__).resolve().parents[1]

if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

# Configure application settings.
from app.core import config
from app.core import database

config.clear_settings_cache()
settings = config.get_settings()
config.settings = settings

# Configure the application database.
database.reset_engine(settings)

# Register all application models.
import app.models

# Start with a clean test database.
database.Base.metadata.drop_all(bind=database.engine)
database.Base.metadata.create_all(bind=database.engine)

# Seed development data.
from app.db.init_db import init_db

_db = database.SessionLocal()

try:
    init_db(_db)
finally:
    _db.close()

# Reload application after database configuration.
import app.main

importlib.reload(app.main)

import pytest


@pytest.fixture
def client():
    from fastapi.testclient import TestClient

    with TestClient(app.main.app) as test_client:
        yield test_client