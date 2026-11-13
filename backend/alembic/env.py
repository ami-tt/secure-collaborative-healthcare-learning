"""
Alembic environment configuration.

This file configures SQLAlchemy migrations using the database URL
provided through Alembic configuration.

The application's SQLAlchemy Base metadata is imported so Alembic
can detect all registered models during migrations.
"""

import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool


# ---------------------------------------------------------------------
# Add backend directory to Python path
# ---------------------------------------------------------------------

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ---------------------------------------------------------------------
# Alembic configuration
# ---------------------------------------------------------------------

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# IMPORTANT:
# Do not override sqlalchemy.url here.
# Alembic must respect the URL supplied by:
#   1. alembic.ini
#   2. alembic_cfg.set_main_option() in integration tests
#
# This allows migrations to run against the intended database.


# ---------------------------------------------------------------------
# Import application metadata and models
# ---------------------------------------------------------------------

from app.core.database import Base

import app.models.user  # noqa: F401
import app.models.institution  # noqa: F401
import app.models.dataset  # noqa: F401
import app.models.audit  # noqa: F401
import app.models.fl_project  # noqa: F401
import app.models.fl_session  # noqa: F401
import app.models.fl_participant  # noqa: F401
import app.models.base  # noqa: F401
import app.models.checkpoint  # noqa: F401
import app.models.metric  # noqa: F401


target_metadata = Base.metadata


# ---------------------------------------------------------------------
# Create migration engine
# ---------------------------------------------------------------------

def get_engine():
    """Create an engine using the URL supplied by Alembic configuration."""

    section = config.get_section(config.config_ini_section)

    if section is None:
        raise RuntimeError(
            "Alembic configuration section is missing."
        )

    database_url = config.get_main_option("sqlalchemy.url")

    if not database_url:
        raise RuntimeError(
            "Database URL is missing from Alembic configuration."
        )

    return engine_from_config(
        section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )


# ---------------------------------------------------------------------
# Offline migrations
# ---------------------------------------------------------------------

def run_migrations_offline():
    """Run migrations without creating a database connection."""

    database_url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# ---------------------------------------------------------------------
# Online migrations
# ---------------------------------------------------------------------

def run_migrations_online():
    """Run migrations using a live database connection."""

    connectable = get_engine()

    try:
        with connectable.connect() as connection:

            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                compare_type=True,
                compare_server_default=True,
            )

            with context.begin_transaction():
                context.run_migrations()

    finally:
        connectable.dispose()


# ---------------------------------------------------------------------
# Execute migrations
# ---------------------------------------------------------------------

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()