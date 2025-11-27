import logging

from bluehost_log_parser import my_secrets
from logging import Logger
from pymysql.err import DataError
from sqlalchemy.engine import Engine
from sqlalchemy import exc, create_engine, text, TextClause

LOGS_TABLE = "logs"
SOURCES_TABLE = "sources"


def whois_updates(whois_data: list[str]) -> None:
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
                            `COUNTRY` = '{data[3]}',
                            `ALPHA2` = '{data[1]}',
                            `DESCRIPTION` = '{data[2]}'
                        WHERE `SOURCE` = '{data[0]}';""")
                )
            except exc.ProgrammingError as pe:
                logger.error(pe)
            except DataError as de:
                logger.error(de)

        if errors >= 1:
            logger.warning(f"sources table: {errors} errors encountered")

        logger.info(
            f"\tsources table: {len(whois_data) - errors} updated with country names and ASN description."
        )


def asn_alphas(alpha2s: list[str]) -> list[str]:
    """
    Function takes in a list of ASN_ALPHA2 codes and returns its ASN_ALPHA (3-letter code for country name) equivalent from countries table.
    """
    logger: Logger = logging.getLogger(__name__)

    try:
        engine: Engine = create_engine(f"mysql+pymysql://{my_secrets.local_dburi}")

    except exc.SQLAlchemyError as e:
        logger.critical(str(e))
        exit()

    asn_alphas = []

    try:
        with engine.connect() as conn, conn.begin():
            logger.info(
                "Getting ASN_ALPHA (3-letter code for country name) from countries table"
            )
            for a in alpha2s:
                q_alphas: TextClause = text(
                    f"SELECT ALPHA3 from countries where ALPHA2 = '{a}';"
                )

                result = conn.execute(q_alphas).fetchone()[0]
                asn_alphas.append(result)

    except TypeError:
        print("check if table 'countries' is/was populated via 'populate_tables.py'")
        logger.error(
            "check if table 'countries' is/was populated via 'populate_tables.py'"
        )

        exit()

    return asn_alphas


if __name__ == "__main__":
    # whois_updates()
   print(asn_alphas(["AL", "AR"]))
