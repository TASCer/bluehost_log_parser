import logging
from logging import Logger

from sqlalchemy import Engine, create_engine, exc, text

from bluehost_log_parser.database.config import (
    DB_URI,
    PUBLIC_LOGS_TABLE,
    SOHO_LOGS_TABLE,
    SOURCES_TABLE,
    VIEW_COUNTRY_ACTIVITY,
    VIEW_SOHO_NON_200_RESP,
)

logger: Logger = logging.getLogger(__name__)


def source_countries(engine) -> bool:
    """
    Function creates a database view noting the count of countries accessing the websites.

    :param engine: fatabase engine
    :return: True if view created
    """
    with engine.connect() as conn, conn.begin():
        try:
            with engine.connect() as conn, conn.begin():
                conn.execute(
                    text(f"""

                    CREATE OR REPLACE
                    
                    VIEW {VIEW_COUNTRY_ACTIVITY}
                    AS
                    SELECT
                        COUNT(`bluehost_weblogs`.`{PUBLIC_LOGS_TABLE}`.`SOURCE`) AS `COUNT`,
                        `bluehost_weblogs`.`{SOURCES_TABLE}`.`COUNTRY` AS `COUNTRY`
                    FROM
                        (`bluehost_weblogs`.`{PUBLIC_LOGS_TABLE}`
                        JOIN `bluehost_weblogs`.`{SOURCES_TABLE}` ON (`bluehost_weblogs`.`{PUBLIC_LOGS_TABLE}`.`SOURCE` = `bluehost_weblogs`.`{SOURCES_TABLE}`.`SOURCE`))
                    GROUP BY `bluehost_weblogs`.`{SOURCES_TABLE}`.`COUNTRY`
                    ORDER BY COUNT(`bluehost_weblogs`.`{PUBLIC_LOGS_TABLE}`.`SOURCE`) DESC;""")
                )

            return True

        except exc.SQLAlchemyError as e:
            logger.critical(str(e))
            return False


def soho_non_200_responses(engine) -> bool:
    """
    Function creates a database view noting the count of html status codes not equal to 200.

    :param engine: fatabase engine
    :return: True if view created
    """
    with engine.connect() as conn, conn.begin():
        try:
            with engine.connect() as conn, conn.begin():
                conn.execute(
                    text(f"""

                    CREATE OR REPLACE

                    VIEW {VIEW_SOHO_NON_200_RESP}
                    AS
                    SELECT
                        *
                    FROM
                        `bluehost_weblogs`.`{SOHO_LOGS_TABLE}`
                    WHERE RESPONSE !='200';""")
                )

            return True

        except exc.SQLAlchemyError as e:
            logger.critical(str(e))
            return False


def all(engine) -> bool:
    """
    Function controls the creation of all local database views.

    :param engine: database engine
    :return: True if all views created
    """
    source_countries_created = source_countries(engine=engine)
    soho_logs_not_200_created = soho_non_200_responses(engine=engine)

    return not (not soho_logs_not_200_created and not source_countries_created)


if __name__ == "__main__":
    engine: Engine = create_engine(f"mysql+pymysql://{DB_URI}")
    print(all(engine=engine))
