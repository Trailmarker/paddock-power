# -*- coding: utf-8 -*-

from logging.config import fileConfig

# The 'alembic_helpers' for GeoAlchemy 2 help us deal with various difficulties concerning GeoAlchemy
from alembic import context
from geoalchemy2 import alembic_helpers as geoalchemy2_alembic_helpers
# , load_spatialite
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy.event import listen

# Import Base model and some SpatiaLite utilities
from mlapp_schema.data import Base, enforceForeignKeys, extendedIncludeObject, installSpatiaLiteMetadata, loadSpatiaLite

# Import all other models so that Alembic can detect them

# Initial migration: base features
from mlapp_schema.data.models import *

# This is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# Other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")

    print(f"include_object: {geoalchemy2_alembic_helpers.include_object}")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},

        # Additional items to eg exclude SpatiaLite tables from autogeneration
        include_object=extendedIncludeObject,
        process_revision_directives=geoalchemy2_alembic_helpers.writer,
        render_item=geoalchemy2_alembic_helpers.render_item,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        echo=True,
        # implicit_returning=False,
    )

    if connectable.dialect.name == "sqlite":
        # Load the SpatiaLite extension when the engine connects to the DB
        listen(connectable, 'connect', enforceForeignKeys)
        listen(connectable, 'connect', loadSpatiaLite)

    # Important: the use of begin() instead of connect() here turns out to be
    # crucial to the transactional behaviour of the migrations
    with connectable.begin() as connection:

        installSpatiaLiteMetadata(connection)
        context.configure(
            connection=connection,
            target_metadata=target_metadata,

            # Additional items to eg exclude SpatiaLite tables from autogeneration
            include_object=extendedIncludeObject,
            process_revision_directives=geoalchemy2_alembic_helpers.writer,
            render_item=geoalchemy2_alembic_helpers.render_item,
            transaction_per_migration=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
