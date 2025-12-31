import logging
import sqlalchemy as sa

from bluehost_log_parser import create_tables
from bluehost_log_parser.insert_activity import SOHO_LOGS_TABLE, PUBLIC_LOGS_TABLE
from bluehost_log_parser.create_tables import SOURCES_TABLE, COUNTRIES_TABLE
from bluehost_log_parser import my_secrets, populate_tables, create_views
from logging import Logger
from sqlalchemy import (
    create_engine,
    CursorResult,
    exc,
    Engine,
    text,
)
from sqlalchemy_utils import database_exists, create_database
from typing import Any

DB_HOSTNAME: str = f"{my_secrets.local_dbhost}"
DB_NAME: str = f"{my_secrets.local_dbname}"
DB_USER: str = f"{my_secrets.local_dbuser}"
DB_PW: str = f"{my_secrets.local_dbpassword}"
DB_URI: str = f"{my_secrets.local_dburi}"


def schema() -> bool:
    """
    Function checks if database schema (name) is created and available.

    :return: True if exists/created
    """
    logger: Logger = logging.getLogger(__name__)

    try:
        engine: Engine = create_engine(f"mysql+pymysql://{DB_URI}")

        if not database_exists(engine.url):
            create_database(engine.url)
            logger.info(f"Database '{DB_NAME}' did not exist and has been created.")

    except (exc.SQLAlchemyError, exc.OperationalError) as e:
        logger.error(e)
        return False

    return True


def tables() -> bool:
    """
    Function checks if database tables are created and available.

    :return: True if exists/created
    """
    logger: Logger = logging.getLogger(__name__)

    try:
        engine: Engine = create_engine(f"mysql+pymysql://{DB_URI}")

    except (exc.SQLAlchemyError, exc.OperationalError) as e:
        logger.critical(str(e))
        return False

    table_check: Any = sa.inspect(engine)

    public_logs_table: bool = table_check.has_table(
        PUBLIC_LOGS_TABLE, schema=f"{DB_NAME}"
    )
    soho_logs_table: bool = table_check.has_table(SOHO_LOGS_TABLE, schema=f"{DB_NAME}")
    sources_table: bool = table_check.has_table(SOURCES_TABLE, schema=f"{DB_NAME}")
    countries_table: bool = table_check.has_table(COUNTRIES_TABLE, schema=f"{DB_NAME}")

    if not countries_table:
        create_tables.countries_table(engine)
        # populate table from tab separated file
        with engine.begin() as conn:
            result: CursorResult[Any] = conn.execute(
                text("SELECT EXISTS (SELECT 1 FROM countries);")
            )
            check: list[Any] = [r[0] for r in result]
        if check[0] == 0:
            populate_tables.countries()

    if not sources_table:
        create_tables.sources_table(engine)

    if not public_logs_table:
        create_tables.log_tables(engine, PUBLIC_LOGS_TABLE)

    if not soho_logs_table:
        create_tables.log_tables(engine, SOHO_LOGS_TABLE)

    if create_views.all(engine):
        return True

    else:
        return False


if __name__ == "__main__":
    engine = create_engine(f"mysql+pymysql://{DB_URI}")
    print(tables())
