import logging
import sqlalchemy as sa

from bluehost_log_parser import my_secrets
from logging import Logger
from sqlalchemy import (
    create_engine,
    exc,
    inspect,
    types,
    Column,
    Table,
    MetaData,
    ForeignKey,
    Index,
)
from sqlalchemy_utils import database_exists, create_database

from bluehost_log_parser.insert_activity import MY_LOGS_TABLE

DB_HOSTNAME = f"{my_secrets.local_dbhost}"
DB_NAME = f"{my_secrets.local_dbname}"
DB_USER = f"{my_secrets.local_dbuser}"
DB_PW = f"{my_secrets.local_dbpassword}"
DB_URI = f"{my_secrets.local_dburi}"

LOGS_TABLE = "logs"
SOURCES_TABLE = "sources"
MY_LOGS_TABLE = "my_logs"


def schema():
    """
    Function checks to see if schema/DB_NAME is present/created and return True
    If not return False.
    """
    logger: Logger = logging.getLogger(__name__)
    try:
        engine = create_engine(
            f"mysql+pymysql://{DB_USER}:{DB_PW}@{DB_HOSTNAME}/{DB_NAME}"
        )

        if not database_exists(engine.url):
            create_database(engine.url)
            logger.info(f"Database {DB_NAME} did not exist and has been created.")

    except (exc.SQLAlchemyError, exc.OperationalError) as e:
        logger.error(e)
        return False

    return True


def tables():
    """
    Function checks to see if all tables are present/created and return True
    If not return True
    """
    logger: Logger = logging.getLogger(__name__)

    try:
        engine = create_engine(
            f"mysql+pymysql://{DB_USER}:{DB_PW}@{DB_HOSTNAME}/{DB_NAME}"
        )

    except (exc.SQLAlchemyError, exc.OperationalError) as e:
        logger.critical(str(e))
        return False

    logs_check: inspect = sa.inspect(engine)

    logs_tbl: bool = logs_check.has_table(LOGS_TABLE, schema=f"{DB_NAME}")
    my_logs_tbl: bool = logs_check.has_table(MY_LOGS_TABLE, schema=f"{DB_NAME}")
    sources_tbl: bool = logs_check.has_table(SOURCES_TABLE, schema=f"{DB_NAME}")

    meta = MetaData()

    if not logs_tbl:
        try:
            logs = Table(
                LOGS_TABLE,
                meta,
                Column(
                    "ACCESSED",
                    types.TIMESTAMP(timezone=True),
                    primary_key=True,
                    nullable=False,
                ),
                Column(
                    "SOURCE",
                    types.VARCHAR(15),
                    ForeignKey("sources.SOURCE"),
                    nullable=False,
                ),
                Column("CLIENT", types.VARCHAR(200), primary_key=True, nullable=False),
                Column("AGENT", types.VARCHAR(100), primary_key=True, nullable=False),
                Column("ACTION", types.VARCHAR(12), primary_key=True, nullable=False),
                Column("FILE", types.VARCHAR(120), primary_key=True, nullable=False),
                Column("TYPE", types.VARCHAR(20), primary_key=True, nullable=False),
                Column("CODE", types.VARCHAR(10), primary_key=True, nullable=False),
                Column("SIZE", types.VARCHAR(100), primary_key=True, nullable=False),
                Column("REF_URL", types.VARCHAR(100), primary_key=True, nullable=False),
                Column("REF_IP", types.VARCHAR(100), primary_key=True, nullable=False),
            )
            Index("accessed", logs.c.ACCESSED)

        except (
            AttributeError,
            exc.SQLAlchemyError,
            exc.ProgrammingError,
            exc.OperationalError,
        ) as e:
            logger.error(str(e))
            return False

    if not my_logs_tbl:
        try:
            my_logs = Table(
                MY_LOGS_TABLE,
                meta,
                Column(
                    "ACCESSED",
                    types.TIMESTAMP(timezone=True),
                    primary_key=True,
                    nullable=False,
                ),
                Column(
                    "SOURCE",
                    types.VARCHAR(15),
                    ForeignKey("sources.SOURCE"),
                    nullable=False,
                ),
                Column("CLIENT", types.VARCHAR(200), primary_key=True, nullable=False),
                Column("AGENT", types.VARCHAR(100), primary_key=True, nullable=False),
                Column("ACTION", types.VARCHAR(12), primary_key=True, nullable=False),
                Column("FILE", types.VARCHAR(120), primary_key=True, nullable=False),
                Column("TYPE", types.VARCHAR(20), primary_key=True, nullable=False),
                Column("CODE", types.VARCHAR(10), primary_key=True, nullable=False),
                Column("SIZE", types.VARCHAR(100), primary_key=True, nullable=False),
                Column("REF_URL", types.VARCHAR(100), primary_key=True, nullable=False),
                Column("REF_IP", types.VARCHAR(100), primary_key=True, nullable=False),
            )
            Index("accessed", my_logs.c.ACCESSED)

        except (
            AttributeError,
            exc.SQLAlchemyError,
            exc.ProgrammingError,
            exc.OperationalError,
        ) as e:
            logger.error(str(e))
            return False

    if not sources_tbl:
        try:
            sources = Table(
                SOURCES_TABLE,
                meta,
                Column("SOURCE", types.VARCHAR(15), primary_key=True),
                Column("COUNTRY", types.VARCHAR(100)),
                Column("ALPHA2", types.VARCHAR(2)),
                Column("DESCRIPTION", types.VARCHAR(160)),
            )
            Index("country", sources.c.COUNTRY)

        except (
            AttributeError,
            exc.SQLAlchemyError,
            exc.ProgrammingError,
            exc.OperationalError,
        ) as e:
            logger.error(str(e))
            return False

    meta.create_all(engine)

    return True
