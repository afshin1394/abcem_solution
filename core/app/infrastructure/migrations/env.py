from logging.config import fileConfig

from sqlalchemy import engine_from_config, text, MetaData
from sqlalchemy import pool

from alembic import context

from app.infrastructure.postgres_async import engine
# Import your models and base class

from app.infrastructure.schemas.base_db_model import Base
from app.infrastructure.schemas.table_step_type import TableStepTestType
from app.infrastructure.schemas.table_call_test import TableCallTest
from app.infrastructure.schemas.table_speed_test_servers import TableSpeedTestServer
from app.infrastructure.schemas.table_technology_type import TableTechnologyType
from app.infrastructure.schemas.table_cell_info import TableCellInfo
from app.infrastructure.schemas.table_device_info import TableDeviceInfo
from app.infrastructure.schemas.table_complaint_type import TableComplaintType
from app.infrastructure.schemas.table_problematic_service import TableProblematicService
from app.infrastructure.schemas.table_walk_test_detail import TableWalkTestDetail
from app.infrastructure.schemas.table_walk_test import TableWalkTest
from app.infrastructure.schemas.table_walk_test_status import TableWalkTestStatus
from app.infrastructure.schemas.table_complaint_type import TableComplaintType
from app.infrastructure.schemas.table_speed_test_results import TableSpeedTestResults

# This is the Alembic Config object, which provides access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging. This sets up loggers.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target_metadata to your models' metadata (necessary for auto_generation)
target_metadata = Base.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table":
        object_schema = getattr(object, 'schema', None)
        if object_schema is None:
            return True
        return object_schema == "sms"
    return True

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
    context.configure(
        url=url,
        target_metadata=target_metadata,
        version_table="core_service",  # <--- custom version table
        literal_binds=True,
        compare_type=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
        connect_args={"options": "-c search_path=core_service"},  # <--- Important
    )


    with connectable.connect() as connection:
        # 🛠️ CREATE the schema if it doesn't exist (BEFORE configuring Alembic context)
        connection.execute(text('CREATE SCHEMA IF NOT EXISTS core_service'))
        context.configure(
            connection=connection, target_metadata=target_metadata,
            version_table_schema="core_service",  # Important!
            include_schemas=False,  # Important for multiple schemas
            include_object = include_object,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
