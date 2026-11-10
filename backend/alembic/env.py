"""Alembic environment configuration.



This file is executed by Alembic when running migration commands.

It sets up the SQLAlchemy engine using the same DATABASE_URL

that the application uses (via pydantic Settings).  The Base

metadata is imported from the application's core database module

so that ``autogenerate`` can detect all existing models.

"""



import os

import sys

from logging.config import fileConfig



from alembic import context



# Add the project root to the import path so ``app`` package can be imported.

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))

sys.path.append(PROJECT_ROOT)



# Import the application's settings to get DATABASE_URL.

from app.core.config import settings



# this is the Alembic Config object, which provides

# access to the values within the .ini file in use.

config = context.config



# Interpret the config file for Python logging.

if config.config_file_name is not None:

    fileConfig(config.config_file_name)



# -----------------------------------------------------------------------------

# Set up SQLAlchemy engine using the same DATABASE_URL the app uses.

# ``engine_from_config`` reads the ``sqlalchemy.url`` key from alembic.ini.

# We override it with the environment variable / Settings value.

# -----------------------------------------------------------------------------

config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)



from sqlalchemy import engine_from_config, pool



def get_engine():

    return engine_from_config(

        config.get_section(config.config_ini_section),

        prefix="sqlalchemy.",

        poolclass=pool.NullPool,

    )



engine = get_engine()



# Import the Base metadata that includes all model definitions.

from app.core.database import Base



# Ensure all model modules are imported so that their tables are registered

# with Base.metadata.  Importing the modules is enough – the classes are

# defined at import time.

# NOTE: If new models are added, import them here as well.

import app.models.user  # noqa: F401

import app.models.institution  # noqa: F401

import app.models.dataset  # noqa: F401

import app.models.audit  # noqa: F401

import app.models.fl_project  # noqa: F401

import app.models.fl_session  # noqa: F401

import app.models.fl_session_participant  # noqa: F401

import app.models.base  # noqa: F401



# -----------------------------------------------------------------------------

# target_metadata is what Alembic uses for "autogenerate" support.

# -----------------------------------------------------------------------------

target_metadata = Base.metadata



def run_migrations_offline():

    """Run migrations in 'offline' mode.



    This configures the context with just a URL and not an Engine, and

    then calls ``context.run_migrations()``.

    """

    url = config.get_main_option("sqlalchemy.url")

    context.configure(

        url=url,

        target_metadata=target_metadata,

        literal_binds=True,

        dialect_opts={"paramstyle": "named"},

    )



    with context.begin_transaction():

        context.run_migrations()





def run_migrations_online():

    """Run migrations in 'online' mode.



    In this scenario we create an Engine and associate a connection with the

    context.

    """

    connectable = engine



    with connectable.connect() as connection:

        context.configure(

            connection=connection,

            target_metadata=target_metadata,

            compare_type=True,

            compare_server_default=True,

        )



        with context.begin_transaction():

            context.run_migrations()



if context.is_offline_mode():

    run_migrations_offline()

else:

    run_migrations_online()
