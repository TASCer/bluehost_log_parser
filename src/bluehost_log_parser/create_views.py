import logging

from bluehost_log_parser import my_secrets
from bluehost_log_parser.insert_activity import SOHO_LOGS_TABLE, PUBLIC_LOGS_TABLE
from logging import Logger
from sqlalchemy import exc, create_engine, text

logger: Logger = logging.getLogger(__name__)

DB_HOSTNAME: str = f"{my_secrets.local_dbhost}"
DB_NAME: str = f"{my_secrets.local_dbname}"
DB_USER: str = f"{my_secrets.local_dbuser}"
DB_PW: str = f"{my_secrets.local_dbpassword}"
DB_URI: str = f"{my_secrets.local_dburi}"

SOURCES_TABLE: str = "sources"
VIEW_COUNTRY_ACTIVITY = "country_activity"


def all(engine) -> bool:
    """
    Function creates all local database Views.

    :param engine: datanase engine
    :return: True if all views created
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


if __name__ == "__main__":
    engine = create_engine(f"mysql+pymysql://{DB_URI}")
    print(all(engine=engine))
