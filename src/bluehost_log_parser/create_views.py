import logging

from bluehost_log_parser import my_secrets
from logging import Logger
from sqlalchemy import exc, create_engine, text

logger: Logger = logging.getLogger(__name__)

DB_HOSTNAME: str = f"{my_secrets.local_dbhost}"
DB_NAME: str = f"{my_secrets.local_dbname}"
DB_USER: str = f"{my_secrets.local_dbuser}"
DB_PW: str = f"{my_secrets.local_dbpassword}"
DB_URI: str = f"{my_secrets.local_dburi}"

LOGS_TABLE: str = "logs"
SOURCES_TABLE: str = "sources"
COUNTRIES_TABLE: str = "countries"
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
                        COUNT(`bluehost-weblogs`.`logs`.`SOURCE`) AS `COUNT`,
                        `bluehost-weblogs`.`sources`.`COUNTRY` AS `COUNTRY`
                    FROM
                        (`bluehost-weblogs`.`logs`
                        JOIN `bluehost-weblogs`.`sources` ON (`bluehost-weblogs`.`logs`.`SOURCE` = `bluehost-weblogs`.`sources`.`SOURCE`))
                    GROUP BY `bluehost-weblogs`.`sources`.`COUNTRY`
                    ORDER BY COUNT(`bluehost-weblogs`.`logs`.`SOURCE`) DESC;""")
                )

            return True

        except exc.SQLAlchemyError as e:
            logger.critical(str(e))
            return False


if __name__ == "__main__":
    engine = create_engine(f"mysql+pymysql://{DB_URI}")
    print(all(engine=engine))
