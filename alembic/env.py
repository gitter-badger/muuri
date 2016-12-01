from __future__ import with_statement

import sys
import logging

sys.dont_write_bytecode = True

from alembic import context
from sqlalchemy import engine_from_config

logging.basicConfig(stream = sys.stdout, level = logging.DEBUG)
log = logging.getLogger(__name__)

config = context.config

from muuri.database import Base
target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    engine = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix = 'sqlalchemy.',
        echo = True,
        #poolclass = pool.NullPool
    )

    with engine.connect() as connection:
        log.debug(":: Connected to database")
        context.configure(
            connection = connection,
            target_metadata = target_metadata
        )

        with context.begin_transaction():
            log.debug(":: Running migrations")
            context.run_migrations()


if context.is_offline_mode():
    log.debug("-- OFFLINE MODE")
    run_migrations_offline()
else:
    log.debug("-- ONLINE MODE")
    run_migrations_online()
