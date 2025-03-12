import logging
import my_secrets

from logging import Logger
from sqlalchemy.engine import Engine
from sqlalchemy import exc, create_engine, text

# SQL TABLE constants
SOURCES = "sources"


def update(unique_ips: set[str]) -> None:
    """
    Updates sources/lookup table with unique source ip addresses from latest processing
    :param: set
    :return: None
    """
    logger: Logger = logging.getLogger(__name__)

    try:
        engine: Engine = create_engine(
            f"mysql+pymysql://{my_secrets.dbuser}:{my_secrets.dbpass}@{my_secrets.dbhost}/{my_secrets.dbname}"
        )

    except exc.SQLAlchemyError as e:
        logger.critical(str(e))
        exit()

    with engine.connect() as conn, conn.begin():
        for ip in unique_ips:
            conn.execute(text(f"""INSERT IGNORE into {SOURCES} values('{ip}', '', '', '');"""))
