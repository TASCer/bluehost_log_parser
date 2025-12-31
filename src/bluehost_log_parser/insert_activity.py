import logging

from bluehost_log_parser import my_secrets
from datetime import datetime
from dateutil.parser import parse
from logging import Logger
from sqlalchemy.engine import Engine
from sqlalchemy import exc, create_engine, text

PUBLIC_LOGS_TABLE = "public_logs"
SOHO_LOGS_TABLE = "soho_logs"

logger: Logger = logging.getLogger(__name__)


def parse_timestamp(ts: str) -> datetime:
    """
    Function takes in a str from log file and returns a datetime

    :param ts: string timestamp
    :return: datetime timestamp
    """
    ts = ts.replace(":", " ", 1)
    ts_split: list[str] = ts.split(" ", 2)
    ts = " ".join(ts_split[0:2])
    ts_parsed: datetime = parse(ts)

    return ts_parsed


def soho_log_updates(db_engine, soho_logs):
    """
    Function inserts latest LogEntrys into the my_logs table.

    :param db_engine: database engine
    :param soho_logs: list of LogEntry coming from SOHO clients
    """
    with db_engine.connect() as conn, conn.begin():
        for log in soho_logs:
            ts_parsed = parse_timestamp(log.server_timestamp)

            try:
                conn.execute(
                    text(
                        f"""INSERT IGNORE INTO {SOHO_LOGS_TABLE} VALUES('{ts_parsed}', '{log.SOURCE}', '{log.CLIENT}', '{log.AGENT}', '{log.METHOD}', '{log.REQUEST}', '{log.HTTP}', '{log.RESPONSE}', '{log.SIZE}', '{log.REFERRER}', '{log.SITE}');"""
                    )
                )
            except (exc.SQLAlchemyError, exc.ProgrammingError, exc.DataError) as e:
                logger.error(e)

    logger.info(
        f"{len(soho_logs)} log entries inserted into table: '{SOHO_LOGS_TABLE}'"
    )


def public_log_updates(db_engine, public_logs):
    """
    Function inserts latest LogEntrys into the logs table.

    :param db_engine: database engine
    :param public_logs: list of LogEntrys coming from PUBLIC clients
    """
    with db_engine.connect() as conn, conn.begin():
        for log in public_logs:
            ts_parsed: datetime = parse_timestamp(log.server_timestamp)

            try:
                conn.execute(
                    text(
                        f"""INSERT IGNORE INTO {PUBLIC_LOGS_TABLE} VALUES('{ts_parsed}', '{log.SOURCE}', '{log.CLIENT}', '{log.AGENT}', '{log.METHOD}', '{log.REQUEST}', '{log.HTTP}', '{log.RESPONSE}', '{log.SIZE}', '{log.REFERRER}', '{log.SITE}');"""
                    )
                )
                
            except (
                exc.SQLAlchemyError,
                exc.ProgrammingError,
                exc.DataError,
                exc.InvalidRequestError,
            ) as e:
                logger.error(e)

    logger.info(
        f"{len(public_logs)} log entries inserted into table: '{PUBLIC_LOGS_TABLE}'"
    )


def update_log_tables(public_log_entries: list, soho_log_entries: list) -> None:
    """
    Function updates database tables with latest parsed logs.

    :param log_entries: all logs not from my SOHO
    :param my_log_entries: all logs from SOHO
    """
    
    try:
        engine: Engine = create_engine(f"mysql+pymysql://{my_secrets.local_dburi}")

    except exc.SQLAlchemyError as e:
        logger.critical(str(e))
        exit()

    public_log_updates(engine, public_log_entries)
    soho_log_updates(engine, soho_log_entries)
