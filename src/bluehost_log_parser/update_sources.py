import logging

from bluehost_log_parser import my_secrets
from logging import Logger
from sqlalchemy.engine import Engine
from sqlalchemy import exc, create_engine, text

LOGS_TABLE = "logs"
SOURCES_TABLE = "sources"


def whois_updates(whois_data: list[str]):
    """
    Updates lookup table 'sources' entries with full country name and ASN Description from ipwhois
    """
    logger: Logger = logging.getLogger(__name__)

    try:
        engine: Engine = create_engine(f"mysql+pymysql://{my_secrets.local_dburi}")

    except exc.SQLAlchemyError as e:
        logger.critical(str(e))
        exit()

    with engine.connect() as conn, conn.begin():
        logger.info(
            "Updating source table with country name and description via IPWhois"
        )

        errors: int = 0

        for data in whois_data:
            try:
                conn.execute(
                    text(f"""UPDATE `{my_secrets.local_dbname}`.`{SOURCES_TABLE}`
                        SET
                            `COUNTRY` = '{whois_data[1]}',
                            `ALPHA2` = '{whois_data[2]}',
                            `DESCRIPTION` = '{whois_data[3]}'
                        WHERE `SOURCE` = '{whois_data[0]}';""")
                )
            except exc.ProgrammingError as e:
                logger.error(e)

        if errors >= 1:
            logger.warning(f"sources table: {errors} errors encountered")

        logger.info(
            f"sources table: {len(whois_data) - errors} updated with country names and ASN description."
        )


if __name__ == "__main__":
    whois_updates()
