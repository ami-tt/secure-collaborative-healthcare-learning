"""Database engine and session management.
Provides a configurable engine that can be reset during tests to respect
environment variable changes or a fresh Settings instance.
"""

from __future__ import annotations

from typing import Generator, Optional

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from app.core.config import Settings, get_settings

# ---------------------------------------------------------------------------
# Engine creation utilities
# ---------------------------------------------------------------------------

def _make_engine(settings_instance: Optional[Settings] = None) -> Engine:
    """Create a SQLAlchemy engine from a Settings instance.
    If ``settings_instance`` is ``None`` the cached Settings singleton is used.
    """
    if settings_instance is None:
        settings_instance = get_settings()
    connect_args: dict = {}
    if settings_instance.DATABASE_URL.startswith("sqlite"):
        # SQLite file DB – disable the same‑thread check.
        connect_args = {"check_same_thread": False}
    return create_engine(
        settings_instance.DATABASE_URL,
        connect_args=connect_args,
        pool_pre_ping=True,
    )

# Engine used by the application at import time.
engine: Engine = _make_engine()

# Session factory bound to the current engine.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for model definitions.
Base = declarative_base()

# ---------------------------------------------------------------------------
# FastAPI dependency
# ---------------------------------------------------------------------------

def get_db() -> Generator[Session, None, None]:
    """Yield a DB session and ensure it is closed after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------------------------------------------------------
# Test helper – reset the engine
# ---------------------------------------------------------------------------

def reset_engine(settings_instance: Optional[Settings] = None) -> None:
    """Dispose the current engine and recreate it.
    Optional ``settings_instance`` can be supplied to force a specific
    configuration; otherwise the cached Settings singleton is consulted.
    """
    global engine, SessionLocal
    try:
        engine.dispose()
    except Exception:
        pass
    engine = _make_engine(settings_instance)
    SessionLocal.configure(bind=engine)
