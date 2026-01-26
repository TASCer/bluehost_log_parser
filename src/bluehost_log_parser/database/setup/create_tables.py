import logging

from logging import Logger
from sqlalchemy import (
    exc,
    types,
    Engine,
    Column,
    Table,
    MetaData,
    ForeignKey,
    Index,
)

logger: Logger = logging.getLogger(__name__)

COUNTRIES_TABLE: str = "countries"
SOURCES_TABLE: str = "sources"
VIEW_COUNTRY_ACTIVITY = "country_activity"

meta = MetaData()


def log_tables(engine: Engine, log_table_name) -> None:
    """
    Function creates database tables consisting of webserver log entries.

    :param engine: database engine
    :param log_table_name: database table name
    :return: None
    """
    try:
        logs = Table(
            log_table_name,
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
            Column("METHOD", types.VARCHAR(12), primary_key=True, nullable=False),
            Column("REQUEST", types.VARCHAR(120), primary_key=True, nullable=False),
            Column("HTTP", types.VARCHAR(20), primary_key=True, nullable=False),
            Column("RESPONSE", types.VARCHAR(10), primary_key=True, nullable=False),
            Column("SIZE", types.VARCHAR(100), primary_key=True, nullable=False),
            Column("REFERRER", types.VARCHAR(100), primary_key=True, nullable=False),
            Column("SITE", types.VARCHAR(40), primary_key=True, nullable=False),
        )
        Index("accessed", logs.c.ACCESSED)

    except (
        AttributeError,
        exc.SQLAlchemyError,
        exc.ProgrammingError,
        exc.OperationalError,
    ) as e:
        logger.error(str(e))

    meta.create_all(engine)


def countries_table(engine) -> None:
    try:
        countries = Table(
            COUNTRIES_TABLE,
            meta,
            Column("NAME", types.VARCHAR(120), primary_key=True),
            Column("ALPHA2", types.VARCHAR(2), unique=True),
            Column("ALPHA3", types.VARCHAR(3), unique=True),
            Column("NUMBER", types.INT(), unique=True),
        )
        Index("name", countries.c.NAME)

    except (
        AttributeError,
        exc.SQLAlchemyError,
        exc.ProgrammingError,
        exc.OperationalError,
    ) as e:
        logger.error(str(e))

    meta.create_all(engine)


def sources_table(engine) -> None:
    try:
        sources = Table(
            SOURCES_TABLE,
            meta,
            Column("SOURCE", types.VARCHAR(15), primary_key=True),
            Column("COUNTRY", types.VARCHAR(100)),
            Column("ALPHA2", types.VARCHAR(2)),
            Column("ALPHA3", types.VARCHAR(3), ForeignKey("countries.ALPHA3")),
            Column("DESCRIPTION", types.VARCHAR(160)),
        )
        Index("source", sources.c.ALPHA2)

    except (
        AttributeError,
        exc.SQLAlchemyError,
        exc.ProgrammingError,
        exc.OperationalError,
    ) as e:
        logger.error(str(e))

    meta.create_all(engine)
