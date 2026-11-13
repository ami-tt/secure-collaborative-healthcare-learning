import os
import pytest

from sqlalchemy import create_engine, text, inspect
from alembic import command
from alembic.config import Config


@pytest.fixture(scope="session")
def pg_url():
    """Get the dedicated PostgreSQL integration-test URL."""

    url = os.getenv("POSTGRES_TEST_URL")

    if not url:
        pytest.skip(
            "POSTGRES_TEST_URL not configured - skipping PostgreSQL integration tests"
        )

    return url


@pytest.fixture(scope="function")
def engine(pg_url):
    """
    Create an independent PostgreSQL engine.

    This does not modify the application's global database engine.
    """

    test_engine = create_engine(
        pg_url,
        pool_pre_ping=True
    )

    try:
        yield test_engine
    finally:
        test_engine.dispose()


def _cleanup_database(engine):
    """
    Clean the dedicated PostgreSQL test database before migrations.

    WARNING: This removes tables and enum types in the current schema.
    Only use POSTGRES_TEST_URL with a disposable test database.
    """

    with engine.begin() as conn:

        inspector = inspect(conn)

        # Drop existing tables, including Alembic version table.
        for table in inspector.get_table_names():
            quoted_table = conn.dialect.identifier_preparer.quote(table)

            conn.execute(
                text(f"DROP TABLE IF EXISTS {quoted_table} CASCADE")
            )

        # Find all enum types in the current schema.
        enum_names = conn.execute(
            text("""
                SELECT t.typname
                FROM pg_type t
                JOIN pg_namespace n
                    ON n.oid = t.typnamespace
                WHERE n.nspname = current_schema()
                  AND t.typtype = 'e'
            """)
        ).scalars().all()

        # Drop existing enum types.
        for enum_name in enum_names:
            quoted_enum = conn.dialect.identifier_preparer.quote(
                enum_name
            )

            conn.execute(
                text(f"DROP TYPE IF EXISTS {quoted_enum} CASCADE")
            )


def test_basic_select(engine):
    """Verify PostgreSQL connectivity."""

    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))

        assert result.scalar_one() == 1


def test_alembic_migration_and_tables(engine, pg_url):
    """Verify that Alembic migrations create the expected tables."""

    # Clean the dedicated test database.
    _cleanup_database(engine)

    # Locate Alembic configuration.
    alembic_ini_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "alembic.ini"
        )
    )

    alembic_cfg = Config(alembic_ini_path)

    # Escape percent signs for ConfigParser interpolation.
    alembic_cfg.set_main_option(
        "sqlalchemy.url",
        pg_url.replace("%", "%%")
    )

    # Apply migrations.
    command.upgrade(alembic_cfg, "head")

        # Verify database tables.
    inspector = inspect(engine)
    tables = set(inspector.get_table_names())

    expected_tables = {
        "institutions",
        "datasets",
        "users",
        "audit_logs",
        "fl_projects",
        "fl_sessions",
        "fl_round_metrics",
        "fl_client_round_metrics",
        "fl_session_participants",
        "model_checkpoints",
    }

    missing = expected_tables - tables

    assert not missing, (
        f"Missing tables after migration: {missing}"
    )