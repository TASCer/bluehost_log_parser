import logging

from bluehost_log_parser import my_secrets
from logging import Logger
from sqlalchemy.engine import Engine
from sqlalchemy import exc, create_engine, text

SOURCES_TABLE = "sources"


def inserts(unique_ips: set[str]) -> list[str]:
    """
    Inserts unique sources into table with unique source ip addresses from latest processing
    :param: set
    :return: list
    """
    logger: Logger = logging.getLogger(__name__)

    try:
        engine: Engine = create_engine(f"mysql+pymysql://{my_secrets.local_dburi}")

    except exc.SQLAlchemyError as e:
        logger.critical(str(e))
        exit()

    with engine.connect() as conn, conn.begin():
        for ip in unique_ips:
            conn.execute(
                text(
                    f"""INSERT IGNORE into {SOURCES_TABLE} values('{ip}', NULL, NULL, NULL);"""
                )
            )

        q_missing_country = conn.execute(
            text(f"SELECT * from {SOURCES_TABLE} WHERE COUNTRY = ''")
        )
        missing_country = [t[0] for t in q_missing_country]

        return missing_country
    # try:
    #     engine: Engine = create_engine(f"mysql+pymysql://{my_secrets.local_dburi}")

    # except exc.SQLAlchemyError as e:
    #     logger.critical(str(e))
    #     exit()

    # q_no_countries = conn.execute(
    #     text(f"SELECT * from {SOURCES_TABLE} WHERE COUNTRY is null")
    # )
    # no_countries = [nc for nc in q_no_countries]

    # return no_countries
