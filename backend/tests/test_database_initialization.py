import os
import importlib
import pytest
from sqlalchemy.orm import Session

# Helper to reload settings after environment changes

def reload_config():
    from app.core import config as cfg
    cfg.clear_settings_cache()
    return cfg

@pytest.fixture
def isolated_db(tmp_path, monkeypatch):
    """Create an isolated SQLite database for each test."""

    # Configure a fresh SQLite database
    db_path = tmp_path / "test.db"

    monkeypatch.setenv("ENVIRONMENT", "development")
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    monkeypatch.setenv("SECRET_KEY", "a" * 32)
    monkeypatch.setenv("FIRST_SUPERADMIN_PASSWORD", "TestSuperPass123!")

    # Refresh configuration
    from app.core import config, database

    config.clear_settings_cache()
    test_settings = config.get_settings()

    # Reset engine using refreshed settings
    database.reset_engine(test_settings)

    # Register all models
    import app.models

    # IMPORTANT: Get the new engine AFTER reset_engine()
    test_engine = database.engine

    # Create tables on the correct engine
    database.Base.metadata.create_all(bind=test_engine)

    # Create session using the same engine
    session = database.SessionLocal()

    try:
        yield session
    finally:
        session.close()
        test_engine.dispose()
        config.clear_settings_cache()





def test_development_initialization_calls_create_all_and_seed(monkeypatch, isolated_db):
    # Force development environment
    os.environ['ENVIRONMENT'] = 'development'
    cfg = reload_config()

    # Import the init_db module fresh to ensure patched functions are used
    init_mod = importlib.import_module('app.db.init_db')

    # Patch create_all and _seed_development_data to track calls
    create_all_called = {'count': 0}
    def fake_create_all(*args, **kwargs):
        create_all_called['count'] += 1
    monkeypatch.setattr(init_mod.Base.metadata, 'create_all', fake_create_all)

    seed_called = {'count': 0}
    def fake_seed(db: Session):
        seed_called['count'] += 1
    monkeypatch.setattr(init_mod, '_seed_development_data', fake_seed)

    # Run init_db
    init_mod.init_db(isolated_db)

    assert create_all_called['count'] == 1, "Base.metadata.create_all should be called once in development"
    assert seed_called['count'] == 1, "_seed_development_data should be called once in development"


def test_production_never_calls_create_all(monkeypatch, isolated_db):
    os.environ.update({
        'ENVIRONMENT': 'production',
        'PROVISION_SUPERADMIN': 'false',
        'SECRET_KEY': 'a'*32,
    })
    cfg = reload_config()
    init_mod = importlib.import_module('app.db.init_db')

    def fake_create_all(*args, **kwargs):
        raise AssertionError('Base.metadata.create_all should not be called in production')
    monkeypatch.setattr(init_mod.Base.metadata, 'create_all', fake_create_all)

    # Should run without raising
    init_mod.init_db(isolated_db)


def test_production_no_provision_superadmin_not_created(monkeypatch, isolated_db):
    os.environ.update({
        'ENVIRONMENT': 'production',
        'PROVISION_SUPERADMIN': 'false',
        'SECRET_KEY': 'b'*32,
    })
    cfg = reload_config()
    init_mod = importlib.import_module('app.db.init_db')

    create_super_called = {'count': 0}
    def fake_create_superadmin(db: Session):
        create_super_called['count'] += 1
    monkeypatch.setattr(init_mod, '_create_superadmin', fake_create_superadmin)

    # Run init_db – _create_superadmin must not be invoked
    init_mod.init_db(isolated_db)
    assert create_super_called['count'] == 0


def test_production_provision_superadmin_called_once(monkeypatch, isolated_db):
    os.environ.update({
        'ENVIRONMENT': 'production',
        'PROVISION_SUPERADMIN': 'true',
        'SECRET_KEY': 'c'*32,
        'FIRST_SUPERADMIN_PASSWORD': 'ProdSuperPass123!',
    })
    cfg = reload_config()
    init_mod = importlib.import_module('app.db.init_db')

    create_super_called = {'count': 0}
    def fake_create_superadmin(db: Session):
        create_super_called['count'] += 1
    monkeypatch.setattr(init_mod, '_create_superadmin', fake_create_superadmin)

    # Seed data function must not be called in production
    seed_called = {'count': 0}
    def fake_seed(db: Session):
        seed_called['count'] += 1
    monkeypatch.setattr(init_mod, '_seed_development_data', fake_seed)

    init_mod.init_db(isolated_db)
    assert create_super_called['count'] == 1, "_create_superadmin should be called exactly once when provisioning is enabled"
    assert seed_called['count'] == 0, "_seed_development_data must not be called in production"


def test_production_superadmin_password_not_overwritten(monkeypatch, isolated_db):
    # First run with an initial password
    os.environ.update({
        'ENVIRONMENT': 'production',
        'PROVISION_SUPERADMIN': 'true',
        'SECRET_KEY': 'd'*32,
        'FIRST_SUPERADMIN_PASSWORD': 'InitialPass123!',
    })
    cfg = reload_config()
    init_mod = importlib.import_module('app.db.init_db')
    init_mod.init_db(isolated_db)

    # Capture the hash after first creation
    from app.models.user import User
    superadmin = isolated_db.query(User).filter(User.email == cfg.get_settings().FIRST_SUPERADMIN_EMAIL).first()
    original_hash = superadmin.password_hash

    # Change the environment password and re‑run init_db
    os.environ['FIRST_SUPERADMIN_PASSWORD'] = 'NewPassShouldNotOverwrite'
    reload_config()
    init_mod.init_db(isolated_db)

    superadmin = isolated_db.query(User).filter(User.email == cfg.get_settings().FIRST_SUPERADMIN_EMAIL).first()
    assert superadmin.password_hash == original_hash, "Existing superadmin password must not be overwritten in production"

def test_repeated_development_initialization_is_idempotent(monkeypatch, isolated_db):
    os.environ['ENVIRONMENT'] = 'development'
    cfg = reload_config()
    init_mod = importlib.import_module('app.db.init_db')

    # First init
    init_mod.init_db(isolated_db)
    from app.models.user import User
    from app.models.institution import Institution
    from app.models.dataset import Dataset
    from app.models.fl_project import FLProject

    counts_first = {
        'users': isolated_db.query(User).count(),
        'institutions': isolated_db.query(Institution).count(),
        'datasets': isolated_db.query(Dataset).count(),
        'projects': isolated_db.query(FLProject).count(),
    }
    # Second init
    init_mod.init_db(isolated_db)
    counts_second = {
        'users': isolated_db.query(User).count(),
        'institutions': isolated_db.query(Institution).count(),
        'datasets': isolated_db.query(Dataset).count(),
        'projects': isolated_db.query(FLProject).count(),
    }
    assert counts_first == counts_second, "Repeated development initialization should not duplicate records"
