import logging


from bluehost_log_parser import my_secrets
from bluehost_log_parser.insert_activity import (
    PUBLIC_LOGS_TABLE,
)  # see TODO , SOHO_LOGS_TABLE
from logging import Logger
from sqlalchemy import exc, create_engine, text, Engine

logger: Logger = logging.getLogger(__name__)

DB_HOSTNAME: str = f"{my_secrets.local_dbhost}"
DB_NAME: str = f"{my_secrets.local_dbname}"
DB_USER: str = f"{my_secrets.local_dbuser}"
DB_PW: str = f"{my_secrets.local_dbpassword}"
DB_URI: str = f"{my_secrets.local_dburi}"

SOHO_LOGS_TABLE: str = "soho_logs"
SOURCES_TABLE: str = "sources"
VIEW_COUNTRY_ACTIVITY = "country_activity"
VIEW_SOHO_NON_200_RESP = "soho_non_200_reponse"


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
                    DEFINER = 'todd'@'%'
                    VIEW {VIEW_COUNTRY_ACTIVITY}
                    AS
                    SELECT
                        COUNT(`bluehost-weblogs`.`{PUBLIC_LOGS_TABLE}`.`SOURCE`) AS `COUNT`,
                        `bluehost-weblogs`.`{SOURCES_TABLE}`.`COUNTRY` AS `COUNTRY`
                    FROM
                        (`bluehost-weblogs`.`{PUBLIC_LOGS_TABLE}`
                        JOIN `bluehost-weblogs`.`{SOURCES_TABLE}` ON (`bluehost-weblogs`.`{PUBLIC_LOGS_TABLE}`.`SOURCE` = `bluehost-weblogs`.`{SOURCES_TABLE}`.`SOURCE`))
                    GROUP BY `bluehost-weblogs`.`{SOURCES_TABLE}`.`COUNTRY`
                    ORDER BY COUNT(`bluehost-weblogs`.`{PUBLIC_LOGS_TABLE}`.`SOURCE`) DESC;""")
                )

            return True

        except exc.SQLAlchemyError as e:
            logger.critical(str(e))
            return False


def soho_non_200_responses(engine):
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
                    DEFINER = 'todd'@'%'
                    VIEW {VIEW_SOHO_NON_200_RESP}
                    AS
                    SELECT
                        *
                    FROM
                        `bluehost-weblogs`.`{SOHO_LOGS_TABLE}`
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

    if soho_logs_not_200_created and source_countries_created:
        return True
    else:
        return False


if __name__ == "__main__":
    engine: Engine = create_engine(f"mysql+pymysql://{DB_URI}")
    print(all(engine=engine))
